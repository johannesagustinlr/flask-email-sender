import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from dotenv import load_dotenv
import os

load_dotenv()


def send_email(receiver: str, subject: str, content: str) -> None:
    server = os.getenv("SMTP_ENDPOINT")
    port = int(os.getenv("SMTP_PORT"))
    sender_email = os.getenv("SMTP_USERNAME")
    receiver_email = receiver
    password = os.getenv("SMTP_PASSWORD")
    # Create the MIME message
    msg = MIMEMultipart()
    msg["From"] = sender_email
    msg["To"] = receiver_email
    msg["Subject"] = subject

    body = content

    msg.attach(MIMEText(body, "plain"))

    try:
        server = smtplib.SMTP(server, port)
        server.starttls()
        server.login(sender_email, password)

        text = msg.as_string()
        server.sendmail(sender_email, receiver_email, text)
        print("Email sent successfully!")
    except Exception as e:
        print(f"Failed to send email: {e}")
    finally:
        server.quit()
