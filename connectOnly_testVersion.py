from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import ElementNotInteractableException
import time as t
from lnkdn_driver import *
import logging
import os
import json
from threading import Thread
import math

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

filenames=[]

profiles=[]



success=[]
fail=[]
pending=[]
text=[]
userAccounts=['Richard.abbott@europa-it-search.com', 'alidaanyalnaik@hotmail.co.uk', 'roy-khan@hotmail.com', 'aqeel_365@hotmail.com']
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

def file_len(fname):
    with open(fname) as f:
        for i, l in enumerate(f):
            pass
    return i + 1

def connectionMsg(account, profiles):
    accountCounter = 0
    login=webDriver()
    login.login(account, 'Europa007')
    logger.info('Logging In ...')
    for k in range(len(profiles)):
        login.redirect(profiles[k])
        logger.info('Redirecting to - ' + profiles[k])
        searchConnect=login.souper(profiles[k])
        logger.info('Searching for CONNECT button - ' + profiles[k])
        if searchConnect != None:
            try:
                t.sleep(4)
                login.connect2()
                logger.info('Using Connect2 function - ' + profiles[k])
                login.message(text['msg'])
                logger.info('Message Sent - ' + profiles[k])
                success.append(profiles[k])
                accountCounter += 1
            except NoSuchElementException:
                print('Maybe Connection Request Already Sent')
                logger.info('Failed to CONNECT2 - ' + profiles[k])
                pending.append(profiles[k])

            except ElementNotInteractableException:
                print('Failed to Connect1 - element not interactable')
                logger.info('Failed to CONNECT1 - element not interactable - ' + profiles[k])
                fail.append(profiles[k])
        else:
            try:
                t.sleep(4)
                login.connect1()
                logger.info('Using Connect1 function - ' + profiles[k])
                login.message(text['msg'])
                logger.info('Message Sent - ' + profiles[k])
                success.append(profiles[k])
                accountCounter += 1
            except NoSuchElementException:
                print('Maybe Connection Request Already Sent')
                logger.info('Failed to CONNECT1 - ' + profiles[k])
                pending.append(profiles[k])
            except ElementNotInteractableException:
                print('Failed to Connect1 - element not interactable')
                logger.info('Failed to CONNECT1 - element not interactable - ' + profiles[k])
                fail.append(profiles[k])
        print(accountCounter)
        if accountCounter==60:
            accountCounter=0
            print('I REACHED 60 CONNECTS, I WILL NOW SLEEP FOR 1 HOUR')
            t.sleep(3600)
    


profileLinks()
logger.info('Links have been appended to the profiles list')

splitLen= math.ceil(file_len('profiles.txt')/len(userAccounts))
profiles0=profiles[0:(splitLen)]
profiles1=profiles[(splitLen):2*(splitLen)]
profiles2=profiles[2*(splitLen):3*(splitLen)]
profiles3=profiles[3*(splitLen):4*(splitLen)]


t1=Thread(target=connectionMsg, args=(userAccounts[0], profiles0,))
t2=Thread(target=connectionMsg, args=(userAccounts[1], profiles1,))
t3=Thread(target=connectionMsg, args=(userAccounts[2], profiles2,))
t4=Thread(target=connectionMsg, args=(userAccounts[3], profiles3,))
t1.start()
t2.start()
t3.start()
t4.start()
t1.join()
t2.join()
t3.join()
t4.join()
##i have x user account that need to go through x profiles, profiles are split into sub- profiles.. 


