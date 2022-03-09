from numpy import sin, pi
import csv

num_cycles = 5
freq = 1
time_step = 0.01 * 1000
min_range = 0
max_range = 100
offset_1 = pi / 2
offset_2 = pi / 2
offset_3 = pi / 2
offset_4 = 0
offset_5 = 0
offset_6 = 0
filename = "sin_wave_2.csv"


def scale(value, old_min, old_max, new_min, new_max):
    old_range = old_max - old_min
    new_range = new_max - new_min
    new_value = (((value - old_min) * new_range) / old_range) + new_min
    return int(new_value)


csv_data = [["Line", "Time (ms)", "X", "Y", "Z", "U", "V", "W"]]

for i in range(1, int(num_cycles * freq * 1000 / time_step + 1)):
    line = [i, int(time_step)]

    angle = i * (2 * pi / (freq / (time_step / 1000)))

    val_1 = scale(sin(angle - pi / 2 + offset_1), -1, 1, min_range, max_range)
    val_2 = scale(sin(angle - pi / 2 + offset_2), -1, 1, min_range, max_range)
    val_3 = scale(sin(angle - pi / 2 + offset_3), -1, 1, min_range, max_range)
    val_4 = scale(sin(angle - pi / 2 + offset_4), -1, 1, min_range, max_range)
    val_5 = scale(sin(angle - pi / 2 + offset_5), -1, 1, min_range, max_range)
    val_6 = scale(sin(angle - pi / 2 + offset_6), -1, 1, min_range, max_range)

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
