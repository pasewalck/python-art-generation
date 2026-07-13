import math
from math import floor

import numpy as np
import webcolors

from PIL import Image

class Body:
    def __init__(self,x,y,vx,vy,mass=10.0,hex_color="#ffffff"):
        self.path = []
        self.pos = np.array([x,y])
        self.vel = np.array([vx,vy])
        self.mass = mass
        self.color = webcolors.hex_to_rgb(hex_color)
    def act(self,t):
        self.path.append(self.pos)
        self.pos = self.pos + self.vel * t

    def np_path(self):
        return np.array(self.path)

def main():
    print("Hello from python-code-art!")

    bodies = [Body(0,-300,0.037,0,2,"#ff99c8"),Body(-90,400,-0.037,-0.045,1,"#a9def9"),Body(90,400,-0.037,0.045,1,"#e4c1f9")]

    #[Body(0,800,0.038,0,2),Body(-50,100,-0.038,-0.05,1),Body(50,100,-0.038,0.05,1)]
    #[Body(0,0,0,0.1,10),Body(-100,0,0,0.4,10),Body(100,0,0,-0.2,10)]

    def euclidean_distance(_a, _b):
        return np.sqrt(np.sum((_a - _b) ** 2))

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
    while sim_i < 280000:
        sim_step(0.1)
        sim_i+=1


    size = 2000
    density = 2

    line_radius = 3
    body_radius = 13

    img = Image.new('RGB', (size,size), color='black')
    offset = size / 2

    draw_step = 2000

    for body in bodies:
        index = 0
        path = body.np_path()

        r = body.color[0]
        g = body.color[1]
        b = body.color[2]

        length = len(path)
        for i in range(floor(length / draw_step)):
            el = path[i*draw_step]
            a = (1.0 / length) * index

            x = floor((el[0]) * density + offset)
            y = floor((el[1]) * density + offset)
            for xi in range(line_radius*2+1):
                for yi in range(line_radius*2+1):
                    if size > x-line_radius+xi >= 0 and size > y-line_radius+yi >= 0:
                        img.putpixel((x-line_radius+xi,y-line_radius+yi), (floor(r*a), floor(g*a), floor(b*a)))

            index += draw_step

        el = path[-1]
        x = floor((el[0]) * density + offset)
        y = floor((el[1]) * density + offset)

        for xi in range(body_radius*2+1):
            for yi in range(body_radius*2+1):
                if size > x - body_radius + xi >= 0 and size > y - body_radius + yi >= 0 and euclidean_distance(np.array([body_radius,body_radius]),np.array([xi,yi])) < body_radius:
                    img.putpixel((x-body_radius+xi,y-body_radius+yi), (floor(r), floor(g), floor(b)))

    img.show()

if __name__ == "__main__":
    main()
