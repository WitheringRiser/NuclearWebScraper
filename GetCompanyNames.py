###                      Company Name Finding Program by Lukas Brazdeikis                      
###                                    Created July 2021                                 
###                                  Last modified 5/8/21                              
### The purpose of this program is to use the web to search and save company names attatched to patent numbers.
### Inputs: 
###		- google_pause_length from RunEntireProgram.py
###		- points_from_EPO.txt
### Outputs:
###		- patent_number_to_company.txt
###		- points_from_EPO_per_company.txt
### Functions:
###		- find_companies_to_patents_with_keyword_matches()				- points_per_company()
###		- run_patent_searches()											- get_points_from_EPO()
###		- save_patent_number_to_company_name()							- save_points_per_company()


from google_patent_scraper import scraper_class
from google_patent_scraper.errors import NoPatentsError
import json
import time
import os


### Input: None
### Output: None. However, global variables scraper (a Scraper object) and patent_numbers (a list of strings) are modified.
def find_companies_to_patents_with_keyword_matches():
	global scraper
	scraper = scraper_class()
	global patent_numbers
	patent_numbers = []

	company_names = []
	for patent_number in points_from_EPO:
		if points_from_EPO[patent_number] == 0:
			pass
		else:
			print('Valid match; searching for company for patent: EP' + str(patent_number))
			if '*' in str(patent_number):
				links.append(['Error: Cannot read patent number'])
			else:
				scraper.add_patents('EP' + str(patent_number))
				patent_numbers.append(str(patent_number))


### Input: google_pause_length (int)
### Output: None. However, global variables company_names (list) and patent_number... (dict) are modified.
def run_patent_searches(google_pause_length):
	global company_names
	company_names = []
	global patent_number_to_company_name
	patent_number_to_company_name = {}

	time.sleep(google_pause_length)

	try:
		scraper.scrape_all_patents()
	except NoPatentsError:
		print('*******************')
		print(' No patents found')
		print('Program terminated.')
		print('*******************')
		os._exit()

	for patent_number in patent_numbers: ## Extracts company name from patent search data
		patent_info = scraper.parsed_patents['EP' + patent_number]
		assignees = json.loads(patent_info['assignee_name_orig'])
		primary_assignee = assignees[0]['assignee_name']
		company_names.append(primary_assignee)
		patent_number_to_company_name[patent_number] = primary_assignee

	print(company_names)


### Input: None.
### Output: None. However, file patent_number_to_company.txt is written to
def save_patent_number_to_company_name():
	file = open('patent_number_to_company.txt', 'w')
	for patent_number in patent_number_to_company_name:
		file.write(str(patent_number) + ': ' + patent_number_to_company_name[patent_number] + '\n')
	file.close()


### Input: None.
### Output: pnts_per_company (dict)
def points_per_company():
	global pnts_per_company
	pnts_per_company = {}
	for patent_number in patent_number_to_company_name:
		points = points_from_EPO[int(patent_number)]
		company = patent_number_to_company_name[patent_number]
		pnts_per_company[company] = points

	return pnts_per_company


### Input: None
### Output: None. However, global variable points_from_EPO is modified
def get_points_from_EPO():
	global points_from_EPO
	points_from_EPO = {}

	file = open('points_from_EPO.txt', 'r')
	for line in file:
		line.strip('\n')
		line_components = line.split(' ')
		points_from_EPO[int(line_components[0])] = int(line_components[1])
	file.close


### Input: None
### Output: None. However, file points_from_EPO... is written to
def save_points_per_company():
	file = open('points_from_EPO_per_company.txt', 'w')
	for company in pnts_per_company:
		file.write(str(company) + ' ' + str(pnts_per_company[company]) + '\n')
	file.close


### Input: google_pause_length (int)
### Output: None
def main(google_pause_length):
	get_points_from_EPO()

	find_companies_to_patents_with_keyword_matches()
	run_patent_searches(google_pause_length)
	pnts_per_company = points_per_company()

	save_patent_number_to_company_name()
	save_points_per_company()


#main()