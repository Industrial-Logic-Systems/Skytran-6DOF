import csv
import tkinter as tk
from enum import auto
from enum import Enum
from math import radians
from tkinter import filedialog

import numpy as np
from numpy import cos
from numpy import sin
from stewart_controller import Stewart_Platform

min = 0  # Minimum allowed length for actuators
max = 200  # Maximum allowed length for actuators
platform_height = 570  # Initial Heigh of the platform
servo_length = 650  # Length of the actuators in their base position
XY_rotate_amount = 60  # Amount to rotate XY-axis so that it matches the chair
PR_rotate_amount = -30  # Amount to rotate Pitch and Roll so that it matches the chair

# Values for the Stewart Platform are defined in stewart_controller.py
platform = Stewart_Platform(507, 264, platform_height, 0.1226, 0.2268)


class verify_values(Enum):
    valid = auto()
    low = auto()
    hi = auto()
    hi_low = auto()


def verify_lengths(lengths, min, max):
    below_min = above_max = False
    for length in lengths:
        if length < min:
            below_min = True
        if length > max:
            above_max = True
    if below_min and above_max:
        return verify_values.hi_low
    if below_min:
        return verify_values.low
    if above_max:
        return verify_values.hi
    return verify_values.valid


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
        pitch_og = line[4]
        roll_og = line[5]
        z = line[3] * 1000 + shift_amts[2]
        yaw = line[6]

        # Rotate XY to match actual chair
        angle = radians(XY_rotate_amount)
        x = x_og * cos(angle) + y_og * sin(angle)
        y = -x_og * sin(angle) + y_og * cos(angle)

        # Rotate Pitch and Roll to match actual chair
        angle = radians(PR_rotate_amount)
        pitch = pitch_og * cos(angle) + roll_og * sin(angle)
        roll = -pitch_og * sin(angle) + roll_og * cos(angle)

        actuator_lengths = platform.calculate(np.array([x, y, z]), np.array([pitch, roll, yaw]))
        actuator_lengths = actuator_lengths - servo_length
        actuator_lengths = [round(x) for x in actuator_lengths]
        result = verify_lengths(actuator_lengths, min, max)

        if result is not verify_values.valid:
            print("Invalid lengths: ", actuator_lengths)
            if result is verify_values.hi_low:
                print(
                    f"There is an actuator length greater than {max} and less than {min}. This likely means that your profile wont work on this platform"
                )
            if result is verify_values.low:
                print(f"There is an actuator length lower than {min}. Try shifting up on the Z-axis")
            if result is verify_values.hi:
                print(f"There is an actuator length greater than {max}. Try shifting down on the Z-axis")
            return None

        convert.extend(actuator_lengths)
        converted.append(convert)
    return converted


def main():
    root = tk.Tk()
    root.withdraw()
    root.wm_attributes("-topmost", 1)

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
            print(f"\nShifting X-axis by {shift_amts[0]}, Y-axis by {shift_amts[1]}, Z-axis by {shift_amts[2]}\n")
            print("\n" * 3)

    print("Conversion finished...")

    file = filedialog.asksaveasfilename(filetypes=[("CSV Files", "*.csv")], defaultextension=[("CSV Files", "*.csv")])
    with open(file, "w", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(converted)


if __name__ == "__main__":
    main()
