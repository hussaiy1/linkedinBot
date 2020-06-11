from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import time
from datetime import datetime
from colorama import init, Fore, Back, Style
import os
import sys
import shutil

init(autoreset=True)

class recruiterDriver(object):

    def __init__(self):
        home = os.path.expanduser('~')
        user = home.split('/')[2]
        shutil.rmtree('/Users/{}/.wdm/drivers/chromedriver'.format(user))
        self.driver = webdriver.Chrome(ChromeDriverManager().install())
    
    def login(self,usrname, pwrd):
        url = 'https://www.linkedin.com/uas/login-cap?session_redirect=https%3A%2F%2Fwww%2Elinkedin%2Ecom%2Fcap&source_app=cap&trk=cap_signin'
        self.driver.get(url)
        username = self.driver.find_element_by_id('username')
        password = self.driver.find_element_by_id('password')
        username.send_keys(usrname)
        password.send_keys(pwrd)
        self.driver.find_element_by_xpath("//button[@class='btn__primary--large from__button--floating']").click()
    
    def search(self,keywords):
        self.driver.find_element_by_xpath("//button[@class='uncollapse-trigger']").click()
        #self.driver.find_element_by_xpath("//div[@class='search-bar']").click()
        time.sleep(5)
        search=self.driver.find_element_by_xpath("//input[@class='js-typeahead tt-input']")
        search.send_keys(keywords)
        #pyautogui.typewrite(keywords)
        self.driver.find_element_by_xpath("//button[@type='submit']").click()

    def profileCount(self):
        content = self.driver.page_source.encode('utf-8').strip()
        soup = BeautifulSoup(content, "html5lib")
        headCount=soup.find('h2', attrs={'id': 'search-info'}).get_text()
        return(headCount)
    
    def printURL(self):
        return(self.driver.current_url)
    
    def changeURL(self, url):
        self.driver.get(url)
    
    def profileLinkScrape(self):
        content = self.driver.page_source.encode('utf-8').strip()
        soup = BeautifulSoup(content, "html5lib")
        searchData=soup.find('ol', attrs={'id': 'search-results'})
        with open('recruiterProfiles.txt', 'a') as f:
            for links in searchData:
                for profileLink in links.findAll('a', href=True):
                    profileURL=profileLink['href']
                    f.write('%s\n' % profileURL)
        f.close()
    
    def publicURL(self):
        content = self.driver.page_source.encode('utf-8').strip()
        soup = BeautifulSoup(content, "html5lib")
        publicProfile=soup.find('li', attrs={'class': 'public-profile searchable'})
        if publicProfile != None:
            publicURL=publicProfile.find('a')['href']
            with open('profiles.txt', 'a') as f:
                f.write('%s\n' % publicURL)
                f.close()
        else:
            dateTimeObj = datetime.now()
            print(Fore.RED + '[{}] PROFILE OUT OF NETWORK '.format(str(dateTimeObj)))
