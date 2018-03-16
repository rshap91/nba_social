#get twitter accounts
import requests
from bs4 import BeautifulSoup

url = 'https://www.basketball-reference.com/friv/twitter.html'

resp = requests.get(url)
soup = BeautifulSoup(resp.text, 'lxml')

trs = soup.findAll("tr")
len(trs)

row_data = [tr.findAll('td', class_='left') for tr in trs]
player_accts = [(rd[0].find('a').text, rd[1].find('a').text) for rd in row_data if rd]

with open("player_twitter_accts.csv", 'w') as f:
    f.writelines(','.join(pa)+'\n' for pa in player_accts)
