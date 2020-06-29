"""
global config file containing frequently varied configurations
"""
__author__ = "sathya.v"

from PyInquirer import style_from_dict, Token

##################################################Console formater######################################################

style = style_from_dict({
    Token.Separator: '#cc5454',
    Token.QuestionMark: '#673ab7 bold',
    Token.Selected: '#cc5454',  # default
    Token.Pointer: '#673ab7 bold',
    Token.Instruction: '',  # default
    Token.Answer: '#f44336 bold',
    Token.Question: '',
})

filter_email = [
    {
        'type': 'input',
        'name': 'filter_id',
        'message': 'Enter filter ID',
        'default': '1'
    }
]
action_prompt = [
    {
        'type': 'input',
        'name': 'action_id',
        'message': 'Enter Action ID to perform action',
        'default': '1'
    }
]
option_prompt = [
    {
        'type': 'input',
        'name': 'option_tag',
        'message': 'Enter option tag from available options',
        'default': ''
    }
]
########################################################################################################################


# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly',
          'https://mail.google.com/']

db_username = "root"
db_password = "jaguarxj"
database = "email_manager"

EMAIL_ENTITY = {
    "email_snapshot_id": {"type": "integer", "required": False},
    "msg_id": {"type": "string", "required": True},
    "from_address": {"type": "string", "required": True},
    "to_address": {"type": "string", "required": True},
    "subject": {"type": "string", "required": True},
    "content": {"type": "string", "required": False},
    "labels": {"type": ["array", "string"], "required": True}
}
################################################# FOLDERS AND LABELS ###################################################

######{LABEL NAME : LABEL ID}###########
folders_options = {
    'CHAT': 'CHAT',
    'SENT': 'SENT',
    'INBOX': 'INBOX',
    'TRASH': 'TRASH',
    'DRAFT': 'DRAFT',
    'SPAM': 'SPAM'

}

add_label_options = {}
################################################## RULES AND FILTER ####################################################

######{RULE ID : ATTRIBUETS}###########

rule_dict = {
    1: {'Field': 'from_address',
        'Predicate': 'Equals',
        'Data': "Google <no-reply@accounts.google.com>"},
    2: {'Field': 'subject',
        'Predicate': 'Contains',
        'Data': "Security alert"},
    3: {'Field': 'content',
        'Predicate': 'Contains',
        'Data': "grant access"},
    4: {'Field': 'from_address',
        'Predicate': 'Contains',
        'Data': "sathya.40293@gmail.com"},
    5: {'Field': 'subject',
        'Predicate': 'Contains',
        'Data': "Project"},
    6: {'Field': 'date',
        'Predicate': 'Greater than',
        'Data': "2020-06-27"}
}

######{FILTER ID : PREDICATE, RULE_ID_KEYS}###########
filter_dict = {
    1: {'Predicate': 'All', 'keys': [1, 2, 3]},
    2: {'Predicate': 'All', 'keys': [4, 5, 6]},
    3: {'Predicate': 'Any', 'keys': [4, 5, 6]},
    4: {'Predicate': 'All', 'keys': [1, 2, 6]}
}

######{ACTION ID : ACTION}###########
action_dict = {1: 'Mark as Read',
               2: 'Mark as UnRead',
               3: 'Move to Folder',
               4: 'Add Label'}
