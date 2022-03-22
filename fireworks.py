import time
import random
import os

# cols and rows must match fullscreen commandline display
cols = 271
rows = 70
index = [" " for i in range(cols * rows)]
fws = []
index_map = {
    "up":-cols,
    "down":cols,
    "left":-1,
    "right":1,
    "up_right":-cols + 2,
    "up_left":-cols - 2,
    "down_right":cols + 2,
    "down_left":cols - 2}

coord_map = {
    "up":1,
    "down":-1,
    "left":-1,
    "right":1,
    "up_right":(2, 1),
    "up_left":(-2, 1),
    "down_right":(2, -1),
    "down_left":(-2, -1)
}

class fw_node:
    global index
    global fws
    global cols
    global rows
    def __init__(self, x, y, direction, strength, fuse, face):
        self.x = x
        self.y = y
        self.index_val = cols * (rows-y) + x
        self.direction = direction
        self.strength = strength
        self.fuse = fuse
        self.face = face
        self.alive = True
        self.count = 0
        index[self.index_val] = self.face
        

    def proceed(self):
        if self.strength < 1:
            self.alive = False
            return

        self.count += 1
        if self.fuse <= self.count:
            self.alive = False
            keys = coord_map.keys()
            for key in keys:
                fws.append(fw_node(self.x, self.y, key, self.strength - 1, int(self.fuse * 0.618), "*"))
        
        if self.alive:
            self.index_val += index_map[self.direction]
            index[self.index_val] = self.face
        
            if self.direction == "up" or self.direction == "down":
                self.y += coord_map[self.direction]
            elif self.direction == "left" or self.direction == "right":
                self.x += coord_map[self.direction]
            else:
                self.x += coord_map[self.direction][0]
                self.y += coord_map[self.direction][1]



fws.append(fw_node(45, 10, "up", 3, 15, "|"))
fws.append(fw_node(180, 10, "up", 3, 15, "|"))

def junk_collector():
    global fws
    global index
    for i, fw in enumerate(fws):
        if not fw.alive:
            for n in range(fw.fuse):
                index[fw.index_val + (-index_map[fw.direction] * n)] = " "
            del fws[i]


count = 2
while count < 50 or fws:
    x = random.randint(0, 2000)
    if x < 270:
        count+=1
        y = random.randint(5, 40)
        fws.append(fw_node(x, y, "up", 3, 20, "|"))
    
    [fw.proceed() for fw in fws]
    os.system('cls')
    print("".join(index))
    junk_collector()
    time.sleep(0.025)


