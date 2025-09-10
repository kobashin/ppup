# filename : pepup.py
# summary : open pepup webpage and add dairy info

# how to use the webdriver
# https://learn.microsoft.com/ja-jp/microsoft-edge/webdriver-chromium/?tabs=python

# download site of the webdriver
# https://developer.microsoft.com/ja-jp/microsoft-edge/tools/webdriver/?form=MA13LH

# trouble shooting
# https://qiita.com/Sho1981/items/fc07d83b33d11a54bfcd

import selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.service import Service
import time
from datetime import datetime
import re

# from funcs import *
import funcs
import config

# Begin : Microsoft Edge session.
'''
If you see the message below when running this program, replace the webdriver.

'This version of Microsoft Edge WebDriver only supports Microsoft Edge version xxx'

Open the link above and download zip.
Unzip it and put the driver on the same folder as this program.
'''

# if a version of the driver matches that of browser, get a web driver
# start try block

try:
    service = Service('msedgedriver.exe')
    driver = webdriver.Edge(service=service)

# catch the exception
except selenium.common.exceptions.SessionNotCreatedException as e:
    # print the message
    print(e.msg)
    # find the correct version of the driver from the message
    exceptionMessage = e.msg
    # extract the version number from the message
    version = re.findall(r'\d+\.\d+\.\d+\.\d+', exceptionMessage)
    # print(version)
    exit()

# catch other exceptions
except Exception as OtherException:
    # print the message
    print('An error occurred. Please check the error message below.')
    # print the class of the exception
    print('Exception class : ', type(OtherException))
    print('Exception message : ', OtherException)
    # end the program
    exit()


# get the target webpage
driver.get('https://pepup.life/users/sign_in')

time.sleep(1)

# fill email and password
email_address, password_value = config.get_login_credentials()
email = driver.find_element(By.NAME, 'user[email]')
email.send_keys(email_address)
password = driver.find_element(By.NAME, 'user[password]')
password.send_keys(password_value)

# click to commit.
# loginButton = driver.find_element(By.NAME, 'commit')
# loginButton.click()

# wait until reCAPTCHA is solved manually.
print('Please solve reCAPTCHA manually within 30 seconds.')
time.sleep(30)

# get current year and month dynamically
tgtYear = datetime.now().year
tgtMonth = datetime.now().month - 1

# get the last day of the month
startDay = 1
endDay = funcs.getLastDay(tgtYear, tgtMonth)

# loop for each day in the month to fill the forms.
for day in range(startDay, endDay + 1):
    # fill the forms in mileage campaign pages.
    today = '{}/{}/{}'.format(tgtYear, tgtMonth, day)
    isWeekend = (funcs.getWeekday(tgtYear, tgtMonth, day) > 4)
    driver.get('https://pepup.life/scsk_mileage_campaigns/' + today)
    time.sleep(1)
    inputs = driver.find_elements(By.TAG_NAME, 'input')

    # if inputs are not found, terminate the program.
    if len(inputs) == 0:
        print('No inputs found.')
        break

    # fill elements
    for i in range(len(inputs)):
        tmpInput = inputs[i]

        # walking
        if i == 0:
            tmpInput.clear()

            # num of walks
            if isWeekend:
                walks = 15000
            else:
                walks = 8000
            # add random number to the walks
            walks += funcs.getRandomInt(0, 1000)
            tmpInput.send_keys(walks)

        # sleep
        elif i == 1:
            tmpInput.clear()
            if isWeekend:
                tmpInput.send_keys(8)
            else:
                tmpInput.send_keys(6)
        # other items
        else:
            if not tmpInput.is_selected():
                tmpInput.click()

        time.sleep(0.2)

    # push button
    buttons = driver.find_elements(By.TAG_NAME, 'button')
    time.sleep(1)
    # the correct index of button[] could be changed.
    inputButton = buttons[3]
    # inputButton.submit()
    inputButton.click()
    time.sleep(1)

# End session.
print('Quit driver.')
driver.quit()
