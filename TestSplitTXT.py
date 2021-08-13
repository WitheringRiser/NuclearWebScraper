###                          Patent Extractor by Lukas Brazdeikis                      
###                                   Created July 2021                               
###                                  Last modified 5/8/21                              
### The purpose of this program is to retreive patents from an EPO patent file. These patents then have their 
### components sorted.
### Inputs: 
###		- num_patents, file_dir, interested_patent_components from RunEntireProgram.py
### Outputs:
###		- Patents.txt
###		- components
### Functions:
###		-   								               - check_if_end_of_patent()
###		- get_components()	  						       - extract_and_replace_text()
###		- separate_line()						           - main()
###		- save_components()								   - check_if_file_is_completely_read()
###		- remove_duplicate_patents()


from bs4 import BeautifulSoup

global components
components = []

global counter
counter = []


### Input: num_patents (int), file_dir (string)
### Output: None. However, global variable components (multidimensional list) is modified
def get_components(num_patents, file_dir):
	all_patents_components = []
	file = open(file_dir, 'r')
	patents_found = 0
	current_patent_components = []
	current_patent_needs_to_be_burned = False
	while patents_found <= num_patents:
		try:
			line = file.readline()
			separated_line = separate_line(line)
			is_line_end_of_patent, is_file_completely_read = check_if_end_of_patent(separated_line)
			if is_file_completely_read: ## Breaks loop if all patents have been read
				print('*******************************')
				print('Reached end of file prematurely')
				print('        stopping here.         ')
				print('*******************************')
				#current_patent_components.append(separated_line)
				#current_patent_components = []
				#current_patent_needs_to_be_burned = False
				break
			if is_line_end_of_patent:
				if current_patent_needs_to_be_burned:
					current_patent_components.append(separated_line)
					current_patent_components = []
					current_patent_needs_to_be_burned = False
				else:
					current_patent_components.append(separated_line)
					all_patents_components.append(current_patent_components)
					current_patent_components = []
					patents_found += 1
			else:
				current_patent_components.append(separated_line)
		except UnicodeDecodeError:
			current_patent_needs_to_be_burned = True
			print('Patent number ' + str(patents_found) + ' cannot be read. It is ignored')
			check_if_file_is_completely_read(1)
	file.close()
	global components
	components = all_patents_components


### Input: line (string)
### Output: separated_line (list of strings)
def separate_line(line):
	separated_line = line.split('	')
	return separated_line


### Input: None
### Output: None. However, Patents.txt is written to
def save_components():
	file = open('Patents.txt', 'w')
	for patent in components:
		for line in patent:
			file.write(str(line) + '\n')


### Input: separated_line (list of strings)
### Output: boolean
def check_if_end_of_patent(separated_line):
	if len(separated_line) < 8:
		is_file_completely_read = check_if_file_is_completely_read(2)
		for line_segment in separated_line:
			if 'PDFEP' in line_segment:
				return True, is_file_completely_read
			else:
				return False, is_file_completely_read
	is_file_completely_read = False
	if separated_line[5] == 'PDFEP':
		return True, is_file_completely_read
	else:
		return False, is_file_completely_read


### Input: list_of_sections_to_extract (list of strings)
### Output: None. However, the global variable components (multidimensional list) is modified
###		- components contains xml, but this function converts a specified section to regular text
def extract_and_replace_text(list_of_sections_to_extract):
	for patent in components:
		for line in patent:
			if line[5] in list_of_sections_to_extract:
				bs_content = BeautifulSoup(line[7], "lxml")
				line[7] = bs_content.text


### Input: counter_entry (int)
### Output: Boolean
### This function is weird and vague as to how it works. Essentially, I tally up the occurence of various parts of the
### program. If there's too many occurences in one area without anything else in between, this function considers
### that to mean the end of the patent file has been reached.
def check_if_file_is_completely_read(counter_entry):
	counter.append(counter_entry)
	if len(counter) < 10:
		return False
	last_10_entries = counter[-10:]
	num_entries_of_one = 0
	num_entries_of_two = 0
	for entry in last_10_entries:
		if entry == 1:
			num_entries_of_one += 1
		if entry == 2:
			num_entries_of_two += 1
	if num_entries_of_one == 0:
		return True
	else:
		return False



### Input: None
### Output: None. However, global var components is modified
def remove_duplicate_patents():
	checked_patents_numbers = []
	for patent in components:
		patent_number = patent[0][1]
		if patent_number in checked_patents_numbers:
			print('Duplicate Found: ' + str(patent_number))
			components.remove(patent)
		else:
			checked_patents_numbers.append(patent_number)



### Input: num_patents (int), file_dir (string), interested_patent_components (list of strings)
def main(num_patents, file_dir, interested_patent_components):

	get_components(num_patents, file_dir)
	print('')
	print('Please wait...')
	print('')
	extract_and_replace_text(interested_patent_components)
	save_components()
	remove_duplicate_patents() # Dont uncomment, breaks the program when using combined keywords (the ones with the '+' in EPO_Keywords.txt)

	
	

	return components

#main(1000, 'C:/Users/lukas/OneDrive/Desktop/ImportPatentTXT/EP3500000.txt', '[ABSTR]')