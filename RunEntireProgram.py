###                          Nuclear research program by Lukas Brazdeikis                  
###                                      Created 2/7/21                                 
###                                   Last modified 6/7/21                              
### Input: None.
### Output: results of relevant websites and their scores ("Results.csv")
### This program aggregates all other python programs in this file so they seamlessly work together
### 1. EPO is scraped for patents. 
### 2. Then the patents are scraped for keywords. 
### 3. The companies attatched to patents with enough keywords are googled. 
### 4. The best website from this google search is then saved. 
### 5. Then all the websites will be scraped. 
### 6. The websites will then be given a score based on keyword matches and website structure.


import WebScrapingRandomSiteSelenium
import time
import TestSplitTXT
import WebScrapingEPO_v2
import GivePointsEPO
import GetCompanyNames
import FindWebsites_v2
import CreateResultsCSV


def main():
	print('Make sure to close Results.csv')
	print('Make sure all input values and files are what they should be.')
	time.sleep(1)
	
	### Variable setup for all below functions
	num_patents = 100000 ## Number of patents to scrape. Average number of patents in a file is ~60000.
						 ## You can set this number to a very high number (ex: 500000), and the program will automatically stop once 
						 ## all patents have been read.
	file_dir = 'C:/Users/lukas/OneDrive/Desktop/ImportPatentTXT/EP3600000.txt' ### Patent file directory
	google_pause_length = 5 ## Wait period between Google searches. Recommended to keep at 5 to prevent Google
							## from blocking your IP and crashing the program
	interested_patent_components = ['ABSTR'] ## What patent section to check for keywords. Options: ABSTR, DESCR, or both.
											 ## Highly recommended to keep at only 'ABSTR'.
	interested_tabs = ['Products', 'Services', 'Applications', 'Industries', 'Sectors'] # Website sections/pages to look for and scrape
	thoroughness = 1000 ## How thorough pages in each interested tab should be scraped. Ex: thoroughness = 3 means every third website. 
						## Recommended to keep at 1000 as you ideally want one link per tab searched. Keeping it lower may mean large websites
						## take a really long time to scrape and there are many pages to load.
	bad_tabs_and_bad_text = { ## Text on the website that will lead to a point reduction. The zeros don't mean anything but are required
							  ## to include in each entry.
	'Financial Statements': 0,
	'Financial Highlights': 0,
	'Dividends': 0,
	'Credit Ratings': 0,
	'Corporate Credit': 0,
	'Financial Reports': 0,
	'Investor Relations': 0,
	'Stock Price': 0,
	'Stock Ticker': 0,
	'Research Centers': 0,
	'Research Funding': 0,
	'School': 0,
	'University': 0,
	'Academics': 0,
	'Campus Life': 0
	#'COVID': 0,
	#'Corona': 0
	}

	### Comment out functions/blocks of functions you do not wish to run. Remember to also uncomment the ones you do want to run.

	### Run these three together. Don't run them seperately.
	components = TestSplitTXT.main(num_patents, file_dir, interested_patent_components)
	components, only_matches = WebScrapingEPO_v2.main(components, num_patents, interested_patent_components,\
	'EPO_keywords.txt', 'EPO_keywords_blacklisted.txt')
	GivePointsEPO.main(components, only_matches)
 
	### Can run this one alone
	GetCompanyNames.main(google_pause_length)

	### Can run this one alone
	FindWebsites_v2.main(google_pause_length)
	
	### Can run this one alone
	WebScrapingRandomSiteSelenium.main(interested_tabs, thoroughness, bad_tabs_and_bad_text)
	
	### Can run this one alone
	CreateResultsCSV.main()
	

main()