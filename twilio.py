from twilio.rest import Client


# Your Account Sid and Auth Token from twilio.com/console
account_sid = 'ACca9675a67a1394aad876dfa16d1d9ea6'
auth_token = 'd239e9f0b6396e8dc50103f403e73bcb'
client = Client(account_sid, auth_token)

message = client.messages \
    .create(
         body='This is the ship that made the Kessel Run in fourteen parsecs?',
         from_='+16467603659',
         to='+919010163166'
     )

print(message.sid)
'''import twilio
import twilio.rest
# Your Account Sid and Auth Token from twilio.com/console
account_sid = 'ACca9675a67a1394aad876dfa16d1d9ea6'
auth_token = 'd239e9f0b6396e8dc50103f403e73bcb'
try:
    client = twilio.rest.TwilioRestClient(account_sid, auth_token)

    message = client.messages.create(
        body='This is the ship that made the Kessel Run in fourteen parsecs?',
        from_='+16467603659',
        to='+919010163166'
        
    )
except twilio.TwilioRestException as e:
    print (e)'''
