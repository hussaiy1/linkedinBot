from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import ElementNotInteractableException
import time as t
from lnkdn_driver import *
import logging
import os
from os import system
import json
from datetime import datetime
from colorama import init, Fore, Back, Style


init(autoreset=True)


profiles=[]
success=[]
fail=[]
pending=[]
text=[]

userAccounts=['Richard.abbott@europa-it-search.com','alidaanyalnaik@hotmail.co.uk', 'roy-khan@hotmail.com', 'aqeel_365@hotmail.com']

with open('message.json', 'r') as jsonf:
    text=json.load(jsonf)

def profileLinks():
    with open('profiles.txt', 'r') as f:
        for line in f:
            profiles.append(line)
        f.close



accountNumb = 0
account=userAccounts[accountNumb]
profileLinks()
logger.info('Links have been appended to the profiles list')

login=webDriver()
login.login(account,'Europa007')
dateTimeObj = datetime.now()
print(Fore.GREEN + '[{}] Logging In... '.format(str(dateTimeObj)))
t.sleep(3)


for i in range(len(profiles)):
    login.redirect(profiles[i])
    logger.info('Redirecting to - ' + profiles[i])
    searchConnect=login.souper(profiles[i])
    logger.info('Searching for CONNECT button - ' + profiles[i])
    dateTimeObj = datetime.now()
    print(Fore.YELLOW + '[{}] Searching for CONNECT button...... '.format(str(dateTimeObj)))
    