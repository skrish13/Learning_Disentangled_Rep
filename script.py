import requests
from bs4 import BeautifulSoup


import requests

def download_file_from_google_drive(id, destination):
    URL = "https://docs.google.com/uc?export=download"

    session = requests.Session()

    response = session.get(URL, params = { 'id' : id }, stream = True)
    token = get_confirm_token(response)

    if token:
        params = { 'id' : id, 'confirm' : token }
        response = session.get(URL, params = params, stream = True)

    save_response_content(response, destination)    

def get_confirm_token(response):
    for key, value in response.cookies.items():
        if key.startswith('download_warning'):
            return value

    return None

def save_response_content(response, destination):
    CHUNK_SIZE = 32768

    with open(destination, "wb") as f:
        for chunk in response.iter_content(CHUNK_SIZE):
            if chunk: # filter out keep-alive new chunks
                f.write(chunk)

parent_url = 'https://sites.google.com/view/disentanglenips2017'

page = requests.get(parent_url)
c = page.content
soup = BeautifulSoup(c)
all_links = soup.find_all("a")
print('Total Papers Found:{}'.format(len(all_links)))
count = len(all_links)
current = 1
for link in all_links:
	try:
		dl = link.attrs['href']
		current+=1
		if '?id=' in dl:
			file_id = dl.split('?id=')[1]
			print 'Downloading {}/{}:{}'.format(current, count,  dl)
			download_file_from_google_drive(file_id, '{}.pdf'.format(current))
	except:
		pass

import os
import subprocess
base = "./"
chunk = os.listdir(base)
print chunk
base_command = 'gs -sDEVICE=pdfwrite -dCompatibilityLevel=1.4 -dPDFSETTINGS=/default -dNOPAUSE -dQUIET -dBATCH -dDetectDuplicateImages -dCompressFonts=true -r150 -sOutputFile=otherone-disentangled_nips17_workshop_book.pdf'
for i in range(0,len(chunk)):
	base_command += " " + base + chunk[i] + " "

print base_command

subprocess.call(base_command)