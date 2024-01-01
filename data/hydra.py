import customtkinter as ctk
# import login
# import main
# from data import db

class hydra:
    def __init__(self):
        
        self.root = ctk.CTk()
        self.level = 1
        self.root.title("hydra list")
        self.root.geometry("250x395")
        
        self.frame = ctk.CTkFrame(border_width=0,master=self.root, height=400, width=250)
        self.frame.grid(padx=1,pady=1)
        
        self.output_area = ctk.CTkTextbox(master=self.frame, font=('Trebuchet MS', 25),
                                               fg_color='#10305c',text_color="#da2020", wrap=ctk.WORD, height=360, width=245)
        self.output_area.grid(padx=1,pady=1)
        
        self.entry = ctk.CTkEntry(master=self.frame, width=245, placeholder_text='guess a password')
        self.entry.grid(padx=1,pady=2)
        self.entry.bind("<Return>", self.on_enter)
        
        with open("data\\hydra_list.txt", 'r') as file:
            for x in file.readlines():
                if isinstance(x,str): self.output_area.insert(ctk.END, f"{x}")

        self.output_area.configure(state='disabled')
        self.root.mainloop()
        
    def on_enter(self, event):
        passwd = self.entry.get()
        if not passwd: return  
        if passwd == "exit":
            self.root.destroy()  
            return
        self.output_area.configure(state='normal')
        with open("data\hydra_list.txt", 'a') as file: 
            file.writelines(passwd+'\n')
        self.output_area.insert(ctk.END, passwd+'\n')
        self.output_area.yview(ctk.END)
        self.entry.delete(0, ctk.END)
        self.output_area.configure(state='disabled')