#Password Manager Project
#CHALASANI SIDDARTH 
#HU21CSEN0101114
from functools import partial
import sqlite3
import hashlib

import tkinter as tk
from tkinter import CENTER, Button, Entry, Label, Tk, filedialog, Text
from tkinter import *
import os
from tkinter import simpledialog


window=Tk()
window.title("Passkey vault")

#table for the passkey
with sqlite3.connect('password.db') as conn:
    cur=conn.cursor()
    cur.execute("""CREATE TABLE IF NOT EXISTS passkey(
                pass text
                )""")
    conn.commit()

#table for the details
with sqlite3.connect('password.db') as conn:
    cur=conn.cursor()
    cur.execute("""CREATE TABLE IF NOT EXISTS details(
                id INTEGER PRIMARY KEY,
                website NOT NULL,
                user_id NOT NULL,
                passkey NOT NULL
                )""")
    conn.commit()


def popup(str):
    return simpledialog.askstring("Enter Details", str)
            

#creating the passkey
def create_passkey():
    window.geometry("300x150")

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

    #saving the created passkey in the database
    def save_passkey():
        key=txt.get()
        if txt.get()==txt1.get():
            cur.execute("INSERT INTO passkey (pass) VALUES(?)", (key,))
            conn.commit()
            login_screen()
        else:
            l2.config(text="Passwords Do not match")
        



    button= Button(window, text="Save", padx=2, command=save_passkey)
    button.pack()

#retrieving the passkey from database
def get_passkey():
    cur.execute("SELECT rowid,* FROM passkey WHERE rowid=1")
    conn.commit()
    return cur.fetchall()[0][1]
    

#Login Screen 
def login_screen():
    for widget in window.winfo_children():
        widget.destroy()

    window.geometry("300x120")

    l=Label(window, text="Enter login key")
    l.config(anchor=CENTER)
    l.pack()

    l2=Label(window)
    l2.pack()

    text=Entry(window, width=30)
    text.pack()

    #checking the login passkey
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
    #deleting an entry
    def delete_entry(data):
        for widget in window.winfo_children():
            widget.destroy()

        window.geometry("300x120")

        l=Label(window, text="Are you sure you want to delete?")
        l.config(anchor=CENTER)
        l.pack()

        def confirm_delete(data):
            cur.execute("DELETE FROM details WHERE rowid=(?)", (data,))
            conn.commit()
            vault()
        
        btn1= Button(window, text="Yes", padx=2,command=partial(confirm_delete,data,))
        btn1.pack()
        btn2= Button(window, text="No", padx=2,command=vault)
        btn2.pack()

        
    
    def edit_entries(data):
        for widget in window.winfo_children():
            widget.destroy()

        window.geometry("300x150")

        l=Label(window, text="What do you want to edit?")
        l.config(anchor=CENTER)
        l.pack()
        btn1= Button(window, text="Website", padx=2,command=partial(edit_website,data,))
        btn1.pack()
        btn2= Button(window, text="User ID", padx=2,command=partial(edit_userid,data,))
        btn2.pack()
        btn3= Button(window, text="Password", padx=2,command=partial(edit_password,data,))
        btn3.pack()
        
        
    def edit_website(data):
        sample1="Enter the website name"
        website=popup(sample1)

        cur.execute("UPDATE details SET website=(?) WHERE rowid=(?)", (website,data,))
        conn.commit()
        vault()
    
    def edit_userid(data):
        sample1="Enter the user id"
        userid=popup(sample1)

        cur.execute("UPDATE details SET user_id=(?) WHERE rowid=(?)", (userid,data,))
        conn.commit()
        vault()
    
    def edit_password(data):
        sample1="Enter the password"
        passkey=popup(sample1)

        cur.execute("UPDATE details SET passkey=(?) WHERE rowid=(?)", (passkey,data,))
        conn.commit()
        vault()
    
    def sign_out():
        for widget in window.winfo_children():
            widget.destroy()

        window.geometry("300x120")

        l=Label(window, text="Are you sure you want to signout?")
        l.config(anchor=CENTER)
        l.pack()

        def confirm_signout():
            login_screen()
        
        btn1= Button(window, text="Yes", padx=2,command=confirm_signout)
        btn1.pack()
        btn2= Button(window, text="No", padx=2,command=vault)
        btn2.pack()


    #resetting the passkey 
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

        #saving the reset passkey into database
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

        button= Button(window, text="Reset", padx=2, command=reset_save)
        button.pack()


    
    window.geometry("1020x300")
    
    l=Label(window, text="Welcome to the Password Vault")
    l.grid(padx=10, pady=10, column=1)

    btn1=Button(window, text="Reset Passkey", command=reset_passkey)
    btn1.grid(padx=20, row=1, column=4)

    b=Button(window, text="Sign Out",command=sign_out)
    b.grid(padx=10, pady=10,row=0, column=4)

    btn=Button(window, text='Add', command=add_entry)
    btn.grid(padx=20, row=2, column=1)

    #displaying the labels for website, userid and passowrd
    l1=Label(window, text="Website")
    l1.grid(row=10, column=0, padx=100)
    l2=Label(window, text="User ID")
    l2.grid(row=10, column=1, padx=100)
    l3=Label(window, text="Password")
    l3.grid(row=10, column=2, padx=100)

    #displaying the details
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
            btn2=Button(window, text="Delete", command=partial(delete_entry, data[i][0]))
            btn2.grid(row=i+11, column=3, padx=2)
            btn3=Button(window, text="Edit", command=partial(edit_entries, data[i][0]))
            btn3.grid(row=i+11, column=4, padx=2)
            

cur.execute("SELECT * FROM passkey")
data=cur.fetchall()
conn.commit()
if data:
    login_screen()
else:
    create_passkey()

window.mainloop()






