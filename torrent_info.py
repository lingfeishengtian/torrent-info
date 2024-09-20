import binascii
import re
import requests
from bs4 import BeautifulSoup
from urllib.parse import unquote_to_bytes, urlparse, parse_qs
import sys

btdigg = "https://btdig.com/"

def get_info_hash(url):
    pattern = r'info_hash=(.*?)&peer_id='
    info_hash = re.search(pattern, url).group(1)
    print("Info hash: ", info_hash)
    return binascii.hexlify(unquote_to_bytes(info_hash)).decode('utf-8')

def get_torrent_info(info_hash):
    if len(info_hash) != 40 and len(info_hash) != 64:
        print("Invalid info hash: ", info_hash)
        return None
    print("Searching torrent for info hash: ", info_hash)
    postTo = btdigg + info_hash
    request = requests.get(postTo)
    parsed = BeautifulSoup(request.text, 'html.parser')
    if parsed.find_all('table') is None or len(parsed.find_all('table')) < 2:
        print("No table found")
        return {"result": "Nothing found"}
    table = parsed.find_all('table')[1]
    
    dict_info = {}
    for row in table.find_all('tr'):
        cells = row.find_all('td')
        if len(cells) > 1:
            dict_info[cells[0].text] = cells[1].text.replace('\xa0', ' ').strip()
    
    return dict_info

# print(get_torrent_info(get_info_hash(url)))
# print(get_torrent_info())

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python torrent_info.py <torrent_url>")
        sys.exit(1)
    url = sys.argv[1]
    info_hash = get_info_hash(url)
    print(get_torrent_info(info_hash))
    sys.exit(0)