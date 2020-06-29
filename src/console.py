"""
util functions to help with the console interaction
"""
__author__ = "sathya.v"

import tabulate
from PyInquirer import prompt

from config import folders_options, add_label_options, filter_email, action_dict, style, filter_dict, action_prompt, \
    option_prompt, rule_dict


class ConsolePrompt():
    """
    hosts helper methods to assist with the console interactions
    """

    def __init__(self):
        pass

    def print_email_snapshot(self, email_obj_list):
        """
        Brief:
            helper method to print tabulated email data
        Args:
            email_obj_list: list of email objects

        Returns:

        """

        header = ['From Address', 'Received Date', 'Labels', 'Subject']
        rows = []
        for email_obj in email_obj_list:
            rows.append(
                [
                    email_obj.from_address,
                    email_obj.date,
                    email_obj.labels,
                    email_obj.subject[:15]
                ]
            )
        if rows:
            print(tabulate.tabulate(rows, header))
        else:
            print("No mails to fetch!!")

    def prompt_filter_id(self):
        """
        Brief:
            helper method to prompt the user for the filter to execute
        Returns:
            filter_id
        """
        print("AVAILABLE RULES")
        header = ['Rule ID', 'Field', 'Predicate', 'Value']
        rows = []
        for key, value in rule_dict.items():
            rows.append(
                [
                    key,
                    value['Field'],
                    value['Predicate'],
                    value['Data']
                ]
            )
        print(tabulate.tabulate(rows, header))
        print("AVAILABLE FILTERS")
        header = ['Filter ID', 'Predicate', 'Rule ID']
        rows = []
        for key, value in filter_dict.items():
            rows.append(
                [
                    key,
                    value['Predicate'],
                    value['keys']
                ]
            )
        print(tabulate.tabulate(rows, header))
        filter_id = int(prompt(filter_email, style=style)['filter_id'])
        return filter_id

    def prompt_action_id(self, email_obj_list):
        """
        Brief:
            helper method to prompt the user for action to perform
        Args:
            email_obj_list: list of email objects
        Returns:
            Action id, Option tag: the action to perform and option tag if additional tags are required to perform that
            action
        """
        print("FILTERED EMAILS")
        self.print_email_snapshot(email_obj_list)
        header = ['Action ID', 'Action', 'Available Options']
        rows = []
        option_tag = None
        for key, value in action_dict.items():
            if key in (1, 2):
                # mark as read un read options
                rows.append([key, value, ''])
            elif key == 3:
                # move to folder option
                rows.append([key, value, ','.join(list(folders_options.keys()))])
            elif key == 4:
                rows.append([key, value, ','.join(list(add_label_options.keys()))])
        print(tabulate.tabulate(rows, header))
        action_id = int(prompt(action_prompt, style=style)['action_id'])
        if action_id in (3, 4):
            option_tag = prompt(option_prompt, style=style)['option_tag']
        return action_id, option_tag
