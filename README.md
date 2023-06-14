# Email Processor

This project uses Google's Gmail API to fetch emails from your Gmail Inbox and store them in a relational database. It then processes these emails based on some rules which are stored in a JSON file.

## Dependencies

This project requires Python 3.7+ and following Python libraries installed:

- Google Client Library
- psycopg2 - PostgreSQL database adapter for Python
- dateutil

## Setup

### Database Setup

This project uses a PostgreSQL database. Update the `db/db_config.json` file with your database host, name, user, password and port details.

### Gmail API Setup

Follow the Gmail API Python Quickstart guide (https://developers.google.com/gmail/api/quickstart/python) to set up your project, enable the Gmail API and download the `credentials.json` file. Move this file to the project directory.

### Install Python Dependencies

Navigate to the project directory and run the following command to install the required Python dependencies.

```bash
pip install -r requirements.txt
```

### How to Run
There are two Python scripts that you will need to run:

fetch_emails.py: This script fetches the emails from your Gmail Inbox and stores them in the database.

```bash
python fetch_emails.py
```

process_emails.py: This script reads the rules from the rules/rules.json file and processes the emails based on these rules.

```bash
python process_emails.py
```

### Rules
Rules are stored in a JSON file (rules/rules.json). Each rule is a JSON object that contains a predicate ("all" or "any"), conditions (field, operator and value) and actions.

Example of a rule:

```json
{
    "predicate": "all",
    "conditions": [
        {"field": "from", "operator": "contains", "value": "@gmail.com"},
        {"field": "subject", "operator": "does not contain", "value": "spam"}
    ],
    "actions": ["mark as read"]
}
```