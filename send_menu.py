from twilio.rest import Client
import os
import sys
import pymongo
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
    curr_line = " "
    while(curr_line!=""):
        curr_line = f.readline()
        if(curr_line=="Location begin\n"):
            print("begin")
            curr_line = f.readline()
            curr_line = curr_line[0:len(curr_line)-2]
            read_location(curr_line, f)
def read_location(location, f):
    all_food[location] = {}
    curr_station = ""
    curr_line = " "
    while(curr_line!="Location End\n"):
        curr_line = f.readline()
        #print(curr_line)
        if(curr_line=="Station Begin\n"):
            curr_line = f.readline()
            curr_station = curr_line[0:len(curr_line)-2]
            all_food[location][curr_station] = []
            while(curr_line!="Station End\n"):
                curr_line = f.readline()
                if(curr_line=="Station End\n"):
                    continue
                all_food[location][curr_station].insert(0, curr_line[0:len(curr_line)-1])
while(True):
    try:
        record = all_users.next()
        to_number = record['phone']
        num_reqs = record['num_reqs']
        date_started = record['date_started']
        locations = record['locations']
        types = record['types']
        meals = record['meals']
        if(not curr_meal in meals):
            continue
        print(to_number)
        load_meals()
        print(str(all_food))
    except StopIteration:
        print("Finished iterating through people")
        break
