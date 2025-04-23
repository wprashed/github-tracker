import requests
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import csv
import os
from datetime import datetime
import json
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

# GitHub API details
GITHUB_API_URL = "https://api.github.com/repos/{owner}/{repo}/issues"
GITHUB_TOKEN = "your_github_token"
OWNER = "your_github_owner"
REPO = "your_github_repo"

# Email Configuration
SEND_EMAIL = True
EMAIL_FROM = "your_email@example.com"
EMAIL_PASSWORD = "your_email_password"
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
EMAIL_TO = "recipient_email@example.com"

# Slack Configuration
SEND_SLACK = True
SLACK_TOKEN = "your_slack_token"
SLACK_CHANNEL = "#your_channel"
SLACK_WEBHOOK_URL = "your_slack_webhook_url"

# CSV Export Configuration
EXPORT_CSV = True
CSV_FILENAME = "github_report.csv"

# Notion API Configuration (optional)
NOTION_TOKEN = "your_notion_token"
DATABASE_ID = "your_notion_database_id"

# Fetch GitHub issues and PRs
def fetch_github_data():
    headers = {
        "Authorization": f"Bearer {GITHUB_TOKEN}",
    }

    url = GITHUB_API_URL.format(owner=OWNER, repo=REPO)
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        issues = response.json()
        return issues
    else:
        print(f"Error fetching GitHub data: {response.status_code}")
        return []

# Parse GitHub issues and PRs
def parse_github_data(issues):
    parsed_issues = []
    parsed_prs = []

    for issue in issues:
        if 'pull_request' in issue:
            parsed_prs.append({
                "title": issue['title'],
                "url": issue['html_url'],
                "user": issue['user']['login'],
                "type": "PR",
                "created_at": issue['created_at']
            })
        else:
            parsed_issues.append({
                "title": issue['title'],
                "url": issue['html_url'],
                "user": issue['user']['login'],
                "type": "Issue",
                "created_at": issue['created_at']
            })
    
    return parsed_issues, parsed_prs

# Send Email Summary
def send_email(issues, prs):
    subject = "GitHub Daily Issues/PR Summary"
    body = "Today's GitHub issues and PRs:\n\n"
    
    body += "📝 Issues:\n"
    for issue in issues:
        body += f"- {issue['title']} ({issue['url']}) by {issue['user']} at {issue['created_at']}\n"
    
    body += "\n🔀 Pull Requests:\n"
    for pr in prs:
        body += f"- {pr['title']} ({pr['url']}) by {pr['user']} at {pr['created_at']}\n"

    msg = MIMEMultipart()
    msg['From'] = EMAIL_FROM
    msg['To'] = EMAIL_TO
    msg['Subject'] = subject

    msg.attach(MIMEText(body, 'plain'))

    with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
        server.starttls()
        server.login(EMAIL_FROM, EMAIL_PASSWORD)
        text = msg.as_string()
        server.sendmail(EMAIL_FROM, EMAIL_TO, text)

    print("Email sent successfully.")

# Send Slack Notification
def send_slack_message(issues, prs):
    client = WebClient(token=SLACK_TOKEN)

    message = "GitHub Daily Summary:\n\n"
    message += "📝 Issues:\n"
    for issue in issues:
        message += f"- {issue['title']} ({issue['url']}) by {issue['user']} at {issue['created_at']}\n"
    
    message += "\n🔀 Pull Requests:\n"
    for pr in prs:
        message += f"- {pr['title']} ({pr['url']}) by {pr['user']} at {pr['created_at']}\n"

    try:
        response = client.chat_postMessage(channel=SLACK_CHANNEL, text=message)
        print("Slack message sent successfully.")
    except SlackApiError as e:
        print(f"Error sending Slack message: {e.response['error']}")

# Export Data to CSV
def export_to_csv(issues, prs):
    fields = ['Title', 'URL', 'User', 'Type', 'Created At']
    rows = []

    for issue in issues:
        rows.append([issue['title'], issue['url'], issue['user'], issue['type'], issue['created_at']])

    for pr in prs:
        rows.append([pr['title'], pr['url'], pr['user'], pr['type'], pr['created_at']])

    with open(CSV_FILENAME, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(fields)
        writer.writerows(rows)

    print(f"CSV report saved as {CSV_FILENAME}.")

# Sync with Notion
def sync_to_notion(issues, prs):
    from notion_client import Client

    notion = Client(auth=NOTION_TOKEN)

    for item in issues + prs:
        notion.pages.create(
            parent={"database_id": DATABASE_ID},
            properties={
                "Title": {"title": [{"text": {"content": item['title']}}]},
                "URL": {"url": item['url']},
                "Type": {"select": {"name": item['type']}},
                "Author": {"rich_text": [{"text": {"content": item['user']}}]},
            }
        )

    print("Synced issues and PRs with Notion.")

# Main function
def main():
    issues = fetch_github_data()
    parsed_issues, parsed_prs = parse_github_data(issues)

    # Send Email
    if SEND_EMAIL:
        send_email(parsed_issues, parsed_prs)

    # Send Slack Notification
    if SEND_SLACK:
        send_slack_message(parsed_issues, parsed_prs)

    # Export to CSV
    if EXPORT_CSV:
        export_to_csv(parsed_issues, parsed_prs)

    # Sync to Notion (optional)
    if NOTION_TOKEN and DATABASE_ID:
        sync_to_notion(parsed_issues, parsed_prs)

if __name__ == "__main__":
    main()