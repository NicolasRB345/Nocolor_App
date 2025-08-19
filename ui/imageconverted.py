import customtkinter as ctk
from PIL import Image
from tkinter import filedialog
import shutil
import os

class ImageConverted(ctk.CTkFrame):
    def __init__(self, master, go_to_home):
        super().__init__(master)
        self.go_to_home = go_to_home
        self.processed_image_path = None

        CAMINHO_LOYOUT = "assets\mainLoyout.png" 
        imageLoyout = Image.open(CAMINHO_LOYOUT)

        logo_img = ctk.CTkImage(light_image=imageLoyout, size=(500, 600))
        logo_label = ctk.CTkLabel(master=self, image=logo_img, text="")
        logo_label.pack(fill="both", expand=True)

        self.image_label = ctk.CTkLabel(
            self,
            fg_color="black",
            text="Your Image appears here",
            width=350, 
            height=400
            )
        self.image_label.place(x=80, y=50)

        download_button = ctk.CTkButton(
            self,
            text="Download 📥",
            fg_color="#bf9900",
            font=("Arial", 16, "bold"),
            command=self.download_image
        )
        download_button.place(x=185, y=470)

        back_button = ctk.CTkButton(
            self,
            text="Convert another Image",
            fg_color="green",
            command=self.go_to_home
        )
        back_button.place(x=183, y=515)

    def update_image(self, image_path):
        self.processed_image_path = image_path
        
        try:
            image = Image.open(image_path)
            
            image.thumbnail((400, 400)) #configure size to show
            
            ctk_image = ctk.CTkImage(light_image=image, size=image.size)
            
            # update label
            self.image_label.configure(image=ctk_image, text="")
            self.image_label.image = ctk_image
        except Exception as e:
            self.image_label.configure(text=f"Something went wrong when loading image:\n{e}")

    def download_image(self):
        if not self.processed_image_path:
            print("No images to save.")
            return

        suggested_fillename = os.path.basename(self.processed_image_path)
        
        save_path = filedialog.asksaveasfilename(
            initialfile=suggested_fillename,
            defaultextension=".png",
            filetypes=[("PNG file", "*.png"), ("All files", "*.*")]
        )

        if save_path:
            shutil.copy(self.processed_image_path, save_path)
            print(f"Image saved succesfully in: {save_path}")