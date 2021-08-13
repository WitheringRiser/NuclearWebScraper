###                        Results File Creator by Lukas Brazdeikis                      
###                                     Created July 2021                                  
###                                  Last modified 5/8/21                              
### The purpose of this program is gather all scores, metrics, and relevant data and put the data onto a csv file.
### Inputs: 
###		- patent_number_to_company.txt
###		- keyword_matches_EPO_to_patent_number.txt
### 	- keyword_matches_from_website_to_website.txt
###		- patent_number_to_website.txt
###		- tab_matches_to_website.txt
###		- points_from_EPO_per_website.txt
###		- points_from_website.txt
### Outputs:
###		- Results.csv
### Functions:
###		- save_output()								  		- read_keyword_matches_EPO_to_patent_number()
###		- true_homepage()	  								- read_keyword_matches_from_website_to_website()
###		- write_header()								    - read_patent_number_to_website()
###		- get_specific_keyword_types_from_patent_number()	- read_tab_matches_to_website()
###		- get_company_name()							    - get_EPO_scores()
###		- has_specific_keyword()							- get_points_from_website()
###		- save_website_text()								- return_keyword_matches_from_website_to_website()
###		- find_keyword_matches_on_website()					- return_tab_matches_to_website()
###		- combine_EPO_scores_and_website_scores()
###		- read_patent_number_to_company_name()


from csv import writer


### Input: None
### Output: None. However, Results.csv is appended to
def save_output():
	csv_file = open('Results.csv', 'a')
	csv_writer = writer(csv_file, delimiter = ';')
	for website in combined_points:
		csv_writer.writerow([\
			get_company_name(website),\
			website,\
			combined_points[website],\
			get_specific_keyword_types_from_patent_number(website, 'primary'),\
			get_specific_keyword_types_from_patent_number(website, 'secondary'),\
			has_specific_keyword(website, 'Nuclear'),\
			has_specific_keyword(website, 'Oil and Gas'),\
			return_keyword_matches_from_website_to_website(website),\
			return_tab_matches_to_website(website),\
			'EP' + str(website_to_patent_number[website])
		 ])
		print(website_to_patent_number[website])
	csv_file.close()


### Input: homepage (string)
### Output: homepage (string)
###		- Note that the output is the same as the input, however, all sublinks attatched have been stripped.
###		- ex: https://www.netalux.com/products becomes https://www.netalux.com
def true_homepage(homepage):
	for i in range(len(homepage[9:])):
		if homepage[9 + i] == '/':
			#print('True homepage: ' + homepage[:i + 9])
			return homepage[:i + 9]

	#print('True homepage: ' + homepage)
	return homepage


### Input: None
### Output: None. However, Results.csv is written to
def write_header():
	csv_file = open('Results.csv', 'w')
	csv_writer = writer(csv_file, delimiter = ';')
	header = ['Company', 'Website', 'Score', 'Primary Keyword Matches from EPO', 'Secondary Keyword Matches from EPO',\
	'Nuclear mentioned on website', 'Oil and Gas mentioned on website', 'Keyword Matches from Website',\
	 'Tab Matches from Website', 'Patent #']
	csv_writer.writerow(header)
	csv_file.close()


### Input: website (string), keyword_type (string)
### Output keywords(list of strings)
def get_specific_keyword_types_from_patent_number(website, keyword_type):
	patent_number = website_to_patent_number[website]
	all_keywords = keyword_matches_EPO_to_patent_number[patent_number]
	keywords = []
	for keyword in all_keywords:
		if keyword_type in keyword:
			keywords.append(keyword)
	return keywords


### Input: website (string)
### Output: company_name (string)
def get_company_name(website):
	patent_number = int(website_to_patent_number[website])
	company_name = patent_number_to_company_name[patent_number]
	return company_name


### Input: website (string), keyword (string)
### Output: string
###		- string output is 'Y' if keyword exists and '' (blank) otherwise
def has_specific_keyword(website, keyword):
	try:
		all_keywords = keyword_matches_from_website_to_website[website]
	except KeyError:
		return ''
	keyword_segments = keyword.split(' ') # Splits a multi-word keyword into a list of single words
	if len(keyword_segments) == 1: # If the keyword was just a single word keyword
		if keyword in all_keywords or keyword.lower() in all_keywords:
			return 'Y'
		else:
			return ''
	else:
		for i in range(len(keyword_segments)): # Checks if each word of a multi-word keyword can be found in all_keywords
			if keyword_segments[i] not in all_keywords and keyword_segments[i].lower() not in all_keywords:
				return ''
		return 'Y'
	return 'Error: function "has_specific_keywords()" ran into an error'


### Input: None
### Output: None. However, global variable combined_points is modified
def combine_EPO_scores_and_website_scores():
	global combined_points
	combined_points = {}
	for website in EPO_points:
		if website == '':
			continue
		else:
			try:
				combined_points[website] = EPO_points[website] + points_from_website[website]
			except KeyError:
				continue


### Input: None
### Output: None. However, global variable patent_number_to_company_name is modified
def read_patent_number_to_company_name():
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
### Output: None. However, global variable keyword_matches_EPO_to_patent_number is modified
def read_keyword_matches_EPO_to_patent_number():
	global keyword_matches_EPO_to_patent_number
	keyword_matches_EPO_to_patent_number = {}
	file = open('keyword_matches_EPO_to_patent_number.txt', 'r')
	for line in file:
		patent_number = ''
		for ch in line:
			if ch == ':':
				end_of_p_number_index = line.find(ch) - 1
				break
			patent_number += ch

		keywords = line[end_of_p_number_index + 4:]
		keywords = keywords.split(',')
		keywords[-1] = keywords[-1].strip('\n')
		try:
			keyword_matches_EPO_to_patent_number[patent_number] = keyword_matches_EPO_to_patent_number[patent_number] + keywords
		except:
			keyword_matches_EPO_to_patent_number[patent_number] = keywords
	file.close()


### Input: None
### Output: None. However, global variable keyword_matches_from_website_to_website is modified
def read_keyword_matches_from_website_to_website():
	global keyword_matches_from_website_to_website
	keyword_matches_from_website_to_website = {}
	file = open('keyword_matches_from_website_to_website.txt', 'r')
	for line in file:
		line = line.split(' ')
		website = line[0].strip('\n')
		website_keywords = []
		for i in range(len(line)):
			if i == 0:
				continue
			keyword = line[i]
			website_keywords.append(keyword.strip('\n'))
		website = true_homepage(website)
		keyword_matches_from_website_to_website[website] = website_keywords

	print(keyword_matches_from_website_to_website)

	file.close()


### Input: None
### Output: None. However, global variable website_to_patent_number is modified
def read_patent_number_to_website():
	global website_to_patent_number
	website_to_patent_number = {}
	file = open('patent_number_to_website.txt', 'r')
	for line in file:
		line = line.split(': ')
		patent_number = line[0].strip('\n')
		website = line[1].strip('\n')
		website = true_homepage(website)
		website_to_patent_number[website] = patent_number

	print(website_to_patent_number)

	file.close()


### Input: None
### Output: None. However, global variable tab_matches_to_website is modified
def read_tab_matches_to_website():
	global tab_matches_to_website
	tab_matches_to_website = {}
	file = open('tab_matches_to_website.txt', 'r')
	for line in file:
		line = line.split(' ')
		website = line[0].strip('\n')
		website_tabs = []
		for i in range(len(line)):
			if i == 0:
				continue
			tab = line[i]
			website_tabs.append(tab.strip('\n'))
		website = true_homepage(website)
		tab_matches_to_website[website] = website_tabs

	file.close()


### Input: None
### Output: None. However, global variable EPO_points is modified
def get_EPO_scores():
	global EPO_points
	EPO_points = {}

	file = open('points_from_EPO_per_website.txt', 'r')
	for line in file:
		line = line.strip('\n')
		split_line = line.split(' ')
		split_line[0] = split_line[0][:-1]
		EPO_points[split_line[0]] = int(split_line[1])


### Input: None
### Output: None. However, global variable points_from_website is modified
def get_points_from_website():
	global points_from_website
	points_from_website = {}

	file = open('points_from_website.txt', 'r')
	for line in file:
		line.strip('\n')
		line_components = line.split(' ')
		points_from_website[line_components[0]] = int(line_components[1])
	file.close


### Input: website (string)
### Output: value in dictionary keyword_matches_from_website_to_website corresponding to the variable website
def return_keyword_matches_from_website_to_website(website):
	try: 
		keyword_matches_from_website_to_website[website]
	except KeyError:
		return None
	return keyword_matches_from_website_to_website[website]


### Input: website (string)
### Output: value in dictionary tab_matches_to_website corresponding to the variable website
def return_tab_matches_to_website(website):
	try: 
		tab_matches_to_website[website]
	except KeyError:
		return None
	return tab_matches_to_website[website]


### Input: None
### Output: None
def main():
	get_points_from_website()
	read_patent_number_to_company_name()

	write_header()
	get_EPO_scores()
	combine_EPO_scores_and_website_scores()

	read_keyword_matches_EPO_to_patent_number()
	read_keyword_matches_from_website_to_website()
	read_patent_number_to_website()
	read_tab_matches_to_website()

	save_output()


#main()