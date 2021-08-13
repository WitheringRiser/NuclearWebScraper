### Import patent TXT
### Downloads a txt file from the Google Cloud Storage platform for EPO
### Note: Program takes a few hours to run/download

from google.cloud import storage
import os

file = 'EP1000000.txt'
year_week =  '2021week05'

os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="silver-approach-319211-5320dd6419d5.json"

client = storage.Client()

bucket = client.bucket('ep-fulltext-for-text-analytics', 'silver-approach-319211')

print('Stage 1 of 4')

blob = bucket.blob(year_week + '/' + file)

print('Stage 2 of 4')

downloaded_blob = blob.download_as_string()

print('Stage 3 of 4')

#file = open ('$license.txt', 'w')
blob.download_to_filename(file)

#file.close()
print('Stage 4 of 4')
