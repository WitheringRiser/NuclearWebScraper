***********************************
          Introduction
***********************************
Program(s) made by Lukas Brazdeikis between June 21 2021 and August 11 2021 for InTechBrew.

External libraries used: beautifulsoup4, requests, googlesearch-python, google-patent-scraper, google-cloud-storage, pandas,
nltk, scikit-learn, selenium

This program helps perform research for new innovations in the nuclear sector. There are various processes and 
programs run that streamline this process. There are two files containing two different programs. The file
named "ImportPatentTXT_V2" solely takes care of downloading EPO patent files from Google Cloud Storage.
All other files are where the meat of the program is. Here there are two subprograms: web scraping
and keyword detection. Below is a general outline of the steps of these programs.

Web scraping program (run through "RunEntireProgram.py" that combines various programs in the order listed below)
1. TestSplitTXT.py: Read through the patent file, separate various components, and save these components in local memory
2. WebScrapingEPO_v2.py: Find and tally primary, secondary, and blacklisted keyword matches.
3. GivePointsEPO.py: Assigns and saves points for each patent based on the number and type of keyword matches.
4. GetCompanyNames.py: Search on patents.google.com to find the company name attatched to each patent number.
5. FindWebsites_V2.py: Find the best link related to a company name through google.com
6. WebScrapingRandomSiteSelenium.py: Scrape a list of websites looking for various website structure and keywords. Results are saved.
7. CreateResultsCSV.py: Gather all scores and relevant data and put into a csv file.

Keyword detection program (run through "KeywordDetector.py" that combines various programs in the order listed below)
1. TestSplitTXT.py: Read through the patent file, separate various components, and save these components in local memory
2. WebScrapingEPO_v2.py: Find and tally primary, secondary, and blacklisted keyword matches. Also save a certain number of 
generic patents to use as a basis for finding keywords that stand out in a select number of good patents.
3. GivePointsEPO.py: Assigns and saves points for each patent based on the number and type of keyword matches.
4. SavePatentTextForKeywordAnalysis.py: Saves good patents that you will later use to find keywords from.
5. KeywordDetector.py: Generates tfidf scores for all words in all patents. Then, selects and saves words from good patents
with a high enough score.


***********************************
     Documentation philosophy
***********************************
This section describes how I have documented my program.

I should disclaim that I have gone through all functions and python files at the end of my project to update the descriptions
and comments. However, there may still exist the occasional error in my comments such as stating something wrong. 

This file contains and overarching view on the programs I have made ("Introduction"), the Python libraries you must install
to run the program for the first time ("Dependencies"), and how to run each program ("Programs setups").

Each python file contains a header at the top with the following information:
1. Date
2. Overall description of program, very similar to what I have stated in "Introduction."
3. Overall inputs and outputs of the file as a whole.
4. A list of all functions used in the program in the order that they appear in the file.

Each python file also has comments scattered throughout the file:
1. Each function has a header stating the inputs and outputs of the file.
2. Some long or complicated functions have in-line comments to explain big chunks of code or confusing chunks of code.

The functions and variable names are meant to be self-explanatory, so comments explaining these are rare. However, the 
variables that are meant to be changed as part of configuration of the program are heavily commented.


***********************************
          Dependencies
***********************************

These are dependancies required to run the program for the first time.
These are various Python libararies you must install on your computer.
You can install "pip" to make the installation of these python libraries simpler.
Instructions:
1. Install pip
After pip is installed, open command prompt or terminal and type the following commands:
1. pip install beautifulsoup4
2. pip install requests
3. pip install googlesearch-python
4. pip install google-patent-scraper
5. pip install google-cloud-storage
6. pip install pandas
7. pip install nltk
8. pip install scikit-learn
9. pip install selenium
All of these 9 lines refer to all of the python libraries used for the program.


***********************************
         Programs setups
***********************************

How to set up various programs:

Set up the standard program:
	- Open RunEntireProgram.py in a code editor
	- Change variables at the start of the main function.
	- Comment out any functions you do not wish to run. In the rare scenario
	  that the program crashes, you can comment out all completed functions
	  to save time.
		- Note that some functions need to be run in blocks while other can
		  just be run standalone.
	- Modify the following files as desired:
 		"EPO_keywords.txt", "EPO_keywords_blacklisted.txt", 
		"blacklisted_websites.txt", "keywords.txt"

Set up the keyword detector:
	- Open KeywordDetector.py in a code editor
	- Change variables at the start of the main function.
	- Modify the following files as desired:
		"keyword_detector_keywords.txt", "keyword_detector_blacklisted_keywords.txt"ss

Set up the program used to download patent files from the EPO Google Cloud Storage platform:
	- Open the separate folder on Google Drive "ImportPatentTXT_V2"
	- Open the Python file in a code editor
	- Change variables at the top of the program

Set up the program to test your IP address:
	- Open TestVPN.py in a code editor
	- Change variables at the top of the main function as desired


***********************************
       .TXT File Formatting
***********************************

The various text file inputs are very picky as to how they should be formatted.
Make sure to not leave any excessive/erroneous spaces or other characters.
In this folder "DOCUMENTATION", there are several example files to showcase how the input should be.
