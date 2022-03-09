import csv

from numpy import cos
from numpy import pi
from numpy import sin


def scale(value, old_min, old_max, new_min, new_max):
    old_range = old_max - old_min
    new_range = new_max - new_min
    new_value = (((value - old_min) * new_range) / old_range) + new_min
    return int(new_value)


csv_data = [["Line", "Time (ms)", "X", "Y", "Z", "U", "V", "W"]]

for i in range(1, 1001):
    line = []
    line.append(i)
    line.append(10)
    val = scale(sin(i / 100), -1, 1, 0, 100)
    line.append(val)
    line.append(val)
    line.append(val)
    line.append(val)
    line.append(val)
    line.append(val)

    csv_data.append(line)

with open("data_2.csv", "w", newline="") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerows(csv_data)
