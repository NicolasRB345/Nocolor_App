import customtkinter as ctk
from ui.home import Home
from ui.imageconverted import ImageConverted
import sys
import os


def resource_path(relative_path):
    #Obtém o caminho absoluto para o recurso, funciona para dev e para PyInstaller
    try:
        # PyInstaller cria uma pasta temporária e armazena o caminho em _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        # Se não estiver rodando como .exe, o base_path é o diretório normal
        base_path = os.path.abspath(".")
    
    return os.path.join(base_path, relative_path)


class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.geometry("500x600")
        self.title("Nocolor - Remove Background")
        self.iconbitmap(resource_path("assets/icone.ico"))
        self.resizable(False, False)

        self.home = Home(self, self.show_removed_background)
        self.imageconverted = ImageConverted(self, self.show_home_frame)

        self.home.pack(fill="both", expand=True)
        
    def show_removed_background(self, image_path):
        self.home.pack_forget()
        self.imageconverted.update_image(image_path) 
        self.imageconverted.pack(fill="both", expand=True)

    def show_home_frame(self):
        self.imageconverted.pack_forget()
        self.home.pack(fill="both", expand=True)


if __name__ == '__main__':
    app = App()
    app.mainloop()