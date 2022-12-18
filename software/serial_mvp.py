import serial
import matplotlib.pyplot as plt
import numpy as np
import time
import pdb

def initialize_serial():
    arduino_port = "/dev/ttyACM0"
    baud_rate = 115200
    serial_port = serial.Serial(arduino_port, baud_rate, timeout=1)
    return serial_port

def process_serial_input(serial_port):
    start_time = time.perf_counter()
    data = {
        1: [[], []],
        2: [[], []],
        3: [[], []],
        4: [[], []],
    }
    plt.ion()
    fig = plt.figure()
    ax1 = fig.add_subplot(111)
    # ax2 = fig.add_subplot(222)
    # ax3 = fig.add_subplot(223)
    # ax4 = fig.add_subplot(224)
    ax1.set_xbound(lower=0, upper=20)
    ax1.set_ybound(lower=0, upper=1024)
    # ax2.set_xbound(lower=0, upper=20)
    # ax2.set_ybound(lower=0, upper=1024)
    # ax3.set_xbound(lower=0, upper=20)
    # ax3.set_ybound(lower=0, upper=1024)
    # ax4.set_xbound(lower=0, upper=20)
    # ax4.set_ybound(lower=0, upper=1024)

    line1, = ax1.plot(data[1][0], data[1][1], 'k-') 
    # line2, = ax2.plot(data[2][0], data[2][1], 'g-')
    # line3, = ax3.plot(data[3][0], data[3][1], 'b-')
    # line4, = ax4.plot(data[4][0], data[4][1], 'r-')

    #serial
    while True:
        try:
            curr_data = int(serial_port.readline().decode())
            data[curr_data//10000][1].append(curr_data%10000)
            data[curr_data//10000][0].append(time.perf_counter()-start_time)
        except (UnicodeDecodeError, ValueError, KeyError):
            continue
        line1.set_xdata(data[1][0])
        line1.set_ydata(data[1][1])
        # line2.set_xdata(data[2][0])
        # line2.set_ydata(data[2][1])
        # line3.set_xdata(data[3][0])
        # line3.set_ydata(data[3][1])
        # line4.set_xdata(data[4][0])
        # line4.set_ydata(data[4][1])

        if len(data[1][0]) == 0:
            continue
        if data[1][0][-1] < 10:
            ax1.set_xbound(lower=0, upper=20)
            # ax2.set_xbound(lower=0, upper=20)
            # ax3.set_xbound(lower=0, upper=20)
            # ax4.set_xbound(lower=0, upper=20)
        else:
            ax1.set_xbound(lower=data[1][0][-1]-10, upper=data[1][0][-1]+10)
            # ax2.set_xbound(lower=data[1][0][-1]-10, upper=data[1][0][-1]+10)
            # ax3.set_xbound(lower=data[1][0][-1]-10, upper=data[1][0][-1]+10)
            # ax4.set_xbound(lower=data[1][0][-1]-10, upper=data[1][0][-1]+10)

        fig.canvas.draw()
        fig.canvas.flush_events()

if __name__ == "__main__":
    serial_port = initialize_serial()
    process_serial_input(serial_port)