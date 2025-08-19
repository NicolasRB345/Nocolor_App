import customtkinter as ctk
from PIL import Image
from tkinter import filedialog
from removing import remove_background as backend_remove
import threading
import queue
import sys
import os


def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)


class Home(ctk.CTkFrame):
    def __init__(self, master, go_to_image_converted):
        super().__init__(master)
        self.go_to_image_converted = go_to_image_converted
        self.caminho_input = None

        CAMINHO_LOYOUT = resource_path("assets/homeLoyout.png") 
        image_loyout_home = Image.open(CAMINHO_LOYOUT)

        logo_img = ctk.CTkImage(light_image=image_loyout_home, size=(500, 600))
        logo_label = ctk.CTkLabel(master=self, image=logo_img, text="")
        logo_label.pack(fill="both", expand=True)

        self.imagetoconvert = ctk.CTkButton(
            self, text="Click here to upload\nyour image 🖼️",
            width=30, height=120, fg_color="grey", text_color="black",
            font=("Arial", 15), corner_radius=10, border_width=2,
            border_color='black', command=self.upload_image
        )
        self.imagetoconvert.place(x=170, y=340)

        self.buttomremove = ctk.CTkButton(
            self, text='Remove Background', fg_color="#bf9900",
            width=150, height=30, font=("Arial", 15, "bold"),
            corner_radius=10, command=self.start_removal
        )
        self.buttomremove.place(x=165, y=530)

        self.loading_label = ctk.CTkLabel(self, text="", font=("Arial", 16, "bold"))
        self.progress_bar = ctk.CTkProgressBar(self, width=250, mode='indeterminate')

    def upload_image(self):
        path = filedialog.askopenfilename(
            title="Choose your image",
            filetypes=[("Imagens", "*.png *.jpg *.jpeg")]
        )
        if path:
            self.caminho_input = path
            imagem = Image.open(self.caminho_input)
            imagem.thumbnail((167, 167))
            imagem_ctk = ctk.CTkImage(light_image=imagem, size=imagem.size)
            self.imagetoconvert.configure(image=imagem_ctk, text='')
            self.imagetoconvert.image = imagem_ctk

    def start_removal(self):
        if self.caminho_input:
            self.loading_label.place(x=175, y=550)
            self.progress_bar.place(x=125, y=575)
            self.progress_bar.start()

            self.imagetoconvert.configure(state="disabled")
            self.buttomremove.configure(state="disabled")

            self.result_queue = queue.Queue()
            thread = threading.Thread(
                target=self.run_background_removal,
                args=(self.caminho_input, self.result_queue)
            )
            thread.start()
            self.check_queue()

    def run_background_removal(self, input_path, result_queue):
        caminho_output = backend_remove(input_path)
        result_queue.put(caminho_output)

    def check_queue(self):
        try:
            result = self.result_queue.get(block=False)
            if result:
                self.progress_bar.stop()
                self.loading_label.place_forget()
                self.progress_bar.place_forget()
                self.imagetoconvert.configure(state="normal")
                self.buttomremove.configure(state="normal")
                self.go_to_image_converted(result)
        except queue.Empty:
            self.after(100, self.check_queue)