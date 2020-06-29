"""
filter script which runs the configured filters from config.py and performs the required actions
"""
__author__ = "sathya.v"

from collections import defaultdict

import mysql.connector
from apiclient import errors
from googleapiclient.discovery import build
from pyfiglet import Figlet

from authenticate import Authenticate
from config import db_password, db_username, database, filter_dict, add_label_options, folders_options, action_dict, \
    rule_dict
from console import ConsolePrompt
from email_dao import EmailDAO


class PerformAction():
    """
    action class which contains the logic towards the required action
    """

    def __init__(self):
        pass

    def mark_as_read(self, **kwargs):
        """
        marks the emails as read
        Args:
            email obj list:

        Returns:

        """
        for email_obj in kwargs['email_obj_list']:
            if 'UNREAD' in email_obj.labels: email_obj.labels.remove('UNREAD')

    def mark_as_unread(self, **kwargs):
        """
        marks the emails as unread
        Args:
            email obj list:

        Returns:

        """
        for email_obj in kwargs['email_obj_list']:
            if 'UNREAD' not in email_obj.labels: email_obj.labels.append('UNREAD')

    def move_to_folder(self, **kwargs):
        """
        moves the emails to the given folders
        Args:
            email obj list , destination folder

        Returns:

        """
        for email_obj in kwargs['email_obj_list']:
            # remove existing folder from labels list
            email_obj.labels = [label for label in email_obj.labels if label not in list(folders_options.keys())]
            # add new folder to email labels
            email_obj.labels.append(kwargs['option_tag'])

    def add_label(self, **kwargs):
        """
        adds the given labels to the emails.
        Args:
            email obj list, new label:

        Returns:

        """
        for email_obj in kwargs['email_obj_list']:
            email_obj.labels.append(kwargs['option_tag'])


class RunFilters():
    """
    main filter class which hosts the core filter logic and methods
    """

    def __init__(self):
        self.service = None
        self.email_obj_list = None
        self.oauth_obj = None
        self.console_obj = ConsolePrompt()
        self.action_obj = PerformAction()

        self.db_obj = mysql.connector.connect(
            host="localhost",
            user=db_username,
            password=db_password,
            database=database
        )
        self.comparator_map = {
            'Equals': '=',
            'Does not equal': '!=',
            'Contains': 'like',
            'Does not Contain': 'not like',
            'Less than': '<',
            'Greater than': '>'
        }
        self.action_mapper = {
            'Mark as Read': self.action_obj.mark_as_read,
            'Mark as UnRead': self.action_obj.mark_as_unread,
            'Move to Folder': self.action_obj.move_to_folder,
            'Add Label': self.action_obj.add_label,
        }

    def _fetch_filters(self):
        """
        Brief:
            Method to fetch filter data from config and construct the filter data
        Args:

        Returns:
            filter_conditions: dict
        """
        filter_id = self.console_obj.prompt_filter_id()
        filter_data = defaultdict(list)
        filter_data[filter_dict[filter_id]['Predicate']].extend(
            [rule_dict[key_id] for key_id in filter_dict[filter_id]['keys']])
        return filter_data

    def _construct_query(self, filter_data):
        """
        Brief:
            method to construct the fetch query based on the filter condition
        Args:
            filter_data: dict

        Returns:
            query: string
        """
        base_query = "SELECT * FROM email_snapshot"
        for key, rules in filter_data.items():
            condition_query = ""
            for rule in rules:
                if condition_query == "":
                    # fist condition, append where
                    condition_query += " where "
                else:
                    # not the first condiion,append operators
                    condition_query += " and " if key == 'All' else " or "
                if rule['Predicate'] not in ('Contains', 'Does not Contain'):
                    condition_query += rule['Field'] + " " + self.comparator_map[rule['Predicate']] + " '" + rule[
                        'Data'] + "'"
                else:
                    condition_query += rule['Field'] + " " + self.comparator_map[rule['Predicate']] + " '%" + rule[
                        'Data'] + "%'"
        return base_query + condition_query

    def _populate_available_labels(self):
        """
        Brief:
            helper method to populate the available labels by making a RESTApi call to the server
        Returns:

        """
        self.service = build('gmail', 'v1', credentials=self.oauth_obj.cred)
        result = self.service.users().labels().list(userId='me').execute()
        labels = result.get('labels', [])
        for label in labels:
            # separating folders from add on labels
            if label['name'] not in list(folders_options.keys()):
                add_label_options[label['name']] = label['id']

    def perform_updates(self):
        """
        Brief:
            helper method to list the available labels and update the email data
        Returns:
            None
        """
        if self.email_obj_list:
            self._populate_available_labels()
            action_id, option_tag = self.console_obj.prompt_action_id(self.email_obj_list)
            self.action_mapper[action_dict[action_id]](email_obj_list=self.email_obj_list, option_tag=option_tag)
        else:
            print("no email match the filter conditions")

    def process_filters(self):
        """
        Brief:
            Method to Apply the filters from config upon the available emails
        Returns:
            status : Boolean

        """
        try:
            filter_data = self._fetch_filters()
            fetch_query = self._construct_query(filter_data)
            dao_obj = EmailDAO(self.db_obj.cursor(dictionary=True))
            self.email_obj_list = dao_obj.get_email_snapshot(fetch_query)
            self.perform_updates()
            if self.email_obj_list:
                dao_obj.update_email_snapshot(self.email_obj_list)
                print("Updates saved")
                self.console_obj.print_email_snapshot(self.email_obj_list)
        except errors.HttpError as error:
            print("Exception in fetch email method %s" % error)
            raise
        except Exception as ex:
            print("Exception in fetch email method %s" % ex)
            raise
        finally:
            self.db_obj.commit()
            self.db_obj.close()

    def trigger_script(self):
        """
        Brief:
            Driver method to start the applying the filters from config
            Call apply filter method and prompt for the filter id to be executed
            Construct the query as per the filter rules
            fetch the relevant data from DB
            perform required modifications
            update the database
        Returns:
            status : Boolean
        """
        oauth_obj = Authenticate()
        print("Authenticating...")
        oauth_obj.authenticate()
        print("Authentication Complete...")
        self.oauth_obj = oauth_obj
        self.process_filters()


if __name__ == "__main__":
    f = Figlet(font='slant')
    print(f.renderText('Email Manager'))
    run_filters_obj = RunFilters()
    run_filters_obj.trigger_script()
