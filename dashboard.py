from flask import Flask, render_template
from github_tracker import fetch_github_data, parse_github_data

app = Flask(__name__)

@app.route("/")
def home():
    issues = fetch_github_data()
    parsed_issues, parsed_prs = parse_github_data(issues)
    return render_template("dashboard.html", issues=parsed_issues, prs=parsed_prs)

if __name__ == "__main__":
    app.run(debug=True)