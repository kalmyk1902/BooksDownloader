import getfile
import threading
import tkinter as tk
from tkinter import ttk, messagebox

def getvalues():
    lis = getfile.pdf(char.get(), form.get())

    results.configure(state='normal')
    results.delete('1.0', tk.END)
    results.insert(tk.END, lis)
    results.configure(state='disabled')

    if lis != 'Мы ничего не нашли :(' and lis != 'Нет подключения к интернету!':
        NEW_LIST = []
        choose.configure(state='readonly')
        for i, j in enumerate(lis.split('\n'), 1):
            NEW_LIST.append(i)
        choose.configure(values=NEW_LIST)
        downloadbtn.configure(state='enabled')
    else:
        choose.configure(state='disabled')
        downloadbtn.configure(state='disabled')

def update_progress(total_size, bytes_read):
    progress['value'] = bytes_read / total_size * 100
    progress.update()

    if bytes_read >= total_size:
        messagebox.showinfo('Book Downloader', 'Скачивание книги завершено')

def download():
    CHOOSED = choose.get()
    if CHOOSED:
        try:
            downloadbtn.configure(state='disabled')
            getfile.send(CHOOSED, update_progress)
            downloadbtn.configure(state='enabled')
        except:
            messagebox.showerror('ERROR!', 'Нет подключения к интернету!')


def start_get():
    threading.Thread(target=getvalues).start()

def start_download():
    threading.Thread(target=download).start()


letters = ['І','А','Б','В','Г','Д','З','И','К','Л','М','Н','О','П','Р','С','Т','Ф','Х','Ч']
digits = [1,2,3,4,5,6,7,8,9,10,11]

root = tk.Tk()

root.title('Book Downloader')
root.geometry('600x700')
root.iconbitmap('etc/icon.ico')

title = ttk.Label(root, text='СКАЧАТЬ УЧЕБНИК', font=('Arial Bold', '15', 'bold'))
title.place(relx=0.3, rely=0.14)
instr = ttk.Label(root, text='Выберите настройки для поиска учебников.\nЗатем выберите и скачайте учебник')
instr.place(relx=0.25, rely=0.26)
txt1 = ttk.Label(root, text='Буква:')
txt2 = ttk.Label(root, text='Класс:')
choose_txt = ttk.Label(root, text='Выбрать:')
char = ttk.Combobox(root, values=letters, width=6, state='readonly')
form = ttk.Combobox(root, values=digits, width=6, state='readonly')
choose = ttk.Combobox(root, width=6, state='disabled', values=[])
char.place(relx=0.2, rely=0.4)
txt1.place(relx=0.2, rely=0.36)
form.place(relx=0.65, rely=0.4)
txt2.place(relx=0.65, rely=0.36)
choose.place(relx=0.43, rely=0.4)
choose_txt.place(relx=0.43, rely=0.36)
btn = ttk.Button(root, text='Найти', command=start_get)
btn.place(relx=0.42, rely=0.5)
downloadbtn = ttk.Button(root, text='СКАЧАТЬ', state='disabled', command=start_download)
results = tk.Text(root, width=48, height=6, state='disabled')
progress = ttk.Progressbar(root, length=360, mode='determinate')
results.place(relx=0.11, rely=0.6)
downloadbtn.place(relx=0.42, rely=0.9)
progress.place(relx=0.2, rely=0.82)

root.mainloop()