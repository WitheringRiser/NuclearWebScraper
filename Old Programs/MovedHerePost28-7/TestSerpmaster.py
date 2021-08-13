import requests
from pprint import pprint
from bs4 import BeautifulSoup



# Specify content type and form the request body
headers = {'Content-Type': ''}
job_params = {
    'q': 'Concordia Textiles',
    'num': 1,
    'parse': True
}
# Post job and get response
response = requests.post(
    'https://rt.serpmaster.com',
    headers=headers,
    json=job_params,
    auth=('damona', 'R936n9PmXc')
)

html = response.text

soup = BeautifulSoup(html, 'html.parser')

# Print the response body
pprint(soup)