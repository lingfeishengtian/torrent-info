import binascii
import requests
from bs4 import BeautifulSoup
from urllib.parse import unquote_to_bytes, urlparse, parse_qs

url = """tracker.opentrackr.org:1337/announce?info_hash=%04mr%e5%7f%0c%e1%88%06%e0jr>%a1%b9'%ff%af%9d&&peer_id=-BT7b0W-%15%b8ol;%c7%15%bf%c2*%af%1f&port=60354&uploaded=0&downloaded=0&left=0&corrupt=0&key=D1D543AE&numwant=200&compact=1&no_peer_id=1"""
btdigg = "https://btdig.com/"

def get_info_hash(url):
    parsed_url = urlparse(url)
    query_list = parse_qs(parsed_url.query, encoding='raw_unicode_escape', errors='backslashreplace')
    info_hash = query_list['info_hash'][0]
    print(binascii.hexlify(unquote_to_bytes("%04mr%e5%7f%0c%e1%88%06%e0jr>%a1%b9'%ff%af%9d&")).decode('utf-8'))
    return binascii.hexlify(info_hash.encode('raw_unicode_escape')).decode('utf-8')

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

# print(get_torrent_info(get_info_hash(url)))
print(get_torrent_info('046d72e57f0ce18806e06a723ea1b927ffaf9d26'))