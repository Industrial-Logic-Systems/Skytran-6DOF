import csv
import tkinter as tk
from tkinter import filedialog

import numpy as np
from stewart_controller import Stewart_Platform

root = tk.Tk()
root.withdraw()


filename = filedialog.askopenfilename()
with open(filename) as f:
    # read csv and save to list
    reader = csv.reader(f)
    lines = list(reader)

lines = lines[1:]
lines = [[int(x) for x in line] for line in lines]
print(lines)

length = 10

platform = Stewart_Platform(6.2, 5, length, 0.2269, 0.82)

converted = [["Line", "Time (ms)", "X", "Y", "Z", "U", "V", "W"]]

for line in lines:
    convert = [line[0], line[1]]
    x = line[2]
    y = line[3]
    z = line[4]
    u = line[5]
    v = line[6]
    w = line[7]
    servo_lengths = platform.calculate(np.array([x, y, z]), np.array([u, v, w]))
    servo_lengths = servo_lengths - length
    print(servo_lengths)
    convert.extend(servo_lengths)
    print(convert)
    converted.append(convert)

file = filedialog.asksaveasfile(filetypes=[("CSV Files", "*.csv")], defaultextension=[("CSV Files", "*.csv")])
writer = csv.writer(file)
writer.writerows(converted)
file.close()
