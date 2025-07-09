# Send SMS via Twilio or similar

# tasks/sms.py

from twilio.rest import Client

def send_sms(account_sid, auth_token, twilio_number, target_number, message):
    try:
        client = Client(account_sid, auth_token)
        message = client.messages.create(
            body=message,
            from_=twilio_number,
            to=target_number
        )
        return f"SMS sent successfully. SID: {message.sid}"
    except Exception as e:
        return f"Failed to send SMS: {e}"
