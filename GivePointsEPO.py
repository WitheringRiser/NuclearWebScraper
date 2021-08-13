###                         EPO Scoring Program by Lukas Brazdeikis                      
###                                    Created July 2021                                 
###                                  Last modified 5/8/21                              
### The purpose of this program is to give score to various patents based on keyword matches.
### Inputs: 
###		- _components, _only_matches from RunEntireProgram.py
### Outputs:
###		- points_from_EPO.txt
### Functions:
###		- give_points()
###		- save_points_from_EPO()
###		- get_patent_number()
###		- print_estimated_time_remaining()


import time

global points_from_EPO
points_from_EPO = {}


### Input: None
### Output: None. However, global variable points_from_EPO is modified
def give_points():
	for key in only_matches:
		patent_number = get_patent_number(key)
		try:
			points_from_EPO[patent_number] +=1
			points_from_EPO[patent_number] -=1
		except:
			points_from_EPO[patent_number] = 0

		only_matches[key] = int(only_matches[key])
		only_matches[key.replace('secondary', 'primary')] = int(only_matches[key.replace('secondary', 'primary')])

		if '(primary)' in key:
			pass
		elif '(secondary)' in key:
			if only_matches[key] < 0:
				if only_matches[key.replace('secondary', 'primary')] == 0:
					pass
				if only_matches[key.replace('secondary', 'primary')] == 1:
					pass
				if only_matches[key.replace('secondary', 'primary')] > 1:
					points_from_EPO[patent_number] += 50
			elif only_matches[key] == 0:
				if only_matches[key.replace('secondary', 'primary')] == 0:
					pass
				if only_matches[key.replace('secondary', 'primary')] == 1:
					points_from_EPO[patent_number] += 100
				if only_matches[key.replace('secondary', 'primary')] > 1:
					points_from_EPO[patent_number] += 175
			elif only_matches[key] == 1:
				if only_matches[key.replace('secondary', 'primary')] == 0:
					pass
				if only_matches[key.replace('secondary', 'primary')] == 1:
					points_from_EPO[patent_number] += 150
				if only_matches[key.replace('secondary', 'primary')] > 1:
					points_from_EPO[patent_number] += 200
			elif only_matches[key] > 1:
				if only_matches[key.replace('secondary', 'primary')] == 0:
					points_from_EPO[patent_number] += 150
				if only_matches[key.replace('secondary', 'primary')] == 1:
					points_from_EPO[patent_number] += 200
				if only_matches[key.replace('secondary', 'primary')] > 1:
					points_from_EPO[patent_number] += 200


### Input: None
### Output: None. However, points_from_EPO.txt is written to
def save_points_from_EPO():
	file = open('points_from_EPO.txt', 'w')
	for patent_number in points_from_EPO:
		file.write(str(patent_number) + ' ' + str(points_from_EPO[patent_number]) + '\n')
	file.close


### Input: key (dict)
### Output: patent_number (int)
def get_patent_number(key):
	patent_number = ''
	i = 0
	while key[i] != ' ':
		patent_number += key[i]
		i += 1
	patent_number = int(patent_number)
	return patent_number


### Input: None
### Output: None. However, print statements are made
def print_estimated_time_remaining():
	num_of_patents = 0
	for patent in points_from_EPO:
		if points_from_EPO[patent] >= 100:
			num_of_patents += 1
	MINUTES_PER_RESULT = 0.4
	FRACTION_OF_PATENTS_TO_PASS = 0.75
	time_in_min_to_completion = num_of_patents * MINUTES_PER_RESULT
	time_in_hours_to_completion = time_in_min_to_completion / 60
	estimated_num_patents_to_pass = num_of_patents * FRACTION_OF_PATENTS_TO_PASS
	print('*********************************')
	print('Estimated time to completion: ' + str(time_in_min_to_completion) + 'min or ' +\
	 str(time_in_hours_to_completion) + 'h.')
	print('Estimated number of patents found: ' + str(estimated_num_patents_to_pass))
	print('*********************************')


### Input: _components (multidimensional list), _only_matches (dict)
### Output: None
def main(_components, _only_matches):
	global components
	components = _components
	global only_matches
	only_matches = _only_matches

	give_points()
	print(points_from_EPO)
	save_points_from_EPO()

	print_estimated_time_remaining()

	time.sleep(2)