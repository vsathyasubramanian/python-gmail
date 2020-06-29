import datetime
import json

import validictory

from config import EMAIL_ENTITY


class Validator():
    """
    A decorator that validates the entities when used along with
    setter method of the entities
    :calling: @Validator(schema)
    :schema: {"type":"integer","required":True,"minimum":1,}
    """

    def __init__(self, schema):
        self.schema = schema

    def __call__(self, funct):
        def inner(*arg, **kwargs):
            try:
                validictory.validate(arg[1], self.schema)
                funct(*arg, **kwargs)
            except Exception:
                print('validation error!!')
                raise

        return inner


class EmailEntity():
    """
    email entity class with validator
    """

    def __init__(self, email_details=None):

        self.__email_snapshot_id = None
        self.__msg_id = None
        self.__from_address = None
        self.__to_address = None
        self.__date = None
        self.__subject = None
        self.__content = None
        self.__labels = None

        if email_details and type(email_details) is dict:
            for attr, value in list(email_details.items()):
                if value:
                    setattr(self, attr, value)

    @property
    def email_snapshot_id(self):
        return self.__email_snapshot_id

    @email_snapshot_id.setter
    @Validator(EMAIL_ENTITY['email_snapshot_id'])
    def email_snapshot_id(self, email_snapshot_id):
        self.__email_snapshot_id = email_snapshot_id

    @property
    def msg_id(self):
        return self.__msg_id

    @msg_id.setter
    @Validator(EMAIL_ENTITY['msg_id'])
    def msg_id(self, msg_id):
        self.__msg_id = msg_id

    @property
    def from_address(self):
        return self.__from_address

    @from_address.setter
    @Validator(EMAIL_ENTITY['from_address'])
    def from_address(self, from_address):
        self.__from_address = from_address

    @property
    def to_address(self):
        return self.__to_address

    @to_address.setter
    @Validator(EMAIL_ENTITY['to_address'])
    def to_address(self, to_address):
        self.__to_address = to_address

    @property
    def subject(self):
        return self.__subject

    @subject.setter
    @Validator(EMAIL_ENTITY['subject'])
    def subject(self, subject):
        self.__subject = subject

    @property
    def date(self):
        return self.__date

    @date.setter
    def date(self, date):
        if not isinstance(date, datetime.date):
            print("Validation error!!")
            raise
        self.__date = date

    @property
    def content(self):
        return self.__content

    @content.setter
    @Validator(EMAIL_ENTITY['content'])
    def content(self, content):
        self.__content = content

    @property
    def labels(self):
        return self.__labels

    @labels.setter
    @Validator(EMAIL_ENTITY['labels'])
    def labels(self, labels):
        if isinstance(labels, str):
            labels = json.loads(labels)
        self.__labels = labels
