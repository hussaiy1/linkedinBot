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
from linkedin_api import Linkedin


init(autoreset=True)

system('title' + 'LINKEDIN BOT 2.0')

if os.path.isfile('linkedin_msg_log.log'):
    os.remove('linkedin_msg_log.log')
else:
    pass

logger= logging.getLogger('linkedin_msg_log.log')
logger.setLevel(logging.DEBUG)

fh=logging.FileHandler('linkedin_msg_log.log')
formatter=logging.Formatter('%(asctime)s - %(message)s')

fh.setFormatter(formatter)
fh.setLevel(logging.DEBUG)
logger.addHandler(fh)

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

def writeSuccess():
    with open('success.txt', 'w') as f:
        for i in range(len(success)):
            f.write(success[i]+ '\n')
        f.close()

def writeFail():
    with open('fail.txt', 'w') as f:
        for i in range(len(fail)):
            f.write(fail[i]+ '\n')
        f.close()

def writePending():
    with open('pending.txt', 'w') as f:
        for i in range(len(pending)):
            f.write(pending[i]+ '\n')
        f.close()


def getName(account, link):
    api = Linkedin(account, 'Europa007')
    theURL = link.replace("\n", "")
    id = theURL.split("/")[4]
    profile = api.get_profile(id)
    lastname = profile['lastName']
    firstname = profile['firstName']
    name = "{} {}".format(firstname, lastname)
    return name

accountNumb = 0
account=userAccounts[accountNumb]
profileLinks()
logger.info('Links have been appended to the profiles list')

login=webDriver()
login.login(account,'Europa007')
logger.info('Logging In ...')
dateTimeObj = datetime.now()
print(Fore.GREEN + '[{}] Logging In... '.format(str(dateTimeObj)))
t.sleep(3)

accountCounter = 0

for i in range(len(profiles)):
    login.redirect(profiles[i])
    logger.info('Redirecting to - ' + profiles[i])
    searchConnect=login.souper(profiles[i])
    logger.info('Searching for CONNECT button - ' + profiles[i])
    dateTimeObj = datetime.now()
    print(Fore.YELLOW + '[{}] Searching for CONNECT button...... '.format(str(dateTimeObj)))
    name = getName(userAccounts[accountNumb], profiles[i])
    if searchConnect != None:
        try:
            t.sleep(4)
            login.connect2()
            logger.info('Using Connect2 function - ' + profiles[i])
            connectMsg = text['jobTitle'] + '\n' + text['greeting'] + ' ' + name + ',\n' + text['msg']
            login.message(connectMsg)
            logger.info('Message Sent - ' + profiles[i])
            dateTimeObj = datetime.now()
            print(Fore.GREEN + '[{}] Message Sent to {}'.format(str(dateTimeObj), name))
            success.append(profiles[i])
            accountCounter += 1

        except NoSuchElementException:
            dateTimeObj = datetime.now()
            print(Fore.YELLOW + '[{}] Maybe Connection Request Already Sent -'.format(str(dateTimeObj)))
            logger.info('Failed to CONNECT2 - ' + profiles[i])
            pending.append(profiles[i])

        except ElementNotInteractableException:
            logger.info('Failed to CONNECT1 - element not interactable - ' + profiles[i])
            dateTimeObj = datetime.now()
            print(Fore.RED + '[{}] Failed to Connect - element not interactable -'.format(str(dateTimeObj)))
            fail.append(profiles[i])

    else:
        try:
            t.sleep(4)
            login.connect1()
            logger.info('Using Connect1 function - ' + profiles[i])
            connectMsg = text['jobTitle'] + '\n' + text['greeting'] + ' ' + name + ',\n' + text['msg']
            login.message(connectMsg)
            logger.info('Message Sent - ' + profiles[i])
            dateTimeObj = datetime.now()
            print(Fore.GREEN + '[{}] Message Sent to {}'.format(str(dateTimeObj), name))
            success.append(profiles[i])
            accountCounter += 1
        except NoSuchElementException:
            dateTimeObj = datetime.now()
            print(Fore.YELLOW + '[{}] Maybe Connection Request Already Sent - '.format(str(dateTimeObj)))
            logger.info('Failed to CONNECT1 - ' + profiles[i])
            pending.append(profiles[i])
        except ElementNotInteractableException:
            dateTimeObj = datetime.now()
            print(Fore.RED + '[{}] Failed to Connect - element not interactable - '.format(str(dateTimeObj)))
            logger.info('Failed to CONNECT1 - element not interactable - ' + profiles[i])
            fail.append(profiles[i])
    print(Fore.GREEN + '[{}] Moving to next account, no. of account messaged so far: {} '.format(str(dateTimeObj), accountCounter))
    if accountCounter%100==0:
        accountNumb += 1
        if accountNumb == (len(userAccounts)):
            accountNumb = 0
        account=userAccounts[accountNumb]
        dateTimeObj = datetime.now()
        print(Fore.GREEN + '[{}] Changing Accounts using {} '.format(str(dateTimeObj), userAccounts[accountNumb]))
        login.relogin(userAccounts[accountNumb],'Europa007')
        logger.info('Logging In ...')
        print(Fore.GREEN + '[{}] Logged In To {} '.format(str(dateTimeObj), userAccounts[accountNumb]))
        t.sleep(2)
    else:
        pass

	

writeSuccess()
writeFail()
writePending()

dateTimeObj = datetime.now()
print(Fore.GREEN + '[{}] Process Complete '.format(str(dateTimeObj)))
#selenium.common.exceptions.ElementNotInteractableException: Message: element not interactable
#time.sleep(3)
#login.connect2()
#time.sleep(3)


#login.message(text)

