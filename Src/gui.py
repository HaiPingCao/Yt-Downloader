from customtkinter import *

set_appearance_mode("Dark")

class App(CTk):
     WIDTH = 800
     HEIGHT = 600
    
     def __init__(self):
        super().__init__()
        self.build_ui()
        
     
     def start(self):
        self.mainloop()

     def build_ui(self):
          self.title("YTMA")
          self.geometry(f"{App.WIDTH}x{App.HEIGHT}")
          self.update()
          
          
          '''============Main zone============'''
          self.L_zone = CTkFrame(
               master=self, 
               border_width=1,
               width=App.WIDTH*2/3, 
               )
          self.R_zone = CTkFrame(
               master=self, 
               border_width=2,
               width=App.WIDTH*2/3, 
               )
          
          self.L_zone.pack(side=LEFT, expand=True, fill=BOTH)
          self.R_zone.pack(side=LEFT, expand=True, fill=BOTH)

          '''============Search zone [MZ]============'''
          
          self.Search_zone = CTkFrame(
               master=self.L_zone, 
               border_width=1,
               height=App.HEIGHT*3/4,
               )
          self.Search_zone.pack(side=TOP, expand=True, fill=BOTH)

          entry = CTkEntry(master=self.Search_zone, placeholder_text="Enter URL", width=400,)
          button = CTkButton(master=self.Search_zone, text="Search", width=100, command=lambda: print(entry.get()))
          entry.pack(side=LEFT, expand=True, fill=X)
          # entry.place(sticky='n')
          button.pack(side=LEFT, expand=False)

          '''============Control zone [MZ]============'''
          self.control_zone = CTkFrame(
               master=self.L_zone, 
               border_width=1, 
               )
          self.control_zone.pack(side=TOP, expand=True, fill=BOTH)
          
          self.progressbar = CTkProgressBar(master=self.control_zone, width=300, mode="determinate")
          self.slider = CTkSlider(master=self.control_zone, width=100, from_=0, to=1, command=lambda x: self.progressbar.set(x))
          self.slr = CTkButton(master=self.control_zone, text="slr", command=lambda: self.slider.set(0.5))
          
          
          self.progressbar.pack(side=LEFT, expand=True)
          self.slider.pack(side=LEFT, expand=False)
          self.slr.pack(side=LEFT, expand=False)




if __name__ == "__main__":
     app=App()
     app.start()