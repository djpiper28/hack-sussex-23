from twilio.rest import Client

account_sid = "AC9167ba5c96b89ef9dd55b819587187b2"
auth_token = "ebbf449085659d3e39e217cf6c0d8a07"
client = Client(account_sid, auth_token)

message = client.messages.create(
    from_="whatsapp:+14155238886", to="whatsapp:+447519840821", body="test123"
)

print(message.sid)
