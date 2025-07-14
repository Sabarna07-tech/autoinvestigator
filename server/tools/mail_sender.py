import smtplib
from dotenv import load_dotenv
import os
from email.message import EmailMessage

# Load environment variables from a .env file
load_dotenv()

class MailSender:
    """
    This class is a utility class that sends mail to the receivers using smtplib.

    Functions:
    - sendMail(subject:str, message:str, dest:str) -> sends mail to a destination mail.
    - sendMailBatch(subject:str, message:str, dests:list) -> sends mail to multiple receivers.
    """
    def __init__(self):
        """
        Initializes the SMTP connection.
        """
        try:
            # Fetch credentials from environment variables
            self.__sender_mail = os.getenv("SENDER_MAIL")
            self.__pass = os.getenv("MAIL_PASS")

            # Validate that credentials are set
            if not self.__sender_mail or not self.__pass:
                raise ValueError("SENDER_MAIL and MAIL_PASS must be set in the .env file")

            # Establish a connection to the SMTP server
            self.sender = smtplib.SMTP('smtp.gmail.com', 587)
            self.sender.starttls()
            self.sender.login(self.__sender_mail, self.__pass)
        except Exception as e:
            print(f"Error occurred during MailSender initialization: {e}")
            raise

    def sendMail(self, subject: str, message: str, dest: str) -> bool:
        """
        Sends a message to a particular receiver with a subject.

        Args:
            subject (str): The subject of the email.
            message (str): The message to be sent.
            dest (str): The receiver's email id.

        Returns:
            bool: True on success, False on failure.
        """
        try:
            msg = EmailMessage()
            msg['Subject'] = subject
            msg['From'] = self.__sender_mail
            msg['To'] = dest
            msg.set_content(message)  # Set the plain text content

            self.sender.send_message(msg)
            return True
        except Exception as e:
            print(f"Something went wrong while sending mail to {dest}: {e}")
            # Corrected: removed raise e to prevent crash and allow return
            return False

    def sendMailBatch(self, subject: str, message: str, dests: list) -> int:
        """
        Sends mail to a list of receivers with a subject.

        Args:
            subject (str): The subject of the email.
            message (str): The message to be sent.
            dests (list): A list of receiver email ids.

        Returns:
            int: The number of successfully sent emails.
        """
        success_count = 0
        for dest in dests:
            if self.sendMail(subject, message, dest):
                success_count += 1
        return success_count

    def __del__(self):
        """
        Destructor to close the SMTP connection gracefully.
        """
        if hasattr(self, 'sender') and self.sender:
            try:
                self.sender.quit()
            except Exception as e:
                print(f"Error occurred while quitting SMTP connection: {e}")

# --- Integration Helper Function ---

# Instantiate the sender once to be used by the application
mailer = MailSender()

def send_verification_email(email: str, verification_code: str):
    """
    Sends a verification email to the user with the provided verification code.
    This function uses the MailSender class to dispatch the email.
    """
    subject = "Your Verification Code"
    body = f"Thank you for registering. Your verification code is: {verification_code}"
    mailer.sendMail(subject, body, email)


# Example of how the class would be used for testing purposes
if __name__ == '__main__':
    print("Running MailSender test...")
    # Ensure you have a .env file with SENDER_MAIL and MAIL_PASS for this to work
    try:
        test_mailer = MailSender()
        subject = "Test Email from AutoInvestigator"
        msg = "This is a test email to confirm the MailSender class is working."
        # Replace with a real email address for testing
        test_recipient = "example@gmail.com"
        
        print(f"Sending test email to {test_recipient}...")
        if test_mailer.sendMail(subject=subject, message=msg, dest=test_recipient):
            print("Test email sent successfully!")
        else:
            print("Failed to send test email.")
            
        del test_mailer # Clean up the connection
        
    except Exception as e:
        print(f"An error occurred during the test: {e}")