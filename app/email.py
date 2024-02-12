import smtplib
from dotenv import load_dotenv
import os
from datetime import datetime

load_dotenv()

# Sender and recipient details
sender_email = "ecovision@jactbb.com"
sender_password = os.getenv("email_password")



def email_transaction(receipient, username, price, description):
    subject = "Ecovision - Transaction"
    
    body = f"""
Dear {username},

The following payment transaction has been made:
Date: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
Amount: ${price}
Description: {description}

If you have any questions, contact us on the EcoVision platform.

Your sincerely,
Financial Department
EcoVision
    """
    
    message = f"From: {sender_email}\nTo: {receipient}\nSubject: {subject}\n\n{body}"
    
    with smtplib.SMTP("wednesday.mxrouting.net", 587) as server:
        server.starttls()
        
        server.login(sender_email, sender_password)

        server.sendmail(sender_email, receipient, message)
        
        print(f"Email to {receipient} sent successfully!")



def email_upgrade_account(receipient, username, price, description):
    email_transaction(receipient, username, price, description)
    
    subject = "Ecovision - Account Upgrade"
    
    body = f"""
Dear {username},

Thank you for upgrading your account to our custom plan.

If you have any questions, contact us on the EcoVision platform.

Your sincerely,
Financial Department
EcoVision
    """
    
    message = f"From: {sender_email}\nTo: {receipient}\nSubject: {subject}\n\n{body}"
    
    with smtplib.SMTP("wednesday.mxrouting.net", 587) as server:
        server.starttls()
        
        server.login(sender_email, sender_password)

        server.sendmail(sender_email, receipient, message)
        
        print(f"Email to {receipient} sent successfully!")