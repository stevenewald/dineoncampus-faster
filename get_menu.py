from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import sys
import time
import os
import warnings
from twilio.rest import Client

# This is not written with good programming practice. This is just written for me to get texts about what items they are pretending to have today.

account_sid = os.environ['ACCOUNT_SID']
auth_token = os.environ['AUTH_TOKEN']
client = Client(account_sid, auth_token)
warnings.filterwarnings("ignore", category=DeprecationWarning)
ffo = webdriver.FirefoxOptions()
ffo.headless = True
ff = webdriver.Firefox(options=ffo, executable_path=r'/home/ubuntu/dineoncampus-faster/geckodriver')
ff.get("https://dineoncampus.com/northwestern")
time.sleep(5)
location_dropdown = ff.find_element_by_id("locations__BV_toggle_")
time_dropdown = ff.find_element_by_id("periods__BV_toggle_")
station_dropdown = ff.find_element_by_id("categories__BV_toggle_")

allison_breakfast = ["Comfort 1", "Comfort 2", "Bakery-Dessert"]
allison_lunch = ["Flame 3", "Bakery-Dessert"]
allison_dinner = ["Flame 3", "Bakery-Dessert"]

sargent_breakfast = ["Kitchen", "Desserts"]
sargent_lunch = ["Flame", "Desserts"]
sargent_dinner = ["Flame", "Desserts"]

elder_breakfast = ["Kitchen Entree", "Kitchen Sides", "Bakery & Dessert"]
elder_lunch = ["Flame", "Bakery & Dessert"]
elder_dinner = ["Flame", "Bakery & Dessert"]

plex_breakfast = ["Breakfast"]
plex_lunch = ["Flame", "Bakery/Dessert"]
plex_dinner = ["Flame", "Bakery/Dessert"]

# Yes, using time.sleep is a bad way of waiting until items are loaded. But dineoncampus provides 0(0) way of knowing whether it's loading or loaded. I'm sure there's some way to
# Check whether it's done loading, but unfortunately this is run on a $.002/hr aws ec2 instance and I simply do not care enough.

locations = [["Allison", [allison_breakfast, allison_lunch, allison_dinner]], ["Sargent", [sargent_breakfast, sargent_lunch, sargent_dinner]], ["Elder", [elder_breakfast, elder_lunch, elder_dinner]], ["Plex West", [plex_breakfast, plex_lunch, plex_dinner]]]
meals = ["Breakfast", "Lunch", "Dinner"]
meal = meals[int(sys.argv[1])]
final_text = "Meal options for " + meal + ":\n"
for location in locations:
    location_dropdown.click()
    location_item = ff.find_elements_by_xpath("//a[contains(text(),'" + location[0] + "')]")[0]
    location_item.click()
    final_text+=location[0]+":\n"
    time.sleep(3)
    time_dropdown.click()
    time.sleep(.5)
    meal_item = ff.find_elements_by_xpath("//a[contains(text(),'" + meal + "')]")[0]
    meal_item.click()
    time.sleep(5)
    stations = location[1]
    if(meal=="Breakfast"):
        stations = stations[0]
    elif(meal=="Lunch"):
        stations = stations[1]
    elif(meal=="Dinner"):
        stations = stations[2]
    else:
        raise ValueError("Incorrect meal") #shouldn't trigger
    for station in stations:
        station_dropdown.click()
        station_objs = ff.find_elements_by_xpath("//a[contains(text(),'" + station + "')]")
        if(station=="Breakfast" and location=="Plex West"):
            station_objs = [station_objs[1]]
        clicked = False
        try:
            station_objs[0].click()
            clicked = True
            all_items = ff.find_elements_by_class_name("menu-tile-item")
            for item in all_items:
                food = item.text
                food = food[0:food.index("\n")]
                if(meal=="Breakfast" and (food.find("Pancakes")==-1 and food.find("Bacon")==-1)):
                    continue
                final_text+=food+"\n"
        except:
            print("error")
        if(not clicked):
            station_dropdown.click()
        final_text+="\n"
    final_text+="\n\n\n"
    time.sleep(1)
print(final_text)
message = client.messages \
    .create(
         body=final_text,
         from_='+17579193238',
         to='+17818004140'
     )
    
#ff.save_screenshot(r'C:/Users/steve/Desktop/menu/1.png')
#pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract'
#print(pytesseract.image_to_string(r'C:\Users\steve\Desktop\menu\1.png'))
ff.close()
