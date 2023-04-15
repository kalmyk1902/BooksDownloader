import os
import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent

url = 'https://e-padruchnik.adu.by/'
user = UserAgent().random

headers = {
    'user-agent': user,
    'referer': url
}

def pdf(letter, digit):
    try:
        global rows

        data = {
            'char': letter,
            'class': digit,
            'mode': 'char'
        }

        lg = requests.post(url, data=data, headers=headers)

        soup = BeautifulSoup(lg.content, 'html.parser')
        tb = soup.find('table', {'id': 'booklist'})
        rows = tb.select('tr[book-id]')
        if not rows:
            return 'Мы ничего не нашли :('

        results = ''
        for index, row in enumerate(rows):
            row.find('br').insert_before(' ')
            results += (f"{index + 1}. {row.select('td')[4].text} / {row.select('td')[2].text}\n")
        results = results[:-2]
        return results
    
    except requests.exceptions.ConnectionError:
        return 'Нет подключения к интернету!'
    
def send(choice, callback):
    ch_result = rows[int(choice)-1]
    book_id = ch_result.get('book-id')
    final = requests.post(url, data={'id': book_id, 'getbook': ''}, headers=headers, stream=True)

    FILE_SIZE = int(final.headers.get('Content-Length', 0))
    BLOCK_SIZE = 1024*1024

    name_raw = final.headers['Content-Disposition']
    filename_index = name_raw.index('filename=') + len('filename=')
    filename = name_raw[filename_index:].strip('"')

    if not os.path.exists('downloads'):
        os.mkdir('downloads')
    with open(f'downloads/{filename}', 'wb') as f:
        BYTES_READ = 0
        for chunk in final.iter_content(BLOCK_SIZE):
            f.write(chunk)
            BYTES_READ += len(chunk)
            callback(FILE_SIZE, BYTES_READ)
