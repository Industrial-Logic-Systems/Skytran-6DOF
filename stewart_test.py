import numpy as np
from stewart_controller import Stewart_Platform
import matplotlib.pyplot as plt
from numpy import sin, cos


def main():
    pi = np.pi

    # Call object
    # platform = Stewart_Platform(6.2, 5, 0, 0.2269, 0.2269)
    platform = Stewart_Platform(6.2, 5, 10, 0.2269, 0.82)

    # Initialize Plots
    fig, ax = plt.subplots()

    # Loop through various angles
    for ix in range(0, 360, 45):
        angle = np.pi * ix / 180
        print("angle: ", angle)
        # servo_angles = platform.calculate_matrix(np.array([2, 1, 0]), np.array([0, angle, 0]))
        servo_angles = platform.calculate(np.array([5 * cos(angle), 5 * sin(angle), 0]), np.array([0, 0, 0]))
        print(servo_angles)
        ax = platform.plot_platform()
        plt.pause(1000000000)

        plt.draw()

    # servo_angles = platform.calculate_matrix(np.array([2, 1, 0]), np.array([0, angle, 0]))
    servo_angles = platform.calculate(np.array([3, 3, 0]), np.array([0, 0, pi / 4]))
    print(servo_angles)
    ax = platform.plot_platform()
    plt.pause(1000000000)

    plt.draw()


if __name__ == "__main__":
    main()
