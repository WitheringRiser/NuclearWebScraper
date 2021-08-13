###                         Keyword Detector by Lukas Brazdeikis                      
###                                     Created July 2021                                  
###                                  Last modified 6/8/21                              
### The purpose of this program is to find new, relevant keywords. You give it keywords you are interested in
### (keywords_detector_keywords.txt) and blacklisted keywords (keyword_detector_blacklisted_keywords.txt).
### Then, the program finds patents with these keywords, then determines other keywords that show up in these
### patents that were not in the keyword files. These new keywords show up in KeywordDetectorOutput.py.
### The new keywords are found based on their tfidf score compared to a database of XXXX number of ordinary patents.
### Inputs: 
###     - No variables inputted into the main function. However, there are variable declarations inside the 
###       main function.
###     - keyword_detector_keywords.txt
###     - keyword_detector_blacklisted_keywords.txt
### Outputs:
###     - patent_text_for_keyword_analysis.txt
###     - patent_text_for_keyword_analysis_important_patents.txt
###     - KeywordDetectorOutput.csv
### Functions:
###     - create_text_db()                                      - create_average_tf_idf_scores_for_good_patents()
###     - create_good_patent_text_db()                          - get_good_keyword_ids()
###     - combine_text_databases()                              - get_good_keywords_from_ids()
###     - find_Tfid()                                           - write_output_to_csv()
###     - create_list_of_dicts_of_word_importance_per_patent()  - run_other_programs()
###     - get_list_of_numbers()                                 - main()
###     - create_word_list()                                    - combine_text_databases()
###     - create_tf_idf_values_for_good_patents()
###     - average_out_percent_of_good_patents_have_a_match()


import pandas
import nltk
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import TfidfVectorizer
import numpy
from csv import writer
import TestSplitTXT
import WebScrapingEPO_v2
import GivePointsEPO
import SavePatentTextForKeywordAnalysis


### Input: None.
### Output: None. However, global variables text_db and file_length are modified
def create_text_db():
    global text_db
    text_db = []
    global file_length
    file_length = 0

    file = open('patent_text_for_keyword_analysis.txt', 'r')
    for line in file:
        text_db.append(line)
        file_length += 1
    file.close()


### Input: None
### Output: None. However, global variables text_db_good_patents and file_length_good_patents are modified
def create_good_patent_text_db():
    
    global text_db_good_patents
    text_db_good_patents = []
    global file_length_good_patents
    file_length_good_patents = 0

    file = open('patent_text_for_keyword_analysis_important_patents.txt', 'r')
    for line in file:
        text_db_good_patents.append(line)
        file_length_good_patents += 1
    file.close()


### Input: None.
### Output: None. However, global variable text_db (list of strings) is modified
def combine_text_databases():
    text_db.extend(text_db_good_patents)


### Looks at all the words in all patents. Then, generates tf_idf for each unique word in each patent.
### Input: None.
### Output: None. However, global variables tf_idf and vec are modified
def find_Tfid():
    global tf_idf, vec
    nltk.download('stopwords')
    ignored_words = list(stopwords.words('english')) ## Stop words are common insignificant words like "and", "as", "the"

    ignored_words.extend(get_list_of_numbers(2001)) ## Ignored numbers 0 - 2000. Removes some of the numbers from results, though not all. Ex: removes "7" but not "7a".

    vec = TfidfVectorizer(stop_words = ignored_words)

    tf_idf =  vec.fit_transform(text_db)


### Creates a list of dictionaries for each patent entry. These dictionaries has the word index followed by the tf_idf score for each unique word in the patent.
### Input: None.
### Output: None. However, global variable list_of_dicts_of... is modified
def create_list_of_dicts_of_word_importance_per_patent():
    global list_of_dicts_of_word_importance_per_patent
    list_of_dicts_of_word_importance_per_patent = []

    
    for i in range(len(text_db)):
        tf_idf_coo_array = tf_idf[i].tocoo() ### Reformated so I can turn entries into a dict in next line
        tf_idf_dict = {k:v for k,v in zip(tf_idf_coo_array.col, tf_idf_coo_array.data)}
        list_of_dicts_of_word_importance_per_patent.append(tf_idf_dict)


### Input: amount_of_numbers (int)
### Output: numbers_list (list of ints)
def get_list_of_numbers(amount_of_numbers):
    numbers_list = []
    for i in range(amount_of_numbers):
        numbers_list.append(str(i))
    return numbers_list


### List of all unique words in all patents. The index of this list matches up with the key values of list_of_dicts_of_word_importance_per_patent
### Input: None.
### Output: None. However, global variable word_list is also modified
def create_word_list():
    global word_list
    word_list = vec.get_feature_names()


### Input: None.
### Output: None. However, global variable list_of_dicts_of... is modified
def create_tf_idf_values_for_good_patents():
    global list_of_dicts_of_word_importance_per_good_patent
    list_of_dicts_of_word_importance_per_good_patent = list_of_dicts_of_word_importance_per_patent[file_length:] ### Extracts part of list after all cumulative patents so that you get only good patents


### Input: None.
### Output: None. However, global variable good_key_value_pairs is modified
def create_key_value_pairs_tf_idf_scores_for_good_patents():
    global good_key_value_pairs
    good_key_value_pairs = []

    for list_of_patent_scores in list_of_dicts_of_word_importance_per_good_patent:
        key_value_pairs = list_of_patent_scores.items()
        key_value_pairs = sorted(key_value_pairs, key = lambda x: x[1])
        good_key_value_pairs.append(key_value_pairs)


### Input: None.
### Output: None. However, global variables cumulative_tf_idf_... and percent_of_good_patents_... are modified.
def create_cumulative_tf_idf_scores_for_good_patents():
    global cumulative_tf_idf_scores_for_good_patents
    cumulative_tf_idf_scores_for_good_patents = dict()
    global percent_of_good_patents_have_a_match
    percent_of_good_patents_have_a_match = dict()
    for patent in good_key_value_pairs:
        for pair in patent:
            word_id = int(pair[0])
            tf_idf_value = pair[1]
            if word_id in cumulative_tf_idf_scores_for_good_patents:
                cumulative_tf_idf_scores_for_good_patents[word_id] += tf_idf_value
                percent_of_good_patents_have_a_match[word_id] += 1
            else:
                cumulative_tf_idf_scores_for_good_patents[word_id] = tf_idf_value
                percent_of_good_patents_have_a_match[word_id] = 1
    average_out_percent_of_good_patents_have_a_match()


### Input: None.
### Output: None. However, percent_of_good_patents_... is modified
def average_out_percent_of_good_patents_have_a_match():
    for key in percent_of_good_patents_have_a_match:
        percent_of_good_patents_have_a_match[key] /= file_length_good_patents
        percent_of_good_patents_have_a_match[key] *= 100


### Input: None.
### Output: None. However, global variable average_tf_idf_scores... is modified
def create_average_tf_idf_scores_for_good_patents():
    global average_tf_idf_scores_for_good_patents
    average_tf_idf_scores_for_good_patents = dict(cumulative_tf_idf_scores_for_good_patents)
    print(file_length_good_patents)
    for key in average_tf_idf_scores_for_good_patents:
        average_tf_idf_scores_for_good_patents[key] /= file_length_good_patents


### Input: minimum_number_required (int), tolerance (int)
### Output: None. However, global var good_keyword_ids is modified
def get_good_keyword_ids(minimum_number_required, tolerance):
    global good_keyword_ids
    good_keyword_ids = dict()
    try:
        percentage_matches_required = minimum_number_required / file_length_good_patents
    except ZeroDivisionError:
        print('****************')
        print('No patents found')
        print('****************')
    percentage_matches_required *= 100
    print(percentage_matches_required)
    for key in average_tf_idf_scores_for_good_patents: ## Saves words in good patents that meet a certain threshold
        if average_tf_idf_scores_for_good_patents[key] >= tolerance:
            if percent_of_good_patents_have_a_match[key] >= percentage_matches_required:
                good_keyword_ids[key] = average_tf_idf_scores_for_good_patents[key]


### Input: None.
### Output: None. However, global var good_keywords is modified
def get_good_keywords_from_ids():
    global good_keywords
    good_keywords = dict()
    for key in good_keyword_ids:
        word = word_list[key]
        good_keywords[word] = good_keyword_ids[key]


### Input: None.
### Output: None. However, KeywordDetectorOutput.csv is appended to
def write_output_to_csv():
    csv_file = open('KeywordDetectorOutput.csv', 'a')
    csv_writer = writer(csv_file, delimiter = ';')
    csv_writer.writerow(['Keyword', 'Average tfidf value'])
    for key in good_keywords:
        csv_writer.writerow([\
            key,\
            good_keywords[key]\
         ])
    csv_file.close()


### Input: keywords_file (string), blacklisted_keywords_file (string)
### Output: None.
def run_other_programs(keywords_file, blacklisted_keywords_file, num_patents, file_dir, google_pause_length,\
    interested_patent_components, EPO_score_needed_to_save_patent, num_patents_to_save):

    components = TestSplitTXT.main(num_patents, file_dir, interested_patent_components)
    components, only_matches = WebScrapingEPO_v2.main(components, num_patents, interested_patent_components,\
        keywords_file, blacklisted_keywords_file, num_patents_to_save)
    GivePointsEPO.main(components, only_matches)
    SavePatentTextForKeywordAnalysis.main(components, interested_patent_components, EPO_score_needed_to_save_patent)


### Input: None.
### Output: None
def main():
    ## Variable setup part 1
    minimum_times_keyword_needs_to_show_up = 1 ## Minimum number of good patents that a keyword needs to show up in in order to show up in the output csv file.
    minimum_avg_tfidf_score = 0.01 ## Recommended to keep between 0.01 (many keywords show up in results) and 0.05 (fewer keywords show up in results)
    keywords_file = 'keyword_detector_keywords.txt' ## File directory where keywords exist that you wish to find related keywords from
    blacklisted_keywords_file = 'keyword_detector_blacklisted_keywords.txt'


    ## Variable setup part 2 (only passed to run_other_programs())
    num_patents = 50000 ## Number of patents to scrape to find the good patents. Maximum ~50000. Keep high if your keywords file is small, low if your keywords file is large.
    file_dir = 'C:/Users/lukas/OneDrive/Desktop/ImportPatentTXT/EP3500000.txt' ### Patent file
    google_pause_length = 5 ## Wait period between Google searches (5 is recommended, however lower numbers can be used if you're not using many google searches)
    interested_patent_components = ['ABSTR'] ## What patent section to check for keywords. Options: ABSTR, DESCR or both
    EPO_score_needed_to_save_patent = 100 ## Score requirement needed for a patent to be considered a good patent. Recommended to keep at 150, but can have between 100 and 200.
    num_patents_to_save = 1000 ## How many random patents to save to compare good patents against. Recommended to have at least 1000.

    run_other_programs(keywords_file, blacklisted_keywords_file, num_patents, file_dir, google_pause_length,\
        interested_patent_components, EPO_score_needed_to_save_patent, num_patents_to_save)

    create_text_db()
    create_good_patent_text_db()
    combine_text_databases()
    find_Tfid()
    create_list_of_dicts_of_word_importance_per_patent()
    
    create_word_list()

    create_tf_idf_values_for_good_patents()
    create_key_value_pairs_tf_idf_scores_for_good_patents()

    create_cumulative_tf_idf_scores_for_good_patents()
    create_average_tf_idf_scores_for_good_patents()

    get_good_keyword_ids(minimum_times_keyword_needs_to_show_up, minimum_avg_tfidf_score)
    #print(good_keyword_ids)

    get_good_keywords_from_ids()
    print(good_keywords)

    write_output_to_csv()


main()