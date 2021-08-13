###                    Patent information analyzer by Lukas Brazdeikis                  
###                                     Created 29/6/21                                 
###                                   Last modified 6/7/21                              
### Input: Patent information from EPO ("Articles.txt"), keywords to look for in patents ("EPO_keywords.txt").
### Output: Company names of all patents ("EPO_company_names.txt") and keyword matches ("EPO_keyword_matches.txt").
### This program takes the patent information gathered by "GenerateArticleListFromEPO.py" and divides up the components.
### The company names are saved, and the patent description is searched for keywords.

from bs4 import BeautifulSoup
import requests
from csv import writer
import time

### Gets the html contents of the EPO website
def get_patent_entries(site):
	response = requests.get(site)
	soup = BeautifulSoup(response.text, 'html.parser')
	html_contents = soup.body.contents

### Sorts the patent information into it's different components like description, company name, etc.
def sort_article_components(articles_file):
	articles_file = open(articles_file, 'r')

	article_numbers = []
	article_titles = []
	patent_numbers_dates_companies_and_countries = []
	misc_dates = []
	patent_summaries = []
	scope_of_articles = []

	current_line_num = -1
	contents = articles_file.readlines()
	for i in range(len(contents)):
		current_line_num += 1
		contents[i] = contents[i].strip('\n')
		try:
			number = int(contents[i][0:-1])
			if contents[i][-1] == '.':
				sorted_article_list = divide_up_article_components(current_line_num, contents,\
					article_numbers, article_titles, patent_numbers_dates_companies_and_countries,\
					misc_dates, patent_summaries)

				for j in range(4):
					i += 1
		except ValueError:
			pass

	articles_file.close()

	return sorted_article_list

### Helped function for sort_article_components()
def divide_up_article_components(current_line_num, contents, article_numbers, article_titles,\
	patent_numbers_dates_companies_and_countries, misc_dates, patent_summaries):
	article_numbers.append(contents[current_line_num])
	article_titles.append(contents[current_line_num + 1].strip('\n'))
	patent_numbers_dates_companies_and_countries.append(contents[current_line_num + 2].strip('\n'))
	misc_dates.append(contents[current_line_num + 3].strip('\n'))
	patent_summaries.append(contents[current_line_num + 4].strip('\n'))

	sorted_article_list = []
	sorted_article_list.append(article_numbers)
	sorted_article_list.append(article_titles)
	sorted_article_list.append(patent_numbers_dates_companies_and_countries)
	sorted_article_list.append(misc_dates)
	sorted_article_list.append(patent_summaries)

	return sorted_article_list

	return article_numbers, article_titles, patent_numbers_dates_companies_and_countries,\
	misc_dates, patent_summaries

### Searches for keyword matches in the article description
def find_keyword_matches_in_article(keywords_file, sorted_article_list):
	articles = sorted_article_list[4]

	numbers = sorted_article_list[0]
	num_matches = {}
	for i in range(len(numbers)):
		for j in range(2):
			if j == 0:
				num_matches[numbers[i] + ' (primary)'] = 0
				num_matches[numbers[i] + ' (secondary)'] = 0

	keywords_primary, keywords_secondary = get_keywords(keywords_file)


	for i in range(len(articles)):
		article_number = numbers[i]
		article = articles[i]
		for j in range(len(keywords_primary)):
			keyword = keywords_primary[j]
			if keyword in article:
				print(keyword + ' found in ' + article_number)
				num_matches[article_number  + ' (primary)'] = num_matches[article_number  + ' (primary)'] + article.count(keyword)

	for i in range(len(articles)):
		article_number = numbers[i]
		article = articles[i]
		for j in range(len(keywords_secondary)):
			keyword = keywords_secondary[j]
			if keyword in article:
				print(keyword + ' found in ' + article_number)
				num_matches[article_number  + ' (secondary)'] = num_matches[article_number  + ' (secondary)'] + article.count(keyword)

	return num_matches

### Extracts the company name from the patent information
def get_company_names(sorted_article_list):
	patent_numbers_dates_companies_and_countries = sorted_article_list[2]
	company_names = []
	for item in patent_numbers_dates_companies_and_countries:
		start_index_of_company_name = item.rfind('•') + 2
		company_name_and_country = item[start_index_of_company_name:].strip('\n')
		country_not_reached = True
		company_name = ''
		for i in range(len(company_name_and_country)):
			if company_name_and_country[i] == '[':
				if company_name_and_country[i + 3] == ']':
					break
			else:
				company_name += company_name_and_country[i]
		if company_name[-1] == ' ':
			company_name = company_name[:-1]
		company_names.append(company_name)			

	
	return company_names

### Saves the company names to the file "EPO_company_names.txt"
def save_company_names(company_names):
	file = open('EPO_company_names.txt', 'w')
	for company in company_names:
		file.write(company + '\n')

	file.close()

### Saves the number of keyword matches found in the article to the file "EPO_keyword_matches.txt"
def save_keyword_matches(num_matches):
	file = open('EPO_keyword_matches.txt', 'w')
	for key in num_matches:
		file.write(str(key) + ' ' + str(num_matches[key]) + '\n')
	file.close()

### Extracts primary and secondary keywords from "EPO_keywords.txt" and returns two lists
def get_keywords(keywords_file):
	with open(keywords_file, 'r') as file:
		keywords_primary = []
		keywords_secondary = []
		for line in file:
			if line[-2:] == '1\n':
				keywords_primary.append(line.strip('1\n'))
				keywords_primary.append(line.strip('1\n').lower())
			elif line[-2:] == '2\n':
				keywords_secondary.append(line.strip('2\n'))
				keywords_secondary.append(line.strip('2\n').lower())
			elif line[-1] == '1':
				keywords_primary.append(line.strip('1'))
				keywords_primary.append(line.strip('1').lower())
			elif line[-1] == '2':
				keywords_secondary.append(line.strip('2'))
				keywords_secondary.append(line.strip('2').lower())
			else:
				print('ERROR: Cannot read entry for: ' + line)
	return keywords_primary, keywords_secondary


###Main function. This is where the program starts.
def main():
	num_websites_checked = [0]
	articles_file = 'Articles.txt'

	sorted_article_list = sort_article_components(articles_file)

	num_matches = find_keyword_matches_in_article('EPO_keywords.txt', sorted_article_list)
	print(num_matches)

	company_names = get_company_names(sorted_article_list)
	print('Company names:')
	print(company_names)

	save_company_names(company_names)

	save_keyword_matches(num_matches)

	time.sleep(1)




#main()