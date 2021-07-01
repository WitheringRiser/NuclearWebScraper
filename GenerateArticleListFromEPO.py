#Created 26/6/21

from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from bs4 import BeautifulSoup
import time
import random
import pyautogui

def wheel_element(element, deltaY = 120, offsetX = 0, offsetY = 0):
  error = element._parent.execute_script("""
    var element = arguments[0];
    var deltaY = arguments[1];
    var box = element.getBoundingClientRect();
    var clientX = box.left + (arguments[2] || box.width / 2);
    var clientY = box.top + (arguments[3] || box.height / 2);
    var target = element.ownerDocument.elementFromPoint(clientX, clientY);

    for (var e = target; e; e = e.parentElement) {
      if (e === element) {
        target.dispatchEvent(new MouseEvent('mouseover', {view: window, bubbles: true, cancelable: true, clientX: clientX, clientY: clientY}));
        target.dispatchEvent(new MouseEvent('mousemove', {view: window, bubbles: true, cancelable: true, clientX: clientX, clientY: clientY}));
        target.dispatchEvent(new WheelEvent('wheel',     {view: window, bubbles: true, cancelable: true, clientX: clientX, clientY: clientY, deltaY: deltaY}));
        return;
      }
    }    
    return "Element is not interactable";
    """, element, deltaY, offsetX, offsetY)
  if error:
    raise WebDriverException(error)

def get_articles(site, browser):
	# copy-text--1PF5F1f5 item__content-abstract---5sQYrej
	articles = browser.find_element_by_class_name('publications-list--mYtsKGTt')
	print(articles.text)

	#grandchild = article_tag.below().below()
	#print(grandchild)

	return articles.text


def setup(site):

	#url = "https://worldwide.espacenet.com/patent/search?f=publications.lang%3Ain%3Den%7Cpublications.pd%3Ain%3D20140101-20211231&q=cpc%3DF"
	url = site
	browser = webdriver.Chrome()
	browser.get(url)
	time.sleep(10 * random_offset(10))
	#articles = browser.find_element_by_class_name('loading--2XHFsexm publications-list__loader--3ZaL4s2T loading--inline--2tlc_Dk-')
	#webdriver.ActionChains(browser).move_to_element(articles).perform()
	#time.sleep(2)
	#wheel_element(articles, -500)
	pyautogui.moveTo(200, 800)
	time.sleep(1)
	for i in range(50):
		pyautogui.scroll(-2000)
		if i % 3 == 0:
			time.sleep(0.5)
		time.sleep(0.2)

	time.sleep(2)
	html = browser.page_source
	time.sleep(1)


	return browser

def random_offset(percentage):
	offset = 0.01 * random.randint(100 - percentage, 100 + percentage)
	return offset

def store_articles(articles):
	with open('Articles.txt', 'w') as file:
		for ch in articles:
			try:
				file.write(ch)
			except UnicodeEncodeError as char:
				file.write('*')




def main():
	site = "https://worldwide.espacenet.com/patent/search?f=publications.lang%3Ain%3Den%7Cpublications.pd%3Ain%3D20140101-20211231&q=cpc%3DF"
	browser = setup(site)

	articles = get_articles(site, browser)

	store_articles(articles)

	#browser.quit()

main()

