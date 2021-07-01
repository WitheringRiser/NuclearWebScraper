###                    Web Scraper Program for EPO by Lukas Brazdeikis                  ###
###                                     Created 29/6/21                                 ###
###                                  Last modified 29/6/21                              ###

from bs4 import BeautifulSoup
import requests
from csv import writer
import time
'''
html_doc = """<html><head><title>The Dormouse's story</title></head>
<body>
<p class="title"><b>The Dormouse's story</b></p>

<p class="story">Once upon a time there were three little sisters; and their names were
<a href="http://example.com/elsie" class="sister" id="link1">Elsie</a>,
<a href="http://example.com/lacie" class="sister" id="link2">Lacie</a> and
<a href="http://example.com/tillie" class="sister" id="link3">Tillie</a>;
and they lived at the bottom of a well.</p>

<p class="story">...</p>
"""
soup = BeautifulSoup(html_doc, 'html.parser')
html_contents = soup.contents
print(html_contents)
'''

###Get html contents of a given website###
def find_keyword_matches_on_website(homepage, site, do_you_want_to_know_indices_where_product_pages_can_be, num_websites_checked):
	try:
		response = requests.get(site)
	except requests.exceptions.MissingSchema:
		response = requests.get(homepage + site)
	soup = BeautifulSoup(response.text, 'html.parser')

	html_contents = soup.body.contents

	all_text = []

	html_contents_length = len(html_contents)
	#print(html_contents_length)

	###Add the text of html contents to the list all_text###
	html_contents_indices_where_products_pages_can_be = []


	for i in range(html_contents_length):

	#How to tell if html content is a comment: str(type(html_contents[i])) == "<class 'bs4.element.Comment'>"

		if html_contents[i] != '\n' and not (str(type(html_contents[i])) == "<class 'bs4.element.Comment'>"):
			'''
			print('The line that has a problem: ' + html_contents[i] + ' end of line \n')
			print('Type: ' + str(type(html_contents[i])) + '\n')
			print('Is comment: ' + str(str(type(html_contents[i])) == "<class 'bs4.element.Comment'>") + '\n')
			'''
			line_to_add = ['Filler1', '']
			line_to_add[0] = html_contents[i].get_text()
			if do_you_want_to_know_indices_where_product_pages_can_be:
				if 'Products' in line_to_add[0]:
					#print('Product section found at html section number ' + str(i))
					#print(html_contents[i])
					html_contents_indices_where_products_pages_can_be.append(i)
			all_text.append(line_to_add)
			num_sections_of_website = len(all_text)
	
	
	###Write website text to a csv file###
	with open('website_lines.csv', 'w') as csv_file:
		
		csv_writer = writer(csv_file, delimiter = ' ')
		header = ['Lines on website', '']
		csv_writer.writerow(header)
		for i in range(num_sections_of_website):
			try:
				csv_writer.writerow(all_text[i])
			except UnicodeEncodeError as bad_char:
				print('***Error: unidentifiable character. 1/' + str(num_sections_of_website) + 'th of the page cannot be read \n')
	
	'''
	with open('website_lines.txt', 'w') as file:
		for i in range(len(all_text)):
			file.write(str(all_text[i]))
	'''

	###Copy csv file to a txt file###
	num_lines_of_website = 0

	
	with open('website_lines.txt', 'w') as file:
		with open('website_lines.csv', 'r') as csv_file:
			for line in csv_file:
				num_lines_of_website += 1
				file.write(line)


	###Checks is a keyword from keywords.txt is found on the website###
	with open('keywords.txt') as keywords:
		list_of_keywords = []
		for line in keywords:
			list_of_keywords.append(line.strip('\n'))
			list_of_keywords.append(line.lower().strip('\n'))

	
	with open('website_lines.txt', 'r') as website_lines:
		current_line = 0
		for line in website_lines:
			current_line += 1
			if current_line == 1:
				continue
			for keyword in list_of_keywords:
				if keyword in line:
					print('Match found for "' + keyword + '": "' + line.strip('\n'))
					print('At website line ' + str(current_line) + ' out of ' + str(num_lines_of_website) + ' lines\n')
	
	num_websites_checked[0] += 1
	return html_contents_indices_where_products_pages_can_be, html_contents

def get_product_links(html_contents_indices_where_products_pages_can_be, html_contents):
	###Searching for the product page(s)###
	
	list_of_product_links = []
	for i in html_contents_indices_where_products_pages_can_be:
		all_a_html = html_contents[i].find_all('a')
		for a in all_a_html:
			link = a.get('href')
			if 'product' in link:
				list_of_product_links.append(link)
	return list_of_product_links
	
###Get a list of links to search through.
###Thoroughness refers to how many of the links you want to conduct searches for. 1 means every link, 3 means every 3rd link, etc.
def search_through_multiple_links_to_find_keyword_matches(homepage, list_of_product_links, thoroughness, num_websites_checked):
	results = []
	for i in range(len(list_of_product_links)):
		if i % thoroughness == 0:
			html_contents_indices_where_products_pages_can_be, html_contents = find_keyword_matches_on_website(homepage, list_of_product_links[i], False, num_websites_checked)

def write_product_links(list_of_product_links):
	with open('list_of_product_links.txt', 'w') as file:
		for link in list_of_product_links:
			file.write(link + '\n')

###Pass in the html text you're looking for along with the html_contents with the index you know the text can be found.
def find_html_content_of_a_given_html_text(parent_html_text, html_contents, indices_where_text_can_be_found):
	'''
	for i in range(len(html_contents)):
		if html_contents[i].get_text().lower() == parent_html_text:
			return html_contents[i]
		else:
			return find_sub_links(parent_html_text_lower, html_contents.contents[i])
	'''
	list_of_sublinks = []

	for i in indices_where_text_can_be_found:
		relevant_html_contents = html_contents[i]
		for child in relevant_html_contents.descendants:
			if child.string == parent_html_text or child.string == parent_html_text.lower():
				list_of_sublinks.append(find_sublinks(child))

	return list_of_sublinks

#Get a list of links underneat the menu item given by html_contents.
def find_sublinks(html_contents):
	try:
		new_parent = html_contents.find_next_sibling()
	except TypeError:
		return

	if new_parent == None:
		return

	list_of_sublinks = []
	#for i in range(len(new_parent)):
	all_a_html = new_parent.find_all('a')
	for a in all_a_html:
		link = a.get('href')
		list_of_sublinks.append(link)

	return list_of_sublinks


def refine_list(list_of_sublinks):
	new_list_of_sublinks = []
	for i in range(len(list_of_sublinks)):
		try:
			sub_section_length = len(list_of_sublinks[i])
		except TypeError:
			sub_section_length = 0
		for j in range(sub_section_length):
			new_list_of_sublinks.append(list_of_sublinks[i][j])
	return new_list_of_sublinks

def get_patent_entries(site):
	response = requests.get(site)
	soup = BeautifulSoup(response.text, 'html.parser')
	html_contents = soup.body.contents

	#print(html_contents)
	#entries = soup.find(class__='publications-list--mYtsKGTt')
	#print(entries)

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
		#print(current_line_num)
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


def find_keyword_matches_in_article(keywords_file, sorted_article_list):
	articles = sorted_article_list[4]

	numbers = sorted_article_list[0]
	num_matches = {}
	for i in range(len(numbers)):
		num_matches[numbers[i]] = 0

	with open(keywords_file, 'r') as file:
		keywords = []
		for line in file:
			keywords.append(line.strip('\n'))
			keywords.append(line.strip('\n').lower())


	for i in range(len(articles)):
		article_number = numbers[i]
		article = articles[i]
		for j in range(len(keywords)):
			keyword = keywords[j]
			if keyword in article:
				num_matches[article_number] = num_matches[article_number] + article.count(keyword)

	return num_matches


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

def save_company_names(company_names):
	file = open('EPO_company_names.txt', 'w')
	for company in company_names:
		file.write(company + '\n')

	file.close()

def save_keyword_matches(num_matches):
	file = open('EPO_keyword_matches.txt', 'w')
	for key in num_matches:
		file.write(str(key) + ' ' + str(num_matches[key]) + '\n')
	file.close()


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




main()