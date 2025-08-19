import os
from rembg import remove
from PIL import Image

def remove_background(input_path: str) -> str:

    output_folder = "output_images"

    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    filename = os.path.basename(input_path)
    name_only, _ = os.path.splitext(filename)

    output_filename = f"{name_only}_removed.png"

    output_path = os.path.join(output_folder, output_filename)

    try:
        input_image = Image.open(input_path)
        
        output_image = remove(input_image)
        
        output_image.save(output_path)
        
        print(f"Image processed and saved: {output_path}")
        return output_path

    except Exception as e:
        print(f"Something went wrong when processing image: {e}")
        return None