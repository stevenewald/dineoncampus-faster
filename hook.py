from flask import Flask, request, redirect
from twilio.twiml.messaging_response import MessagingResponse
import os
from twilio.rest import Client
account_sid = os.environ['ACCOUNT_SID']
auth_token = os.environ['AUTH_TOKEN']
client = Client(account_sid, auth_token)
app = Flask(__name__)
@app.route("/sms", methods=['GET', 'POST'])
def sms_reply():
    """Respond to incoming calls with a simple text message."""
    # Start our TwiML response
    resp = MessagingResponse()
    # Add a message
    resp.message("Test SMS response")
    #from_number = request.form['From']
    #to_number = request.form['To']
    #message = client.messages.create(body="Test_response", from_='+17579193238', to='+17818004140')
    return str(resp)
if __name__ == "__main__":
    app.run(debug=True)
