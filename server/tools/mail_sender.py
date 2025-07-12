import smtplib
from dotenv import load_dotenv
import os
from email.message import EmailMessage # Import EmailMessage

load_dotenv()

class MailSender:
    """
    This class is a utility class that sends mail to the receivers

    Functions:
    sendMail(subject:str, message:str, dest:str) -> sends mail to a destination mail
    sendMailBatch(subject:str, message:str, dests:list) -> sends mail to multiple receivers
    """
    def __init__(self):
        try:
            self.__sender_mail = os.getenv("SENDER_MAIL")
            self.__pass = os.getenv("MAIL_PASS")
            self.sender = smtplib.SMTP('smtp.gmail.com', 587)
            self.sender.starttls()
            self.sender.login(self.__sender_mail,self.__pass)
        except Exception as e:
            print("Error occurred : \n",e)
            raise e

    def sendMail(self, subject:str, message:str, dest:str)->bool:
        """
        Sends message to a particular receiver with a subject

        Args:
            subject : subject of the email
            message : message to be send
            dest : receiver's email id
        Returns:
            bool : True, on success False, on failure
        """
        try:
            msg = EmailMessage()
            msg['Subject'] = subject
            msg['From'] = self.__sender_mail
            msg['To'] = dest
            msg.set_content(message) # Set the plain text content

            self.sender.sendmail(self.__sender_mail, dest, msg.as_string())
            return True
        except Exception as e:
            print("Something went wrong :\n",e)
            raise e
            return False

    def sendMailBatch(self, subject:str, message:str, dests:list)->int:
        """
        Sends mail to a list on receivers with a subject

        Args:
            subject : subject of the email
            message : message to be send
            dests : list receivers email ids
        Returns:
            int : number of successfully sent emails
        """
        nums = 0
        for dest in dests:
            if self.sendMail(subject, message, dest):
                nums+=1
        return nums

    def __del__(self):
        # Ensure the sender object exists before trying to quit
        if hasattr(self, 'sender') and self.sender:
            self.sender.quit()


if __name__=='__main__':
    sender = MailSender()
    # Example usage with subject
    msg = """dear segomarani,\n\nHere's an update on some of the major conflicts currently happening around the world:\n\n1.  **Russia-Ukraine War:** This conflict, which began in February 2022, continues to be a major point of tension in Eastern Europe.\n\n2.  **Israel-Gaza Conflict:** The situation in Gaza remains highly volatile following a Hamas-led attack in October 2023, with significant humanitarian concerns.\n\n3.  **Sudanese Civil War:** A brutal power struggle erupted in April 2023 between the Sudanese Armed Forces (SAF) and the paramilitary Rapid Support Forces (RSF), leading to a massive displacement crisis.\n\n4.  **Myanmar Civil War:** Since the 2021 military coup, Myanmar has been embroiled in a violent conflict between ethnic armed groups, pro-democracy forces, and the junta.\n\n5.  **Yemeni Civil War:** What began in 2014 as a power struggle has evolved into a regional proxy war, causing immense human suffering.\n\n6.  **Sahel Insurgency:** Parts of West Africa, including Mali, Burkina Faso, and Niger, are experiencing chaotic situations with various militant groups, leading to displacement and instability.\n\n7.  **Ethiopian Civil Conflict:** Despite a peace deal in the Tigray region, tensions and sporadic fighting persist in other parts of Ethiopia.\n\n8.  **Haiti Gang Violence:** Haiti is facing severe challenges due to unchecked gang rule, leading to widespread violence and a breakdown of law and order.\n\nPlease note that this is not an exhaustive list, and the situations are constantly evolving.\n\nSincerely,\nYour AI Assistant"""
    sender.sendMail(subject="Manusher Aukat", message=msg, dest="sabarna.saha1308@gmail.com")
    # Example usage for batch sending
    # sender.sendMailBatch(subject="Batch Test", message="Hello to all!", dests=["recipient1@example.com", "recipient2@example.com"])
    del sender