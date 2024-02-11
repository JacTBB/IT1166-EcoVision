import smtplib
from dotenv import load_dotenv
import os

load_dotenv()

# Sender and recipient details
sender_email = "ecovision@jactbb.com"
sender_password = os.getenv("email_password")
recipient_email = "admin_ecovision@jactbb.com"

# Message content
subject = "Test Email from Python"
body = "This is a test email sent from Python using smtplib."

# Message header
message = f"From: {sender_email}\nTo: {recipient_email}\nSubject: {subject}\n\n{body}"

# Connect to SMTP server
with smtplib.SMTP("wednesday.mxrouting.net", 587) as server:
    server.starttls()
    
    server.login(sender_email, sender_password)

    server.sendmail(sender_email, recipient_email, message)

print("Email sent successfully!")