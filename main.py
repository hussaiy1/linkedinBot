from lnkdn_driver import *
from recruiter import *
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import ElementNotInteractableException
import logging
import os
import time as t
import math
import json
from os import system
from datetime import datetime
from colorama import init, Fore, Back, Style

init(autoreset=True)

system('title' + 'LINKEDIN BOT 2.0')

if os.path.isfile('linkedin_msg_log.log'):
    os.remove('linkedin_msg_log.log')

if os.path.isfile('recruiterProfiles.txt'):
    os.remove('recruiterProfiles.txt')

if os.path.isfile('profiles.txt'):
    os.remove('profiles.txt')


logger= logging.getLogger('linkedin_recruiter_log.log')
logger.setLevel(logging.DEBUG)

fh=logging.FileHandler('linkedin_recruiter_log.log')
formatter=logging.Formatter('%(asctime)s - %(message)s')

fh.setFormatter(formatter)
fh.setLevel(logging.DEBUG)
logger.addHandler(fh)

profiles=[]
success=[]
fail=[]
pending=[]
text=[]

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

headcount=0

if __name__ == "__main__":
    while(headcount==0):
        recruiter=recruiterDriver()
        recruiter.login('xxxxxxxxxxxxxxxx@xxxxxxxxxx.com','xxxxxxxxxxxxxxxxx')
        logger.info('Logging In ...')
        dateTimeObj = datetime.now()
        print(Fore.GREEN + '[{}] Logging In... '.format(str(dateTimeObj)))
        t.sleep(10)
        searchTerm=input(Fore.GREEN + '[{}] What is your search criteria: '.format(str(dateTimeObj)))
        recruiter.search(searchTerm)
        print(Fore.GREEN + '[{}] Sleeping for 5 mins, time to do CUSTOM FILTERS'.format(str(dateTimeObj)))
        t.sleep(180)
        print(Fore.GREEN + '[{}] 2mins left '.format(str(dateTimeObj)))
        currentURL=recruiter.printURL()
        t.sleep(5)
        headcount=recruiter.profileCount()
        headcount=headcount.replace(" candidates", " ")
        headcount=headcount.replace(",", "")
        totalPages=(int(headcount))/25
        t.sleep(5)
        if totalPages > 1000:
            bigListURL=[]
            bigListDigits=[]
            print(Fore.YELLOW + 'There are ' + headcount + ' candidates' + ' , divided into ' + str(math.ceil(totalPages)) + ' pages')
            currentURL=currentURL[:-1]
            for i in range(0,1001):
                if i%25==0:
                    bigListDigits.append(str(i))
            for k in range(len(bigListDigits)):
                bigListURL.append(currentURL + bigListDigits[k])
                recruiter.changeURL(bigListURL[k])
                t.sleep(5)
                recruiter.profileLinkScrape()
                dateTimeObj = datetime.now()
                print(Fore.YELLOW + '[{}] I am getting the URL for individual profiles '.format(str(dateTimeObj)))
            if os.path.isfile('recruiterProfiles.txt'):
                profiles=open('recruiterProfiles.txt','r')
                lines=profiles.readline()
            for line in profiles:
                recruiter.changeURL('https://www.linkedin.com' + line)
                t.sleep(5)
                recruiter.publicURL()
                dateTimeObj = datetime.now()
                print(Fore.YELLOW + '[{}] I have the Linkedin URL '.format(str(dateTimeObj)))
        else:
            print(Fore.YELLOW + 'There are ' + headcount + ' candidates' + ' , divided into ' + str(math.ceil(totalPages)) + ' pages')
            smallListURL=[]
            smallListDigits=[]
            totalPages=math.ceil(totalPages)
            currentURL=currentURL[:-1]
            for i in range(0, int(headcount)):
                if i%25==0:
                    smallListDigits.append(str(i))
            for k in range(len(smallListDigits)):
                smallListURL.append(currentURL + smallListDigits[k])
            for i in range(0, len(smallListURL)):
                recruiter.changeURL(smallListURL[i])
                t.sleep(5)
                recruiter.profileLinkScrape()
                print(Fore.YELLOW + '[{}] I am getting the URL for individual profiles '.format(str(dateTimeObj)))
        if os.path.isfile('recruiterProfiles.txt'):
            profiles=open('recruiterProfiles.txt','r')
            lines=profiles.readline()
            for line in profiles:
                recruiter.changeURL('https://www.linkedin.com' + line)
                t.sleep(5)
                recruiter.publicURL()
                dateTimeObj = datetime.now()
                print(Fore.YELLOW + '[{}] I have the Linkedin URL '.format(str(dateTimeObj)))
    t.sleep(120)
    dateTimeObj = datetime.now()
    print(Fore.YELLOW + '[{}] YOU CAN NOW START CONNECTING WITH THE SCRAPED CANDIDATES \n PLEASE RUN THE FOLLOWING COMMAND:'.format(str(dateTimeObj)))
    print(Fore.GREEN + '[{}] python3 connectOnly.py'.format(str(dateTimeObj)))

	

writeSuccess()
writeFail()
writePending()




