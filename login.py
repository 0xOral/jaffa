import tkinter as tk
import main
import customtkinter as ctk
from PIL import Image, ImageTk
from datetime import datetime
import sys
import getopt
import hashlib
import random
import time
import pyttsx3


class LoginPage:
    def __init__(self, master: ctk.CTk):
        self.master = master
        self.master.geometry("600x440")
        self.master.title('Login')
        self.flag = 1
        self.master.bind("<Return>",self.on_enter)
        img1 = ImageTk.PhotoImage(Image.open("./data/pal.jpg"))
        label1 = ctk.CTkLabel(self.master, image=img1)
        label1.pack()
        img4 = ImageTk.PhotoImage(Image.open("./data/pattern.png"))

        # creare input frame
        self.frame = ctk.CTkFrame(label1, width=320, height=360, corner_radius=25)
        self.frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        background_label = ctk.CTkLabel(self.frame, image=img4)
        background_label.place(x=0, y=0)

        label2 = ctk.CTkLabel(self.frame, text="Elsonbaty", font=('Cairo play', 20))
        label2.place(relx=0.4, rely=0.1)

        self.username_entry = ctk.CTkEntry(self.frame, width=220, placeholder_text='Username')
        self.username_entry.place(x=50, y=110)

        self.password_entry = ctk.CTkEntry(self.frame, width=220, placeholder_text='Password', show="*")
        self.password_entry.place(x=50, y=165)

        label3 = ctk.CTkLabel(self.frame, text="ادعو لاخواننا في غزة", font=('Cairo play', 12))
        label3.place(x=155, y=195)

        copyrights = ctk.CTkLabel(self.frame, text="Copyright © 2023 by sigmas", font=("Cairo Play", 10))
        copyrights.place(x=2, y=340)

        # buttons and images
        Submit_button = ctk.CTkButton(self.frame, width=220, text="Submit", command=self.submit, corner_radius=15)
        Submit_button.place(x=50, y=240)

        img2 = ctk.CTkImage(Image.open("./data/go.png"))
        img3 = ctk.CTkImage(Image.open("./data/go.png"))

        login_button = ctk.CTkButton(master=self.frame, image=img2, text="Login", width=100, height=20,
                                     compound="left", fg_color='white', text_color='black',
                                     command=self.login, hover_color='#AFAFAF')
        login_button.place(x=50, y=290)

        Signup_button = ctk.CTkButton(master=self.frame, image=img3, text="Sign Up", width=100, height=20,
                                      compound="left", fg_color='white', text_color='black',
                                      hover_color='#AFAFAF', command=self.signup)
        Signup_button.place(x=170, y=290)
    def on_enter(self, event):
        self.submit()
        
    def submit(self):
        uname = self.username_entry.get()
        passwd = hash(self.password_entry.get())
        if self.flag == 1:
            if check(uname, passwd):
                self.master.destroy()
                main.play(uname)
                print(f"hi {uname}")

            else:
                self.nouseralert = ctk.CTkLabel(master=self.master, text='incorrect username or password! please try again',
                                           font=('Cairo play', 12))
                self.nouseralert.place()
                self.login()
        else:
            if (add_email(uname, passwd)):
                print(f"{uname} created.")
                self.login()
            else:
                print("")
        
    def login(self):
        ctk.CTkEntry.destroy(self.password_entry)
        ctk.CTkEntry.destroy(self.username_entry)
        self.username_entry = ctk.CTkEntry(self.frame, width=220, placeholder_text='Username')
        self.username_entry.place(x=50, y=110)

        self.password_entry = ctk.CTkEntry(self.frame, width=220, placeholder_text='Password', show="*")
        self.password_entry.place(x=50, y=165)
        self.flag = 1

    def signup(self):
        ctk.CTkEntry.destroy(self.password_entry)
        ctk.CTkEntry.destroy(self.username_entry)
        self.username_entry = ctk.CTkEntry(self.frame, width=220, placeholder_text='New Username')
        self.username_entry.place(x=50, y=110)

        self.password_entry = ctk.CTkEntry(self.frame, width=220, placeholder_text='New Password', show="*")
        self.password_entry.place(x=50, y=165)
        self.flag = 0
        
def check(uname, passwd):
    with open("data\\db.csv", 'r') as file:
        for x in file.readlines():
            x = x.split()
            if x[0][x[0].index(':')+1:] == uname and x[3] == passwd:
                return 1
    return 0

def add_email(uname, passwd, host='guest'):
    try:
        with open("data\\db.csv", 'a') as file:
            time = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
            file.write(f"{host}:{uname} {time} {passwd} /home/{uname}\n")

        return 1
    except Exception as err:
        return err

def _eencode(password, shift=20):
    encrypted_password = ""
    password =  str(len(password)) + str(chr(len(password)*2)) + str(chr(len(password)*23)) + str(password[0]) + password + str(password[0])
    for char in password:
        if char.isalpha():
            encrypted_char = chr((ord(char) + shift) % 4)
            encrypted_password += encrypted_char
        else:
            encrypted_password += str(ord(char)+4)
    for char in password:
        if char.isalpha():
            encrypted_char = chr((ord(char) + 10) % 3)
            encrypted_password += encrypted_char
        else:
            encrypted_password += str(ord(char)+4)
    return "#" + encrypted_password

def hash(password): return hashlib.sha256(password.encode('utf-8')).hexdigest()
    
def _getopt():
    if len(sys.argv) < 5: return 0
    username = password = ''
    command_list = sys.argv[1:]
    options = "u:p:"
    long_options = ["username", "password"]
    try:
        arguments, values = getopt.getopt(command_list, options, long_options)
        for current_arg, current_val in arguments:
            if current_arg == '-u' or current_arg == '--username': username = current_val
            if current_arg == '-p' or current_arg == '--password': password = current_val
    except getopt.error as err: print(err)
    return (username, password)
    
def play(back=1):
    if back:
        arguments = _getopt()
        if arguments:
            name, passwd = arguments
            if (check(name, hash(passwd))): main.play(name)
            else: print("wrong password or usernmae")
            exit()
        
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("dark-blue")
    
    root = ctk.CTk()
    LoginPage(root)
    root.mainloop()

if __name__ == "__main__":
    play()
