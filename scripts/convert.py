import csv
import tkinter as tk
from tkinter import filedialog

import numpy as np
from stewart_controller import Stewart_Platform


def verify_lengths(lengths, min, max):
    for length in lengths:
        if length < min or length > max:
            return False
    return True


def main():
    root = tk.Tk()
    root.withdraw()

    filename = filedialog.askopenfilename()
    with open(filename) as f:
        # read csv and save to list
        reader = csv.reader(f)
        lines = list(reader)

    lines = lines[1:]
    lines = [[int(x) for x in line] for line in lines]
    # print(lines)

    min = 0
    max = 200
    platform_height = 570
    servo_length = 650
    platform = Stewart_Platform(507, 264, platform_height, 0.1226, 0.2268)

    converted = [["Line", "Time (ms)", "X", "Y", "Z", "U", "V", "W"]]

    for line in lines:
        convert = [line[0], line[1]]
        x = line[2]
        y = line[3]
        z = line[4]
        u = line[5]
        v = line[6]
        w = line[7]
        actuator_lengths = platform.calculate(np.array([x, y, z]), np.array([u, v, w]))
        actuator_lengths = actuator_lengths - servo_length
        result = verify_lengths(actuator_lengths, min, max)
        if not result:
            print("Invalid lengths: ", actuator_lengths)
            print("If values are less than {min} try moving the whole motion profile up by adding to the Z axis")
            print(f"If values are greater than {max} it likely means your moving out of range of the platform")
            return
        convert.extend(actuator_lengths)
        converted.append(convert)

    file = filedialog.asksaveasfile(filetypes=[("CSV Files", "*.csv")], defaultextension=[("CSV Files", "*.csv")])
    writer = csv.writer(file)
    writer.writerows(converted)
    file.close()


if __name__ == "__main__":
    main()
