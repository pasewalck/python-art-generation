import math
import os
import random
from math import floor

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

def file_to_data(filepath:str,is_bit_mode:bool):
    data_array = []
    with open(filepath, 'rb') as file:
        data = file.read()
        for index, byte_value in enumerate(data):
            if not is_bit_mode:
                data_array.append(byte_value)
            else:
                for i in range(8):
                    bit = (byte_value >> i) & 1
                    data_array.append(bit)
    return data_array


def main():
    print("Hello from python-code-art!")
    input_path = input("Enter a path: ")
    is_bit_mode = input("Select a mode (bit, byte (default)): ") == "bit"
    input_w = int(input("Enter width ratio (4 is default): ") or "4")
    input_h = int(input("Enter height ratio (5 is default): ") or "5")

    print(f"Generating art for '{input_path}'\n in {'bit' if is_bit_mode else 'byte'}-mode ...")

    files_data_array = []

    if os.path.isdir(input_path):
        for root, dirs, files in os.walk(input_path):
            for filename in files:
                files_data_array.append(file_to_data(os.path.join(root, filename),is_bit_mode))
    else:
        files_data_array.append(file_to_data(input_path,is_bit_mode))

    size = 0
    for fd in files_data_array:
        size += len(fd)

    print(f"Found {len(files_data_array)} files with a total size of {size} {'bytes' if not is_bit_mode else 'bits'} (= {(size * 8 if is_bit_mode else size)/(1000*1000)} mb).")

    width = math.ceil(math.sqrt(size)/input_w*input_h)
    height = math.ceil(math.sqrt(size)/input_h*input_w)
    track_nr = int(min(20,max(1,math.ceil(len(files_data_array) / 10))))
    track_size = int(math.ceil((width / track_nr)))

    margin = floor(track_size*min(2.0,len(files_data_array)*0.1))
    random_tb_margin = track_size * min(10,math.ceil(track_nr/2.0-1))


    img = Image.new('RGB', (width+margin*2, height+margin*2+random_tb_margin), color='white')

    offset_y = random_tb_margin/2

    ran = random.Random()

    index_c = 0

    with alive_bar(size, force_tty=True) as bar:
        for index_i, data_array in enumerate(files_data_array):
            v_last = 0
            for index_ii, value in enumerate(data_array):

                if index_c % track_size == 0 and (index_c // track_size) % height == 0:
                    offset_y = min(max(0,offset_y+ran.randint(-track_size,track_size)),random_tb_margin)

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

                img.putpixel((x+margin, y+margin+offset_y), (r,g,b))
                index_c += 1
    img.show()

if __name__ == "__main__":
    main()
