import math
from math import floor

import numpy as np

from PIL import Image

def main():
    print("Hello from python-code-art!")

    def f(p):
        return math.sin(p)
    def diff_f(p):
        return math.cos(p)

    def diff_numeric(func,p0,h):
        return (func(p0+h) - func(p0)) / h

    width = 800
    height = 640

    img = Image.new('RGB', (width,height), color='white')

    data = np.empty([width, height])
    biggest_diff_diff = 0

    res = (math.pi/128)

    for col in range(width):
        x0 = (col)*res
        a_diff_y = diff_f(x0)
        for row in range(height):
            c_h = (math.pi/8)*((height - row)/height)
            n_diff_y = diff_numeric(f,x0,c_h)
            diff_diff = math.fabs(n_diff_y - a_diff_y)
            if diff_diff >= biggest_diff_diff:
                biggest_diff_diff = diff_diff
            data[col][row] = diff_diff

    for col in range(width):
        for row in range(height):
            a = floor(200*(data[col][row] / biggest_diff_diff))
            img.putpixel((col,row), (a,a,a))

    for col in range(width):
        x0 = (col-width/2)*(math.pi/64)
        y = f(x0)
        diff_y = diff_f(x0)
        img.putpixel((col, math.floor(-y/res)+height//2), (255, 0, 0))
        img.putpixel((col, math.floor(-diff_y/res)+height//2), (0, 0, 200))

    img.show()

if __name__ == "__main__":
    main()
