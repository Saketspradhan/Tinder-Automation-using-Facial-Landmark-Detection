import re
from json import loads
from random import choice, random
from secrets import (entry_nodeIp, gmaps_api_key, password, user_agents_list,
                     username)
from ssl import CERT_NONE, create_default_context
from sys import exit
from time import sleep
from urllib import error, parse, request

import cv2
import numpy as np
from openpyxl import load_workbook
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

ctx = create_default_context()
ctx.check_hostname = False
ctx.verify_mode = CERT_NONE

params = dict()
params['address'] = input('Enter location from where you want to match: ')
params['key'] = gmaps_api_key
if len(params['address']) < 1: exit('!!! No address entered !!!')
target_site = entry_nodeIp + parse.urlencode(params)

exit_node = request.urlopen(target_site, context=ctx)
data = exit_node.read().decode()
print('Retrieved', len(data), '\n')

try: json_object = loads(data)
except: json_object = None
if not json_object or 'status' not in json_object or json_object['status'] != 'OK': exit('!!! Given location could not be identified, please try using more relevent keywords !!!')
    
latitude = json_object['results'][0]['geometry']['location']['lat']
longitude = json_object['results'][0]['geometry']['location']['lng']
print('Latitude:', latitude, '\nLongitude:', longitude)
print(json_object['results'][0]['formatted_address'])

# location_found = False
# while location_found != True:
#     city_name = input('Enter city from where you want to match girls: ').strip()
#     workbook = load_workbook(filename=r'ENTER PATH TO worldcities.xlsx')
#     sheet = workbook.active
    
#     for i, value in enumerate(sheet['B']):
#         if value.value == city_name:
#             location_found = True
#             latitude = sheet['C' + str(i+1)].value
#             longitude = sheet['D' + str(i+1)].value
#             print('Location found:\n' + sheet['B' + str(i+1)].value + ', ' + sheet['H' + str(i+1)].value + ', ' + sheet['E' + str(i+1)].value)
#             print(f'\nLatitude = {latitude}\nLongitude = {longitude}\n')
#             break
    
#     if location_found == False and city_name.isascii() == False: print('Please enter city name in English only.\n')
#     elif (location_found == False): print(r'City not found :(\nPlease try another location.\n')

random_agent = choice(user_agents_list)
sleep(2)

chrome_options = webdriver.ChromeOptions()
# chrome_options.add_argument(r'--incognito')
# chrome_options.add_argument(r'start-maximized')
chrome_options.add_argument(r'--ignore-certificate-errors')
chrome_options.add_argument(r'--ignore-ssl-errors')
chrome_options.add_argument(r"--test-type")
chrome_options.add_argument(f'user-agent={random_agent}')
chrome_options.add_argument(r'window-size=1200x600')
chrome_options.add_experimental_option(r"excludeSwitches", ["enable-automation"])
chrome_options.add_experimental_option(r'useAutomationExtension', False)

PATH = r"ENTER PATH TO chromedriver.exe"
face_cascade = cv2.CascadeClassifier(r'ENTER PATH TO haarcascade_frontalface_default.xml')
driver = webdriver.Chrome(options=chrome_options, executable_path=PATH)


def geoLocationTest():
    Map_coordinates = dict({
        "latitude": latitude, 
        "longitude": longitude,
        "accuracy": 100
        }) 
    driver.execute_cdp_cmd("Emulation.setGeolocationOverride", Map_coordinates)
    driver.get(url = r"https://tinder.com/")


def tinderLogin():
    sleep(3)
    try:
        i_accept = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, r'//*[@id="content"]/div/div[2]/div/div/div[1]/button'))
        )
        i_accept.click()
    except: pass
    sleep(3)

    try:
        log_in = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, r'//*[@id="content"]/div/div[1]/div/main/div[1]/div/div/div/div/header/div/div[2]/div[2]/button'))
        )
        log_in.click()
    except: driver.quit()
    sleep(6)

    search_for_more_options = driver.find_element_by_xpath(r'//*[@id="modal-manager"]/div/div/div[1]/div/div[3]').text
    if(search_for_more_options.find("MORE OPTIONS") == -1): pass
    else:
        more_options = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, r'//*[@id="modal-manager"]/div/div/div[1]/div/div[3]/span/button'))
        )
        more_options.click()
    sleep(4)

    try:
        facebook_login = WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.XPATH, r'//*[@id="modal-manager"]/div/div/div[1]/div/div[3]/span/div[2]/button'))
        )
        facebook_login.click()
    except: driver.quit()
    sleep(8)


def facebookVerification(): # Switch between currently open windows
    base_window = driver.window_handles[0]
    driver.switch_to_window(driver.window_handles[1])

    email_in = driver.find_element_by_xpath(r'//*[@id="email"]')
    email_in.send_keys(username)
    sleep(3)

    pw_in = driver.find_element_by_xpath(r'//*[@id="pass"]')
    pw_in.send_keys(password)
    sleep(3)

    login_button = driver.find_element_by_xpath(r'//*[@id="u_0_0"]')
    login_button.click()
    sleep(8)

    driver.switch_to_window(base_window)


def grantPermissions():
    try:
        allow_location = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH, r'//*[@id="modal-manager"]/div/div/div/div/div[3]/button[1]'))
        )
        allow_location.click()
    except: pass
    sleep(4)

    try:
        disable_notifications = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, r'//*[@id="modal-manager"]/div/div/div/div/div[3]/button[2]'))
        )
        disable_notifications.click()
    except: pass
    sleep(10)

    try:
        likes_recieved_popup = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH, r'//*[@id="modal-manager"]/div/div/div/div[3]/button[2]'))
        )
        likes_recieved_popup.click()
    except: pass
    sleep(3)


def swipping():
    liked = disliked = super_liked, counter = 0
    while True:
        counter += 1
        try:
            sleep(2)
            expand_view = WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.XPATH, r'//*[@id="content"]/div/div[1]/div/main/div[1]/div/div/div[1]/div/div[1]/div[3]/div[3]/button'))
            )
            expand_view.click()
            sleep(1)

            her_details = driver.find_element_by_xpath(r'//*[@id="content"]/div/div[1]/div/main/div[1]/div/div/div[1]/div[1]/div/div[2]').text
            her_name = ' '.join(re.findall(r'^([A-Za-z]+.[A-Za-z]*)', her_details))
            her_age = ' '.join(re.findall(r'\n([0-9]{2})\n', her_details))
            her_info = re.findall(r'[0-9]{2}\n((.|\n)*?)(My Anthem|My Top Spotify Artists|Recent Instagram Photos|REPORT)', her_details)
            her_spotify = re.findall(r'My Anthem((.|\n)*?)(My Top Spotify Artists|Recent Instagram Photos|REPORT)', her_details)
            her_artists = re.findall(r'My Top Spotify Artists((.|\n)*?)(Back|Recent Instagram Photos|REPORT)', her_details)
            her_instagram = False if (her_details.find('Recent Instagram Photos') == -1) else True
            sleep(2)

            fetch_url = driver.find_element_by_xpath(r'//*[@id="content"]/div/div[1]/div/main/div[1]/div/div/div[1]/div[1]/div/div[1]/span/div/div[1]/span[1]/div')
            url_html = fetch_url.get_attribute('innerHTML')
            url = re.findall(r'(https:\/\/images-ssl\.gotinder\.com\/.+)&quot', url_html)[0]
            # next_photo = driver.find_element_by_xpath(r'//*[@id="content"]/div/div[1]/div/main/div[1]/div/div/div[1]/div[1]/div[1]/div[3]/div[1]/svg[1]')
            # next_photo.click()
            # previous_photo = driver.find_element_by_xpath(r'//*[@id="content"]/div/div[1]/div/main/div[1]/div/div/div[1]/div[1]/div[1]/div[3]/div[1]/svg[1]')
            # previous_photo.click()


            def url_to_image(url):
                resp = request.urlopen(url)
                image = np.asarray(bytearray(resp.read()), dtype="uint8")
                image = cv2.imdecode(image, cv2.IMREAD_COLOR)
                return image


            print("Downloading image at url %s"%(url))
            img = url_to_image(url)
            sleep(2)
            resized = cv2.resize(img, (int(img.shape[1]/1.5), int(img.shape[0]/1.5)))
            gray = cv2.cvtColor(resized, cv2.COLOR_BGR2GRAY)

            faces = face_cascade.detectMultiScale(
                    gray,
                    scaleFactor=1.1,
                    minNeighbors=5,
                    minSize=(30, 30),
                    flags=cv2.CV_FEATURE_PARAMS_HAAR
                )

            face_recognized = False
            for i, (x, y, w, h) in enumerate(faces):
                cv2.rectangle(resized, (x, y), (x+w, y+h), (255, 255, 255), 2)
                cv2.putText(resized, 'Face No.' + str(i+1), (x-10, y-10), 
                                cv2.QT_FONT_NORMAL, 0.7, (0, 0, 255), 2) 
                print(f'Person Identified: {i+1}')
                face_recognized = True

            cv2.imshow(her_name, resized)
            cv2.waitKey(1000)
            cv2.destroyAllWindows()

            close_full_view = driver.find_element_by_xpath(r'//*[@id="content"]/div/div[1]/div/main/div[1]/div/div/div[1]/div[1]/div/div[1]/span/a')
            close_full_view.click()
            sleep(1)

            with open(r'ENTER PATH TO database.txt', 'a', encoding='utf-8') as database:
                database.write(f'Name: {her_name}\n')
                if her_age != '': database.write(f'Age: {her_age}\n\n')
                database.write('Information & About:\n')
                
                her_info = her_info[0][0]
                my_list = [her_info[0]]
                proxy = her_info[1]
                for i, letter in enumerate(her_info[1:]):
                    if letter.isupper() and proxy == ' ':
                        my_list.append(letter)
                        continue
                    elif letter.isupper() or (letter.isnumeric() and proxy.islower()) or letter == '-':
                        if proxy.isupper(): 
                            my_list.append(letter)
                            continue
                        database.write(''.join(my_list) + '\n')
                        my_list = []
                    my_list.append(letter)
                    if i == len(her_info)-2: database.write(''.join(my_list) + '\n')
                    proxy = letter

                if her_spotify != []: database.write(f'Favourite Songs:{her_spotify[0][0]}\n') 
                if her_artists != []: database.write(f'Favourite Artists on Spotify: {her_artists[0][0]}\n')
                database.write(f'Instagram connected: {her_instagram}\n\n')
                database.write('********************************************************\n')
                database.close()

            rand = random()
            if rand < 0.2 and face_recognized == True: # like 
                liked += 1
                like_button = driver.find_element_by_xpath(r'//*[@id="content"]/div/div[1]/div/main/div[1]/div/div/div[1]/div[1]/div[2]/div[4]/button')
                like_button.click()
                print(f'Card number: {counter}, {liked} liked')
            elif rand == 0.100 and face_recognized == True: # super-like 
                super_liked += 1
                super_like_button = driver.find_element_by_xpath(r'//*[@id="content"]/div/div[1]/div/main/div[1]/div/div/div[1]/div[1]/div[2]/div[3]/div/div/div/button')
                super_like_button.click() 
                print(f'Card number: {counter}, {liked} super-liked!')
            else: # dislike
                disliked += 1
                dislike_button = driver.find_element_by_xpath(r'//*[@id="content"]/div/div[1]/div/main/div[1]/div/div/div[1]/div[1]/div[2]/div[2]/button')
                dislike_button.click()
                print(f'Card number: {counter}, {liked} disliked')            
        except Exception:
            try:
                add_tinder_to_home_screen = driver.find_element_by_xpath(r'//*[@id="modal-manager"]/div/div/div[2]/button[2]')
                add_tinder_to_home_screen.click()
            except Exception:
                try:
                    swipped_popular_profile = driver.find_element_by_xpath(r'//*[@id="modal-manager"]/div/div/button[2]')
                    swipped_popular_profile.click()
                except Exception:
                    if_matched = driver.find_element_by_xpath(r'//*[@id="modal-manager-canvas"]/div/div/div[1]/div/div[3]/div[3]/form').text
                    if if_matched == 'Say something nice!':
                        exit_matched = driver.find_element_by_xpath(r'//*[@id="modal-manager-canvas"]/div/div/div[1]/div/div[4]/button')
                        exit_matched.click()
                        sleep(4)
                        return_to_tinder = driver.find_element_by_xpath(r'//*[@id="content"]/div/div[1]/div/main/div[1]/div/div/div/div[1]/div/div/div[1]/a[2]/button')
                        return_to_tinder.click()
                    else: pass


geoLocationTest()
tinderLogin()
facebookVerification()
grantPermissions()
swipping()