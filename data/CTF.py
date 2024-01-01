import customtkinter as ctk
import login
import main
from data import db

game_keys = {
    1: 'a5aaaf63ed98239e733575a2ed3d47b7ad6606d1143de8f6634f845741f2ceaa', # cat data\tasks
    2: '89fda3c317080e102ba50afd69f230abc3e18e3a582033bcf0146bcf68a45f40', # Jaffa hash
    3: 'bbc2e3a9e1e5f6cd00696efd3be5a562539c2f5f4db731519f341c4e989efe20', # atlantis
    4: 4,
    5: 5
}

class game:
    def __init__(self):
        
        self.root = ctk.CTk()
        self.level = 1
        self.root.title("jaffa CTF")
        self.root.geometry("400x235")
        self.text_color = '#daa520'
        
        self.frame = ctk.CTkFrame(border_width=0,master=self.root, height=235, width=400)
        self.frame.grid(padx=1,pady=1)
        
        self.output_area = ctk.CTkTextbox(master=self.frame, font=('Trebuchet MS', 15),
                                               fg_color='#202020',text_color="#daa520", wrap=ctk.WORD, height=200, width=400)
        self.output_area.grid(padx=1,pady=1)
        self.output_area.insert(ctk.END, db.game_onscraen)
        self.output_area.insert(ctk.END, db.level_1)
        self.output_area.configure(state='disabled')
        
        self.entry = ctk.CTkEntry(master=self.frame, width=395, placeholder_text='Enter the flage')
        self.entry.grid(padx=1,pady=2)
        self.entry.bind("<Return>", self.on_enter)

        self.root.mainloop()
        


    def on_enter(self, event):
        flag = self.entry.get()
        if not flag: return  
        self.output_area.configure(state='normal')
        if login.hash(flag.strip()) != game_keys[self.level]:
            self.output_area.insert(ctk.END, "worng flag.\n")
            self.output_area.yview(ctk.END)
            self.entry.delete(0, ctk.END)
            return
        self.text_color = main.Jaffa.increment_color("", self.text_color, 10)
        self.output_area.configure(text_color=self.text_color)
        self.level += 1
        next_level = db.levels[self.level]
        self.output_area.insert(ctk.END, next_level)
        self.output_area.yview(ctk.END)
        self.entry.delete(0, ctk.END)
        self.output_area.configure(state='disabled')
        
    def stop(self):
        self.root.destroy()
