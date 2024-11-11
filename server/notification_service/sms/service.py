from twilio.rest import Client
from config.config import twilio_config
from twilio.base.exceptions import TwilioRestException
from .templates import send_alert

key = twilio_config.config()
account_sid = key['account_sid']
auth_token = key['auth_token']

def send_verification_sms(phone_number, code):
    try:
        client = Client(account_sid, auth_token)

        message = client.messages.create(
            body=f"Welcome to Exodus,\n your verification code is {code}",
            from_=key['phone_number'],
            to=phone_number
        )

        print(message.sid)
        return {'Message': 'SMS has been sent, use the code in the SMS as verification', "statusCode": 200}

    except TwilioRestException as err:
        print(err)
        return {'Message': 'SMS not sent', "statusCode": 500}
    
def send_alert_sms(phone_number, message):
    try:
        client = Client(account_sid, auth_token)

        message = client.messages.create(
            body=send_alert.sms(message),
            from_=key['phone_number'],
            to=phone_number
        )
        return {'Message': 'SMS has been sent', "statusCode": 200}
    
    except TwilioRestException as err:
        print(err)
        return {'Message': 'SMS not sent', "statusCode": 500}
