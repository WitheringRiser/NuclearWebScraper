###                         Website Finder by Lukas Brazdeikis                      
###                                     Created 1/7/21                                  
###                                  Last modified 5/8/21                              
### The purpose of this program is to find the best link related to a company name through a Google search.
### Inputs: 
###		- google_pause_length from RunEntireProgram.py
###		- points_from_EPO_per_company.txt
### 	- blacklisted_websites.txt
### Outputs:
###		- websites_to_scrape.txt
###		- points_from_EPO_per_website.txt
###		- patent_number_to_company.txt
###		- patent_number_to_website.txt
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
import requests
import time
from googlesearch import search
import random

global company_names
company_names = []
global num_matches
num_matches = {}
global company_to_website
company_to_website = {}
global good_links
good_links = []


### Input: google_pause_length (int)
### Output: None
def find_links_to_patents_with_keyword_matches(google_pause_length):
	links = []
	for company in pnts_per_company:
		if pnts_per_company[company] == 0:
			pass
		else:
			print('Valid match; searching for link for: ' + company)
			if '*' in company:
				links.append(['Error: Cannot read company name'])
			else:
				run_google_search(company, google_pause_length)


### Takes a company name, does a google search, and returns a list of the top 10 search results.
### Input: query (string), google_pause_length (int)
### Output: None. However, global variable good_links is modified with the addition of the best link from the search
def run_google_search(query, google_pause_length):
	links = ['Google search for "' + query + '" in this sublist.']
	for result in search(query, tld="com", num=10, stop=10, pause=google_pause_length * random_offset(10)):
		links.append(result)

	good_link = get_good_link(links)
	print('Link: ' + good_link)
	company_to_website[query] = good_link
	good_links.append(good_link)


### Input: percentage value (int between 0 and 100)
### Output: offset (int close to 1)
###		- offset is a random number close to 1 with an offset between 0 and the percentage.
def random_offset(percentage):
	offset = 0.01 * random.randint(100 - percentage, 100 + percentage)
	return offset


### Input: links (list of strings)
### Output: good_link (string)
def get_good_link(links):
	good_link = ''
	try:
		blacklisted_found = False
		for j in range(len(blacklisted_websites)):
			if blacklisted_websites[j] in links[1]:
				print('Blacklisted site found: ' + blacklisted_websites[j])
				blacklisted_found = True
				print('Website added')
				good_link = ''
		if not blacklisted_found:
			good_link = links[1]

	except IndexError:
		good_link = ''

	return good_link


### Input: good_links (list of strings)
### Output: None. However, websites_to_scrape.txt is modified
def save_good_links_to_file(good_links):
	file = open('websites_to_scrape.txt', 'w')
	print('Good links:')
	print(good_links)
	for link in good_links:
		file.write(link + '\n')
	file.close


### Input: None
### Output: None. However, points_from_EPO... is written to
def save_points():
	file = open('points_from_EPO_per_website.txt', 'w')
	for key in company_to_website:
		true_hmpg = true_homepage(company_to_website[key])
		file.write(true_hmpg + ': ' + str(pnts_per_company[key]) + '\n')
	file.close()


### Input: homepage (string)
### Output: homepage (string)
###		- Note that the output is the same as the input, however, all sublinks attatched have been stripped.
###		- ex: https://www.netalux.com/products becomes https://www.netalux.com
def true_homepage(homepage):
	for i in range(len(homepage[9:])):
		if homepage[9 + i] == '/':

			return homepage[:i + 9]

	return homepage


### Input: None
### Output: None. However, global variable pnts_per_company is modified
def get_pnts_per_company():
	global pnts_per_company
	pnts_per_company = {}

	file = open('points_from_EPO_per_company.txt', 'r')
	for line in file:
		line.strip('\n')
		pnts_per_company[line[:-5]] = int(line[-4:])
	file.close


### Input: None
### Output: None. However, global variable patent_number_to_company_name is modified
def get_patent_number_to_company_name():
	global patent_number_to_company_name
	patent_number_to_company_name = {}
	file = open('patent_number_to_company.txt', 'r')
	for line in file:
		line = line.split(': ')
		patent_number = int(line[0])
		company_name = line[1].strip('\n')
		print(str(patent_number), company_name)
		patent_number_to_company_name[patent_number] = company_name

	file.close()


### Input: None
### Output: None. However, patent_number_to_website.txt is written to
def save_patent_number_to_website():
	file = open('patent_number_to_website.txt', 'w')
	for patent in patent_number_to_company_name:
		company = patent_number_to_company_name[patent]
		website = company_to_website[company]
		file.write(str(patent) + ': ' + website + '\n')
	file.close()


### Input: None
### Output: None. However, blacklisted_websites.txt is written to
def get_blacklisted_websites():
	global blacklisted_websites
	blacklisted_websites = []
	file = open('blacklisted_websites.txt', 'r')
	for line in file:
		line = line.strip('\n')
		blacklisted_websites.append(line)
	file.close()


### Allows only one patent per website. Removes excess sites from "websites_to_scrape.txt"
### Input: None
### Output: None. However, global variable good_links is modified
def remove_duplicate_links():
	good_links_true_hmpg = []
	for link in good_links:
		true_hmpg = true_homepage(link)
		print(true_hmpg)
		good_links_true_hmpg.append(true_hmpg)
	for link in good_links_true_hmpg:
		if good_links_true_hmpg.count(link) > 1:
			print(good_links_true_hmpg)
			list_of_indices_of_duplicates = [i for i,d in enumerate(good_links_true_hmpg) if d==link]
			print(list_of_indices_of_duplicates)
			current_index = list_of_indices_of_duplicates[0]
			other_indices = list_of_indices_of_duplicates[1:]
			reverse_other_indices = other_indices[::-1]
			print(reverse_other_indices)
			for index in reverse_other_indices:
				del good_links_true_hmpg[index]
				del good_links[index]


### Input: google_pause_length
### Output: None
def main(google_pause_length):

	get_blacklisted_websites()

	get_pnts_per_company()

	find_links_to_patents_with_keyword_matches(google_pause_length)
	print(good_links)

	remove_duplicate_links()
	save_good_links_to_file(good_links)

	time.sleep(0.1)

	print(pnts_per_company)

	save_points()

	get_patent_number_to_company_name()
	save_patent_number_to_website()


#main(2, 1)