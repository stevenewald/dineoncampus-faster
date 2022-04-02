from twilio.rest import Client
import os
import sys
import json
import pymongo
from datetime import date
from pymongo import MongoClient
account_sid = os.environ['ACCOUNT_SID']
auth_token = os.environ['AUTH_TOKEN']
connection_string = os.environ['CONNECTION_STRING']
client = Client(account_sid, auth_token)
dbClient = MongoClient(connection_string)
users = dbClient["docf"]["users"]
all_users = users.find()
message = str(sys.argv[1])
while(True):
    try:
        record = all_users.next()
        to_number = record['phone']
        num_reqs = record['num_reqs']
        date_started = record['date_started']
        locations = record['locations']
        types = record['types']
        meals = record['meals']
        active = record['active']
        if(not active):
            continue
        message1 = client.messages.create(body=message, from_='+17579193238', to=to_number)
    except StopIteration:
        print("Finished iterating through users")
        break
