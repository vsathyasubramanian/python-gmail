# Python Gmail Integration
![pylint badge](https://github.com/vsathyasubramanian/python-gmail/blob/python-gmail_v2/pylint.svg)

A simple email manager CLI program using Gmail API to fetch emails and store it in a local DB and process filters on it 

Pylint report is available in ![pylint report](https://github.com/vsathyasubramanian/python-gmail/blob/python-gmail_v2/pylint report.txt)
Documentation files can be accessed from ![index](https://github.com/vsathyasubramanian/python-gmail/blob/python-gmail_v2/docs/index.html)

## Requirements

Python version > 3.6

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install the required additional packages. All the required additional packages are available in requirements.txt

```bash
pip -r requirements.txt
```


## Usage
### Database initialization

Before triggering the scripts source the sql file to create and initialize the database tables.

```bash
mysql -u 'root' -p 'password' < email_manager_initial_data.sql
```

Change the database user name and password in the config.py file if need be.

### script usage
This is a two part CLI program.

The first script would trigger an OAuth request to the google server and upon successful authentication would create the required token.pickle file which shall be used for sending requests to the server henceforth
It fetches all the mails from the google servers and parses it and stores it in local database 

```bash
python trigger_email_retrival.py
```


The second script can be run in two modes, Auto would read the rule from config.py and execute it on the emails and Manual would prompt the user for rules options.The updates are performed based on the action chosen and the updates are pushed to the servers along with a local database is update.

```bash
python trigger_email_rules.py <<auto/manual>>
```
