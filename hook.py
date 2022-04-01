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
    first = False
    if(user==None):
        first = True
        users.insert_one({"phone":from_number, "num_reqs":0, "date_started":str(date.today()),"locations":["Allison", "Sargent", "Elder","Plex"],"types":["Comfort","Rooted","Flame","Dessert"],"meals":["Breakfast","Lunch","Dinner"]})
    else:
        first = False
        user["num_reqs"]=user["num_reqs"]+1
        users.replace_one({"phone":from_number},user, False)

    resp = MessagingResponse()
    if(first):
        resp.message("Welcome to the Northwestern menu texting service!\nYou're now receiving menus for all locations, stations, and times\nType HELP to change settings or STOP to cancel")
        return str(resp)
    else:
        existing_user_response(from_number, user, resp, body)
    return str(resp)
def existing_user_response(from_number, user, resp, body):
    if(body=="Allison" or body=="Sargent" or body=="Plex" or body=="Elder"):
        if(body in user["locations"]):
            user["locations"].remove(body)
            users.replace_one({"phone":from_number},user,False)
            resp.message("Removed " + body + " from your locations")
        else:
            user["locations"].insert(0, body)
            users.replace_one({"phone":from_number},user,False)
            resp.message("Added " + body + " to your locations")
    elif(body=="Comfort" or body=="Rooted" or body=="Flame" or body=="Dessert"):
        if(body in user["types"]):
            user["types"].remove(body)
            users.replace_one({"phone":from_number},user,False)
            resp.message("Removed " + body + " from your stations")
        else:
            user["types"].insert(0, body)
            users.replace_one({"phone":from_number},user,False)
            resp.message("Added " + body + " to your stations")
    elif(body=="Breakfast" or body=="Lunch" or body=="Dinner"):
        if(body in user["meals"]):
            user["meals"].remove(body)
            users.replace_one({"phone":from_number},user,False)
            resp.message("Removed " + body + " from your meals")
        else:
            user["meals"].insert(0, body)
            users.replace_one({"phone":from_number},user,False)
            resp.message("Added " + body + " to your meals")
    else:
        resp.message("Unrecognized command. Type HELP for options")
if __name__ == "__main__":
    app.run(debug=True)
