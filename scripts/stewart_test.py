import matplotlib.pyplot as plt
import numpy as np
from numpy import cos
from numpy import sin
from stewart_controller import Stewart_Platform


def main():
    pi = np.pi

    # Call object
    # platform = Stewart_Platform(6.2, 5, 0, 0.2269, 0.2269)

    """
    Bottom: Radius = 50.7 cm    - 507 mm
            Angle  = 7 degrees  - 0.1226 rad
    Top:    Radius = 26.4 cm    - 264 mm
            Angle  = 13 degrees - 0.2268 rad
    """

    # platform = Stewart_Platform(6.2, 5, 10, 0.2269, 0.82)
    platform_height = 570
    servo_length = 650
    platform = Stewart_Platform(507, 264, platform_height, 0.1226, 0.2268)

    # Initialize Plots
    fig, ax = plt.subplots()

    # Loop through various angles
    # for ix in range(0, 360, 45):
    #    angle = np.pi * ix / 180
    #    print("angle: ", angle)
    #    # servo_angles = platform.calculate_matrix(np.array([2, 1, 0]), np.array([0, angle, 0]))
    #    servo_angles = platform.calculate(np.array([5 * cos(angle), 5 * sin(angle), 0]), np.array([0, 0, 0]))
    #    print(servo_angles)
    #    ax = platform.plot_platform()
    #    plt.pause(1000000000)

    #    plt.draw()

    # servo_angles = platform.calculate_matrix(np.array([2, 1, 0]), np.array([0, angle, 0]))
    actuator_lengths = platform.calculate(np.array([0, 0, 0]), np.array([0, 0, 0]))

    print(actuator_lengths)
    print(actuator_lengths - servo_length)
    ax = platform.plot_platform()
    plt.pause(1000000000)

    plt.draw()


if __name__ == "__main__":
    main()
