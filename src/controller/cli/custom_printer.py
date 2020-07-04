"""
Util functions to help with the console interaction
"""
__author__ = "sathya.v"

import tabulate

from config.config import action_dict, condition_dict


class CustomPrinter:
    """
    Hosts helper methods to assist with the console interactions
    """

    def __init__(self):
        pass

    def print_email_snapshot(self, email_obj_list):
        """
        Brief:
            Helper method to print tabulated email data
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
              Helper method to print tabulated rule data
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

    def print_action_id(self):
        """
        Brief:
            Helper method to prompt the user for action to perform

        Returns:
            None
        """
        header = ['Action ID', 'Action']
        rows = []
        for key, value in action_dict.items():
            rows.append([key, value])
        print(tabulate.tabulate(rows, header))

    def print_condition_data(self):
        """
        Brief:
            Helper method to print tabulated condition data

        Returns:
            None
        """

        rule_header = ['Condition ID' 'Field', 'Predicate', 'Value']
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
