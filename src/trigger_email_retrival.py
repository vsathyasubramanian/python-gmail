from pyfiglet import Figlet
from console import ConsolePrompt
from email_retriever import EmailRetriever

if __name__ == "__main__":
    f = Figlet(font='slant')
    print(f.renderText('Email Manager'))
    fetch_email_obj = EmailRetriever()
    retrieved_email_obj_list = fetch_email_obj.fetch_emails('google')
    ConsolePrompt().print_email_snapshot(retrieved_email_obj_list)

