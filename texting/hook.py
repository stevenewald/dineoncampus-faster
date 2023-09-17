from flask import Flask, request, redirect
from twilio.twiml.messaging_response import MessagingResponse
import os
from twilio.rest import Client
from pymongo import MongoClient
import pymongo
from profanity_check import predict, predict_prob
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
        users.insert_one({"phone":from_number, "num_reqs":0, "active":True, "date_started":str(date.today()),"locations":["Allison", "Sargent", "Elder","Plex"],"types":["Comfort","Rooted","Flame","Dessert"],"meals":["Breakfast","Lunch","Dinner"]})
    else:
        first = False
        user["num_reqs"]=user["num_reqs"]+1
        users.replace_one({"phone":from_number},user, False)

    resp = MessagingResponse()
    if(first):
        resp.message("Welcome to the Northwestern menu texting service!\nYou're now receiving menus for all locations, stations, and times\nType HELP to change settings or STOP to cancel.\nThis service was just launched, expect bugs and issues until April 14, the official launch date.\nText 781-800-4140(Steve) if you find any bugs or issues. Thanks!")
        return str(resp)
    else:
        existing_user_response(from_number, user, resp, body)
    return str(resp)
def existing_user_response(from_number, user, resp, body):
    body = body.casefold()
    if(predict([body])>.7):
        resp.message("Reported to morty")
        return str(resp)
    if(body=="allison" or body=="sargent" or body=="plex" or body=="elder"):
        if(body.capitalize() in user["locations"]):
            user["locations"].remove(body.capitalize())
            users.replace_one({"phone":from_number},user,False)
            resp.message("Removed " + body + " from your locations")
        else:
            user["locations"].insert(0, body.capitalize())
            users.replace_one({"phone":from_number},user,False)
            resp.message("Added " + body + " to your locations")
    elif(body=="comfort" or body=="rooted" or body=="flame" or body=="dessert" or body=="500 degrees"):
        if(body.capitalize() in user["types"]):
            user["types"].remove(body.capitalize())
            users.replace_one({"phone":from_number},user,False)
            resp.message("Removed " + body + " from your stations")
        else:
            user["types"].insert(0, body.capitalize())
            users.replace_one({"phone":from_number},user,False)
            resp.message("Added " + body + " to your stations")
    elif(body=="breakfast" or body=="lunch" or body=="dinner"):
        if(body.capitalize() in user["meals"]):
            user["meals"].remove(body.capitalize())
            users.replace_one({"phone":from_number},user,False)
            resp.message("Removed " + body + " from your meals")
        else:
            user["meals"].insert(0, body.capitalize())
            users.replace_one({"phone":from_number},user,False)
            resp.message("Added " + body + " to your meals")
    elif(body=="help" or body=="settings" or body=="info"):
        pass
    elif(body=="start" or body=="unstop" or body=="yes"):
        user["active"] = True
        users.replace_one({"phone":from_number},user,False)
    elif(body=="cancel" or body=="end" or body=="quit" or body=="stop" or body=="stopall" or body=="unsubscribe"):
        user["active"] = False
        users.replace_one({"phone":from_number},user,False)
    elif(body=="stations"):
        station_list = user["types"]
        station_string = "Your stations: "
        for station in station_list:
            station_string = station_string + station.casefold() + ", "
        if(len(station_list)>0):
            station_string = station_string[0:len(station_string)-2]
        resp.message(station_string)
    elif(body=="locations"):
        location_list = user["locations"]
        location_string = "Your locations: "
        for location in location_list:
            location_string = location_string + location.casefold() + ", "
        if(len(location_list)>0):
            location_string = location_string[0:len(location_string)-2]
        resp.message(location_string)
    elif(body=="meals"):
        meal_list_unsorted = user["meals"]
        meal_string = "Your meals: "
        meal_list = []
        if(meal_list_unsorted.count("Dinner")>0):
            meal_list.insert(0, "dinner")
        if(meal_list_unsorted.count("Lunch")>0):
            meal_list.insert(0, "lunch")
        if(meal_list_unsorted.count("Breakfast")>0):
            meal_list.insert(0, "breakfast")
        for meal in meal_list:
            meal_string = meal_string + meal + ", "
        if(len(meal_list)>0):
            meal_string = meal_string[0:len(meal_string)-2]
        resp.message(meal_string)
    else:
        resp.message("Unrecognized command. Type HELP for options")
if __name__ == "__main__":
    app.run(debug=True)
