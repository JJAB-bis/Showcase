import tkinter as tk
import numpy as np
from map_gen import World

w,h,s = 50,50,10

world = World(h,w)
world.run()
arr = world.map_2_array()

colors = ['dark blue','yellow','light green', 'grey', 'dark green']

root = tk.Tk()
canvas = tk.Canvas(root,width=h*s,height=w*s)
Y,X = arr.shape
for y in range(Y):
    for x in range(X):
        y1,x1,y2,x2 = map(lambda x:x*s, (y,x,y+1,x+1))
        canvas.create_rectangle(x1,y1,x2,y2, fill = colors[arr[y,x]])
canvas.pack()
print(arr)

canvas.mainloop()
