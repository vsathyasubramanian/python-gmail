# Python Gmail Integration
![pylint badge](https://github.com/vsathyasubramanian/python-gmail/blob/python-gmail_v2/pylint.svg)

A simple email manager CLI program using Gmail API to fetch emails and store it in a local DB and process filters on it 

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
python fetch_mails.py
```


The second script would prompt the user the filter to be executed and the action to be performed upon the filtered emails. (the rules,filters,actions can be modified in config.py)
The updates are performed based on the action chosen and the local database is updated.

```bash
python run_filters.py
```
