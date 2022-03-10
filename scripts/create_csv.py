import csv

from numpy import cos
from numpy import pi
from numpy import sin

num_cycles = 5
freq = 1
time_step = 0.01 * 1000
frequency = 50
filename = "circle_6.csv"


csv_data = [["Line", "Time (ms)", "X", "Y", "Z", "PITCH", "ROLL", "YAW"]]

for i in range(1, int(num_cycles * freq * 1000 / time_step + 1)):
    line = [i, int(time_step)]

    angle = i * (2 * pi / (freq / (time_step / 1000)))

    val_1 = frequency * cos(angle)
    val_2 = frequency * sin(angle)
    val_3 = 100
    val_4 = pi / 24 * cos(angle)
    val_5 = pi / 24 * cos(angle)
    val_6 = pi / 24 * sin(angle)

    line.append(val_1)
    line.append(val_2)
    line.append(val_3)
    line.append(val_4)
    line.append(val_5)
    line.append(val_6)

    csv_data.append(line)

with open(filename, "w", newline="") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerows(csv_data)
