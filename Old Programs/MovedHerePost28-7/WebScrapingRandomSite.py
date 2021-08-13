###                        Web Scraper Program by Lukas Brazdeikis                      ###
###                                     Created 25/6/21                                 ###
###                                  Last modified 1/7/21                               ###
### This program takes a website as input and ouputs true/false based on the following: ###
###                        1. The website has a products page AND                       ###
###  2. The website has a certain keyword mentioned on the homepage and/or product page ###

from bs4 import BeautifulSoup
import requests
from csv import writer
import time
import os.path

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
def find_keyword_matches_on_website(homepage, site, do_you_want_to_know_indices_where_product_pages_can_be, num_websites_checked): ## ##
	try:
		response = requests.get(site)
	except requests.exceptions.MissingSchema:
		response = requests.get(homepage + site)
	soup = BeautifulSoup(response.text, 'html.parser')

	print(homepage)
	print(type(soup.body))
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
			#print(html_contents[i])
			try:
				line_to_add[0] = html_contents[i].get_text()
			except AttributeError:
				line_to_add[0] = ''
			if do_you_want_to_know_indices_where_product_pages_can_be:
				if 'Products' in line_to_add[0] or 'products' in line_to_add[0]:
					print('***Found***')
					#print('Product section found at html section number ' + str(i))
					#print(html_contents[i])
					html_contents_indices_where_products_pages_can_be.append(i)
			all_text.append(line_to_add)
			num_sections_of_website = len(all_text)
	
	
	###Write website text to a txt file###
	file = open('website_lines.txt', 'w')
	'''
	csv_writer = writer(csv_file, delimiter = ' ')
	header = ['Lines on website', '']
	csv_writer.writerow(header)
	'''
	for i in range(num_sections_of_website):
		try:
			for j in range(len(all_text[i])):
				file.write(str(all_text[i][j]))
		except UnicodeEncodeError as bad_char:
			#print('***Error: unidentifiable character. 1/' + str(num_sections_of_website) + 'th of the page cannot be read \n')
			for k in range(len(all_text[i])):
				for l in range(len(all_text[i][k])):
					try:
						file.write(str(all_text[i][k][l]))
					except UnicodeEncodeError:
						file.write('*')
	file.close()
	
	'''
	with open('website_lines.txt', 'w') as file:
		for i in range(len(all_text)):
			file.write(str(all_text[i]))
	'''

	###Copy csv file to a txt file###
	num_lines_of_website = 0

	'''
	with open('website_lines.txt', 'w') as file:
		with open('website_lines.csv', 'r') as csv_file:
			for line in csv_file:
				num_lines_of_website += 1
				file.write(line)
	'''

	###Checks is a keyword from keywords.txt is found on the website###
	with open('keywords.txt') as keywords:
		list_of_keywords = []
		for line in keywords:
			list_of_keywords.append(line.strip('\n'))
			list_of_keywords.append(line.lower().strip('\n'))


	num_matches = 0
	
	with open('website_lines.txt', 'r') as website_lines:
		current_line = 0
		for line in website_lines:
			current_line += 1
			if current_line == 1:
				continue
			for keyword in list_of_keywords:
				if keyword in line:
					print('Match found for "' + keyword + '": "' + line.strip('\n'))
					num_matches += 1
					print('At website line ' + str(current_line) + ' out of ' + str(num_lines_of_website) + ' lines\n')
	
	num_websites_checked[0] += 1
	return html_contents_indices_where_products_pages_can_be, html_contents, num_matches

'''
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
'''	


###Get a list of links to search through.
###Thoroughness refers to how many of the links you want to conduct searches for. 1 means every link, 3 means every 3rd link, etc.
def search_through_multiple_links_to_find_keyword_matches(homepage, list_of_product_links, thoroughness, num_websites_checked, num_matches): ##
	results = []
	for i in range(len(list_of_product_links)):
		if i % thoroughness == 0:
			html_contents_indices_where_products_pages_can_be, html_contents, matches = find_keyword_matches_on_website(homepage, list_of_product_links[i], False, num_websites_checked)
			num_matches[1] += matches


def write_product_links(list_of_product_links): ##
	with open('list_of_product_links.txt', 'w') as file:
		for link in list_of_product_links:
			file.write(link + '\n')

###Pass in the html text you're looking for along with the html_contents with the index you know the text can be found.
def find_html_content_of_a_given_html_text(parent_html_text, html_contents, indices_where_text_can_be_found): ##
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
			if child.string != None:
				if parent_html_text in child.string or parent_html_text.lower() in child.string:
					list_of_sublinks.append(find_sublinks(child))

	return list_of_sublinks

#Get a list of links underneat the menu item given by html_contents.
def find_sublinks(html_contents): ##
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


def refine_list(list_of_sublinks): ##
	new_list_of_sublinks = []
	for i in range(len(list_of_sublinks)):
		try:
			sub_section_length = len(list_of_sublinks[i])
		except TypeError:
			sub_section_length = 0
		for j in range(sub_section_length):
			new_list_of_sublinks.append(list_of_sublinks[i][j])
	return new_list_of_sublinks


def save_output(num_websites_checked, num_matches, homepage):
	csv_file = open('Results.csv', 'a')
	csv_writer = writer(csv_file, delimiter = ',')
	csv_writer.writerow([homepage, num_matches[0], num_matches[1]/num_websites_checked, num_matches[0] + num_matches[1]])
	csv_file.close()


def search_a_website_and_the_sublinks(homepage):
	num_matches = [0, 0]
	num_websites_checked = [0]
	do_you_want_to_know_indices_where_product_pages_can_be = True

	html_contents_indices_where_products_pages_can_be, html_contents, num_matches[0] = find_keyword_matches_on_website(homepage, homepage, True, num_websites_checked)
	list_of_sublinks = find_html_content_of_a_given_html_text('Products', html_contents, html_contents_indices_where_products_pages_can_be)
	list_of_sublinks = refine_list(list_of_sublinks)
	print('Sublinks: ', end='')
	print(list_of_sublinks)

	write_product_links(list_of_sublinks)

	search_through_multiple_links_to_find_keyword_matches(homepage, list_of_sublinks, 10, num_websites_checked, num_matches)

	print('Number websites checked: ' + str(num_websites_checked[0]))

	print(num_matches)

	save_output(num_websites_checked[0], num_matches, homepage)

def read_website_links():
	websites = []

	file = open('websites_to_scrape.txt', 'r')
	for line in file:
		websites.append(line.strip('\n'))
	return websites


###Main function. This is where the program starts.
def main():
	csv_file = open('Results.csv', 'w')
	csv_writer = writer(csv_file, delimiter = ',')
	header = ['Website,No. of Kywrd Mtchs on Homepage,Avg. No. of Kywrd Mtchs on Each Product Page,Total No. of Kywrd Mtchs',' ']
	csv_writer.writerow(header)
	csv_file.close()
	
	websites = read_website_links()
	for website in websites:
		if website != '' and website != None:
			search_a_website_and_the_sublinks(website)
	
	#search_a_website_and_the_sublinks(homepage)
	#search_a_website_and_the_sublinks('https://www.ebara.co.jp/en/index.html')
	#list_of_product_links = get_product_links(html_contents_indices_where_products_pages_can_be, html_contents)
	

	

	time.sleep(0.1)


#main()