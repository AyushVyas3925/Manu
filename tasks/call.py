

from twilio.rest import Client

def make_call(account_sid, auth_token, twilio_number, target_number, message_url):
    try:
        client = Client(account_sid, auth_token)

        call = client.calls.create(
            to=target_number,
            from_=twilio_number,
            url=message_url  # Must be a public URL hosting TwiML instructions
        )

        return f"Call initiated successfully. SID: {call.sid}"
    except Exception as e:
        return f"Failed to make call: {e}"
