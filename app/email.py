import os
from datetime import datetime
from dotenv import load_dotenv
import smtplib
from email.message import EmailMessage

load_dotenv()

# Sender and recipient details
sender_email = "ecovision@jactbb.com"
sender_password = os.getenv("email_password")



def email_transaction(receipient, username, price, description):
    subject = "Ecovision - Transaction"
    body = """
<!DOCTYPE html>
<html>
<head>
    <style>
        body {{
            background-color: rgb(220, 230, 220);
            font-family: "Lucida Sans Unicode", "Lucida Grande", sans-serif;
        }}

        #header {{
            margin-top: 50px;
            margin-left: auto;
            margin-right: auto;
            width: max-content;
        }}
        #header h1 {{
            display: flex;
            margin: 0;
        }}
        #header img {{
            width: 50px;
            height: 50px;
        }}
        #header span {{
            padding: 4px;
            font-size: 30px;
            font-weight: bold;
        }}

        #content {{
            margin: 50px;
            margin-top: 20px;
            padding: 50px;
            background-color: rgb(232, 238, 232);
            border-radius: 10px;
        }}
        #content h2 {{
            margin-top: 0;
        }}
        #content table td {{
            padding-right: 30px;
        }}
        #content a {{
            color: rgb(80,80,180);
            text-decoration: none;
        }}
    </style>
</head>
<body>
    <div id="header">
        <h1>
            <img src="https://i.ibb.co/NjCMcCr/icon-nobackground.png">
            <span>EcoVision</span>
        </h1>
    </div>

    <div id="content">
        <h2>
            Dear {username},
        </h2>
    
        <h3>
            You have made a payment on EcoVision:
        </h3>
        <table>
            <tr>
                <td>Description</td>
                <td>{description}</td>
            </tr>
            <tr>
                <td>Date</td>
                <td>{date}</td>
            </tr>
            <tr>
                <td>Amount</td>
                <td>${price}</td>
            </tr>
        </table>

        <br>
    
        <p>
            If you have any questions, contact us on the <a href="https://ecovision.jactbb.com">EcoVision</a> platform.
        </p>
    
        <p>
            Your sincerely,<br>
            Financial Department<br>
            EcoVision
        </p>
    </div>
</body>
</html>
"""
    body = body.format(username=username, description=description, date=datetime.now().strftime("%Y-%m-%d %H:%M:%S"), price=price)
    
    
    
    message = EmailMessage()
    message['From'] = sender_email
    message['To'] = receipient
    message['Subject'] = subject
    message.add_alternative(body, subtype='html')
    
    
    
    with smtplib.SMTP("wednesday.mxrouting.net", 587) as server:
        server.starttls()
        
        server.login(sender_email, sender_password)

        server.send_message(message)
        
        print(f"Email to {receipient} sent successfully!")



def email_upgrade_account(receipient, username, price, description):
    email_transaction(receipient, username, price, description)
    
    subject = "Ecovision - Account Upgrade"
    body = """
<!DOCTYPE html>
<html>
<head>
    <style>
        body {{
            background-color: rgb(220, 230, 220);
            font-family: "Lucida Sans Unicode", "Lucida Grande", sans-serif;
        }}

        #header {{
            margin-top: 50px;
            margin-left: auto;
            margin-right: auto;
            width: max-content;
        }}
        #header h1 {{
            display: flex;
            margin: 0;
        }}
        #header img {{
            width: 50px;
            height: 50px;
        }}
        #header span {{
            padding: 4px;
            font-size: 30px;
            font-weight: bold;
        }}

        #content {{
            margin: 50px;
            margin-top: 20px;
            padding: 50px;
            background-color: rgb(232, 238, 232);
            border-radius: 10px;
        }}
        #content h2 {{
            margin-top: 0;
        }}
        #content table td {{
            padding-right: 30px;
        }}
        #content a {{
            color: rgb(80,80,180);
            text-decoration: none;
        }}
    </style>
</head>
<body>
    <div id="header">
        <h1>
            <img src="https://i.ibb.co/NjCMcCr/icon-nobackground.png">
            <span>EcoVision</span>
        </h1>
    </div>

    <div id="content">
        <h2>
            Dear {username},
        </h2>
    
        <h3>
            Thank you for upgrading your account to our custom plan.
        </h3>
        <p>
            We wanted to take a moment to express our gratitude for upgrading your account to our custom plan.<br>
            Your support means a lot to us, and we're excited to provide you with even better services tailored to your needs.
        </p>

        <br>
    
        <p>
            If you have any questions, contact us on the <a href="https://ecovision.jactbb.com">EcoVision</a> platform.
        </p>
    
        <p>
            Your sincerely,<br>
            Financial Department<br>
            EcoVision
        </p>
    </div>
</body>
</html>
"""
    body = body.format(username=username)
    
    
    
    message = EmailMessage()
    message['From'] = sender_email
    message['To'] = receipient
    message['Subject'] = subject
    message.add_alternative(body, subtype='html')


    
    with smtplib.SMTP("wednesday.mxrouting.net", 587) as server:
        server.starttls()
        
        server.login(sender_email, sender_password)

        server.send_message(message)
        
        print(f"Email to {receipient} sent successfully!")