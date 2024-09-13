import binascii
import requests
from bs4 import BeautifulSoup
from urllib.parse import unquote_to_bytes

url = """"""
btdigg = "https://btdig.com/"

def retrieve_info_hash(url):
    # Extract the info_hash from the URL
    info_hash = url.split('info_hash=')[-1]
    return info_hash

def url_decode_to_bytes(encoded_str):
    decoded_bytes = []
    return unquote_to_bytes(encoded_str)

def get_info_hash(url):
    return (binascii.hexlify(url_decode_to_bytes(retrieve_info_hash(url)))).decode('utf-8')

def get_torrent_info(info_hash):
    print("Searching torrent for info hash: ", info_hash)
    postTo = btdigg + info_hash
    request = requests.get(postTo)
    parsed = BeautifulSoup(request.text, 'html.parser')
    table = parsed.find_all('table')[1]
    
    dict_info = {}
    for row in table.find_all('tr'):
        cells = row.find_all('td')
        if len(cells) > 1:
            dict_info[cells[0].text] = cells[1].text.replace('\xa0', ' ').strip()
    
    return dict_info

print(get_torrent_info(get_info_hash(url)))