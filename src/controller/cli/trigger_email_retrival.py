"""
Console script to trigger the email retrieval process
"""
__author__ = "sathya.v"

from pyfiglet import Figlet

from controller.cli.custom_printer import CustomPrinter
from middleware.email_retriever import EmailRetriever

if __name__ == "__main__":
    print(Figlet(font='slant').renderText('Email Manager'))
    retrieve_email_obj = EmailRetriever()
    retrieved_email_obj_list = retrieve_email_obj.retrieve_emails('../credentials/', 'google')
    CustomPrinter().print_email_snapshot(retrieved_email_obj_list)