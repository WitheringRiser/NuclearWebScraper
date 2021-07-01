#Created 1/7/21

from bs4 import BeautifulSoup
import requests
import time
from googlesearch import search
import random

def find_links_to_patents_with_keyword_matches(how_many_keyword_matches_to_qualify, company_names, num_matches):

	links = []
	for key in num_matches:
		if int(num_matches[key]) >= how_many_keyword_matches_to_qualify:
			company_name = company_names[int(key.strip('.')) - 1]
			if '*' in company_name:
				links.append(['Error: Cannot read company name'])
			else:
				links.append(run_google_search(company_name))

	return links


def unpack_files():
	file = open('EPO_company_names.txt', 'r')
	company_names = []
	for line in file:
		company_names.append(line.strip('\n'))
	file.close()

	file = open('EPO_keyword_matches.txt', 'r')
	num_matches = {}
	for line in file:
		key = ''
		line = line.strip('\n')
		for i in range(len(line)):
			if line[i] != ' ':
				key += line[i]
			else:
				num_matches[key] = line[i + 1:]
	file.close()

	return company_names, num_matches


def run_google_search(query):
	links = ['Google search for "' + query + '" in this list.']
	for result in search(query, tld="com", num=10, stop=10, pause=2 * random_offset(10)):
		links.append(result)

	return links

def random_offset(percentage):
	offset = 0.01 * random.randint(100 - percentage, 100 + percentage)
	return offset

def main():
	company_names, num_matches = unpack_files()

	links = find_links_to_patents_with_keyword_matches(10, company_names, num_matches)
	print(links)

main()