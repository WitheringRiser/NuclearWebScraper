from google.cloud import storage
import os

file = 'EP1000000.txt'
year_week =  '2021week05'

os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="silver-approach-319211-5320dd6419d5.json"

client = storage.Client()

bucket = client.bucket('ep-fulltext-for-text-analytics', 'silver-approach-319211')

blob = bucket.blob(year_week + '/' + file)

downloaded_blob = blob.download_as_string()

file = open (file, w):
for ch in downloaded_blob:
	try:
		file.write(ch)
	except UnicodeEncodeError:
		file.write('*')