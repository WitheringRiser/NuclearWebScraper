###                           Website finder by Lukas Brazdeikis                  
###                                     Created 1/7/21                                 
###                                   Last modified 6/7/21                              
### Input: Company names ("EPO_company_names.txt") and keyword matches ("EPO_keyword_matches.txt")
### Output: A list of websites that can be scraped ("websites_to_scrape.txt")
### This program looks at company names attatched to patents with a certain amount of keyword matches. 
### The relevant company names are googled, and then the best link is saved from the google search.

from bs4 import BeautifulSoup
import requests
import time
from googlesearch import search
import random

global points_from_EPO
points_from_EPO = {}
global company_names
company_names = []
global num_matches
num_matches = {}
global company_to_website
company_to_website = {}
global good_links
good_links = []

### Checks to see if the article's keyword matches are above the desired amount. If so, then the company name is googled.
'''
def find_links_to_patents_with_keyword_matches(how_many_keyword_matches_to_qualify, company_names, num_matches, google_pause_length):

	links = []
	for key in num_matches:
		if int(num_matches[key]) >= how_many_keyword_matches_to_qualify:
			company_name = company_names[int(key.strip('.')) - 1]
			if '*' in company_name:
				links.append(['Error: Cannot read company name'])
			else:
				links.append(run_google_search(company_name, google_pause_length))

	return links
'''

def find_links_to_patents_with_keyword_matches(google_pause_length):
	links = []
	for company in points_from_EPO:
		if points_from_EPO[company] == 0:
			pass
		else:
			print('Valid match; searching for link for: ' + company)
			if '*' in company:
				links.append(['Error: Cannot read company name'])
			else:
				run_google_search(company, google_pause_length)


def give_points():
	for key in num_matches:
		company_index = get_company_index(key)
		company = company_names[company_index]
		try:
			points_from_EPO[company] +=1
			points_from_EPO[company] -=1
		except:
			points_from_EPO[company] = 0

		num_matches[key] = int(num_matches[key])
		num_matches[key.replace('secondary', 'primary')] = int(num_matches[key.replace('secondary', 'primary')])


		if '(primary)' in key:
			pass
		elif '(secondary)' in key:
			if num_matches[key] == 0:
				if num_matches[key.replace('secondary', 'primary')] == 0:
					pass
				if num_matches[key.replace('secondary', 'primary')] == 1:
					company_index = get_company_index(key)
					company = company_names[company_index]
					points_from_EPO[company] += 100
				if num_matches[key.replace('secondary', 'primary')] > 1:
					company_index = get_company_index(key)
					company = company_names[company_index]
					points_from_EPO[company] += 175
					print(points_from_EPO[company])
					print('No secondary, 2+ primary')
			elif num_matches[key] == 1:
				if num_matches[key.replace('secondary', 'primary')] == 0:
					pass
				if num_matches[key.replace('secondary', 'primary')] == 1:
					company_index = get_company_index(key)
					company = company_names[company_index]
					points_from_EPO[company] += 150
				if num_matches[key.replace('secondary', 'primary')] > 1:
					company_index = get_company_index(key)
					company = company_names[company_index]
					points_from_EPO[company] += 200
			elif num_matches[key] > 1:
				if num_matches[key.replace('secondary', 'primary')] == 0:
					company_index = get_company_index(key)
					company = company_names[company_index]
					points_from_EPO[company] += 150
				if num_matches[key.replace('secondary', 'primary')] == 1:
					company_index = get_company_index(key)
					company = company_names[company_index]
					points_from_EPO[company] += 200
				if num_matches[key.replace('secondary', 'primary')] > 1:
					company_index = get_company_index(key)
					company = company_names[company_index]
					points_from_EPO[company] += 200


def get_company_index(key):
	company_number = ''
	i = 0
	while key[i] != '.':
		company_number += key[i]
		i += 1
	company_number = int(company_number)
	company_index = company_number - 1
	return company_index

def get_primary_version_of_key(key):
	key.replace('secondary', 'primary')


### Takes files "EPO_company_names.txt" and "EPO_keyword_matches.txt" and saves their contents in a list or dictionary.
def unpack_files():
	file = open('EPO_company_names.txt', 'r')
	for line in file:
		company_names.append(line.strip('\n'))
	file.close()

	file = open('EPO_keyword_matches.txt', 'r')
	for line in file:
		key = ''
		line = line.strip('\n')
		for i in range(len(line)):
			if line[i] != ')':
				key += line[i]
			else:
				key += line[i]
				num_matches[key] = line[i + 2:]
	file.close()

	print(num_matches)

	return company_names, num_matches

### Takes a company name, does a google search, and returns a list of the top 10 search results.
def run_google_search(query, google_pause_length):
	links = ['Google search for "' + query + '" in this sublist.']
	for result in search(query, tld="com", num=10, stop=10, pause=google_pause_length * random_offset(10)):
		links.append(result)

	good_link = get_good_link(links)
	print('Good link: ' + good_link)
	company_to_website[query] = good_link
	good_links.append(good_link)


### Gets a random offset depending on the percentage given. E.g. percentage = 10 will return random number between 0.9 and 1.1.
def random_offset(percentage):
	offset = 0.01 * random.randint(100 - percentage, 100 + percentage)
	return offset

def get_good_link(links):
	good_link = ''
	try:
		if "wiki" in links[1] or "linkedin" in links[1] or "bloomberg" in links[1] or "foursquare" in links[1]:
			if "wiki" in links[2] or "linkedin" in links[2] or "bloomberg" in links[2] or "foursquare" in links[2]:
				good_link = ''
			else:
				print('Website added')
				good_link = links[2]
		else:
			good_link = links[1]
			print('Website added')
	except IndexError:
		good_link = ''

	return good_link
### Sifts through the links generated by the google search and determines if they are worth saving. If the link appears good, it is saved.
def make_file_of_links(links):
	good_links = []
	for i in range(len(links)):
		try:
			if "wiki" in links[i][1] or "linkedin" in links[i][1] or "bloomberg" in links[i][1] or "foursquare" in links[i][1]:
				if "wiki" in links[i][2] or "linkedin" in links[i][2] or "bloomberg" in links[i][2] or "foursquare" in links[i][2]:
					good_links.append('')
				else:
					print('Website added')
					good_links.append(links[i][2])
			else:
				good_links.append(links[i][1])
				print('Website added')
		except IndexError:
			good_links.append('')

	return good_links

### The good links from make_file_of_links() are saved to "websites_to_scrape.txt"
def save_good_links_to_file(good_links):
	file = open('websites_to_scrape.txt', 'w')
	for link in good_links:
		file.write(link + '\n')
	file.close

def save_points():
	file = open('points.txt', 'w')
	for key in company_to_website:
		true_hmpg = true_homepage(company_to_website[key])
		file.write(true_hmpg + ': ' + str(points_from_EPO[key]) + '\n')
	file.close()

def true_homepage(homepage):
	for i in range(len(homepage[9:])):
		if homepage[9 + i] == '/':
			#print('True homepage: ' + homepage[:i + 9])
			return homepage[:i + 9]

	#print('True homepage: ' + homepage)
	return homepage


###Main function. This is where the program starts.
def main(google_pause_length, num_patent_keywords_to_qualify):
	company_names, num_matches = unpack_files()

	give_points()
	find_links_to_patents_with_keyword_matches(google_pause_length)
	print(good_links)

	save_good_links_to_file(good_links)

	time.sleep(0.1)

	print(points_from_EPO)

	save_points()

#main(2, 1)