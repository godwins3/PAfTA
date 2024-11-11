import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from .templates import send_verification
from config import config


def send_verification_email(email, code):
    # Get Gmail configuration
    gmail_creds = config.gmail_config()
    sender = gmail_creds['sender']
    password = gmail_creds['password']

    recipient = email

    # The subject line for the email.
    subject = "Exodus Verification"

    # The email body for recipients with non-HTML email clients.
    body_text = f"Welcome to Exodus, your verification code is {code}"

    # The HTML body of the email.
    body_html = send_verification.html(code)

    # Create the email message
    message = MIMEMultipart('alternative')
    message['Subject'] = subject
    message['From'] = sender
    message['To'] = recipient

    # Attach both plain-text and HTML versions
    message.attach(MIMEText(body_text, 'plain'))
    message.attach(MIMEText(body_html, 'html'))

    # Try to send the email
    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.login(sender, password)
            server.sendmail(sender, recipient, message.as_string())
        
        return {'Message': 'Email has been sent, use the code in the email as verification', "statusCode": 200}
    except Exception as e:
        print(f"Error sending email: {str(e)}")
        return {'Message': 'Email not sent, kindly contact support.', "statusCode": 500}


def send_password_reset_email(email, reset_token):
    # Get Gmail configuration
    gmail_creds = config.gmail_config()
    sender = gmail_creds['sender']
    password = gmail_creds['password']

    recipient = email

    # The subject line for the email.
    subject = "Exodus Password Reset"

    # The email body for recipients with non-HTML email clients.
    body_text = f"Use the following link to reset your password: http://yourdomain.com/reset-password?token={reset_token}"

    # The HTML body of the email.
    body_html = f"""
    <html>
    <body>
    <h2>Exodus Password Reset</h2>
    <p>Click the following link to reset your password:</p>
    <a href="http://yourdomain.com/reset-password?token={reset_token}">Reset Password</a>
    </body>
    </html>
    """

    # Create the email message
    message = MIMEMultipart('alternative')
    message['Subject'] = subject
    message['From'] = sender
    message['To'] = recipient

    # Attach both plain-text and HTML versions
    message.attach(MIMEText(body_text, 'plain'))
    message.attach(MIMEText(body_html, 'html'))

    # Try to send the email
    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.login(sender, password)
            server.sendmail(sender, recipient, message.as_string())
        
        return {'Message': 'Password reset email has been sent', "statusCode": 200}
    except Exception as e:
        print(f"Error sending email: {str(e)}")
        return {'Message': 'Email not sent, kindly contact support.', "statusCode": 500}
