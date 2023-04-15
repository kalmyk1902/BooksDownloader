"""

© Copyright 2023 Kalmyk1902
Распространяется по лицензии MIT
getfile.py: поиск книг на сайте и 
скачивание их


"""

#импортируем нужные библиотеки
import os
import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent

url = 'https://e-padruchnik.adu.by/' #создаем переменную с ссылкой
user = UserAgent().random #создаем переменную с пользователем, вошедшего на сайт

#метаданные запроса
headers = {
    'user-agent': user, #кто отправил запрос (в нашем случае рандомный браузер)
    'referer': url #кому отправили запрос (в нашем случае ссылка на сайт)
}

#функция поиска книги
def pdf(letter, digit):
    try: #пробуем выполнить код без ошибок
        global rows #создаем глобальную переменную результатов поиска (для того чтобы ее было видно в main.py)

        #создаем данные для отправки
        data = {
            'char': letter, #первая буква книги
            'class': digit, #номер класса
            'mode': 'char' #режим поиска (по букве)
        }

        lg = requests.post(url, data=data, headers=headers) #отправляем данные на сервер и получаем результаты поиска

        soup = BeautifulSoup(lg.content, 'html.parser') #создаем корневую переменную анализа данных
        tb = soup.find('table', {'id': 'booklist'}) #ищем в html коде таблицу со всеми найденными книгами
        rows = tb.select('tr[book-id]') #ищем все возможные книги и их id
        if not rows: #если книги не были найдены...
            return 'Мы ничего не нашли :(' #выходим из функции с сообщением об этом

        results = '' #создаем текстовую переменную
        for index, row in enumerate(rows): #на каждую книгу в списке найденных делаем следующее
            row.find('br').insert_before(' ') #ставим пробел между названием книги и ее авторами
            #вписываем результате в формате -> номер книги, название книги и ее авторы, год ее выпуска
            results += (f"{index + 1}. {row.select('td')[4].text} / {row.select('td')[2].text}\n")
        results = results[:-2] #последний пробел убираем чтобы не создавать проблем
        return results #выдаем в программу список найденных книг
    
    except requests.exceptions.ConnectionError: #если отсутствует интернет...
        return 'Нет подключения к интернету!' #выходим из функции с сообщением об этом
    
#функция скачивания книги    
def send(choice, callback):
    ch_result = rows[int(choice)-1] #запоминаем выбранный номер книги
    book_id = ch_result.get('book-id') #ищем id книги по этому номеру
    final = requests.post(url, data={'id': book_id, 'getbook': ''}, headers=headers, stream=True) #отправляем данные на сервер и начинаем качать книгу

    FILE_SIZE = int(final.headers.get('Content-Length', 0)) #получаем полный размер файла
    BLOCK_SIZE = 1024*1024 #ставим ограничение по размеру файла на каждую операцию (можно менять, сейчас стоит 1 МБ)

    name_raw = final.headers['Content-Disposition'] #ищем имя файла
    filename_index = name_raw.index('filename=') + len('filename=') #получаем его
    filename = name_raw[filename_index:].strip('"') #переводим из чисел в буквы название

    if not os.path.exists('downloads'): #если папки downloads нету...
        os.mkdir('downloads') #создаем её
    with open(f'downloads/{filename}', 'wb') as f: #создаем файл в этой папке
        BYTES_READ = 0 #создаем переменную размера скачанного и ставим значение на 0
        for chunk in final.iter_content(BLOCK_SIZE): #на каждую операцию скачивания файла делаем следующее
            f.write(chunk) #скачиваем содержимое файла
            BYTES_READ += len(chunk) #обновляем размер скачанного
            callback(FILE_SIZE, BYTES_READ) #обновляем шкалу прогресса в main.py
            #функция использует функцию для обновления шкалы прогресса чтобы обновлять ее там