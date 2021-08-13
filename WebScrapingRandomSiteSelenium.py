###                         Web Scraper Program by Lukas Brazdeikis                      
###                                     Created 5/7/21                                  
###                                  Last modified 5/8/21                              
### The purpose of this program is to scrape websites looking for keywords and basic website structure.
### The prevalence of keywords, tabs, bad tabs/text, and website size is then turned into various metrics 
### that are saved in various text files.
### Inputs: 
###		- interested_tabs, thoroughness, _bad_tabs_and_bad_text from RunEntireProgram.py
###		- websites_to_scrape.txt
### 	- keywords.txt
### Outputs:
###		- website_lines.txt
###		- list_of_product_links.txt
###		- points_from_website.txt
###		- keyword_matches_from_website_to_website.txt
###		- tab_matches_to_website.txt
### Functions:
###		- get_html_contents()								  - random_offset()
###		- find_html_contents_where_products_pages_can_be()	  - search_through_multiple_links_to_find_keyword_matches()
###		- find_tab_matches()								  - write_product_links()
###		- find_bad_tabs_and_bad_text()						  - calculate_website_structure_score()
###		- get_all_website_text()							  - find_html_content_of_a_given_html_text()
###		- calculate_website_size()							  - find_sublinks()
###		- save_website_text()								  - refine_list()
###		- find_keyword_matches_on_website()					  - search_a_website_and_the_sublinks()
###		- add_keyword_matches_to_points()					  - read_website_links()
###		- add_tab_matches_to_points()						  - save_points_from_website()
###		- add_bad_tab_and_bad_text_matches_to_points()		  - save_keyword_matches()
###		- add_website_size_to_points()						  - save_tab_matches()
###		- get_keywords_list()								  - reset_bad_tabs_bad_text()
### 	- true_homepage()									  - main()


from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.common.exceptions import InvalidArgumentException
from selenium.common.exceptions import WebDriverException
import requests
from csv import writer
import time
import os.path
import random

global score_values
score_values = {}
global scores
scores = {}
global website_structure
website_structure = {}
global num_404_pages
num_404_pages = [0]
global points
points = {}
global list_of_possible_scores_to_add
list_of_possible_scores_to_add = []


### Input: homepage (string), site (string)
###		- site represents the sublinks without the homepage (ex: site = '/products')
### Output: html_contents (a BeautifulSoup object).
###		- html_contents is the body of the html contents of the website
def get_html_contents(homepage, site):

	url = site

	## Creates a browser via Selenium. Selenium is used here to give a "human touch" to loading the website. 
	### Compared to using BeautifulSoup, Selenium lowers the chance of being blocked due to bot behavior.
	browser = webdriver.Chrome()
	browser.minimize_window()

	homepage = true_homepage(homepage)

	## Attempts to load the website via Selenium. If it can't load, there are "except" statements to solve that.
	try:
		browser.get(url)
		print('Visiting ' + url)
	except InvalidArgumentException: ## Takes care of the issue when you run a sublink through this function.
									 ## Sometimes the sublink only contains the portion after ".com".
									 ## For example the sublink might only be "/products/laser-system."
									 ## This except statement then combines the sublink to the homepage to
									 ## get a valid url.
		try:
			browser.get(homepage + url)
			print('Visiting ' + homepage + url)
		except WebDriverException:   ## This exception occurs if the above try statement fails. This means that
									 ## the website truly cannot be found. Therefore, this function returns
									 ## "dummy" values that imply that nothing was found on this website
			return [0], sample_html, 0
	except WebDriverException:		 ## This exception combats a "TypeError" that used to crash the program. This
									 ## error is resolved by returning "dummy" values that imply that nothing was
									 ## found on this website. Very similar to the above exception.
		return [0], sample_html, 0

	time.sleep(1 * random_offset(10))

	## Uses BeautifulSoup to begin extracting and saving the html contents of the website. 
	### A switch to BeautifulSoup from Selenium is made as the html contents are easier to navigate/interact with in BS.
	html = browser.page_source
	soup = BeautifulSoup(html, 'html.parser')

	## This code finishes the extraction and saving of html contents. If there are issues, there are "except"
	## statements to solve that
	try:
		html_contents = soup.body.contents
	except: ## Tries to get around the rare error: "AttributeError 'NoneType' object has no attribute 'contents'". The code
			## below is very similar to the code found above.
		try:
			browser.get(url)
		except InvalidArgumentException:
			browser.get(homepage + url)
			print('Visiting ' + homepage + url)
		try: ## Gives the website a bit more time to load before trying to extract html contents
			time.sleep(2)
			html = browser.page_source
			time.sleep(2)
			soup = BeautifulSoup(html, 'html.parser')
			time.sleep(2)
			html_contents = soup.body.contents
		except: ## Returns "dummy" values that imply nothing was found on this website. 
				## Dummy variables are needed so the code doesn't crash later due to undefined variables.
			return [0], sample_html, 0

	return html_contents


### Input: html_contents (a BeautifulSoup object), html_contents_length (int), do_you_want_to_know... (boolean), interested_tabs (list of strings)
###		- do_you_want_to_know... is True if the html_contents of a homepage are sent through and 
###		  False if the html_contents of a subpage are sent through. A value of True means that the function will search for interested tabs.
### Output: html_content_indices_where_products_pages_can_be (list of ints).
###		- html_content_indices... is saved so that when I search for the existance of tabs, I don't have to search through every section 
###       of html_contents
def find_html_contents_where_products_pages_can_be(html_contents, html_contents_length,\
 do_you_want_to_know_indices_where_product_pages_can_be, interested_tabs):
	html_contents_indices_where_products_pages_can_be = []

	for i in range(html_contents_length):
		line_to_add = ['', ''] 
		if check_if_html_content_subsection_is_valid_V1(html_contents[i]):
			try:
				line_to_add[0] = html_contents[i].get_text()
			except AttributeError:
				line_to_add[0] = ''
			if do_you_want_to_know_indices_where_product_pages_can_be:
				for tab in interested_tabs:
					if tab in line_to_add[0]:
						if i not in html_contents_indices_where_products_pages_can_be:
							html_contents_indices_where_products_pages_can_be.append(i)

	return html_contents_indices_where_products_pages_can_be


### Input: html_contents (a BeautifulSoup object), html_contents_length (int), do_you_want_to_know... (boolean), interested_tabs (list of strings)
### Output: None. However, the global variable tab_matches (list of strings) is modified.
def find_tab_matches(html_contents, html_contents_length, interested_tabs, do_you_want_to_know_indices_where_product_pages_can_be):
	for i in range(html_contents_length):
		line_to_add = ['', ''] 
		if check_if_html_content_subsection_is_valid_V1(html_contents[i]):
			try:
				line_to_add[0] = html_contents[i].get_text() ## 27/7
			except AttributeError:
				line_to_add[0] = ''
			if do_you_want_to_know_indices_where_product_pages_can_be:
				for tab in interested_tabs:
					if tab in line_to_add[0]:
						tab_matches.append(tab)

### Input: html_contents (a BeautifulSoup object), html_contents_length (int), do_you_want_to_know... (boolean)
### Output: None. However, the global variable bad_tabs_bad_text (dictionary) is modified.
def find_bad_tabs_and_bad_text(html_contents, html_contents_length, do_you_want_to_know_indices_where_product_pages_can_be):
	for i in range(html_contents_length):
		line_to_add = ['', ''] 
		if check_if_html_content_subsection_is_valid_V1(html_contents[i]):
			try:
				line_to_add[0] = html_contents[i].get_text() 
			except AttributeError:
				line_to_add[0] = ''
			if do_you_want_to_know_indices_where_product_pages_can_be:
				for key in bad_tabs_and_bad_text:
					if key in line_to_add[0]:
						bad_tabs_and_bad_text[key] += 1


### Input: html_contents (a BeautifulSoup object), html_contents_length (int)
### Output: all_text(list of strings)
def get_all_website_text(html_contents, html_contents_length):
	all_text = []

	for i in range(html_contents_length):
		line_to_add = ['', ''] 
		if check_if_html_content_subsection_is_valid_V1(html_contents[i]):
			try:
				line_to_add[0] = html_contents[i].get_text() ## 27/7
			except AttributeError:
				line_to_add[0] = ''	
		all_text.append(line_to_add)

	return all_text


### Input: html_contents (a BeautifulSoup object)
### Output: None. However, the global variable total_number_of_all_sublinks (list comprising of a single int) is modified
def calculate_website_size(html_contents):
	global total_number_of_all_sublinks
	total_number_of_all_sublinks = [0]
	for i in range(len(html_contents)):
		if check_if_html_content_subsection_is_valid_V2(html_contents[i]):
			continue
		all_a_html = html_contents[i].find_all('a')
		total_number_of_all_sublinks[0] += len(all_a_html)
	print('Website size (total number of sublinks): ' + str(total_number_of_all_sublinks[0]))


### Input: num_sections_of_website (int), all_text (list of strings)
### Output: None. However, the file website_lines.txt is created and written in.
def save_website_text(num_sections_of_website, all_text):
	file = open('website_lines.txt', 'w')
	for i in range(num_sections_of_website):
		try:
			for j in range(len(all_text[i])):
				file.write(str(all_text[i][j]))
		except UnicodeEncodeError as bad_char:
			for k in range(len(all_text[i])):
				for l in range(len(all_text[i][k])):
					try:
						file.write(str(all_text[i][k][l]))
					except UnicodeEncodeError:
						file.write('*')
	file.close()


### Input: homepage (string), site (string), do_you_want_to_know... (boolean), num_websites_checked (int),
### list_of_keywords (list of strings) interested_tabs (list of strings)
### Output: html_content_indices_where... (list of ints), html_contents (BeautifulSoup object), num_matches (int)
def find_keyword_matches_on_website(homepage, site, do_you_want_to_know_indices_where_product_pages_can_be,\
num_websites_checked, list_of_keywords, interested_tabs):

	html_contents = get_html_contents(homepage, site)
	
	all_text = []
	html_contents_length = len(html_contents)
	html_contents_indices_where_products_pages_can_be = []
	num_sections_of_website = 0

	html_contents_indices_where_products_pages_can_be = find_html_contents_where_products_pages_can_be(html_contents,\
	 html_contents_length, do_you_want_to_know_indices_where_product_pages_can_be, interested_tabs)
	find_tab_matches(html_contents, html_contents_length, interested_tabs, do_you_want_to_know_indices_where_product_pages_can_be)
	find_bad_tabs_and_bad_text(html_contents, html_contents_length, do_you_want_to_know_indices_where_product_pages_can_be)
	all_text = get_all_website_text(html_contents, html_contents_length)
	num_sections_of_website = len(all_text)


	if do_you_want_to_know_indices_where_product_pages_can_be: ## If on the homepage, calculate website size
		calculate_website_size(html_contents)
	
	save_website_text(num_sections_of_website, all_text)

	num_lines_of_website = 0
	num_matches = 0
	
	with open('website_lines.txt', 'r') as website_lines: ## Tallies keyword matches and saves the scores attatched to the keywords
		current_line = 0
		for line in website_lines:
			current_line += 1
			if current_line == 1:
				continue
			for keyword in list_of_keywords:
				if keyword in line:
					score = score_values[keyword]
					list_of_possible_scores_to_add.append(score)
					num_matches += 1
					keyword_matches.append(keyword)

	list_of_possible_scores_to_add.sort(key=lambda x: x, reverse=True)
	
	num_websites_checked[0] += 1
	print('Number of keyword matches on this homepage/subpage: ' + str(num_matches))

	return html_contents_indices_where_products_pages_can_be, html_contents, num_matches


### Input: list_of_possible_scores_to_add (list of ints), homepage (string)
### Output: None. However, global variable points (dictionary) is modified.
def add_keyword_matches_to_points(list_of_possible_scores_to_add, homepage):
	score = 0
	if len(list_of_possible_scores_to_add) > 4:
		score += 5 * list_of_possible_scores_to_add[0] + 5 * list_of_possible_scores_to_add[1] + 5 * list_of_possible_scores_to_add[2]\
		+ 5 * list_of_possible_scores_to_add[3]
	else:
		for scr in list_of_possible_scores_to_add:
			score += 5 * scr
	try:
		points[true_homepage(homepage)] += 1
		points[true_homepage(homepage)] -= 1
	except:
		points[true_homepage(homepage)] = 0

	points[true_homepage(homepage)] += score
	print('+' + str(score) + ' points for keyword matches')
	

### Input: homepage (string)
### Output: None. However, global variable points (dictionary) is modified.
def add_tab_matches_to_points(homepage):
	true_hmpg = true_homepage(homepage)
	num_tab_matches = website_structure[true_hmpg]

	try:
		points[true_hmpg] += 1
		points[true_hmpg] -= 1
	except:
		points[true_hmpg] = 0

	if num_tab_matches == 1:
		points[true_hmpg] += 50
		print('+50 points for tab matches')
	elif num_tab_matches == 2:
		points[true_hmpg] += 75
		print('+75 points for tab matches')
	elif num_tab_matches >= 3:
		points[true_hmpg] += 100
		print('+100 points for tab matches')

### Input: homepage (string)
### Output: None. However, global variable points (dictionary) is modified.
def add_bad_tab_and_bad_text_matches_to_points(homepage):
	true_hmpg = true_homepage(homepage)

	total_category_matches = 0 # Max one match per item in bad_tab_and_bad_text
	for key in bad_tabs_and_bad_text:
		if bad_tabs_and_bad_text[key] > 1:
			total_category_matches += 1
	if total_category_matches >= 3:
		points[true_hmpg] -= 75
		print('-75 points for bad keyword/tab matches')
	elif total_category_matches >= 2:
		points[true_hmpg] -= 50
		print('-50 points for bad keyword/tab matches')
	elif total_category_matches == 1:
		points[true_hmpg] -= 25
		print('-25 points for bad keyword/tab matches')


### Input: homepage (string)
### Output: None. However, global variable points (dictionary) is modified.
def add_website_size_to_points(homepage):
	true_hmpg = true_homepage(homepage)
	total_number_of_all_sublinks = total_number_of_all_sublinks[0]

	try:
		points[true_hmpg] += 1
		points[true_hmpg] -= 1
	except:
		points[true_hmpg] = 0

	if total_number_of_all_sublinks >= 500:
		points[true_hmpg] -= 150
		print('-100 points for website size')
	elif total_number_of_all_sublinks >= 300:
		points[true_hmpg] -= 100
		print('-100 points for website size')
	elif total_number_of_all_sublinks >= 200:
		points[true_hmpg] -= 50
		print('-50 points for website size')
	elif total_number_of_all_sublinks >= 150:
		points[true_hmpg] -= 25
		print('-25 points for website size')


### Input: None. However, keywords.txt is read from
### Output: list_of_keywords (list of strings). Also, global variable score_values (dictionary) is modified
def get_keywords_list():
	with open('keywords.txt') as keywords:
		list_of_keywords = []
		for line in keywords:
			line = line.strip('\n')
			list_of_keywords.append(line[:-2]) ## The keyword
			score_values[line[:-2]] = int(line[-1:]) ## The keyword point value
			list_of_keywords.append(line.lower()[:-2])
			score_values[line[:-2].lower()] = int(line[-1:])

	return list_of_keywords


### Input: homepage (string)
### Output: homepage (string)
###		- Note that the output is the same as the input, however, all sublinks attatched have been stripped.
###		- ex: https://www.netalux.com/products becomes https://www.netalux.com
def true_homepage(homepage):
	for i in range(len(homepage[9:])):
		if homepage[9 + i] == '/':
			return homepage[:i + 9]

	return homepage


### Input: percentage value (int between 0 and 100)
### Output: offset (int close to 1)
###		- offset is a random number close to 1 with an offset between 0 and the percentage.
def random_offset(percentage):
	offset = 0.01 * random.randint(100 - percentage, 100 + percentage)
	return offset


### Input: homepage (string), _2D_list_of_sublinks (list of lists of strings), thoroughness (int), num_websites_checked (int),
### num_matches (list of two ints), list_of_keywords (list of strings), interested_tabas (list of strings)
###		- thoroughness refers to how often a sublink under one of the interested tabs should be searched.
###		  Ex: thoroughness == 10 means that every 10th link under each tab of interested_tabs will be searched for keywords.
### Output: None. However, global variables num_matches and num_websites_checked are modified.

def search_through_multiple_links_to_find_keyword_matches(homepage, _2D_list_of_sublinks, thoroughness, num_websites_checked,\
 num_matches, list_of_keywords, interested_tabs): ##
	results = []
	for list_of_sublinks in _2D_list_of_sublinks:
		for i in range(len(list_of_sublinks)):
			if i % thoroughness == 0: ### Considers the first sublink in each list_of_sublinks and every X sublink in each list_of_sublinks where X = thoroughness
				html_contents_indices_where_products_pages_can_be, html_contents, matches = find_keyword_matches_on_website(homepage, list_of_sublinks[i],\
					False, num_websites_checked, list_of_keywords, interested_tabs)
				other_options = False
				for j in range(len(html_contents)): ### Searches through html contents of the website
					if check_if_html_content_subsection_is_valid_V3(html_contents[j]):
						if not other_options:
							if '404' in html_contents[j].get_text(): ### If you reach a page that has a 'Error 404'
								try:
									print(list_of_sublinks)
									print('Error 404: ' + list_of_sublinks[i])
									print('Next link tried in its place: ' + list_of_sublinks[i + 1])
									html_contents_indices_where_products_pages_can_be, html_contents, matches = find_keyword_matches_on_website(homepage, list_of_sublinks[i + 1],\
									False, num_websites_checked, list_of_keywords, interested_tabs)
									num_websites_checked[0] -= 1
									num_matches[1] += matches
									num_404_pages[0] += 1
									other_options = True
								except IndexError:
									pass
				if other_options == False: ### Adds matches to num_matches if it wasn't already added.
					num_matches[1] += matches


### Input: _2D_list_of_sublinks (list of lists of strings), interested_tabs (list of strings)
### Output: None. However, list_of_products_links.txt is written to.
def write_product_links(_2D_list_of_sublinks, interested_tabs): ##
	with open('list_of_product_links.txt', 'w') as file:
		for i in range(len(_2D_list_of_sublinks)):
			file.write(interested_tabs[i] + '\n')
			list_of_sublinks = _2D_list_of_sublinks[i]
			for link in list_of_sublinks:
				file.write(link + '\n')


### Input: _2D_list_of_sublinks (list of lists of strings), interested_tabs (list of strings), true_hmpg (string)
### Output: None. However, global variable website_structure (dictionary) is modified.
def calculate_website_structure_score(_2D_list_of_sublinks, interested_tabs, true_hmpg):
	for i in range(len(_2D_list_of_sublinks)):
		list_of_sublinks = _2D_list_of_sublinks[i]
		if len(list_of_sublinks) >= 1:
			website_structure[true_hmpg] += 1


### Input: parents_html_text (a BeautifulSoup object), html_contents (a BeautifulSoup object), indicies_where... (list of ints)
def find_html_content_of_a_given_html_text(parents_html_text, html_contents, indices_where_text_can_be_found): ## ---
	_2D_list_of_sublinks = []
	list_of_sublinks = []

	for parent_html_text in parents_html_text:
		for i in indices_where_text_can_be_found:
			relevant_html_contents = html_contents[i]
			for child in relevant_html_contents.descendants:
				if child.string != None:
					if parent_html_text in child.string or parent_html_text.lower() in child.string:
						find_sublinks(child, i, list_of_sublinks)
		_2D_list_of_sublinks.append(list_of_sublinks)
		list_of_sublinks = []

	return _2D_list_of_sublinks


### Input: html_contents (a BeautifulSoup object), i (int), list_of_sublinks (list of strings)
### 	- Note: html_contents here is NOT ALL html_contents of the website. Only a specific portion of them.
### Output: list_of_sublinks
###		- the input is appended and returned. The addition includes more sublinks found in the inputted html_contents
def find_sublinks(html_contents, i, list_of_sublinks): ## ---
	if str(type(html_contents)) == "<class 'bs4.element.Comment'>":
		return

	if html_contents.parent.name == 'a':
		html_contents = html_contents.parent

	try:
		link = html_contents.get('href')
		if link != '#' and link != None and 'javascript:void' not in link:
			list_of_sublinks.append(link)
	except:
		pass

	try:
		new_parent = html_contents.find_next_sibling()
	except TypeError:
		return
	except AttributeError:
		new_parent = html_contents


	if new_parent == None:
		return

	all_a_html = new_parent.find_all('a')
	for a in all_a_html:
		link = a.get('href')
		if link != None and 'javascript:void' not in link:
			list_of_sublinks.append(link)

	return list_of_sublinks


### Input: _2D_list... (list of lists of strings)
### Output: _2D_list... (list of lists of strings)
###		- This output is a modified version of the input.
###       Removes sublists of length 0
def refine_list(_2D_list_of_sublinks): 
	new_2D_list_of_sublinks = []
	new_list_of_sublinks = []
	for list_of_sublinks in _2D_list_of_sublinks:
		for i in range(len(list_of_sublinks)):
			try:
				sub_section_length = len(list_of_sublinks[i])
			except TypeError:
				sub_section_length = 0
			for j in range(sub_section_length):
				new_list_of_sublinks.append(list_of_sublinks[i][j])
		new_2D_list_of_sublinks.append(new_list_of_sublinks)
	return new_2D_list_of_sublinks


### Input: homepage (string), interested_tabs (list of strings), thoroughness (int)
### Output: None. However, global variables num_matches (list), num_websites_checked (list of a single int),
### scores (dictionary) are modified.
def search_a_website_and_the_sublinks(homepage, interested_tabs, thoroughness):
	global num_matches
	num_matches = [0, 0]
	global num_websites_checked
	num_websites_checked = [0]
	do_you_want_to_know_indices_where_product_pages_can_be = True

	list_of_keywords = get_keywords_list()

	true_hmpg = true_homepage(homepage)

	scores[true_hmpg] = 0
	website_structure[true_hmpg] = 0

	html_contents_indices_where_products_pages_can_be, html_contents, num_matches[0] = find_keyword_matches_on_website(homepage, homepage, True,\
	 num_websites_checked, list_of_keywords, interested_tabs)
	_2D_list_of_sublinks = find_html_content_of_a_given_html_text(interested_tabs, html_contents, html_contents_indices_where_products_pages_can_be)

	write_product_links(_2D_list_of_sublinks, interested_tabs)
	calculate_website_structure_score(_2D_list_of_sublinks, interested_tabs, true_hmpg)

	search_through_multiple_links_to_find_keyword_matches(homepage, _2D_list_of_sublinks, thoroughness, num_websites_checked, num_matches,\
	 list_of_keywords, interested_tabs)

	print('Number of sublinks checked: ' + str(num_websites_checked[0]))

	scores[true_hmpg] /= num_websites_checked[0]


### Input: None
### Output: websites (list of strings)
def read_website_links():
	websites = []

	file = open('websites_to_scrape.txt', 'r')
	for line in file:
		websites.append(line.strip('\n'))
	return websites

### Input: None. 
### Output: None. However, points_from_website.txt is written to
def save_points_from_website():
	file = open('points_from_website.txt', 'w')
	for website in points:
		file.write(str(website) + ' ' + str(points[website]) + '\n')
	file.close

### Input: website (string)
### Output: None. However, keyword_matches_from_website_to_website.txt is appended to.
def save_keyword_matches(website):
	true_hmpg = true_homepage(website)
	file = open('keyword_matches_from_website_to_website.txt', 'a')
	if len(keyword_matches) > 0:
		file.write(true_hmpg)
		for keyword in keyword_matches:
			file.write(' ' + keyword)
		file.write('\n')
	file.close()

### Input: website (string)
### Output: None. However, tab_matches_to_website.txt is appended to
def save_tab_matches(website):
	print('Tab matches: ', end = '')
	print(tab_matches)
	true_hmpg = true_homepage(website)
	file = open('tab_matches_to_website.txt', 'a')
	if len(tab_matches) > 0:
		file.write(true_hmpg)
		for tab in tab_matches:
			file.write(' ' + tab)
		file.write('\n')
	file.close()

### Input: None
### Output: None. However, global variable bad_tabs_and_bad_text (dict) is modified
def reset_bad_tabs_bad_text():
	for key in bad_tabs_and_bad_text:
		bad_tabs_and_bad_text[key] = 0


### Input: html_contents_subsection (a component of a BeautifulSoup object?)
### Output: html_contents_subsection (a component of a BeautifulSoup object?)
def check_if_html_content_subsection_is_valid_V1(html_contents_subsection):
	return html_contents_subsection != '\n' and not (str(type(html_contents_subsection)) == "<class 'bs4.element.Comment'>")


### Input: html_contents_subsection (a component of a BeautifulSoup object?)
### Output: html_contents_subsection (a component of a BeautifulSoup object?)
def check_if_html_content_subsection_is_valid_V2(html_contents_subsection):
	return str(type(html_contents_subsection)) == "<class 'bs4.element.Comment'>" or\
		 str(type(html_contents_subsection)) == "<class 'bs4.element.NavigableString'>"


### Input: html_contents_subsection (a component of a BeautifulSoup object?)
### Output: html_contents_subsection (a component of a BeautifulSoup object?)
def check_if_html_content_subsection_is_valid_V3(html_contents_subsection):
	return html_contents_subsection != '\n' and not (str(type(html_contents_subsection)) == "<class 'bs4.element.Comment'>")\
					and not (str(type(html_contents_subsection)) == "<class 'bs4.element.NavigableString'>")\
					and not isinstance(html_contents_subsection, str)


### Main function. This is where the program starts.
### Input: interested_tabs (list of strings), thoroughness (int), _bad_tabs_and_bad_text (list of strings)
### Output: None
def main(interested_tabs, thoroughness, _bad_tabs_and_bad_text):
	global bad_tabs_and_bad_text
	bad_tabs_and_bad_text = _bad_tabs_and_bad_text

	### Temporarily opened to allow the files to be appended to later ('a' vs. 'w')
	file = open('keyword_matches_from_website_to_website.txt', 'w')
	file.close()
	file = open('tab_matches_to_website.txt', 'w')
	file.close()

	### Goes through all the websites and runs "search_a_website_and_the_sublinks" for each site.
	### Sets and resets various values for each website too
	websites = read_website_links()
	for website in websites:
		if website != '' and website != None:
			print('-----------------------------')
			print('      New Website Now        ')
			print('Checking website: ' + website)
			global list_of_possible_scores_to_add
			list_of_possible_scores_to_add = [] ### All scores from all keywords in all sublinks
			global keyword_matches
			keyword_matches = [] ### List of keywords that show up for the website in question. Only used to save to file
			global tab_matches
			tab_matches = [] ### List of tab matches that show up for the website in question. Only used to save to file
			reset_bad_tabs_bad_text()
			try:
				search_a_website_and_the_sublinks(website, interested_tabs, thoroughness)
			except Exception as e:
				print('Failed to search website: ' + website)
				print('Exception received: ')
				print(e)
				print('')
				list_of_possible_scores_to_add = [0]
				website_structure[true_homepage(website)] = 0

			add_keyword_matches_to_points(list_of_possible_scores_to_add, website)
			add_bad_tab_and_bad_text_matches_to_points(website)
			add_tab_matches_to_points(website)
			save_keyword_matches(website)
			save_tab_matches(website)
			print('Points from this website and all subsites (does not include EPO score): ', end = '')
			print(points[true_homepage(website)])
	
	time.sleep(0.1)

	save_points_from_website()