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
all_meals = ["Breakfast", "Lunch", "Dinner"]
curr_meal = all_meals[int(sys.argv[1])]
all_food = {}
def load_meals():
    path = ""
    if(curr_meal=="Breakfast"):
        path = "/home/ubuntu/menus/breakfast"
    elif(curr_meal=="Lunch"):
        path = "/home/ubuntu/menus/lunch"
    elif(curr_meal=="Dinner"):
        path = "/home/ubuntu/menus/dinner"
    f = open(path)
    return json.load(f)
all_food = load_meals()
print(all_food)
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
        if(not curr_meal in meals):
            continue
        message = "Meal options for " + curr_meal + " on " + date.today().strftime("%B %d") + ":\n\n"
        first_location = True
        for location in locations:
            if(not first_location):
                message = message + "\n\n"
            first_location = False
            if(location=="Plex"):
                location = "Plex West"
            curr_location = all_food[location]
            message = message + location + ":\n"
            first_station = True
            for station in curr_location:
                if((not "Comfort" in types) and (station=="Comfort 1" or station=="Comfort 2" or station=="Kitchen" or station=="Kitchen Entree" or station=="Kitchen Sides" or station=="Comfort")):
                    continue
                if((not "Rooted" in types) and (station=="Rooted 1" or station=="Rooted 2" or station=="Rooted" or station=="Pure Eats 1" or station=="Pure Eats 2" or station=="Pure Eats" or station=="Pure Eats Fruit")):
                    continue
                if((not "Flame" in types) and (station=="Flame 3" or station=="Flame")):
                    continue
                if((not "500 Degrees" in types) and (station=="500 Degrees 1" or station=="500 Degrees" or station=="Pizza/Flatbread")):
                    continue
                if((not "Dessert" in types) and (station=="Bakery/Dessert" or station=="Bakery & Dessert" or station=="Desserts" or station=="Bakery-Dessert")):
                    continue
                if(not first_station):
                    message = message + "\n"
                first_station = False
                message = message + station + ":\n"
                for item in curr_location[station]:
                    message = message + item + "\n"
        print(message)
        message1 = client.messages.create(body=message, from_='+17579193238', to=to_number)
    except StopIteration:
        print("Finished iterating through users")
        break
