"""
DAO file with all database interaction methods
"""
__author__ = "sathya.v"

import json

from email_entity import EmailEntity


class EmailDAO():
    """
    dao class hosting all the db interaction methods
    """

    def __init__(self, cursor_obj):
        self.cursor_obj = cursor_obj

    def bulk_insert_email_snapshot(self, email_entity_list):
        """
        Brief:
            dao method to insert data into email_snapshot table
        Args:
            email_entity_list: list of object
        Returns:
            status: boolean
        """
        try:
            query = "INSERT INTO email_snapshot (msg_id, labels, from_address, to_address, date, subject, content) \
                     VALUES (%s, %s, %s, %s, %s, %s, %s)"
            attribute_values = []
            for email_entity in email_entity_list:
                attribute_values.append(
                    (email_entity.msg_id,
                     json.dumps(email_entity.labels),
                     email_entity.from_address,
                     email_entity.to_address,
                     email_entity.date,
                     email_entity.subject,
                     email_entity.content
                     )
                )
            self.cursor_obj.executemany(query, attribute_values)
            return True
        except Exception as ex:
            print("Error in storing it in database %s " % ex)
            return False

    def get_email_snapshot(self, query):
        """
        Brief:
            dao method to get data into email_snapshot table
        Args:
            query: constructed fetch query
        Returns:
            status: list of email_obj
        """
        try:
            self.cursor_obj.execute(query)
            object_list = []
            result = self.cursor_obj.fetchall()
            for record in result:
                object_list.append(EmailEntity(record))
            return object_list
        except Exception as ex:
            print("Error in fetching data from database %s " % ex)
            return False

    def update_email_snapshot(self, email_entity_list):
        """
        Brief:
            dao method to update data into email_snapshot table
            performs an update with replace operation
        Args:
            email_entity_list: list of object
        Returns:
            status: boolean
        """
        try:
            query = "REPLACE INTO email_snapshot (email_snapshot_id, msg_id, labels, from_address, to_address, date, subject, content) \
                     VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
            attribute_values = []
            for email_entity in email_entity_list:
                attribute_values.append(
                    (email_entity.email_snapshot_id,
                     email_entity.msg_id,
                     json.dumps(email_entity.labels),
                     email_entity.from_address,
                     email_entity.to_address,
                     email_entity.date,
                     email_entity.subject,
                     email_entity.content
                     )
                )
            self.cursor_obj.executemany(query, attribute_values)
            return True
        except Exception as ex:
            print("Error in updating it in database %s " % ex)
            return False
