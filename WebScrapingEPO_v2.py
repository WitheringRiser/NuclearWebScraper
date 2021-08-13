###                          Patent Scraper by Lukas Brazdeikis                      
###                                     Created 29/6/21                                  
###                                  Last modified 5/8/21                              
### The purpose of this program is to scrape patents looking for various primary, secondary, and blacklisted keywords.
### Matches of these keywords are then saved. Also saved patent text that's used in the KeywordDetector.py program
### Inputs: 
###		- _components, num_patents, _interested_patent_components, keywords_file, blacklisted_keywords_file from
###       RunEntireProgram.py
### Outputs:
###		- components, only_matches
###		- keyword_matches_EPO_to_patent_number.txt
###		- patent_text_for_keyword_analysis.txt
###		- EPO_keyword_matches.txt
### Functions:
###		- find_keyword_matches_in_article()								  - save_patent_text_for_keyword_analysis()
###		- search_primary_keyword_matches()	 							  - save_keyword_matches()
###		- search_secondary_keyword_matches()							  - get_keywords()
###		- search_blacklisted_keyword_matches()						      - search_primary_keyword_matches_multiple_keywords()
###		- search_secondary_keyword_matches_multiple_keywords()			  - tally_primary_keyword_match()
###		- tally_secondary_keyword_match()								  - anti_tally_blacklisted_keyword_match()
###		- get_blacklisted_keywords()
###		- find_interested_sections()							 		  - save_keyword_multiple()
###		- main()


from bs4 import BeautifulSoup
import requests
from csv import writer
import time

global only_matches
only_matches = {}


### Input: keywords_file (string), blacklisted_keywords_file (string), num_patents (int)
### Output: num_matches (dict)
def find_keyword_matches_in_article(keywords_file, blacklisted_keywords_file, num_patents):
	global num_matches
	num_matches = {}

	for patent in components:
		num_matches[patent[0][1] + ' (primary)'] = 0
		num_matches[patent[0][1] + ' (secondary)'] = 0

	keywords_primary, keywords_secondary = get_keywords(keywords_file)
	blacklisted_keywords = get_blacklisted_keywords(blacklisted_keywords_file)
	print(keywords_primary)
	print(keywords_secondary)
	
	file = open('keyword_matches_EPO_to_patent_number.txt', 'w')
	file.close()
	
	search_primary_keyword_matches(keywords_primary)					
	search_secondary_keyword_matches(keywords_secondary)
	search_blacklisted_keyword_matches(blacklisted_keywords)

	search_primary_keyword_matches_multiple_keywords(keyword_list_primary_multiples)
	search_secondary_keyword_matches_multiple_keywords(keyword_list_secondary_multiples)

	return num_matches


### Input: keywords_primary (list of strings)
### Output: None. However, the global variables num_matches and only_matches are modified via tally_primary_keyword_matches()
def search_primary_keyword_matches(keywords_primary):
	file = open('keyword_matches_EPO_to_patent_number.txt', 'a')
	for patent in components:
		interested_sections = find_interested_sections(interested_patent_components, patent)
		patent_number = patent[0][1]
		file.write(str(patent_number) + ': ')
		for i in range(len(keywords_primary)):
			keyword = keywords_primary[i]
			for section in interested_sections:
				if keyword in section:
					print(keyword + ' found in ' + patent_number)
					tally_primary_keyword_match(patent_number, file, keyword)
					break ## 11/8
		file.write('\n')
	file.close()


### Input: keywords_secondary (list of strings)
### Output: None. However, the global variables num_matches and only_matches are modified via tally_secondary_keyword_matches()
def search_secondary_keyword_matches(keywords_secondary):
	file = open('keyword_matches_EPO_to_patent_number.txt', 'a')
	for patent in components:
		interested_sections = find_interested_sections(interested_patent_components, patent)
		patent_number = patent[0][1]
		file.write(str(patent_number) + ': ')
		for i in range(len(keywords_secondary)):
			keyword = keywords_secondary[i]
			for section in interested_sections:
				if keyword in section:
					print(keyword + ' found in ' + patent_number)
					tally_secondary_keyword_match(patent_number, file, keyword)
					break ## 11/8
		file.write('\n')
	file.close()


### Input: blacklisted_keywords (list of strings)
### Output: None. However, the global variables num_matches and only_matches are modified via anti_tally_blacklisted_keyword_matches()
def search_blacklisted_keyword_matches(blacklisted_keywords):
	file = open('keyword_matches_EPO_to_patent_number.txt', 'a')
	for patent in components:
		interested_sections = find_interested_sections(interested_patent_components, patent)
		patent_number = patent[0][1]
		file.write(str(patent_number) + ': ')
		for i in range(len(blacklisted_keywords)):
			keyword = blacklisted_keywords[i]
			for section in interested_sections:
				if keyword in section:
					print(keyword + ' found in ' + patent_number + ' (blacklisted keyword)')
					anti_tally_blacklisted_keyword_match(patent_number, file, keyword)
					break ## 11/8
		file.write('\n')
	file.close()



### Input: keywords_multiple (list of lists of strings)
### Output: None. However, the global variables num_matches and only_matches are modified via tally_primary_keyword_matches()
def search_primary_keyword_matches_multiple_keywords(keywords_multiple_primary):
	file = open('keyword_matches_EPO_to_patent_number.txt', 'a')
	for patent in components:
		interested_sections = find_interested_sections(interested_patent_components, patent)
		patent_number = patent[0][1]
		file.write(str(patent_number) + ': ')
		for i in range(len(keywords_multiple_primary)):
			keyword_set = keywords_multiple_primary[i]
			good_keyword_set = True
			for keyword in keyword_set:
				#print('**1' + str(keyword) + str(keyword_set))
				if len(interested_sections) == 0: # if statement fixes an unknown bug
					good_keyword_set = False
					break
				for section in interested_sections:
					#print('2')
					if keyword not in section:
						#print('3')
						good_keyword_set = False
						break ## 11/8
			if good_keyword_set:
				print('Match found for keyword combination in ' + str(patent_number) + ': ' + str(keyword_set))
				tally_primary_keyword_match(patent_number, file, keyword_set)
		file.write('\n')
	file.close()	



### Input: keywords_multiple (list of lists of strings)
### Output: None. However, the global variables num_matches and only_matches are modified via tally_primary_keyword_matches()
def search_secondary_keyword_matches_multiple_keywords(keywords_multiple_secondary):
	file = open('keyword_matches_EPO_to_patent_number.txt', 'a')
	for patent in components:
		interested_sections = find_interested_sections(interested_patent_components, patent)
		patent_number = patent[0][1]
		file.write(str(patent_number) + ': ')
		for i in range(len(keywords_multiple_secondary)):
			keyword_set = keywords_multiple_secondary[i]
			good_keyword_set = True
			for keyword in keyword_set:
				if len(interested_sections) == 0: # if statement fixes an unknown bug
					good_keyword_set = False
					break
				for section in interested_sections:
					if keyword not in section:
						good_keyword_set = False
						break ## 11/8
			if good_keyword_set:
				print('Match found for keyword combination in ' + str(patent_number) + ': ' + str(keyword_set))
				tally_secondary_keyword_match(patent_number, file, keyword_set)
		file.write('\n')
	file.close()	


### Input: patent_numer(int), file(a file object)
### Output: None. However, global variables only_matches and num_matches are modified
def tally_primary_keyword_match(patent_number, file, keyword):
	num_matches[patent_number  + ' (primary)'] = num_matches[patent_number  + ' (primary)'] + 1
	if type(keyword) == list:
		string_of_keywords = ''
		for inner_keyword in keyword:
			string_of_keywords += inner_keyword + '+'
		string_of_keywords = ',' + string_of_keywords[:-1] + ' (primary)'
		file.write(string_of_keywords)
	else:
		file.write(',' + str(keyword) + ' (primary)')
	try:
		only_matches[patent_number  + ' (primary)'] == None #Checks if this dictionary key exists
		only_matches[patent_number  + ' (primary)'] = only_matches[patent_number  + ' (primary)'] + 1
		try:
			only_matches[patent_number  + ' (secondary)'] == None
			only_matches[patent_number  + ' (secondary)'] = only_matches[patent_number  + ' (secondary)'] + 0
		except KeyError:
			only_matches[patent_number  + ' (secondary)'] = 0
	except KeyError:
		only_matches[patent_number  + ' (primary)'] = 1
		try:
			only_matches[patent_number  + ' (secondary)'] == None
			only_matches[patent_number  + ' (secondary)'] = only_matches[patent_number  + ' (secondary)'] + 0
		except KeyError:
			only_matches[patent_number  + ' (secondary)'] = 0


### Input: patent_numer(int), file(a file object)
### Output: None. However, global variables only_matches and num_matches are modified
def tally_secondary_keyword_match(patent_number, file, keyword):
	num_matches[patent_number  + ' (secondary)'] = num_matches[patent_number  + ' (secondary)'] + 1
	if type(keyword) == list:
		string_of_keywords = ''
		for inner_keyword in keyword:
			string_of_keywords += inner_keyword + '+'
		string_of_keywords = ',' + string_of_keywords[:-1] + ' (secondary)'
		file.write(string_of_keywords)
	else:
		file.write(',' + str(keyword) + ' (secondary)')
	try:
		only_matches[patent_number  + ' (primary)'] == None
		only_matches[patent_number  + ' (primary)'] = only_matches[patent_number  + ' (primary)'] + 0
		try:
			only_matches[patent_number  + ' (secondary)'] == None
			only_matches[patent_number  + ' (secondary)'] = only_matches[patent_number  + ' (secondary)'] + 1
		except KeyError:
			only_matches[patent_number  + ' (secondary)'] = 1
	except KeyError:
		only_matches[patent_number  + ' (primary)'] = 0
		try:
			only_matches[patent_number  + ' (secondary)'] == None
			only_matches[patent_number  + ' (secondary)'] = only_matches[patent_number  + ' (secondary)'] + 1
		except KeyError:
			only_matches[patent_number  + ' (secondary)'] = 1


### Input: patent_numer(int), file(a file object)
### Output: None. However, global variables only_matches and num_matches are modified
def anti_tally_blacklisted_keyword_match(patent_number, file, keyword):
	num_matches[patent_number  + ' (secondary)'] = num_matches[patent_number  + ' (secondary)'] - 1
	file.write(',' + str(keyword) + ' (blacklisted)')
	try:
		only_matches[patent_number  + ' (primary)'] == None
		only_matches[patent_number  + ' (primary)'] = only_matches[patent_number  + ' (primary)'] + 0
		try:
			only_matches[patent_number  + ' (secondary)'] == None
			only_matches[patent_number  + ' (secondary)'] = only_matches[patent_number  + ' (secondary)'] - 1
		except KeyError:
			only_matches[patent_number  + ' (secondary)'] = -1
	except KeyError:
		only_matches[patent_number  + ' (primary)'] = 0
		try:
			only_matches[patent_number  + ' (secondary)'] == None
			only_matches[patent_number  + ' (secondary)'] = only_matches[patent_number  + ' (secondary)'] - 1
		except KeyError:
			only_matches[patent_number  + ' (secondary)'] = -1
							

### Input: interested_patent_components (list of strings), patent (list)
### Output: interested_sections (list of strings)
def find_interested_sections(interested_patent_components, patent):
	interested_sections = []
	for line in patent:
		if line[5] in interested_patent_components:
			interested_sections.append(line[7].lower())
	return interested_sections


### Input: num_patents (int), interested_patent_components (list of strings)
### Output: None. However, patent_text_for... is written to.
def save_patent_text_for_keyword_analysis(num_patents, interested_patent_components):
	file = open('patent_text_for_keyword_analysis.txt', 'w')
	for i in range(num_patents):
		patent = components[i]
		interested_sections = find_interested_sections(interested_patent_components, patent)
		for section in interested_sections:
			section = section.lower()
			if ' the ' in section or ' to ' in section or ' of ' in section: ### Checking roughly if patent is in english
				file.write(section)
	file.close()


### Input: num_matches (dict)
### Output: None. However, EPO_keyword_matches.txt is written to
def save_keyword_matches(num_matches):
	file = open('EPO_keyword_matches.txt', 'w')
	for key in num_matches:
		file.write(str(key) + ' ' + str(num_matches[key]) + '\n')
	file.close()


### Input: keywords_file (string)
### Output: keywords_primary (list of strings), keywords_secondary (list of strings)
def get_keywords(keywords_file):
	global keyword_list_primary_multiples
	keyword_list_primary_multiples = []
	global keyword_list_secondary_multiples
	keyword_list_secondary_multiples = []

	with open(keywords_file, 'r') as file:
		keywords_primary = []
		keywords_secondary = []
		for line in file: ### Strips and sorts keywords into appropriate formats and categories
			if '+' in line:
				save_keyword_multiple(line)
				continue
			if line[-2:] == '1\n':
				keywords_primary.append(line.strip('1\n').lower())
			elif line[-2:] == '2\n':
				keywords_secondary.append(line.strip('2\n').lower())
			elif line[-1] == '1':
				keywords_primary.append(line.strip('1').lower())
			elif line[-1] == '2':
				keywords_secondary.append(line.strip('2').lower())
			else:
				print('ERROR: Cannot read entry for: ' + line)
	print('Primary multiple keywords pairs: ', end = '')
	print(keyword_list_primary_multiples)
	print('Secondary multiple keywords pairs: ', end = '')
	print(keyword_list_secondary_multiples)
	return keywords_primary, keywords_secondary


### Input: blacklisted_keywords_file (string)
### Output: keywords_blacklisted (list of strings)
def get_blacklisted_keywords(blacklisted_keywords_file):
	with open(blacklisted_keywords_file, 'r') as file:
		keywords_blacklisted = []
		for line in file:
			keywords_blacklisted.append(line.strip('\n'))
	return keywords_blacklisted


### Input: line (a string)
### Output: None. However, global vars keyword_list_primary_multiples and keyword_list_secondary_multiples are modified
def save_keyword_multiple(line):
	if line[-2:] == '1\n':
		line = line.strip('1\n').lower()
		items = line.split('+')
		keyword_list_primary_multiples.append(items)
	elif line[-2:] == '2\n':
		line = line.strip('2\n').lower()
		items = line.split('+')
		keyword_list_secondary_multiples.append(items)
	elif line[-1] == '1':
		line = line.strip('1').lower()
		items = line.split('+')
		keyword_list_primary_multiples.append(items)
	elif line[-1] == '2':
		line = line.strip('2').lower()
		items = line.split('+')
		keyword_list_secondary_multiples.append(items)
	else:
		print('ERROR: Cannot read entry for: ' + line)


### Input: _components (multidimensional list), num_patents (int), _interested_patent_components (list of strings),
### keywords_file (string), blacklisted_keywords_file (string)
### Output: components (multidimensional list, only_matches (dict)
def main(_components, num_patents, _interested_patent_components, keywords_file, blacklisted_keywords_file, num_patents_to_save = 1000):

	num_websites_checked = [0]

	global components
	components = _components
	global interested_patent_components
	interested_patent_components = _interested_patent_components

	save_patent_text_for_keyword_analysis(num_patents_to_save, interested_patent_components)

	num_matches = find_keyword_matches_in_article(keywords_file, blacklisted_keywords_file, num_patents)

	print(only_matches)

	time.sleep(1)

	return components, only_matches