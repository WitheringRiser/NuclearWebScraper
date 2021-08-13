### This program is run in KeywordDetector.py
### This program saves patents with a certain EPO score (good patents) that will later be used to find keywords from


from csv import writer

def get_points_from_EPO():
    global points_from_EPO
    points_from_EPO = {}

    file = open('points_from_EPO.txt', 'r')
    for line in file:
        line.strip('\n')
        line_components = line.split(' ')
        points_from_EPO[int(line_components[0])] = int(line_components[1])
    file.close   


def find_interested_sections(interested_patent_components, patent):
	interested_sections = []
	for line in patent:
		if line[5] in interested_patent_components:
			interested_sections.append(line[7].lower())
	return interested_sections


def add_num_patents_to_csv():
    csv_file = open('KeywordDetectorOutput.csv', 'w')
    csv_writer = writer(csv_file, delimiter = ';')
    csv_writer.writerow(['Number of patents checked: ',num_patents[0]])
    csv_file.close()	


def save_patent_text(components, interested_sections, EPO_score_needed_to_save_patent):
	global num_patents
	num_patents = [0]
	file = open('patent_text_for_keyword_analysis_important_patents.txt', 'w')
	for patent in components:
		patent_number = int(patent[0][1])
		try: ## Checks if patent number exists
			if points_from_EPO[patent_number] >= EPO_score_needed_to_save_patent:
				patent_texts = find_interested_sections(interested_sections, patent)
				for patent_text in patent_texts:
					file.write(patent_text.lower())
					num_patents[0] += 1
		except KeyError: ## If patent number doesn't exist, ignore it
			continue
	file.close()


def main(components, interested_sections, EPO_score_needed_to_save_patent):
	get_points_from_EPO()
	save_patent_text(components, interested_sections, EPO_score_needed_to_save_patent)
	add_num_patents_to_csv()

#main()