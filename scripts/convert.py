import csv
import tkinter as tk
from math import radians
from tkinter import filedialog

import numpy as np
from numpy import cos
from numpy import sin
from stewart_controller import Stewart_Platform

min = 0
max = 200
platform_height = 570
servo_length = 650
platform = Stewart_Platform(507, 264, platform_height, 0.1226, 0.2268)


def verify_lengths(lengths, min, max):
    for length in lengths:
        if length < min or length > max:
            return False
    return True


def get_converted(lines, shift_amts):
    converted = [["Line", "Time (ms)", "X", "Y", "Z", "U", "V", "W"]]

    prev_time = 0.0
    for i, line in enumerate(lines):
        # print(f"Calculating line: {i}")
        cur_time = line[0] * 1000
        convert = [i, int(cur_time - prev_time)]
        prev_time = cur_time
        x_og = line[1] * 1000 + shift_amts[0]
        y_og = line[2] * 1000 + shift_amts[1]
        angle = radians(225)
        x = x_og * cos(angle) + y_og * sin(angle)
        y = -x_og * sin(angle) + y_og * cos(angle)
        z = line[3] * 1000 + shift_amts[2]
        u = line[4]
        v = line[5]
        w = line[6]
        actuator_lengths = platform.calculate(np.array([x, y, z]), np.array([u, v, w]))
        actuator_lengths = actuator_lengths - servo_length
        result = verify_lengths(actuator_lengths, min, max)
        if not result:
            print("Invalid lengths: ", actuator_lengths)
            print("If values are less than {min} try moving the whole motion profile up by adding to the Z axis")
            print(f"If values are greater than {max} it likely means your moving out of range of the platform")
            return None
        actuator_lengths = [int(x) for x in actuator_lengths]
        convert.extend(actuator_lengths)
        converted.append(convert)
    return converted


def main():
    root = tk.Tk()
    root.withdraw()

    filename = filedialog.askopenfilename()
    with open(filename) as f:
        # read csv and save to list
        reader = csv.reader(f)
        lines = list(reader)

    lines = lines[1:]
    lines = [
        [
            float(line[0]),
            float(line[1]),
            float(line[2]),
            float(line[3]),
            float(line[4]),
            float(line[5]),
            float(line[6]),
        ]
        for line in lines
    ]
    # print(lines)

    print("Starting conversion...")

    converted = None
    shift_amts = [0, 0, 0]
    while converted is None:
        converted = get_converted(lines, shift_amts)
        if converted is None:
            user_input = input("Would you like to shift the motion profile by any amount? (y/n)")
            if user_input and user_input.lower()[0] == "y":
                axis = input("Which axis would you like to shift? (x, y, z): ")
                axis = axis.lower()
                if axis[0] == "x":
                    shift_amts[0] = int(input("How much would you like to shift the motion profile by? (In mm): "))
                elif axis[0] == "y":
                    shift_amts[1] = int(input("How much would you like to shift the motion profile by? (In mm): "))
                elif axis[0] == "z":
                    shift_amts[2] = int(input("How much would you like to shift the motion profile by? (In mm): "))
                else:
                    print("Invalid axis")
            else:
                return
            print(f"Shifting X-axis by {shift_amts[0]}, Y-axis by {shift_amts[1]}, Z-axis by {shift_amts[2]}")

    print("Conversion finished...")

    file = filedialog.asksaveasfilename(filetypes=[("CSV Files", "*.csv")], defaultextension=[("CSV Files", "*.csv")])
    with open(file, "w", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(converted)


if __name__ == "__main__":
    main()
