from bs4 import BeautifulSoup


content = []
# Read the XML file
with open("sample.xml", "r") as file:
    # Read each line in the file, readlines() returns a list of lines
    content = file.readlines()
    # Combine the lines in the list into a string
    content = "".join(content)
    bs_content = BeautifulSoup(content, "lxml")

result = bs_content.find_all("data")
print(result)

