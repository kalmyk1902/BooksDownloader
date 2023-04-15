"""

© Copyright 2023 Kalmyk1902
Распространяется по лицензии MIT
main.py: графический интерфейс программы
и взаимодействие с поиском


"""
#импортируем нужные библиотеки
import getfile
import threading
import tkinter as tk
from tkinter import ttk, messagebox

#функция поиска книг
def getvalues():
    lis = getfile.pdf(char.get(), form.get()) #ищем книги по нужному запросу (см. getfile.py)

    #обновление окна результатов
    results.configure(state='normal') #временное включение окна
    results.delete('1.0', tk.END) #очистка окна
    results.insert(tk.END, lis) #вставка результатов в окно
    results.configure(state='disabled') #отключение окна

    if lis != 'Мы ничего не нашли :(' and lis != 'Нет подключения к интернету!': #если книги найдены успешно...
        NEW_LIST = [] #создаем список значений для выбора книги
        choose.configure(state='readonly') #включаем список значений
        for i, j in enumerate(lis.split('\n'), 1): #берем из результата номера значений до пробела в списке
            NEW_LIST.append(i) #записываем их в список
        choose.configure(values=NEW_LIST) #обновляем список в программе
        downloadbtn.configure(state='enabled') #включаем кнопку скачивания
    else: #в других случаях (ничего не найдено / нету интернета)
        choose.configure(state='disabled') #выключаем список
        downloadbtn.configure(state='disabled') #выключаем кнопку скачивания

#функция обновления шкалы прогресса
def update_progress(total_size, bytes_read):
    progress['value'] = bytes_read / total_size * 100 #высчитываем процент скачанного по формуле: размер скачанного / полный размер файла * 100
    progress.update() #обновляем шкалу

    if bytes_read >= total_size: #когда размер скачанного сравняется с полным размером файла
        messagebox.showinfo('Book Downloader', 'Скачивание книги завершено') #выдаем сообщение об успешном скачивании

#функция скачивания
def download():
    CHOOSED = choose.get() #берем выбранный номер книги
    if CHOOSED: #если что то выбрано...
        try: #пробуем выполнить код без ошибок
            downloadbtn.configure(state='disabled') #временно выключаем кнопку скачивания
            getfile.send(CHOOSED, update_progress) #скачиваем файл (см. getfile.py)
            downloadbtn.configure(state='enabled') #после скачивания обратно включаем кнопку
        except: #при возникновении ошибки (чаще всего отсутствие интернета)
            messagebox.showerror('ERROR!', 'Нет подключения к интернету!') #выдаем сообщение об ошибке


#функции запуска потоков
def start_get():
    threading.Thread(target=getvalues).start()

def start_download():
    threading.Thread(target=download).start()

#потоки используются чтобы программа не зависала при нажатии кнопок
#а нормально продолжала работать

#создаем списки: 1. первых букв в названии книги, 2. номер класса
letters = ['І','А','Б','В','Г','Д','З','И','К','Л','М','Н','О','П','Р','С','Т','Ф','Х','Ч']
digits = [1,2,3,4,5,6,7,8,9,10,11]

root = tk.Tk() #создаем корневую переменную окна программы

root.title('Book Downloader') #задаем ей имя
root.geometry('600x700') #размеры окна
root.iconbitmap('etc/icon.ico') #иконку

title = ttk.Label(root, text='СКАЧАТЬ УЧЕБНИК', font=('Arial Bold', '15', 'bold')) #название программы
title.place(relx=0.3, rely=0.14) #размещаем
instr = ttk.Label(root, text='Выберите настройки для поиска учебников.\nЗатем выберите и скачайте учебник') #инструкции
instr.place(relx=0.25, rely=0.26) #размещаем
txt1 = ttk.Label(root, text='Буква:') #текст к списку букв
txt2 = ttk.Label(root, text='Класс:') #текст к списку классов
choose_txt = ttk.Label(root, text='Выбрать:') #текст к выбору книги 
char = ttk.Combobox(root, values=letters, width=6, state='readonly') #выбор буквы
form = ttk.Combobox(root, values=digits, width=6, state='readonly') #выбор класса
choose = ttk.Combobox(root, width=6, state='disabled', values=[]) #выбор книги
char.place(relx=0.2, rely=0.4) #размещаем их всех...
txt1.place(relx=0.2, rely=0.36)
form.place(relx=0.65, rely=0.4)
txt2.place(relx=0.65, rely=0.36)
choose.place(relx=0.43, rely=0.4)
choose_txt.place(relx=0.43, rely=0.36)
btn = ttk.Button(root, text='Найти', command=start_get) #кнопка поиска книг
btn.place(relx=0.42, rely=0.5) #размещаем
downloadbtn = ttk.Button(root, text='СКАЧАТЬ', state='disabled', command=start_download) #кнопка скачивания файла
results = tk.Text(root, width=48, height=6, state='disabled') #окно результатов поиска
progress = ttk.Progressbar(root, length=360, mode='determinate') #шкала прогресса
results.place(relx=0.11, rely=0.6) #размещаем их всех...
downloadbtn.place(relx=0.42, rely=0.9)
progress.place(relx=0.2, rely=0.82)

root.mainloop() #запускаем программу