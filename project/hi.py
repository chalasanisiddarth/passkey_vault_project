from curses.textpad import Textbox
from functools import partial
import sqlite3
import hashlib

import tkinter as tk
from tkinter import CENTER, Button, Entry, Label, Tk, filedialog, Text
from tkinter import *
import os
from tkinter import simpledialog
from turtle import bgcolor

from numpy import pad

window=Tk()
window.title("Passkey vault")

with sqlite3.connect('password.db') as conn:
    cur=conn.cursor()
    cur.execute("""CREATE TABLE IF NOT EXISTS passkey(
                pass text
                )""")
    conn.commit()

with sqlite3.connect('password.db') as conn:
    cur=conn.cursor()
    cur.execute("""CREATE TABLE IF NOT EXISTS details(
                id INTEGER PRIMARY KEY,
                website NOT NULL,
                user_id NOT NULL,
                passkey NOT NULL
                )""")
    conn.commit()

'''
def popup(str):
    
    return simpledialog.askstring("Enter Details", str)
            

#Create Password screen
def create_passkey():
    window.geometry("300x300")

    l=Label(window, text="Enter new login key")
    l.config(anchor=CENTER)
    l.pack()

    txt=Entry(window, width=30)
    txt.pack()
    
    l1=Label(window, text="Re-Enter new login key")
    l1.config(anchor=CENTER)
    l1.pack()

    txt1=Entry(window, width=30)
    txt1.pack()

    l2=Label(window)

    def save_passkey():
        key=txt.get()
        if txt.get()==txt1.get():
            cur.execute("INSERT INTO passkey (pass) VALUES(?)", (key,))
            conn.commit()
            vault()
        else:
            l2.config(text="Passwords Do not match")
        



    button= Button(window, text="Save", pady=20, command=save_passkey)
    button.pack()

def get_passkey():
    cur.execute("SELECT rowid,* FROM passkey WHERE rowid=1")
    conn.commit()
    return cur.fetchall()[0][1]
    

#Login Screen 
def login_screen():
    for widget in window.winfo_children():
        widget.destroy()

    window.geometry("300x300")

    l=Label(window, text="Enter login key")
    l.config(anchor=CENTER)
    l.pack()

    l2=Label(window)
    l2.pack()

    text=Entry(window, width=30)
    text.pack()


    def check_password():
        password=get_passkey()

        if password==text.get():
            vault()
        else:
            text.delete(0, 'end')
            l2.config(text="Passwords do not match")



    button= Button(window, text="Submit", pady=5, padx=5,command=check_password)
    button.pack()

#Password Vault Screen
def vault():
    for widget in window.winfo_children():
        widget.destroy()

    #Adding an entry into the database
    def add_entry():
        
        sample1="Enter the website name"
        sample2="Enter your user id"
        sample3="Enter your password"

        website=popup(sample1)
        userid=popup(sample2)
        passkey=popup(sample3)

        cur.execute("INSERT INTO details (website,user_id,passkey)VALUES(?,?,?)", (website,userid,passkey,))
        conn.commit()

        vault()
    
    def delete_entry(data):


        cur.execute("DELETE FROM details WHERE rowid=(?)", (data,))
        conn.commit()
        vault()

        
        

    def reset_passkey():
        for widget in window.winfo_children():
            widget.destroy()
        
        l2=Label(window, text="Enter current login key")
        l2.config(anchor=CENTER)
        l2.pack()

        txt2=Entry(window, width=30)
        txt2.pack()

        l3=Label(window)
        l3.pack()

        window.geometry("400x400")
        l=Label(window, text="Enter new login key")
        l.config(anchor=CENTER)
        l.pack()

        txt=Entry(window, width=30)
        txt.pack()
    
        l1=Label(window, text="Re-Enter new login key")
        l1.config(anchor=CENTER)
        l1.pack()

        txt1=Entry(window, width=30)
        txt1.pack()

        def reset_save():
            if txt2.get()==get_passkey():
                if txt.get()==txt1.get():
                    reset=txt.get()
                    cur.execute("DELETE FROM passkey WHERE rowid=1")
                    cur.execute("INSERT INTO passkey VALUES(?)", (reset,))
                    conn.commit()
                    login_screen()
            else:
                txt2.delete(0, 'end')
                l2=Label(window)
                l2.config(text="Passwords do not match")
                l2.pack()



        button= Button(window, text="Reset", pady=20, command=reset_save)
        button.pack()


    
    window.geometry("950x300")
    
    l=Label(window, text="Welcome to the Password Vault")
    l.grid(padx=10, pady=10)

    btn=Button(window, text='+', command=add_entry)
    btn.grid(padx=20)


    btn1=Button(window, text="Reset Passkey", command=reset_passkey)
    btn1.grid(padx=20)

    l1=Label(window, text="Website")
    l1.grid(row=8, column=0, padx=100)
    l2=Label(window, text="User ID")
    l2.grid(row=8, column=1, padx=100)
    l3=Label(window, text="Password")
    l3.grid(row=8, column=2, padx=100)

    cur.execute("SELECT * FROM details")
    data=cur.fetchall()
    if data!=None:
        for i in range(0,len(data)):
            l4=Label(window, text=(data[i][1]))
            l4.grid(row=i+11, column=0, padx=100)
            l5=Label(window, text=(data[i][2]))
            l5.grid(row=i+11, column=1, padx=100)
            l6=Label(window, text=(data[i][3]))
            l6.grid(row=i+11, column=2, padx=100)
            btn2=Button(window, text="Delete", command=partial(delete_entry, data[i][0])) #command=partial(delete_entry,data[i+1]))
            btn2.grid(row=i+11, column=3, padx=2)
            

cur.execute("SELECT * FROM passkey")
data=cur.fetchall()
conn.commit()
if data:
    login_screen()
else:
    create_passkey()


window.mainloop()

'''

cur.execute("DELETE FROM details WHERE id=1")
cur.execute("SELECT * FROM details")
data=cur.fetchall()
for i in data:
    print(i)
conn.commit()


