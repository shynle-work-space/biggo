from modules.file_access import FileAccess
from modules.errors import Error
from io import BytesIO
from PIL import Image
from time import sleep

def compress_img(fs_id: str, owner_id:str):
    # read original image from database
    read_result = FileAccess().read_fs(fs_id)
    if isinstance(read_result, Error):
        return read_result
    

    fs_name, fs_content = read_result
    imgIO = BytesIO(fs_content)
    img = Image.open(imgIO)

    # Mimic a very long task
    sleep(5)

    # Compress image and save to memory as bytes
    with BytesIO() as compressed_img:
        img.save(compressed_img, optimize=True, quality=15, format="WEBP")
        compressed_img_bytes = compressed_img.getvalue()

    # Save the bytes to database
    compressed_id = FileAccess().create_fs(owner_id, compressed_img_bytes, filename=fs_name, tag='compressed', original=fs_id)
    return compressed_id