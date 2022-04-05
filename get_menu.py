from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import sys
import time
import json
import os
import warnings
from twilio.rest import Client

# This is not written with good programming practice. This is just written for me to get texts about what items they are pretending to have today.

warnings.filterwarnings("ignore", category=DeprecationWarning)
ffo = webdriver.FirefoxOptions()
ffo.headless = True
#todo: make directory load with $HOME
ff = webdriver.Firefox(options=ffo, executable_path=r'/home/ubuntu/dineoncampus-faster/geckodriver')
ff.get("https://dineoncampus.com/northwestern")
time.sleep(5)
location_dropdown = ff.find_element_by_id("locations__BV_toggle_")
time_dropdown = ff.find_element_by_id("periods__BV_toggle_")
station_dropdown = ff.find_element_by_id("categories__BV_toggle_")

allison_breakfast = ["Comfort 1", "Comfort 2", "Rooted 1", "Flame 3", "Bakery-Dessert"]
allison_lunch = ["Comfort 1", "Comfort 2", "Rooted 1", "Rooted 2", "Pure Eats 1", "Pure Eats 2", "Flame 3", "500 Degrees 1", "Bakery-Dessert"]
allison_dinner = ["Comfort 1", "Comfort 2", "Rooted 1", "Rooted 2", "Pure Eats 1", "Pure Eats 2", "Flame 3", "500 Degrees 1", "Bakery-Dessert"]

sargent_breakfast = ["Kitchen", "Rooted", "Desserts"]
sargent_lunch = ["Kitchen", "Pure Eats", "Pure Eats Fruit", "Rooted", "Flame", "500 Degrees", "Desserts"]
sargent_dinner = ["Kitchen", "Pure Eats", "Pure Eats Fruit", "Rooted", "Flame", "500 Degrees", "Desserts"]

elder_breakfast = ["Kitchen Entree", "Kitchen Sides", "Rooted", "Bakery & Dessert"]
elder_lunch = ["500 Degrees", "Flame", "Kitchen Entree", "Kitchen Sides", "Rooted", "Pure Eats", "Bakery & Dessert"]
elder_dinner = ["500 Degrees", "Kitchen Entree", "Kitchen Sides", "Rooted", "Pure Eats", "Flame", "Bakery & Dessert"]

plex_breakfast = ["Breakfast", "Bakery/Dessert"]
plex_lunch = ["Comfort", "Flame", "Pizza/Flatbread", "Bakery/Dessert"]
plex_dinner = ["Comfort", "Flame", "Pizza/Flatbread", "Bakery/Dessert"]

plex_east = ["Pure Eats", "Pure Eats Salad", "Pure Eats Soup", "Pure Eats Stir Fry"]

# Yes, using time.sleep is a bad way of waiting until items are loaded. But dineoncampus provides 0(0) way of knowing whether it's loading or loaded. I'm sure there's some way to
# Check whether it's done loading, but unfortunately this is run on a $.002/hr aws ec2 instance and I simply do not care enough.

locations = [["Allison", [allison_breakfast, allison_lunch, allison_dinner]], ["Sargent", [sargent_breakfast, sargent_lunch, sargent_dinner]], ["Elder", [elder_breakfast, elder_lunch, elder_dinner]], ["Plex West", [plex_breakfast, plex_lunch, plex_dinner]], ["Plex East", [plex_east, plex_east, plex_east]]]
meals = ["Breakfast", "Lunch", "Dinner"]
meal = meals[int(sys.argv[1])]
final_text = "Meal options for " + meal + ":\n"
food_options = {}
for location in locations:
    location_dropdown.click()
    location_item = ff.find_elements_by_xpath("//a[contains(text(),'" + location[0] + "')]")[0]
    location_item.click()
    final_text+="Location begin\n"
    final_text+=location[0]+":\n"
    time.sleep(5)
    time_dropdown.click()
    time.sleep(1)
    meal_items = ff.find_elements_by_xpath("//a[contains(text(),'" + meal + "')]")
    if(len(meal_items)==0):
        continue # meal not available (elder and plex on sundays for example)
    else:
        meal_items[0].click()
    time.sleep(5)
    stations = location[1]
    if(meal=="Breakfast"):
        stations = stations[0]
        if(location[0]=="Plex East"):
            continue
    elif(meal=="Lunch"):
        stations = stations[1]
    elif(meal=="Dinner"):
        stations = stations[2]
    else:
        raise ValueError("Incorrect meal") #shouldn't trigger
    food_options[location[0]] = {}
    for station in stations:
        time.sleep(1)
        food_options[location[0]][station] = []
        print(station)
        final_text = final_text + "Station Begin\n"
        final_text = final_text + station + ":\n"
        station_dropdown.click()
        station_objs = ff.find_elements_by_xpath("//a[contains(text(),'" + station + "')]")
        if(station=="Pure Eats" and location[0]=="Sargent" and (meal=="Lunch" or meal=="Dinner")):
            station_objs = [station_objs[0]]
        if(station=="Rooted" and location[0]=="Sargent" and (meal=="Lunch" or meal=="Dinner")):
            station_objs = [station_objs[0]]
        if(station=="Pure Eats" and location[0]=="Plex East"):
            station_objs = [station_objs[0]]
        clicked = False
        try:
            print(str(len(station_objs)))
            len_stations = len(station_objs)
            station_objs[len_stations-1].click()
            time.sleep(.5)
            clicked = True
            all_items = ff.find_elements_by_class_name("menu-tile-item")
            for item in all_items:
                food = item.text
                food = food[0:food.index("\n")]
                final_text+=food+"\n"
                food_options[location[0]][station].insert(0, food)
        except:
            print("error")
        if(not clicked):
            station_dropdown.click()
        final_text+="Station End\n"
    final_text+="Location End\n"
    time.sleep(2)
path = ""
if(meal=="Breakfast"):
    path = "/home/ubuntu/menus/breakfast"
elif(meal=="Lunch"):
    path = "/home/ubuntu/menus/lunch"
elif(meal=="Dinner"):
    path = "/home/ubuntu/menus/dinner"
json_obj = json.dumps(food_options)
f = open(path, 'w')
f.write(json_obj)
f.close()
#ff.save_screenshot(r'C:/Users/steve/Desktop/menu/1.png')
#pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract'
#print(pytesseract.image_to_string(r'C:\Users\steve\Desktop\menu\1.png'))
ff.close()
