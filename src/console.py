"""
util functions to help with the console interaction
"""
__author__ = "sathya.v"

import tabulate
from PyInquirer import prompt

from config import action_dict, style, action_prompt, \
    condition_dict, condition_prompt


class ConsolePrompt:
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

    def print_rule_data(self, rule_data_list):
        """
          Brief:
              helper method to print tabulated rule data
          Args:
              rule data_list: list of rule data

          Returns:

          """

        rule_header = ['Field', 'Predicate', 'Value']
        for rule_data in rule_data_list:
            print("Rule Description:")
            rows = []
            for condition in rule_data['conditions']:
                rows.append(
                    [
                        condition['Field'],
                        condition['Predicate'],
                        condition['Data']
                    ]
                )
            print(tabulate.tabulate(rows, rule_header, tablefmt='psql'))
            print("If '%s' of the above conditions are met, Perform the below actions" % rule_data['predicate'])
            print(tabulate.tabulate([[rule_data['action'][0] + ' ' + rule_data['action'][1]]], ['Action'],
                                    tablefmt='psql') + '\n')
        return None

    def print_action_id(self,is_prompt=False):
        """
        Brief:
            helper method to prompt the user for action to perform
        Args:
            is_prompt: checks weather prompt input is required
        Returns:
            Action id
        """
        header = ['Action ID', 'Action']
        rows = []
        for key, value in action_dict.items():
            rows.append([key, value])
        print(tabulate.tabulate(rows, header))
        if is_prompt:
            action_id = int(prompt(action_prompt, style=style)['action_id'])
            return action_id
        return None

    def print_condition_data(self,is_prompt=False):
        """
        Brief:
            helper method to print tabulated condition data
        Args:
            is_prompt: flag to check if prompt is to be shown to retrieve list of condition ids
        Returns:
            None
        """

        rule_header = ['Condiion ID' 'Field', 'Predicate', 'Value']
        rows = []
        for condition_id, condition in condition_dict.items():
            rows.append(
                [
                    condition_id,
                    condition['Field'],
                    condition['Predicate'],
                    condition['Data']
                ]
            )
        print(tabulate.tabulate(rows, rule_header, tablefmt='psql'))
        if is_prompt:
            condition_id_list = list(map(int,prompt(condition_prompt, style=style)['condition_id'].split(',')))
            return condition_id_list
        return None
