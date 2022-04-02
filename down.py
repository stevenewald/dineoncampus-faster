from flask import Flask, request, redirect
from twilio.twiml.messaging_response import MessagingResponse
import os
from twilio.rest import Client
from pymongo import MongoClient
import pymongo
from datetime import date
account_sid = os.environ['ACCOUNT_SID']
auth_token = os.environ['AUTH_TOKEN']
connection_string = os.environ['CONNECTION_STRING']
client = Client(account_sid, auth_token)
dbClient = MongoClient(connection_string)
users = dbClient["docf"]["users"]

app = Flask(__name__)
@app.route("/sms", methods=['GET', 'POST'])
def sms_reply():
    body = request.values.get('Body', None)
    from_number = request.form['From']
    user = users.find_one({"phone":from_number})
    resp = MessagingResponse()
    resp.message("The NU menu messaging service is currently down for maintenance.\n\nPlease try again later or contact Steve at steveewald2025@u.northwestern.edu for details if you're curious or want to help. Thanks!")
    return str(resp)
if __name__ == "__main__":
    app.run(debug=True)
