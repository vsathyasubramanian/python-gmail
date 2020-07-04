"""
Console script to construct the rule dict and trigger the email rule execution process
"""
__author__ = "sathya.v"

import sys

from PyInquirer import prompt
from pyfiglet import Figlet

from config import action_dict, condition_dict, predicate_prompt, rule_list, style
from console import ConsolePrompt
from email_rules import EmailRules


def fetch_rules_from_config():
    """
    Brief:
        Method to fetch rule data from config and construct the rule data list
    Args:

    Returns:
        rule_data: list of dict
        [{
                'predicate': 'All',
                'conditions': [{
                    'Field': 'from_address',
                    'Predicate': 'Equals',
                    'Data': 'Google<no-reply@accounts.google.com>'
                },
                {
                    'Field': 'content',
                    'Predicate': 'Contains',
                    'Data': 'grantaccess'
                }],
                'action': ('MarkasRead','')
            }]
    """

    rule_data = []
    for rule in rule_list:
        rule_data_dict = {'predicate': rule['predicate'],
                          'conditions': [condition_dict[condition_id] for condition_id in rule['condition_ids']],
                          'action': rule['action']}
        rule_data.append(rule_data_dict)
    return rule_data


def fetch_rules_from_runtime():
    """
    Brief:
        Method to fetch rule data option during runtime and construct the rule data list
    Args:

    Returns:
        rule_data: list of dict
        [{
                'predicate': 'All',
                'conditions': [{
                    'Field': 'from_address',
                    'Predicate': 'Equals',
                    'Data': 'Google<no-reply@accounts.google.com>'
                },
                {
                    'Field': 'content',
                    'Predicate': 'Contains',
                    'Data': 'grantaccess'
                }],
                'action': ('MarkasRead','')
            }]
    """
    condition_id_list = ConsolePrompt().print_condition_data(is_prompt=True)
    predicate = prompt(predicate_prompt, style=style)['predicate']
    action_id = ConsolePrompt().print_action_id(is_prompt=True)

    rule_data = []
    rule_data_dict = {'predicate': predicate,
                      'conditions': [condition_dict[condition_id] for condition_id in condition_id_list],
                      'action': action_dict[action_id]}
    rule_data.append(rule_data_dict)
    return rule_data


if __name__ == "__main__":
    # import pdb; pdb.set_trace()
    mode = sys.argv[1]
    print(Figlet(font='slant').renderText('Email Manager'))
    if mode == 'auto':
        rule_data_list = fetch_rules_from_config()
    elif mode == 'manual':
        rule_data_list = fetch_rules_from_runtime()
    else:
        print("Please enter proper mode value --> auto/manual")
        sys.exit()

    email_rules_obj = EmailRules()
    ConsolePrompt().print_rule_data(rule_data_list)
    updated_email_obj_list = email_rules_obj.process_rules(rule_data_list, '../credentials/', 'google')
    if updated_email_obj_list:
        print('After Update:')
        ConsolePrompt().print_email_snapshot(updated_email_obj_list)
