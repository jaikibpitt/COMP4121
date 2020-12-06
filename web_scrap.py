

from selenium import webdriver
from selenium.webdriver.common.by import By

# prepare the option for the chrome driver
options = webdriver.ChromeOptions()
options.add_argument('headless')

# start chrome browser
browser = webdriver.Chrome(options=options)
url = 'https://www.oddsportal.com/rugby-league/australia/nrl/results/'
browser.get(url)
games = browser.find_elements_by_css_selector('td.name')

game_urls = list()
for g in games:
    innerHTML = g.get_attribute('innerHTML')
    innerHTML = innerHTML.split('">')[0]
    href = 'https://www.oddsportal.com'+innerHTML.split('"')[1]+'#home-away'
    game_urls.append(href)

for g_url in game_urls:
    browser.get(g_url)



browser.quit()
