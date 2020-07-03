from pyfiglet import Figlet
from console import ConsolePrompt
from email_rules import EmailRules
from config import rule_list, condition_dict, predicate_prompt, style, action_dict
from PyInquirer import prompt
import sys


def fetch_rules_from_config():
    """
    Brief:
        Method to fetch rule data from config and construct the rule data list
    Args:

    Returns:
        rule_data: list of dict
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
    f = Figlet(font='slant')
    print(f.renderText('Email Manager'))
    email_rules_obj = EmailRules()
    if mode == 'auto':
        rule_data_list = fetch_rules_from_config()
    elif mode == 'manual':
        rule_data_list = fetch_rules_from_runtime()
    else:
        print("Please enter proper mode value --> auto/manual")
        exit()
    ConsolePrompt().print_rule_data(rule_data_list)
    updated_email_obj_list = email_rules_obj.process_rules(rule_data_list, 'google')
    if updated_email_obj_list:
        print('After Update:')
        ConsolePrompt().print_email_snapshot(updated_email_obj_list)
