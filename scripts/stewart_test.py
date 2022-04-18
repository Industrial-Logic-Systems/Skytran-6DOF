from math import radians

import numpy as np
from numpy import cos
from numpy import sin
from stewart_controller import Stewart_Platform


def main():
    """
    Bottom: Radius = 50.7 cm    - 507 mm
            Angle  = 7 degrees  - 0.1226 rad
    Top:    Radius = 26.4 cm    - 264 mm
            Angle  = 13 degrees - 0.2268 rad
    """

    platform_height = 570
    servo_length = 650
    platform = Stewart_Platform(507, 264, platform_height, 0.1226, 0.2268)

    x = 0
    y = 0
    z = 100
    pitch = radians(0)
    roll = radians(0)
    yaw = radians(0)

    angle = radians(60)
    x_cor = x * cos(angle) + y * sin(angle)
    y_cor = -x * sin(angle) + y * cos(angle)

    angle = radians(-30)
    pitch_cor = pitch * cos(angle) + roll * sin(angle)
    roll_cor = -pitch * sin(angle) + roll * cos(angle)

    actuator_lengths = platform.calculate(np.array([x_cor, y_cor, z]), np.array([pitch_cor, roll_cor, yaw]))

    # print("Base:", actuator_lengths)
    actuator_lengths = actuator_lengths - servo_length
    # print("Lengths:", actuator_lengths)
    actuator_lengths = [round(x) for x in actuator_lengths]
    print("Lengths Int:", actuator_lengths)


if __name__ == "__main__":
    main()
