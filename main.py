import customtkinter as ctk
from PIL import Image, ImageTk
from datetime import datetime
import login
import random
import time
import pyttsx3
from data import cli,db
from os import environ
environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'
from pygame import mixer
import pywinstyles
import pywinstyles.py_win_style

class Jaffa:
    
    def __init__(self, master:ctk.CTk, background_image_path, uname, *args):

        self.graph = {
            'Safad': ['Acre','Tiberias'],
            'Acre': ['Haifa','Nazareth','Tiberias','Safad'],
            'Haifa': ['Nazareth','Acre','Jinin','Tulkarm'],
            'Tiberias': ['Safad','Acre','Nazareth','Baysan'],
            'Nazareth': ['Baysan','Tiberias','Acre','Jinin','Haifa'],
            'Baysan': ['Tiberias','Nazareth','Jinin'],
            'Jinin': ['Tulkarm','Nablus','Baysan','Nazareth','Haifa'],
            'Nablus': ['Jinin','Tulkarm','Ramallah'],
            'Tulkarm': ['Haifa','Jinin','Nablus','jaffa'],
            'jaffa': ['Tulkarm','al-Ramla'],
            'Ramallah': ['Al-Quds','al-Ramla','Nablus'],
            'al-Ramla': ['jaffa','Ramallah','Al-Quds','Gaza'],
            'Al-Quds': ['al-Ramla','Ramallah','Hebron'],
            'Hebron': ['Al-Quds','Beersheba'],
            'Beersheba': ['Hebron','Gaza'],
            'Gaza': ['al-Ramla','Beersheba']
        }
        # (x,y)
        self.nodes={'Safad': (450,120),
                    'Acre': (326,130),
                    'Acre-Haifa1': (317.3,170.4),
                    'Acre-Haifa2': (310,178.2),
                    'Haifa': (292,177),
                    'Tiberias': (460,191),
                    'Nazareth': (390,219),
                    'Baysan': (455,301.2),
                    'Jinin': (395,308.8),
                    'Nablus': (384,405),
                    'Tulkarm': (310,367),
                    'jaffa': (229,464),
                    'Ramallah': (364,514),
                    'al-Ramla': (267,506.5),
                    'Al-Quds': (371.5,561),
                    'Hebron': (338.4,651),
                    'Beersheba': (236,748),
                    'Gaza': (137,665.6)}
        self.uname = uname
        self.master = master
        self.text_box_width = 383
        self.text_box_x = 617
        self.text_box_height = 1000
        self.text_box_y = 0
        self.mode = 'dark'
        self.palestine_list = self._palestine_list()
        self.font = 17
        self.Current_drawing = []
        self.command_history = []
        self.current_command_index = -1
        self.general_history = []
        self.oval_container = []
        self.current_song_index = 0
        self.is_any_speak = 0
        self.glass = 0 if "no glass" in args[0] else 1
        
        self.master.title("Jaffa")
        self.master.geometry('1920x1080')
        if self.glass:
            HWND = pywinstyles.py_win_style.detect(self.master)
            pywinstyles.py_win_style.paint(self.master)
            pywinstyles.ChangeDWMAccent(HWND, 5, 1)
            pywinstyles.ChangeDWMAccent(HWND, 19, 3, color=0x000005)
        self.master.bind("<F1>", self.sound_swich)
        self.master.bind("<F2>", self.play_next_song)
        master.bind("<F7>", self._glass)
        # master.bind("<F12>", lambda: exit*())
        
        # cli frame
        
        self.cli_frame = ctk.CTkFrame(border_width=0,master=self.master, height=1000, width=920)
        self.cli_frame.place(x=1000,y=0)
        
        self.entry = ctk.CTkEntry(master=self.cli_frame, width=910)
        self.entry.place(x=5,y=972)
        self.entry.bind("<Return>", self.on_enter)
        self.entry.bind("<Up>", self.on_Up)
        self.entry.bind("<Down>", self.on_Down)
        
        self.output_area = ctk.CTkTextbox(font=('', self.font),fg_color='#202020',text_color="#128612",master=self.cli_frame,
                                          wrap=ctk.WORD, height=956, width=910)
        self.output_area.place(x=5, y=10)
        self.output_area.insert(ctk.END, random.choice(db.onscraen))
        self.output_area.insert(ctk.END, f"{self.uname}@jaffa:~$ ")
        if self.uname != 'dev': self.output_area.configure(state='disabled')
        
        # text_Frame 

        self.Text_frame = ctk.CTkFrame(master, bg_color="#2E4053",border_color='red', height=1000, width=383)
        self.Text_frame.place(x=617,y=0)
        self.tx_canvas = ctk.CTkCanvas(self.Text_frame,width=383,highlightbackground='#2E4053', height=800)
        self.tx_canvas.place(x=0,y=0)
        
        self.bg_phto = ImageTk.PhotoImage(Image.open("data\\text_fram_background.jpg"))
        self.tx_canvas.create_image(0, 0, anchor=ctk.NW, image=self.bg_phto)     

        # Input frame
        self.input_frame = ctk.CTkFrame(self.Text_frame, bg_color="#2E4053", corner_radius=0, border_width=2, height=200, width=383)
        self.input_frame.place(x=0,y=800)

        # Label and CTkComboBox for "From" city
        city_Tlabel = ctk.CTkLabel(self.input_frame, text="From", font=("Cairo Play", 25))
        city_Tlabel.place(x=35, y=20)

        self.from_combobox = ctk.CTkComboBox(self.input_frame,border_width=2,corner_radius=10,border_color='#2E4053',
                                             values=self.palestine_list,width=170)
        self.from_combobox.place(x=130, y=33)
        
        # Label and CTkComboBox for "To" city
        city_Flabel = ctk.CTkLabel(self.input_frame, text="To", font=("Cairo Play", 25))
        city_Flabel.place(x=42, y=60)

        self.to_combobox = ctk.CTkComboBox(self.input_frame,border_width=2,corner_radius=10,border_color='#2E4053',
                                           values=self.palestine_list,width=170)
        self.to_combobox.place(x=130, y=75)

        # swiches wiki and wound
        self.wiki_swich = ctk.CTkCheckBox(self.input_frame,text='Search on Wikipedia')
        self.wiki_swich.place(x=30, y=130)

        self.sound_swich = ctk.CTkCheckBox(self.input_frame,text='Read the output')
        self.sound_swich.place(x=30, y=160)

        # Go button
        img = Image.open("data\\go_button_sympol.png")
        button = ctk.CTkButton(self.input_frame,text="GO",corner_radius=32,fg_color="#6f8f6f",
                            hover_color="#C850C0", border_color="#ccecff",width=80, command=self._Go,
                            border_width=2, image=ctk.CTkImage(dark_image=img, light_image=img))
        button.place(x=220, y=143)
        
        # copyrights
        
        copyrights = ctk.CTkLabel(self.input_frame,anchor='w', text="Copyright © 2023 by sigmas", font=("Cairo Play", 10))
        copyrights.place(x=127, y=0)
        
        # history
        
        self.history_frame = ctk.CTkFrame(master=self.master, height=80, width=1920)
        self.history_frame.place(x=0, y=1000)
        
        self.history = ctk.CTkTextbox(master=self.history_frame, wrap=ctk.WORD,corner_radius=7,
                                 height=70, width=1910,font=('', 17),fg_color="#342a2a"
                                 )
        self.history.place(x=5, y=5)
        if self.uname != 'dev': self.history.configure(state='disabled')
        
        # exit 
        
        img = Image.open("data\\exit.jpg")
        exit_button = ctk.CTkButton(fg_color='#148100',corner_radius=2, master=self.master,command=self.master.destroy,text='',width=30,
                                    image=ctk.CTkImage(dark_image=img, light_image=img))
        exit_button.place(x=970,y=0)
        # ______________________________ خريطه فلسطين _______________________________
        
        self.background_image = Image.open(background_image_path)
        self.background_photo = ImageTk.PhotoImage(self.background_image)

        self.canvas = ctk.CTkCanvas(self.master, width=self.background_image.width, height=self.background_image.height)
        # self.canvas.pack(expand=tk.YES, fill=tk.BOTH)
        
        self.canvas.place(width=self.background_image.width, height=self.background_image.height,x=0,y=0)
        self.canvas.create_image(0, 0, anchor=ctk.NW, image=self.background_photo)
        
        # self.draw_nodes()
        self.play_current_song(0,0.1)
        
    def sound_swich(self, event):
        if self.is_any_speak:
            mixer.music.pause()
            self.is_any_speak = 0
            action = f"ACTION: in {self.get_time()} {self.uname} pause sound.\n"
            self.insert_general_history(action)
        else:
            mixer.music.unpause()
            self.is_any_speak = 1
            action = f"ACTION: in {self.get_time()} {self.uname} resume sound.\n"
            self.insert_general_history(action)

    def on_Up(self, event):
        if self.current_command_index == len(self.command_history):
            print("black")
            self.current_command_index -= 1

        self.entry.delete(0,"end")
        self.entry.insert(ctk.END, self.command_history[self.current_command_index])
        if self.current_command_index != 0: self.current_command_index -= 1
        
    def on_Down(self, event):
        if self.current_command_index == len(self.command_history): return
        if self.current_command_index == 0:
            self.current_command_index += 1
        self.entry.delete(0,"end")
        self.entry.insert(ctk.END, self.command_history[self.current_command_index])
        if self.current_command_index != len(self.command_history): self.current_command_index += 1
    
    def on_enter(self, event):
        self.current_command_index = len(self.command_history)-1
        self.execute_command()

    def _glass(self, event):
        self.master.destroy()
        play("anas", "no glass" if self.glass else 0)

        # if self.glass: pywinstyles.apply_style(self.master, "dark")
        # else: pywinstyles.apply_style(self.master, "aero")
        
    def execute_command(self):
        command = self.entry.get()
        if not command: return  
        self.output_area.configure(state='normal')
        self.history.configure(state='normal')
        self.output_area.insert(ctk.END, f"{command}\n")
        self.command_history.append(command)
        result = self.process_command(command)
        self.display_result(result)
        self.output_area.insert(ctk.END, f"{self.uname}@jaffa:~$ ")
        self.entry.delete(0, ctk.END)
        if self.uname != 'dev': self.history.configure(state='disabled')
        if self.uname != 'dev': self.output_area.configure(state='disabled')
        self.current_command_index += 1

    def process_command(self, command: str):
        s_command = command.split() 
        if command == 'exit' or command == 'good bay' or command == 'quit' or command == 'bay' or command == 'اخرج': exit()
        elif command == 'clear' or command == 'cls' or command == 'امسح':
            self.output_area.delete('1.0', ctk.END)
            action = f"ACTION: in {self.get_time()} {self.uname} clean screan.\n"
            self.insert_general_history(action)
            return ""
        elif command[0] == '+':
            for x in range(command.count('+')): self.font += 1
            self.output_area.configure(font=('', self.font))
            return ""
        elif command[0] == '-':
            for x in range(command.count('-')): self.font -= 1
            self.output_area.configure(font=('', self.font))
            return ""
        elif command == 'clean screen' or command == 'clean all' or command == 'clean' or command == 'cls all' or command == 'cls screen':
            self.clean_screen()
            self.hide_nodes()
            return ""
        elif command == 'show time' or command == 'time': return self.get_time()
        elif command == 'show all nodes' or command == 'nodes' or command == "show nodes":
            self.draw_nodes()
            return ""
        elif command == 'hide all nodes' or command == 'hide nodes' or command == 'hide':
            self.hide_nodes()
            return "All nodes are hided."
        elif s_command[0] == 'whoami':
            if len(s_command) == 1: return self.uname
            return f'ERROR: Invalid argument/option - \'{command[7:]}\'.\nType "whoami" for usage.'
        
        ans = cli.getter(command, self.general_history, self.command_history, self.nodes, self.graph, self.uname)
        if isinstance(ans, str): return ans
        elif ans[0] == 'go':
            if len(ans) == 2: return ans[1]
            self.entry.delete(0, ctk.END)
            self.output_area.insert(ctk.END, "... ")
            self.Go(ans[1], ans[2], ans[3], ans[4])
            return f"welcom to {ans[2]}."
        elif ans[0] == 'adduser':
            login.add_email(ans[1],login.hash(ans[2]),self.uname)
            action = f"ACTION: in {self.get_time()} {self.uname} add user with name {ans[1]}.\n"
            self.insert_general_history(action)
            return f"done, user added successfully\nnew user is {ans[0]}."
        elif ans[0] == 'su':
            if len(ans) == 2: return ans[1]
            if login.check(ans[1], login.hash(ans[2])):
                self.uname = ans[1]
                return ""
            else:
                return f"wrong password or username try again."
        elif ans[0] == 'chpasswd':
            if self.change_password(ans[1],ans[2],ans[3],True if self.uname == "root" else False):
                return "password has been changed."
            elif not ans[2] and self.uname != "root": return "you don't have permissions. change to root or type the password for the user by -p"
            return "wrong password if you type the command right and the database hasn't crash."
        elif ans[0] == 'newcity':
            self.add_city(ans[1], ans[2], ans[3], ans[4])
            if ans[5]: self.draw_node(ans[1], int(ans[2]),int(ans[3]))
            return f"done, {ans[1]} added successfully in ({ans[2]},{ans[3]})."
        elif ans[0] == 'color':
            if ans[1] == 'reset' or ans[1] == '-r':
                self.output_area.configure(text_color="#128612",fg_color="#202020")
                self.history.configure(text_color="#cccccc",fg_color='#342a2a')
                self.mode = 'dark'
                return 'color has been reset'
            self.output_area.configure(text_color=ans[1])
            return f'color changed to {ans[1]}'
        elif ans[0] == 'mode':
            if ans[1] == 'light': 
                if self.mode == 'light': return "system mode is already ligh"
                ctk.set_appearance_mode("light")
                event = "system mode changed to light at " + self.get_time()
                self.mode = 'light'
                return event            
            elif ans[1] == 'dark':
                if self.mode == 'dark': return "system mode is already dark"
                ctk.set_appearance_mode("dark")
                event = "system mode changed to dark at " + self.get_time()
                self.mode = 'dark'
                return event   
            elif ans[1] == 'cmd':
                if self.mode == 'cmd': return "system mode is already cmd"
                self.output_area.configure(text_color="#ececec",fg_color='#0f0f0f')
                self.history.configure(text_color="#800909",fg_color='#3c3c3c')
                event = "system mode changed to cmd at " + self.get_time()
                self.mode = 'cmd'
                return event
            return ans[1]
        elif ans[0] == 'back':
            self.master.destroy()
            login.play()
            return 'bay'
        elif ans[0] == 'cat/passwd':
            with open("data/db.csv") as file: return file.read()
        elif ans[0] == 'music':
            if ans[1] == 'stop': 
                self.stop_music()
                return "music stoped."
            if len(ans) == 2: return ans[1]
            self.play_current_song(index=ans[1], volume=ans[2])
            return "music is running."
            
    def display_result(self, result):
        result += "\n"
        self.output_area.insert(ctk.END, result)
        self.output_area.yview(ctk.END)

    def increment_color(self,hex_color, increment):
        # Convert hex color to RGB
        r = int(hex_color[1:3], 16)
        g = int(hex_color[3:5], 16)
        b = int(hex_color[5:7], 16)

        # Increment RGB values
        r = min(255, r + increment)
        g = min(255, g - increment)
        b = min(255, b - increment)

        # Convert back to hex color
        new_hex_color = "#{:02x}{:02x}{:02x}".format(r, g, b)

        return new_hex_color
    
    def get_time(self):
        now = datetime.now()
        return now.strftime("%d/%m/%Y %H:%M:%S")

    def craete_line(self, x, y, delay=0.01, lenth=50, co=5):
        xx, yy = x[0], x[1]
        x_increment = (y[0]-x[0])/lenth
        y_increment = (y[1]-x[1])/lenth
        fil = '#00ffff'
        for zz in range(lenth):
            line = self.canvas.create_line(x[0],x[1],xx,yy, fill=fil, width=2)
            self.master.update()
            time.sleep(delay)
            xx = xx + x_increment
            yy = yy + y_increment
            fil = self.increment_color(fil,co)
            self.Current_drawing.append(line)

    def hide_nodes(self):
        for oval in self.oval_container:
            self.canvas.delete(oval)
        self.oval_container.clear()
    
    def draw_nodes(self):
        for node, coordinates in self.nodes.items():
            x, y = coordinates
            oval = self.canvas.create_oval(x - 10, y - 10, x + 10, y + 10, fill=self.random_color(), tags=node)
            self.oval_container.append(oval)
            
    def draw_node(self, name, x, y):
        oval = self.canvas.create_oval(x - 10, y - 10, x + 10, y + 10, fill=self.random_color(), tags=name)
        self.canvas.create_text(x, y - 20,font=("Bell MT Bold",12), text=name)
        self.oval_container.append(oval)
        
    def draw_lines(self, list):
        for x in range(0, len(list)-1):
            self.master.update()
            time.sleep(0.7)
            if list[x] == 'Acre' and list[x+1] == 'Haifa':
                A = self.nodes[list[x]]
                B = self.nodes['Acre-Haifa1']
                C = self.nodes['Acre-Haifa2']
                D = self.nodes[list[x+1]]
                
                line = self.craete_line(A, B, lenth=30, co=8)
                self.Current_drawing.append(line)
                line = self.craete_line(B, C, lenth=30, co=8)
                self.Current_drawing.append(line)
                line = self.craete_line(C, D, lenth=30, co=8)
                self.Current_drawing.append(line)
            elif list[x] == 'Haifa' and list[x+1] == 'Acre':
                A = self.nodes[list[x]]
                B = self.nodes['Acre-Haifa2']
                C = self.nodes['Acre-Haifa1']
                D = self.nodes[list[x+1]]
                
                line = self.craete_line(A, B, lenth=30, co=8)
                self.Current_drawing.append(line)
                line = self.craete_line(B, C, lenth=30, co=8)
                self.Current_drawing.append(line)
                line = self.craete_line(C, D, lenth=30, co=8)
                self.Current_drawing.append(line)
            else:    
                A = self.nodes[list[x]]
                B = self.nodes[list[x+1]]
                self.craete_line(A, B, 0.01)
        self.master.update()
    
    def add_city(self,name, x, y, ne):
        self.graph[name] = ne
        self.nodes[name] = (x,y)
        sucsses = []
        for x in ne:
            if x not in self.graph.keys(): 
                self.display_result(f"{x} is not a city in palestine.")
            else:
                self.graph[x].append(name)
                sucsses.append(x)
        action = f"ACTION: in {self.get_time()} {self.uname} add {name} city in ({x},{y}) and have a neighbours {sucsses}\n"
        self.insert_general_history(action)
        self.palestine_list = self._palestine_list()
        self.to_combobox.configure(values=self.palestine_list)
        self.from_combobox.configure(values=self.palestine_list)
    
    def change_password(self, uname, passwd, new_password, is_root):
        if passwd: passwd = login.hash(passwd)
        done = 0
        with open("data\\db.csv", 'r') as file:
            data = file.readlines()
            for i,x in enumerate(data):
                x = x.split()
                if x[0][x[0].index(':')+1:] == uname and (x[3] == passwd or is_root):
                    line = data[i].split()
                    line[3] = login.hash(new_password)
                    data[i] = ' '.join(line) + '\n'
                    done = 1
        if done:
            with open("data\\db.csv", 'w') as file:
                file.writelines(data)
                action = f"ACTION: in {self.get_time()} {self.uname} cahnge {uname} password.\n"
                self.insert_general_history(action)
                return 1
        return 0
        
    def BFS(self, From, To):
        visited = []
        queue = [[From]]
        while(queue):
            path = queue.pop(0)
            node = path[-1]
            if node in visited:
                continue
            visited.append(node)
            if node == To:
                return path 
            else:
                new_nodes = self.graph.get(node, [])
                for node2 in new_nodes:
                    new_path = path.copy()
                    new_path.append(node2)
                    queue.append(new_path)
            
    def random_color(self):
        return "#{:02x}{:02x}{:02x}".format(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
    
    def read(self, speach):
        engine = pyttsx3.init()
        engine.say(speach)
        engine.runAndWait()
        
    def WikiSearch(self, target):
        ctk.CTkCanvas.destroy(self.tx_canvas)
        if target == "Gaza":
            self.tx_canvas = ctk.CTkCanvas(self.Text_frame,width=383,highlightbackground='#2E4053', height=800)
            self.tx_canvas.place(x=0,y=0)
            self.bg_phto = ImageTk.PhotoImage(Image.open("data\\gaza.jpg"))
            self.tx_canvas.create_image(0, 0, anchor=ctk.NW, image=self.bg_phto)   
        else:   
            target_data = ctk.CTkLabel(self.Text_frame,width=360,height=600,text=db.WIKI[target],
                                        anchor='w', wraplength= 353, font=("Cairo Play", 16),
                                    )
            target_data.place(x=15, y=60)
        self.master.update()
    
    def _palestine_list(self):
        list = []
        for x in self.graph:
            list.append(x)
        return list
    
    def clean_screen(self):
        for x in self.Current_drawing:
            self.canvas.delete(x)
    
    def play_sound(self, file_path, volume=1):
        mixer.init()
        mixer.music.load(file_path)
        mixer.music.set_volume(volume)
        mixer.music.play()
        
    def _Go(self):
        To = self.to_combobox.get()
        From = self.from_combobox.get()
        self.Go(From, To)
        
    def Go(self, From, To, wiki=0, sound=0):
        if From == To:
            if not self.is_any_speak: self.play_sound(file_path="data\\sound\\You Serious.mp3")
            return 
            
        lst = self.BFS(From,To)
        if self.Current_drawing:
            self.clean_screen()
        print(lst)
        
        if self.wiki_swich.get() or wiki:
            self.WikiSearch(To)
            self.draw_lines(lst)
            if self.sound_swich.get() or sound:
                self.read(db.WIKI[To])
        elif (sound or self.sound_swich.get()) and (not self.wiki_swich.get() and not wiki):
            self.draw_lines(lst)
            self.read(f"welcome to {To}")
        else:
            self.draw_lines(lst)
        _lst = " -> ".join(lst)
        trip = f"TRIP: in {self.get_time()} {self.uname} start a trip From {From} To {To} by taking the path {{{_lst}}}\n"
        self.insert_general_history(trip)
        
    def insert_general_history(self, trip):
        self.history.insert(ctk.END, trip)
        self.general_history.append(trip)

    def play_next_song(self, event):
        # self.stop_music()
        self.current_song_index = (self.current_song_index + 1) % len(db.playlist)
        self.play_current_song()

    def play_current_song(self,index=0, volume=0.08):
        mixer.init()
        mixer.music.load(db.playlist[index if index else self.current_song_index])
        mixer.music.set_volume(volume)
        mixer.music.play(loops=999)
        mixer.music.rewind()
        self.is_any_speak = 1

    def stop_music(self):
        mixer.music.stop()
        self.is_any_speak = 0
        
def play(uname, *args, **kwargs):
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("dark-blue")
    
    root = ctk.CTk()
    root.attributes('-fullscreen', True)
    app = Jaffa(root, "data\\palestine_states.jpg", uname, args)
    root.mainloop()
    
if __name__ == "__main__":
    play("root")
