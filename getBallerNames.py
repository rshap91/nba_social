# get list of Ballers
import requests
from bs4 import BeautifulSoup
# scrape top 50 players from here
url = "https://www.ranker.com/crowdranked-list/top-10-current-nba-players?var=6&utm_expid=16418821-388.pwrOe5-lSJetLqzNW0S00A.1&utm_referrer=https%3A%2F%2Fwww.google.com%2F"

resp = requests.get(url)
print(resp.status_code)
soup = BeautifulSoup(resp.text, 'lxml')

# this gets first 50 out of 100 ballers
# 51-100 only load when scroll to bottom of page
# These could be gathered using selenium but for now 50 will do.
names = soup.findAll('a', class_='listItem__title listItem__title--link black $tkl')
names = [n.text for n in names]
len(names)


with open('ballers.txt', 'w') as f:
    f.write('\n'.join(names))


# This is a list of all players
# will use for named entity recognition for FB
# NM these HAVE to be gathered with selenium
import os
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
chromedriver = '/Users/rick.shapiro/Documents/Python_Programs/Selenium/Drivers/chromedriver'
os.environ['webdriver.chrome.driver'] = chromedriver

browser = webdriver.Chrome(chromedriver)

url = "https://stats.nba.com/players/list/"
browser.get(url) # spins for a while...
lis = browser.find_elements_by_css_selector('li.players-list__name a')
names = [l.text for l in lis]
len(names)
browser.close()

with open('all_ballers.txt', 'w') as f:
    f.write('\n'.join(names))
