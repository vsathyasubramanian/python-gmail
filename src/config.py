"""
global config file containing frequently varied configurations
"""
__author__ = "sathya.v"

from PyInquirer import Token, style_from_dict

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

condition_prompt = [
    {
        'type': 'input',
        'name': 'condition_id',
        'message': 'Enter comma separated condition ids to include',
        'default': '1,2,3'
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
predicate_prompt = [
    {
        'type': 'input',
        'name': 'predicate',
        'message': 'Enter Predicate Option',
        'default': 'All'
    }
]
########################################################################################################################


# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly',
          'https://mail.google.com/']

DB_USERNAME = "root"
DB_PASSWORD = "testpass"
DATABASE = "email_manager"

EMAIL_ENTITY = {
    "email_snapshot_id": {"type": "integer", "required": False},
    "message_id": {"type": "string", "required": True},
    "from_address": {"type": "string", "required": True},
    "to_address": {"type": "string", "required": True},
    "subject": {"type": "string", "required": True},
    "content": {"type": "string", "required": False},
    "labels": {"type": ["array", "string"], "required": True}
}

################################################## MAPPER TABLES #######################################################
comparator_map = {
    'Equals': '=',
    'Does not equal': '!=',
    'Contains': 'like',
    'Does not Contain': 'not like',
    'Less than': '<',
    'Greater than': '>'
}

action_map = {
    'Mark as Read': 'mark_as_read',
    'Mark as UnRead': 'mark_as_unread',
    'Move to Folder': 'move_to_folder',
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

################################################## RULES AND FILTERS ###################################################

######{ACTION ID : ACTION}###########

action_dict = {
    1: ('Mark as Read', ''),
    2: ('Mark as UnRead', ''),
    3: ('Move to Folder', 'SPAM')
}

######{CONDITION ID : ATTRIBUETS}###########

condition_dict = {
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

######### Hard Coded rule list ##########

rule_list = [
    {
        'condition_ids': [1, 2, 3],
        'predicate': 'All',
        'action': ('Mark as UnRead', '')
    },
    {
        'condition_ids': [4, 5, 6],
        'predicate': 'All',
        'action': ('Move to Folder', 'SPAM')
    }
]
