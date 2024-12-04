import re
import requests
import sqlite3
import tkinter as tk
from tkinter import messagebox
# https://csie.ncut.edu.tw/content.php?key=86OP82WJQO
global URL
form = tk.Tk()
form.title('聯絡資訊爬蟲')
form.geometry('640x480')
form.resizable(0, 0)
form.config(bg='#f0f0f0', cursor="dot")
form.attributes("-alpha", 1)
form.resizable(1, 1)


def error(t):
    messagebox.showerror("網路錯誤", t)


def click():
    '''request url'''
    text.delete(0.0, tk.END)
    URL = url.get()

    try:
        response = requests.get(URL)
        response.raise_for_status()
    except requests.exceptions.HTTPError as err:
        messagebox.showerror("網路錯誤", err.response.status_code)

    text.insert(tk.END, f"{'姓名':　<5}{'職稱':　<15}{'Email':　<15}")
    text.insert(tk.END, f"{'\n':-<71}"+"\n")
    pattern = re.compile(r'<div class="member_name"><a href="[^"]+">([^<]{3})')
    name = pattern.findall(response.text)
    pattern = re.compile(r'<div class="member_info_content">([^<]*教[^<]*)')
    title = pattern.findall(response.text)
    pattern = re.compile(r'mailto://([^"]+)')
    email = pattern.findall(response.text)

    conn = sqlite3.connect('contacts.db')
    cursor = conn.cursor()
    cursor.execute(
        '''CREATE TABLE IF NOT EXISTS contacts(
            iid INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, title TEXT,\
email TEXT)''')
    for i in range(len(name)):
        cursor.execute(
            "INSERT INTO contacts(name, title, email) VALUES(?, ?, ?)",
            (name[i], title[i], email[i])
        )
    cursor.execute("SELECT * FROM contacts")
    contacts = cursor.fetchall()
    for c in contacts:
        text.insert(tk.END, f"{c[1]:　<5}{c[2]:　<15}{c[3]:　<15}{"\n"}")

    cursor.execute("DELETE FROM contacts")
    conn.commit()
    cursor.close()
    conn.close()


labelframe = tk.LabelFrame(borderwidth=0)
labelframe.grid(row=0, column=0, padx=0, pady=0, sticky="nsew")

label = tk.Label(labelframe, text="URL:")
label.grid(row=0, column=0, padx=15, pady=10)

url = tk.Entry(labelframe)
url.grid(row=0, column=1, padx=5, pady=10, sticky="ew")
labelframe.grid_columnconfigure(1, weight=1)

button = tk.Button(labelframe, text="抓取", command=click)
button.grid(row=0, column=2, padx=15, pady=10)
button.config(width=10, height=0, borderwidth=0, bg="#fdfdfd", relief="sunken")


labelframe2 = tk.LabelFrame(borderwidth=0, bg="black")
labelframe2.grid(row=1, column=0, padx=10, pady=15, sticky="nsew")

text = tk.Text(labelframe2, bg="white")
text.grid(row=0, column=0, sticky="nsew")

labelframe2.grid_rowconfigure(0, weight=1)
labelframe2.grid_columnconfigure(0, weight=1)

yscrollbar = tk.Scrollbar(command=text.yview)
text.configure(yscrollcommand=yscrollbar.set)
yscrollbar.grid(row=1, column=1, sticky="nsew")


form.rowconfigure(1, weight=1)  # frame2
form.columnconfigure(0, weight=1)  # all frame
form.mainloop()
