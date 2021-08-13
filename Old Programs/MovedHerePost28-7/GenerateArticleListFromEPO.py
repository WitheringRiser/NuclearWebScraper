###                           EPO Scraper by Lukas Brazdeikis                  
###                                     Created 26/6/21                                 
###                                   Last modified 6/7/21                              
### Input: None.
### Output: Patent information scraped from EPO ("Articles.txt").
### This program goes to EPO and automatically loads up patents.
### The patent information is then saved.


from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from bs4 import BeautifulSoup
import time
import random
import pyautogui


### Gets all the information about the patent in text form.
def get_articles(site, browser):
	# copy-text--1PF5F1f5 item__content-abstract---5sQYrej
	articles = browser.find_element_by_class_name('publications-list--mYtsKGTt')
	print(articles.text)

	#grandchild = article_tag.below().below()
	#print(grandchild)

	return articles.text

### Goes to the EPO website, waits for the page to load, and performs a scrolling action to load more patents.
def setup(site, how_many_scrolls):

	#url = "https://worldwide.espacenet.com/patent/search?f=publications.lang%3Ain%3Den%7Cpublications.pd%3Ain%3D20140101-20211231&q=cpc%3DF"
	url = site
	browser = webdriver.Chrome()
	browser.get(url)
	time.sleep(2 * random_offset(10))
	#articles = browser.find_element_by_class_name('loading--2XHFsexm publications-list__loader--3ZaL4s2T loading--inline--2tlc_Dk-')
	#webdriver.ActionChains(browser).move_to_element(articles).perform()
	#time.sleep(2)
	#wheel_element(articles, -500)
	pyautogui.moveTo(200, 800)
	time.sleep(1)
	for i in range(how_many_scrolls):
		pyautogui.scroll(-2000)
		if i % 3 == 0:
			time.sleep(0.5)
		time.sleep(0.2)

	time.sleep(2)
	html = browser.page_source
	time.sleep(1)

	return browser

### Gets a random offset depending on the percentage given. E.g. percentage = 10 will return random number between 0.9 and 1.1.
def random_offset(percentage):
	offset = 0.01 * random.randint(100 - percentage, 100 + percentage)
	return offset

### All patent info stored to "Articles.txt"
def store_articles(articles):
	with open('Articles.txt', 'w') as file:
		for ch in articles:
			try:
				file.write(ch)
			except UnicodeEncodeError as char:
				file.write('*')



###Main function. This is where the program starts.
def main(how_many_scrolls):
	site = "https://worldwide.espacenet.com/patent/search?f=publications.lang%3Ain%3Den%7Cpublications.pd%3Ain%3D20140101-20211231&q=cpc%3DF"
	#how_many_scrolls = 50
	browser = setup(site, how_many_scrolls)

	articles = get_articles(site, browser)

	store_articles(articles)

	time.sleep(0.1)

	browser.quit()

#main()

