import math
from math import floor

import numpy as np

from PIL import Image

class Body:
    def __init__(self,x,y,vx,vy,mass=10.0):
        self.path = []
        self.pos = np.array([x,y])
        self.vel = np.array([vx,vy])
        self.mass = mass
    def act(self,t):
        self.path.append(self.pos)
        self.pos = self.pos + self.vel * t

    def np_path(self):
        return np.array(self.path)

def main():
    print("Hello from python-code-art!")

    bodies = [Body(0,0,0,0.1,10),Body(-100,0,0,0.4,10),Body(100,0,0,-0.2,10)]

    def euclidean_distance(a, b):
        return np.sqrt(np.sum((a - b) ** 2))

    def sim_step(t):
        for body in bodies:
            for _body in bodies:
                if _body == body:
                    continue
                d = body.pos - _body.pos
                dn = d / np.linalg.norm(d)
                f = (body.mass * _body.mass) / euclidean_distance(_body.pos,body.pos)**2
                vel = (f / _body.mass) * dn * t

                _body.vel = _body.vel + vel
        for body in bodies:
            body.act(t)

    sim_i = 0
    while sim_i < 100000:
        sim_step(0.01)
        sim_i+=1


    size = 10000
    density = 30

    img = Image.new('RGB', (size,size), color='black')
    offset = size / 2

    for body in bodies:
        index = 0
        length = len(body.np_path())
        for i in body.np_path():
            a = floor((255 / math.sqrt(length)) * math.sqrt(index))

            x = floor((i[0]) * density + offset)
            y = floor((i[1]) * density + offset)
            if 1 <= x < size-1 and 1 <= y < size-1:
                for xi in range(13):
                    for yi in range(13):
                        img.putpixel((x-6+xi,y-6+yi), (a, a, a))

            index += 1
    img.show()

if __name__ == "__main__":
    main()
