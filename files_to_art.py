import math
import os
import random

from PIL import Image
from alive_progress import alive_bar

def color_from_byte(v):
    r = (v >> 5) * 255 // 7
    g = ((v >> 2) & 0b00000111) * 255 // 7
    b = (v & 0b00000011) * 255 // 3
    return r,g,b

def color_from_bit(v):
    c = v * 255
    return c,c,c

def main():
    print("Hello from python-code-art!")
    directory_path = input("Enter a path: ")
    is_bit_mode = input("Select a mode (bit, byte (default)): ") == "bit"
    print(f"Generating art for '{directory_path}'\n in {'bit' if is_bit_mode else 'byte'} mode ...")

    files_array = []

    size = 0

    for root, dirs, files in os.walk(directory_path):
        for filename in files:
            data_array = []
            filepath = os.path.join(root, filename)
            with open(filepath, 'rb') as file:
                data = file.read()
                for index, byte_value in enumerate(data):
                    if not is_bit_mode:
                        data_array.append(byte_value)
                        size += 1
                    else:
                        for i in range(8):
                            bit = (byte_value >> i) & 1
                            data_array.append(bit)
                            size += 1

            files_array.append(data_array)

    print(f"Found {len(files_array)} files with a total size of {size} {'bytes' if not is_bit_mode else 'bits'} (= {(size * 8 if is_bit_mode else size)/(1000*1000)} mb).")

    width = math.ceil(math.sqrt(size)/4*5)
    height = math.ceil(math.sqrt(size)/5*4)
    track_size = math.ceil((width / len(files_array)) * 10)

    img = Image.new('RGB', (width+track_size*2, height+track_size*10), color='white')

    offset_y = track_size*5

    ran = random.Random()

    index_c = 0

    with alive_bar(size, force_tty=True) as bar:
        for index_i, data_array in enumerate(files_array):
            v_last = 0
            for index_ii, value in enumerate(data_array):

                if index_c % track_size == 0 and (index_c // track_size) % height == 0:
                    offset_y = min(max(track_size,offset_y+ran.randint(-track_size,track_size)),track_size*9)

                node = (index_c // track_size)
                col = node // height

                if col * track_size + track_size >= width:
                    mod_index_c = index_c - col * track_size * height
                    mod_track_size = width - col * track_size
                    mod_node = (mod_index_c // mod_track_size)
                    rel_x = mod_index_c % mod_track_size
                    y = mod_node % height
                    x = col * track_size + rel_x
                else:
                    rel_x = index_c % track_size
                    y = node % height
                    x = (node // height)*track_size + rel_x

                bar()

                r,g,b = color_from_bit(value) if is_bit_mode else color_from_byte(value)

                img.putpixel((x+track_size, y+offset_y), (r,g,b))
                index_c += 1
    img.show()

if __name__ == "__main__":
    main()
