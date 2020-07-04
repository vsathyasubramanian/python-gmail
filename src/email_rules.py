"""
this file contains the EmailRule class which hosts the methods containing the business logic to help us with
processing the rules on the emails available in our local database and push the changes to the server using
appropriate connectors.
"""
__author__ = "sathya.v"

import mysql.connector
from google_connector import GoogleConnector

from config import DATABASE, DB_PASSWORD, DB_USERNAME, action_map, comparator_map, folders_options
from email_dao import EmailDAO


class Action:
    """
    helper class containing the required logic on executing the action on the emails
    """

    def __init__(self):
        pass

    def mark_as_read(self, **kwargs):
        """
        marks the emails as read
        Args:
            email obj list: list of email objects
            modifier_dict: modifier dict to be updated for creating the update request

        Returns:

        """
        for email_obj in kwargs['email_obj_list']:
            if 'UNREAD' in email_obj.labels:
                email_obj.labels.remove('UNREAD')
        kwargs['modifier_dict']['removeLabelIds'].append('UNREAD')

    def mark_as_unread(self, **kwargs):
        """
        marks the emails as unread
        Args:
            email obj list: list of email objects
            modifier_dict: modifier dict to be updated for creating the update request

        Returns:

        """
        for email_obj in kwargs['email_obj_list']:
            if 'UNREAD' not in email_obj.labels:
                email_obj.labels.append('UNREAD')
        kwargs['modifier_dict']['addLabelIds'].append('UNREAD')

    def move_to_folder(self, **kwargs):
        """
        moves the emails to the given folders
        Args:
            email obj list: list of email objects
            modifier_dict: modifier dict to be updated for creating the update request
            option_tag: the destination folder
        Returns:

        """
        for email_obj in kwargs['email_obj_list']:
            # remove existing folder from labels list
            email_obj.labels = [label for label in email_obj.labels if label not in list(folders_options.keys())]
            # add new folder to email labels
            email_obj.labels.append(kwargs['option_tag'])
        kwargs['modifier_dict']['addLabelIds'].append(kwargs['option_tag'])


class EmailRules:
    """
    EmailRules class hosting the core methods to process the rules on the available emails
        run the filter conditions to construct appropriate select query
        run the query and process the required action on the result
        stores the email entity with the updates in the local database
        uses the appropriate strategy method to authenticate and push the updates to server
    """

    def __init__(self):
        self.action_obj = Action()
        self.db_obj = mysql.connector.connect(
            host="localhost",
            user=DB_USERNAME,
            password=DB_PASSWORD,
            database=DATABASE
        )
        self.modify_email_strategy_mapper = {
            'google': self.modify_email_google_strategy
        }

    def modify_email_google_strategy(self, modifier_dict_list, credential_path):
        """
        Brief:
            Google Email update strategy method which updates emails to google servers

        Pseudo-code:
            calls authentication module first to authenticate and retrieve the OAuth token
            calls batch modify email method to update all email content to mail server
        Args:
            modifier_dict_list: list of modification dict to be given as the body of the request to be sent to google
            credential_path: path of the credential/token file
        Returns:

        """
        google_services_obj = GoogleConnector(credentials_path=credential_path)
        print("Authenticating...")
        google_services_obj.authenticate()
        print("Authentication Complete...")
        for modifier_dict in modifier_dict_list:
            google_services_obj.batch_modify_emails(modifier_dict)

    def __construct_query(self, filter_data):
        """
        Brief:
            method to construct the fetch query based on the filter condition
        Args:
            filter_data: dict

        Returns:
            query: string
        """
        base_query = "SELECT * FROM email_snapshot"
        condition_query = ""
        for condition in filter_data['conditions']:
            if condition_query == "":
                # fist condition, append where
                condition_query += " where "
            else:
                # not the first condiion,append operators
                condition_query += " and " if filter_data['predicate'] == 'All' else " or "
            if condition['Predicate'] not in ('Contains', 'Does not Contain'):
                condition_query += condition['Field'] + " " + comparator_map[condition['Predicate']] + " '" + \
                                   condition['Data'] + "'"
            else:
                condition_query += condition['Field'] + " " + comparator_map[condition['Predicate']] + " '%" + \
                                   condition['Data'] + "%'"
        return base_query + condition_query

    def __construct_modify_request(self, email_obj_list, modifier_dict):
        """
        Brief:
            helper method to construct the request to be sent to google servers to update the changes
        Args:
            email_obj_list: list of email obj
            modifier_dict: modify dict with remove and add labels populated

        Returns:
            modified_dict updated with the list of email message ids
        """
        modifier_dict['ids'] = [email_obj.message_id for email_obj in email_obj_list]
        return modifier_dict

    def process_rules(self, rule_data_list, credential_path, service):
        """
        Brief:
            Method to Apply the rules to retrieve the emails from local db and apply the action process upon the email
            and push it to servers
        Pseudo-code:
            Construct the query as per the filter rules
            fetch the relevant data from DB
            perform required modifications
            update the database
        Args:
            rule_data_list: List of rule dicts to be applied in the emails
            [{
                'predicate': 'All',
                'conditions': [{
                    'Field': 'from_address',
                    'Predicate': 'Equals',
                    'Data': 'Google<no-reply@accounts.google.com>'
                },
                {
                    'Field': 'subject',
                    'Predicate': 'Contains',
                    'Data': 'Securityalert'
                },
                {
                    'Field': 'content',
                    'Predicate': 'Contains',
                    'Data': 'grantaccess'
                }],
                'action': ('MarkasRead','')
            }]
            service: email service name
            credential_path: path of the credential and token file
        Returns:
            status : Boolean

        """
        try:
            email_dao_obj = EmailDAO(self.db_obj.cursor(dictionary=True))
            updated_email_obj_list = []
            modifier_dict_list = []
            for rule_data in rule_data_list:
                modifier_dict = {'removeLabelIds': [], 'addLabelIds': []}
                fetch_query = self.__construct_query(rule_data)
                email_obj_list = email_dao_obj.get_email_snapshot(fetch_query)
                if email_obj_list:
                    getattr(self.action_obj, action_map[rule_data['action'][0]])(email_obj_list=email_obj_list,
                                                                                 option_tag=rule_data['action'][1],
                                                                                 modifier_dict=modifier_dict)
                    modifier_dict = self.__construct_modify_request(email_obj_list, modifier_dict)
                    modifier_dict_list.append(modifier_dict)
                    email_dao_obj.update_email_snapshot(email_obj_list)
                updated_email_obj_list.extend(email_obj_list)
            self.modify_email_strategy_mapper[service](modifier_dict_list, credential_path)
            self.db_obj.commit()

            return updated_email_obj_list

        except Exception as ex:
            print("Exception in process filter method %s" % ex)
            return False
        finally:
            self.db_obj.close()
