# GitHub Issue/PR Tracker

This project allows you to track GitHub Issues and Pull Requests (PRs) from a specific repository, send email and Slack notifications, export data to CSV, and even sync the data to Notion for easy collaboration. Additionally, it includes a Flask-based real-time dashboard to view the current issues and PRs.

## Features

- **Track GitHub Issues and PRs**: Fetch data from a GitHub repository using the GitHub API.
- **Email Summary**: Send a daily summary of issues and PRs via email using SMTP.
- **Slack Notification**: Send daily updates to a Slack channel using the Slack Web API.
- **Export to CSV**: Save the issues and PRs in CSV format for further analysis.
- **Sync with Notion**: Sync the issues and PRs with a Notion database.
- **Flask Dashboard**: Display a real-time dashboard of issues and PRs.
- **CRON Support**: Schedule the script to run daily using a CRON job.

## Requirements

- Python 3.x
- Required libraries:
  - `requests`
  - `smtplib`
  - `slack_sdk`
  - `flask`
  - `notion-client`
  
####You can install the necessary libraries using the following command:

```bash
pip install requests slack_sdk flask notion-client
```

## Setup Instructions

### Step 1: GitHub API Setup

1. Create a GitHub Personal Access Token. You can create one in your [GitHub settings](https://github.com/settings/tokens).
2. Replace the following values in `github_tracker.py` with your GitHub information:
   - `GITHUB_TOKEN`: Your GitHub Personal Access Token.
   - `OWNER`: The GitHub repository owner.
   - `REPO`: The GitHub repository name.

### Step 2: Email Configuration (Optional)

To send email notifications, you'll need to set up your email credentials:

1. Replace the following values in `github_tracker.py`:
   - `EMAIL_FROM`: Your email address.
   - `EMAIL_PASSWORD`: Your email account password.
   - `SMTP_SERVER`: Your email server (e.g., "smtp.gmail.com" for Gmail).
   - `SMTP_PORT`: SMTP port (587 for Gmail).
   - `EMAIL_TO`: Recipient email address.

### Step 3: Slack Configuration (Optional)

To send Slack notifications, create an incoming webhook on Slack and use the following settings:

1. Replace the following values in `github_tracker.py`:
   - `SLACK_TOKEN`: Your Slack API token.
   - `SLACK_CHANNEL`: The Slack channel where the notifications will be sent.
   - `SLACK_WEBHOOK_URL`: Your Slack Webhook URL.

### Step 4: Notion Sync (Optional)

To sync the issues and PRs to Notion:

1. Generate a Notion integration token via the [Notion developers page](https://www.notion.so/my-integrations).
2. Replace the following values in `github_tracker.py`:
   - `NOTION_TOKEN`: Your Notion integration token.
   - `DATABASE_ID`: The ID of your Notion database where issues and PRs will be synced.

### Step 5: CSV Export (Optional)

The script can automatically export the issues and PRs to a CSV file. You can modify the file name and location by changing the `CSV_FILENAME` variable in `github_tracker.py`.

### Step 6: Running the Script

Once you have configured the settings, you can run the tracker:

```bash
python github_tracker.py
```

This will fetch issues and PRs from the specified GitHub repository and perform the following actions based on your configuration:

- Send an email summary (if configured).
- Send a Slack notification (if configured).
- Export the data to CSV (if configured).
- Sync the data to Notion (if configured).

### Step 7: Flask Dashboard (Optional)

If you want to set up a real-time dashboard to view the issues and PRs:

1. Run the Flask app with:

```bash
python dashboard.py
```

2. Open your web browser and navigate to `http://localhost:5000` to see the real-time dashboard.

### Step 8: Scheduling the Script (Optional)

To run the script automatically every day (e.g., for a daily check-in), you can schedule the script using CRON on Linux/macOS.

1. Open the CRON configuration:

```bash
crontab -e
```

2. Add the following line to run the script every day at 9:00 AM:

```bash
0 9 * * * /path/to/python3 /path/to/github_tracker.py
```

## Project Structure

```
/github-tracker
    ├── github_tracker.py        # The main tracking script
    ├── dashboard.py             # Flask dashboard (optional)
    ├── /templates
    │   └── dashboard.html       # Dashboard HTML template
    └── README.txt               # This README file
```

## Customization

You can customize the following aspects of the project:

- **Email Notifications**: Modify the email body and recipient list.
- **Slack Messages**: Customize the message format and Slack channel.
- **CSV Export**: Change the CSV filename and the fields you want to include.
- **Notion Integration**: Adjust the Notion database properties for syncing.
- **Flask Dashboard**: Modify the dashboard template to include additional information or features.

## Troubleshooting

- **GitHub API Limits**: GitHub API has rate limits. If you encounter errors due to rate limiting, check [GitHub’s API rate limits](https://docs.github.com/en/rest/overview/resources-in-the-rest-api#rate-limiting).
- **Slack Errors**: If the Slack message fails, ensure your Slack API token and webhook URL are correct.
- **Email Errors**: If you encounter issues with email delivery, check the SMTP settings and ensure the email account allows "less secure apps" if necessary.

## License

This project is open-source and available under the MIT License.
