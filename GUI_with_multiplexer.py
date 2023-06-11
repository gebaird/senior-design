"""
Created on Thu Mar 30 21:03:58 2023

@author: Grace Baird

Last update: 5/12/2023

"""

import tkinter as tk
from tkinter import *
from tkinter import ttk
from matplotlib.figure import *
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg,
                                               NavigationToolbar2Tk)
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import random
import time
import re
# Import all the i2c stuff
import busio
import board
import adafruit_tca9548a
import time
from datetime import datetime
import adafruit_ads1x15.ads1015 as ADS
from adafruit_ads1x15.analog_in import AnalogIn


###GUI functions

def mainMenu():  # deletes window when button is pushed after time
    indiv_readouts.withdraw()
    root.deiconify()


def create_Main_Window():  # creating main window
    root.title("GAMIX ICP MONITOR")
    root.geometry("%dx%d" % (width, height))
    print("creating main window")
    # creating actual plot with label
    plot_label = tk.Label(root, text="Moving-Averaged ICP (mmHg)", bg='white',
                          font=("Arial", 17))
    plot_label.place(relx=.26, rely=.05)

    # creating button to go to the individual ICP page
    next_button = tk.Button(root, text="Individual ICP Readouts",
                            height=2, width=20, font=('Arial', 15),
                            command=openIndividualReadouts)
    next_button.place(relx=0.87, rely=0)

    # instructions for the clibration input
    calib_instr = tk.Label(root, text="Please input initial ICP value then press ''Calibrate''",
                           bg='snow', font=('Arial', 12))
    calib_instr.place(relx=.71, rely=.69)

    # label for calibration box
    calib_label = tk.Label(root, text='Calibration Value', font=('Arial', 12),
                           bg='white')
    calib_label.place(relx=.74, rely=.72)

    # input box for calibration
    calib_input = tk.Entry(root, textvariable=initial_icp,
                           width=10)
    calib_input.place(relx=.82, rely=.72)

    # recalibrate and calibrate btns

    recalib_btn = tk.Button(root, text="Recalibrate", state=DISABLED,
                            height=1, width=10, font=('Arial', 12),
                            command=lambda: recalibrate(calib_input, calib_btn, recalib_btn))
    calib_btn = tk.Button(root, text="Calibrate", state=NORMAL,
                          height=1, width=10, font=('Arial', 12),
                          command=lambda: calibrate(calib_input, calib_btn, recalib_btn))
    calib_btn.place(relx=.74, rely=.75)
    recalib_btn.place(relx=.81, rely=.75)

    # display for the average value
    avg_readout = tk.Label(root, textvariable=avg_icp,
                           highlightthickness=3, highlightcolor="gray", highlightbackground="gray",
                           height=7, width=14, bg='tomato',
                           name="readout1", font=("Arial", 30))
    avg_readout.place(relx=0.72, rely=0.1)

    # label for average value
    avg_val_label = tk.Label(root, bg='white', font=("Arial", 15),
                             text='Current ICP Value (mmHg)', height=2, width=28)
    avg_val_label.place(relx=0.72, rely=.43)
    # def plot_main(master):  # creating a basic plot on the first page
    print("done creating main window")


def create_Indiv_ICP_Window(master):
    # geometry and title
    indiv_readouts.title("INDIVIDUAL ICP READOUTS")
    indiv_readouts.geometry("%dx%d" % (width, height))
    print("creating individual windows")
    # main menu button to go back to main page

    mainMenu_button = tk.Button(indiv_readouts, text="Main Menu",
                                height=2, width=10, font=('Arial', 17),
                                command=lambda: mainMenu())
    mainMenu_button.place(relx=0, rely=0)
    # if you dont add the lambda it will assign the command value to the return
    # from the mainMenu function which will immediately close the window
    # the lambda function assigns a callable object which will only execute
    # when given an input

    # adding the 6 different labels with string variables that will updated

    # displays for the six different strain gauges
    readout1 = tk.Label(indiv_readouts, textvariable=readout1_var, bg='lightgreen',
                        highlightthickness=3, highlightcolor="black", highlightbackground="black",
                        height=5, width=11,
                        name="readout1", font=("Arial", 30))
    readout1.place(relx=0.12, rely=0.1)

    r1_label = tk.Label(indiv_readouts, bg='white', text='Strain Gauge 1',
                        font=("Arial", 14))
    r1_label.place(relx=0.125, rely=0.36)

    readout2 = tk.Label(indiv_readouts, textvariable=readout2_var, bg='lightgreen',
                        highlightthickness=3, highlightcolor="black", highlightbackground="black",
                        height=5, width=11,
                        name="readout2", font=("Arial", 30))
    readout2.place(relx=0.42, rely=0.1)  # new2
    r2_label = tk.Label(indiv_readouts, bg='white', text='Strain Gauge 2',
                        font=("Arial", 14))
    r2_label.place(relx=0.425, rely=0.36)

    readout3 = tk.Label(indiv_readouts, textvariable=readout3_var, bg='lightgreen',
                        highlightthickness=3, highlightcolor="black", highlightbackground="black",
                        height=5, width=11,
                        name="readout3", font=("Arial", 30))
    readout3.place(relx=0.72, rely=0.1)  # new3
    r3_label = tk.Label(indiv_readouts, bg='white', text='Strain Gauge 3',
                        font=("Arial", 14))
    r3_label.place(relx=0.725, rely=0.36)

    readout4 = tk.Label(indiv_readouts, textvariable=readout4_var, bg='lightgreen',
                        highlightthickness=3, highlightcolor="black", highlightbackground="black",
                        height=5, width=11,
                        name="readout4", font=("Arial", 30))
    readout4.place(relx=0.12, rely=0.5)  # new4
    r4_label = tk.Label(indiv_readouts, bg='white', text='Strain Gauge 4',
                        font=("Arial", 14))
    r4_label.place(relx=0.125, rely=0.76)

    readout5 = tk.Label(indiv_readouts, textvariable=readout5_var, bg='lightgreen',
                        highlightthickness=3, highlightcolor="black", highlightbackground="black",
                        height=5, width=11,
                        name="readout5", font=("Arial", 30))
    readout5.place(relx=0.42, rely=0.5)  # new5
    r5_label = tk.Label(indiv_readouts, bg='white', text='Strain Gauge 5',
                        font=("Arial", 14))
    r5_label.place(relx=0.425, rely=0.76)

    readout6 = tk.Label(indiv_readouts, textvariable=readout6_var, bg='lightgreen',
                        highlightthickness=3, highlightcolor="black", highlightbackground="black",
                        height=5, width=11,
                        name="readout6", font=("Arial", 30))
    readout6.place(relx=.72, rely=0.5)
    r6_label = tk.Label(indiv_readouts, bg='white', text='Strain Gauge 6',
                        font=("Arial", 14))
    r6_label.place(relx=0.725, rely=0.76)

    # adding the add buttons to the readouts
    # 1
    addButton1 = tk.Button(indiv_readouts, text="Add", heigh=1, width=8, state=DISABLED,
                           command=lambda: addBtn(addButton1, removeButton1, readout1, sg1))
    addButton1.place(relx=0.2, rely=0.34)
    # 2
    addButton2 = tk.Button(indiv_readouts, text="Add", heigh=1, width=8, state=DISABLED,
                           command=lambda: addBtn(addButton2, removeButton2, readout2, sg2))
    addButton2.place(relx=0.5, rely=0.34)
    # 3
    addButton3 = tk.Button(indiv_readouts, text="Add", heigh=1, width=8, state=DISABLED,
                           command=lambda: addBtn(addButton3, removeButton3, readout3, sg3))
    addButton3.place(relx=0.8, rely=0.34)
    # 4
    addButton4 = tk.Button(indiv_readouts, text="Add", heigh=1, width=8, state=DISABLED,
                           command=lambda: addBtn(addButton4, removeButton4, readout4, sg4))
    addButton4.place(relx=0.2, rely=0.74)
    # 5
    addButton5 = tk.Button(indiv_readouts, text="Add", heigh=1, width=8, state=DISABLED,
                           command=lambda: addBtn(addButton5, removeButton5, readout5, sg5))
    addButton5.place(relx=0.5, rely=0.74)
    # 6
    addButton6 = tk.Button(indiv_readouts, text="Add", heigh=1, width=8, state=DISABLED,
                           command=lambda: addBtn(addButton6, removeButton6, readout6, sg6))
    addButton6.place(relx=0.8, rely=0.74)

    # adding the remove buttons to the readouts
    # 1
    removeButton1 = tk.Button(indiv_readouts, text="Remove", height=1, width=8,
                              command=lambda: removeBtn(addButton1, removeButton1, readout1, sg1))
    removeButton1.place(relx=0.2, rely=0.37)
    # 2
    removeButton2 = tk.Button(indiv_readouts, text="Remove", height=1, width=8,
                              command=lambda: removeBtn(addButton2, removeButton2, readout2, sg2))
    removeButton2.place(relx=0.5, rely=0.37)
    # 3
    removeButton3 = tk.Button(indiv_readouts, text="Remove", height=1, width=8,
                              command=lambda: removeBtn(addButton3, removeButton3, readout3, sg3))
    removeButton3.place(relx=0.8, rely=0.37)
    # 4
    removeButton4 = tk.Button(indiv_readouts, text="Remove", height=1, width=8,
                              command=lambda: removeBtn(addButton4, removeButton4, readout4, sg4))
    removeButton4.place(relx=0.2, rely=0.77)
    # 5
    removeButton5 = tk.Button(indiv_readouts, text="Remove", height=1, width=8,
                              command=lambda: removeBtn(addButton5, removeButton5, readout5, sg5))
    removeButton5.place(relx=0.5, rely=0.77)
    # 6
    removeButton6 = tk.Button(indiv_readouts, text="Remove", height=1, width=8,
                              command=lambda: removeBtn(addButton6, removeButton6, readout6, sg6))
    removeButton6.place(relx=0.8, rely=0.77)
    print("done creating individual windows")


def openIndividualReadouts():
    root.withdraw()
    indiv_readouts.deiconify()
    print("opening individual windows")


def addBtn(addButton, removeButton, readout, sgnum):  # changes state when add btn is pressed
    removeButton['state'] = NORMAL
    addButton['state'] = DISABLED
    readout['bg'] = 'lightgreen'
    readout['fg'] = 'black'
    readout['highlightcolor'] = 'black'
    readout['highlightbackground'] = 'black'
    readout['fg'] = 'black'
    sgnum.set('1')
    # will add code to add value to calculation


def removeBtn(addButton, removeButton, readout, sgnum):  # changes state when remove btn is pressed
    removeButton['state'] = DISABLED
    addButton['state'] = NORMAL
    readout['bg'] = 'tomato'
    readout['highlightcolor'] = 'gray'
    readout['highlightbackground'] = 'gray'
    readout['fg'] = 'gray'
    sgnum.set('0')
    # will add code to remove value to calculation


def calibrate(box, calib_btn, recalib_btn):  # once calibration btn is pressed
    if box.get() != "":
        btn_pressed.set('T')
        calib_btn['state'] = DISABLED
        box['state'] = DISABLED
        popup = tk.Tk()
        success_message = tk.Label(popup, text="Calibration successful!")
        success_message.pack()
        recalib_btn['state'] = NORMAL
        avg_readout['bg'] = 'lightgreen'
        avg_readout['highlightcolor'] = 'black'
        avg_readout['highlightbackground'] = 'black'


    else:
        popup = tk.Tk()
        warning_message = tk.Label(popup, text="Please enter calibration value and try again!")
        warning_message.pack()


def recalibrate(box, calib_btn, recalib_btn):  # once recalibration btn is pressed
    box['state'] = NORMAL
    box.after(10, box.delete(0, END))
    calib_btn['state'] = NORMAL
    recalib_btn['state'] = DISABLED
    avg_icp.set('-')
    avg_readout['bg'] = 'tomato'
    avg_readout['highlightcolor'] = 'gray'
    avg_readout['highlightbackground'] = 'gray'
    btn_pressed.set('F')


def main_fcn(p2, y):
    time_shown_s = 61
    div = time_shown_s / 10
    # define variables to carry over between readings

    points_taken = 10  # this is the number of points to take a moving average over
    while True:
        print('test')

        ###geting ICP values###
        if initial_icp.get() != '' and btn_pressed.get() == 'T':  # ensuring calibration number has been entered
            print(chan1.voltage)
            print(chan2.voltage)
            print(chan3.voltage)
            print(chan4.voltage)
            print(chan5.voltage)
            print(chan6.voltage)
            print('!')
            # getting voltage values from the channels
            num1 = round(chan1.voltage - initial1, 6)
            num2 = round(chan2.voltage - initial2, 6)
            num3 = round(chan3.voltage - initial3, 6)
            num4 = round(chan4.voltage - initial4, 6)
            num5 = round(chan5.voltage - initial5, 6)
            num6 = round(chan6.voltage - initial6, 6)

            sg1_val = int(sg1.get())
            sg2_val = int(sg2.get())
            sg3_val = int(sg3.get())
            sg4_val = int(sg4.get())
            sg5_val = int(sg5.get())
            sg6_val = int(sg6.get())

            pressure1 = num1
            pressure2 = num2
            pressure3 = num3
            pressure4 = num4
            pressure5 = num5
            pressure6 = num6
            # repeat for the remaining strain gauges

            average_val_initial = ((pressure1 * sg1_val) + (pressure2 * sg2_val) +
                                   (pressure3 * sg3_val) + (pressure4 * sg4_val) + (pressure5 * sg5_val) +
                                   (pressure6 * sg6_val)) / (sg1_val + sg2_val + sg3_val + sg4_val + sg5_val + sg6_val)

            average_val_final = round(average_val_initial, 6)

            if len(average_set) < points_taken - 1:  # this number is the number of points to take the average over
                average_set.append(average_val_final)
                moving_average = average_val_final
            if len(average_set) == points_taken - 1:
                average_set.append(average_val_final)
                moving_average = sum(average_set) / points_taken
            if len(average_set) > points_taken - 1:
                moving_average = moving_average + (average_val_final / points_taken) - (average_set[0] / points_taken)
                average_set.append(average_val_final)
                del average_set[0]
                moving_average_set.append(moving_average)

            # setting the string variables to the numbers so the label will update
            readout1_var.set(str(num1))
            readout2_var.set(str(num2))
            readout3_var.set(str(num3))
            readout4_var.set(str(num4))
            readout5_var.set(str(num5))
            readout6_var.set(str(num6))
            avg_icp.set(str(round(moving_average, 4)))


        else:  # if calibration value has not been entered
            readout1_var.set("-")
            readout2_var.set("-")
            readout3_var.set("-")
            readout4_var.set("-")
            readout5_var.set("-")
            readout6_var.set("-")
            avg_icp.set("-")

        ###Plotting graph###
        tick_marks = [*range(time_shown_s - 1, -1, -int(time_shown_s / div))]
        y = np.append(y, moving_average)
        end = len(y)
        new_y = y[max(0, end - (time_shown_s)): end]
        end2 = len(new_y)
        new_x = np.array(range(end2 - 1, -1, -1))
        p = datetime.now()
        p2 = np.append(p2, p.strftime("%I:%M:%S"))
        new_p2 = p2[max(0, end - (time_shown_s)): end]

        data = (new_x, new_y)
        plot[0].set(data=data)
        plt.ylim(min(y), max(y) + .1)
        plt.xlim(max(new_x), min(new_x) - (time_shown_s / 10))
        ax.set_xticks(tick_marks)
        final_p2 = sorted(new_p2, reverse=True)
        time_vals = np.pad(final_p2, (0, (time_shown_s) - len(new_p2)), 'constant', constant_values=0)
        ax.set_xticklabels(time_vals[tick_marks], rotation=67.5)
        ax.xaxis.set_tick_params(labelsize=12)
        ax.yaxis.set_tick_params(labelsize=12)
        figure.canvas.draw()
        figure.canvas.flush_events()

        time.sleep(.1)


# I2C Setup
i2c = board.I2C()
tca = adafruit_tca9548a.TCA9548A(i2c)

# 1 - white - 4
# 2 - black - 5
# 3 - yellow - 2
# 4 - red - 3
# 5 - blue - 7
# 6 - green - 6
ads1 = ADS.ADS1015(tca[5])
ads2 = ADS.ADS1015(tca[1])
ads3 = ADS.ADS1015(tca[3])
ads4 = ADS.ADS1015(tca[4])
ads5 = ADS.ADS1015(tca[2])
ads6 = ADS.ADS1015(tca[0])

chan1 = AnalogIn(ads1, ADS.P0)
chan2 = AnalogIn(ads2, ADS.P0)
chan3 = AnalogIn(ads3, ADS.P0)
chan4 = AnalogIn(ads4, ADS.P0)
chan5 = AnalogIn(ads5, ADS.P0)
chan6 = AnalogIn(ads6, ADS.P0)

# initial1 = chan1.voltage
# initial2 = chan2.voltage
# initial3 = chan3.voltage
# initial4 = chan4.voltage
# initial5 = chan5.voltage
# initial6 = chan6.voltage
global readout1_var, readout2_var, readout3_var, readout4_var, readout5_var, readout6_var
readout1_var = tk.StringVar()
readout1_var.set("-")
readout2_var = tk.StringVar()
readout2_var.set("-")
readout3_var = tk.StringVar()
readout3_var.set("-")
readout4_var = tk.StringVar()
readout4_var.set("-")
readout5_var = tk.StringVar()
readout5_var.set("-")
readout6_var = tk.StringVar()
readout6_var.set("-")

global sg1, sg2, sg3, sg4, sg5, sg6
sg1 = tk.StringVar()
sg2 = tk.StringVar()
sg3 = tk.StringVar()
sg4 = tk.StringVar()
sg5 = tk.StringVar()
sg6 = tk.StringVar()
sg1.set("1")
sg2.set("1")
sg3.set("1")
sg4.set("1")
sg5.set("1")
sg6.set("1")
global average_set  # this will be the set of instantaneous average readings to be moving averaged
global moving_average  # this will be the current moving average over the last points at any moment
global moving_average_set  # this is the set of moving averages to graph
global average_val_final
global btn_pressed, avg_readout
btn_pressed = tk.StringVar()
btn_pressed.set('F')
initial1 = 0
initial2 = 0
initial3 = 0
initial4 = 0
initial5 = 0
initial6 = 0

global initial_icp, avg_icp
initial_icp = tk.StringVar()
avg_icp = tk.StringVar()
avg_icp.set("-")

average_set = []  # this initializes the set of averages for the moving average
moving_average_set = []
moving_average = 0

root = tk.Tk()
root.configure(bg='white')

# finding the width and height of the window so application is fullscreen
width = root.winfo_screenwidth()
height = root.winfo_screenheight()
create_Main_Window()

##the following code is also what was used to plot the average icp graph
figure, ax = plt.subplots(1, 1, figsize=(12, 9))
plt.ion()
x = np.array([])
y = np.array([])
p2 = np.array([])
plt.ylim(0, 20)
plt.xlim(0, 20)
ax.set_xlabel("Time (s)", size=20)
ax.set_ylabel("ICP Value (mmHg)", size=20)
figure.set_tight_layout(True)
plot = ax.plot(x, y)
canvas = FigureCanvasTkAgg(figure, root)
canvas.draw()
canvas.get_tk_widget().place(relx=0, rely=.08)

# ani = animation.FuncAnimation(fig, animate, interval=500, frames = 100)


# initializing the TopLevel window for individual readouts
indiv_readouts = tk.Toplevel(root, background='white')

# hiding the window so that only the main one is showing until button is clicked
indiv_readouts.withdraw()
create_Indiv_ICP_Window(root)

print("about to get icp")
print("graph plotted")
main_fcn(p2, y)
print("got icp")
tk.mainloop()
"""
Created on Thu Mar 30 21:03:58 2023

@author: Grace Baird

Last update: 5/12/2023

"""

import tkinter as tk
from tkinter import *
from tkinter import ttk
from matplotlib.figure import *
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg,
                                               NavigationToolbar2Tk)
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import random
import time
import re
# Import all the i2c stuff
import busio
import board
import adafruit_tca9548a
import time
from datetime import datetime
import adafruit_ads1x15.ads1015 as ADS
from adafruit_ads1x15.analog_in import AnalogIn


###GUI functions

def mainMenu():  # deletes window when button is pushed after time
    indiv_readouts.withdraw()
    root.deiconify()


def create_Main_Window():  # creating main window
    root.title("GAMIX ICP MONITOR")
    root.geometry("%dx%d" % (width, height))
    print("creating main window")
    # creating actual plot with label
    plot_label = tk.Label(root, text="Moving-Averaged ICP (mmHg)", bg='white',
                          font=("Arial", 17))
    plot_label.place(relx=.26, rely=.05)

    # creating button to go to the individual ICP page
    next_button = tk.Button(root, text="Individual ICP Readouts",
                            height=2, width=20, font=('Arial', 15),
                            command=openIndividualReadouts)
    next_button.place(relx=0.87, rely=0)

    # instructions for the clibration input
    calib_instr = tk.Label(root, text="Please input initial ICP value then press ''Calibrate''",
                           bg='snow', font=('Arial', 12))
    calib_instr.place(relx=.71, rely=.69)

    # label for calibration box
    calib_label = tk.Label(root, text='Calibration Value', font=('Arial', 12),
                           bg='white')
    calib_label.place(relx=.74, rely=.72)

    # input box for calibration
    calib_input = tk.Entry(root, textvariable=initial_icp,
                           width=10)
    calib_input.place(relx=.82, rely=.72)

    # recalibrate and calibrate btns

    recalib_btn = tk.Button(root, text="Recalibrate", state=DISABLED,
                            height=1, width=10, font=('Arial', 12),
                            command=lambda: recalibrate(calib_input, calib_btn, recalib_btn))
    calib_btn = tk.Button(root, text="Calibrate", state=NORMAL,
                          height=1, width=10, font=('Arial', 12),
                          command=lambda: calibrate(calib_input, calib_btn, recalib_btn))
    calib_btn.place(relx=.74, rely=.75)
    recalib_btn.place(relx=.81, rely=.75)

    # display for the average value
    avg_readout = tk.Label(root, textvariable=avg_icp,
                           highlightthickness=3, highlightcolor="gray", highlightbackground="gray",
                           height=7, width=14, bg='tomato',
                           name="readout1", font=("Arial", 30))
    avg_readout.place(relx=0.72, rely=0.1)

    # label for average value
    avg_val_label = tk.Label(root, bg='white', font=("Arial", 15),
                             text='Current ICP Value (mmHg)', height=2, width=28)
    avg_val_label.place(relx=0.72, rely=.43)
    # def plot_main(master):  # creating a basic plot on the first page
    print("done creating main window")


def create_Indiv_ICP_Window(master):
    # geometry and title
    indiv_readouts.title("INDIVIDUAL ICP READOUTS")
    indiv_readouts.geometry("%dx%d" % (width, height))
    print("creating individual windows")
    # main menu button to go back to main page

    mainMenu_button = tk.Button(indiv_readouts, text="Main Menu",
                                height=2, width=10, font=('Arial', 17),
                                command=lambda: mainMenu())
    mainMenu_button.place(relx=0, rely=0)
    # if you dont add the lambda it will assign the command value to the return
    # from the mainMenu function which will immediately close the window
    # the lambda function assigns a callable object which will only execute
    # when given an input

    # adding the 6 different labels with string variables that will updated

    # displays for the six different strain gauges
    readout1 = tk.Label(indiv_readouts, textvariable=readout1_var, bg='lightgreen',
                        highlightthickness=3, highlightcolor="black", highlightbackground="black",
                        height=5, width=11,
                        name="readout1", font=("Arial", 30))
    readout1.place(relx=0.12, rely=0.1)

    r1_label = tk.Label(indiv_readouts, bg='white', text='Strain Gauge 1',
                        font=("Arial", 14))
    r1_label.place(relx=0.125, rely=0.36)

    readout2 = tk.Label(indiv_readouts, textvariable=readout2_var, bg='lightgreen',
                        highlightthickness=3, highlightcolor="black", highlightbackground="black",
                        height=5, width=11,
                        name="readout2", font=("Arial", 30))
    readout2.place(relx=0.42, rely=0.1)  # new2
    r2_label = tk.Label(indiv_readouts, bg='white', text='Strain Gauge 2',
                        font=("Arial", 14))
    r2_label.place(relx=0.425, rely=0.36)

    readout3 = tk.Label(indiv_readouts, textvariable=readout3_var, bg='lightgreen',
                        highlightthickness=3, highlightcolor="black", highlightbackground="black",
                        height=5, width=11,
                        name="readout3", font=("Arial", 30))
    readout3.place(relx=0.72, rely=0.1)  # new3
    r3_label = tk.Label(indiv_readouts, bg='white', text='Strain Gauge 3',
                        font=("Arial", 14))
    r3_label.place(relx=0.725, rely=0.36)

    readout4 = tk.Label(indiv_readouts, textvariable=readout4_var, bg='lightgreen',
                        highlightthickness=3, highlightcolor="black", highlightbackground="black",
                        height=5, width=11,
                        name="readout4", font=("Arial", 30))
    readout4.place(relx=0.12, rely=0.5)  # new4
    r4_label = tk.Label(indiv_readouts, bg='white', text='Strain Gauge 4',
                        font=("Arial", 14))
    r4_label.place(relx=0.125, rely=0.76)

    readout5 = tk.Label(indiv_readouts, textvariable=readout5_var, bg='lightgreen',
                        highlightthickness=3, highlightcolor="black", highlightbackground="black",
                        height=5, width=11,
                        name="readout5", font=("Arial", 30))
    readout5.place(relx=0.42, rely=0.5)  # new5
    r5_label = tk.Label(indiv_readouts, bg='white', text='Strain Gauge 5',
                        font=("Arial", 14))
    r5_label.place(relx=0.425, rely=0.76)

    readout6 = tk.Label(indiv_readouts, textvariable=readout6_var, bg='lightgreen',
                        highlightthickness=3, highlightcolor="black", highlightbackground="black",
                        height=5, width=11,
                        name="readout6", font=("Arial", 30))
    readout6.place(relx=.72, rely=0.5)
    r6_label = tk.Label(indiv_readouts, bg='white', text='Strain Gauge 6',
                        font=("Arial", 14))
    r6_label.place(relx=0.725, rely=0.76)

    # adding the add buttons to the readouts
    # 1
    addButton1 = tk.Button(indiv_readouts, text="Add", heigh=1, width=8, state=DISABLED,
                           command=lambda: addBtn(addButton1, removeButton1, readout1, sg1))
    addButton1.place(relx=0.2, rely=0.34)
    # 2
    addButton2 = tk.Button(indiv_readouts, text="Add", heigh=1, width=8, state=DISABLED,
                           command=lambda: addBtn(addButton2, removeButton2, readout2, sg2))
    addButton2.place(relx=0.5, rely=0.34)
    # 3
    addButton3 = tk.Button(indiv_readouts, text="Add", heigh=1, width=8, state=DISABLED,
                           command=lambda: addBtn(addButton3, removeButton3, readout3, sg3))
    addButton3.place(relx=0.8, rely=0.34)
    # 4
    addButton4 = tk.Button(indiv_readouts, text="Add", heigh=1, width=8, state=DISABLED,
                           command=lambda: addBtn(addButton4, removeButton4, readout4, sg4))
    addButton4.place(relx=0.2, rely=0.74)
    # 5
    addButton5 = tk.Button(indiv_readouts, text="Add", heigh=1, width=8, state=DISABLED,
                           command=lambda: addBtn(addButton5, removeButton5, readout5, sg5))
    addButton5.place(relx=0.5, rely=0.74)
    # 6
    addButton6 = tk.Button(indiv_readouts, text="Add", heigh=1, width=8, state=DISABLED,
                           command=lambda: addBtn(addButton6, removeButton6, readout6, sg6))
    addButton6.place(relx=0.8, rely=0.74)

    # adding the remove buttons to the readouts
    # 1
    removeButton1 = tk.Button(indiv_readouts, text="Remove", height=1, width=8,
                              command=lambda: removeBtn(addButton1, removeButton1, readout1, sg1))
    removeButton1.place(relx=0.2, rely=0.37)
    # 2
    removeButton2 = tk.Button(indiv_readouts, text="Remove", height=1, width=8,
                              command=lambda: removeBtn(addButton2, removeButton2, readout2, sg2))
    removeButton2.place(relx=0.5, rely=0.37)
    # 3
    removeButton3 = tk.Button(indiv_readouts, text="Remove", height=1, width=8,
                              command=lambda: removeBtn(addButton3, removeButton3, readout3, sg3))
    removeButton3.place(relx=0.8, rely=0.37)
    # 4
    removeButton4 = tk.Button(indiv_readouts, text="Remove", height=1, width=8,
                              command=lambda: removeBtn(addButton4, removeButton4, readout4, sg4))
    removeButton4.place(relx=0.2, rely=0.77)
    # 5
    removeButton5 = tk.Button(indiv_readouts, text="Remove", height=1, width=8,
                              command=lambda: removeBtn(addButton5, removeButton5, readout5, sg5))
    removeButton5.place(relx=0.5, rely=0.77)
    # 6
    removeButton6 = tk.Button(indiv_readouts, text="Remove", height=1, width=8,
                              command=lambda: removeBtn(addButton6, removeButton6, readout6, sg6))
    removeButton6.place(relx=0.8, rely=0.77)
    print("done creating individual windows")


def openIndividualReadouts():
    root.withdraw()
    indiv_readouts.deiconify()
    print("opening individual windows")


def addBtn(addButton, removeButton, readout, sgnum):  # changes state when add btn is pressed
    removeButton['state'] = NORMAL
    addButton['state'] = DISABLED
    readout['bg'] = 'lightgreen'
    readout['fg'] = 'black'
    readout['highlightcolor'] = 'black'
    readout['highlightbackground'] = 'black'
    readout['fg'] = 'black'
    sgnum.set('1')
    # will add code to add value to calculation


def removeBtn(addButton, removeButton, readout, sgnum):  # changes state when remove btn is pressed
    removeButton['state'] = DISABLED
    addButton['state'] = NORMAL
    readout['bg'] = 'tomato'
    readout['highlightcolor'] = 'gray'
    readout['highlightbackground'] = 'gray'
    readout['fg'] = 'gray'
    sgnum.set('0')
    # will add code to remove value to calculation


def calibrate(box, calib_btn, recalib_btn):  # once calibration btn is pressed
    if box.get() != "":
        btn_pressed.set('T')
        calib_btn['state'] = DISABLED
        box['state'] = DISABLED
        popup = tk.Tk()
        success_message = tk.Label(popup, text="Calibration successful!")
        success_message.pack()
        recalib_btn['state'] = NORMAL
        avg_readout['bg'] = 'lightgreen'
        avg_readout['highlightcolor'] = 'black'
        avg_readout['highlightbackground'] = 'black'


    else:
        popup = tk.Tk()
        warning_message = tk.Label(popup, text="Please enter calibration value and try again!")
        warning_message.pack()


def recalibrate(box, calib_btn, recalib_btn):  # once recalibration btn is pressed
    box['state'] = NORMAL
    box.after(10, box.delete(0, END))
    calib_btn['state'] = NORMAL
    recalib_btn['state'] = DISABLED
    avg_icp.set('-')
    avg_readout['bg'] = 'tomato'
    avg_readout['highlightcolor'] = 'gray'
    avg_readout['highlightbackground'] = 'gray'
    btn_pressed.set('F')


def main_fcn(p2, y):
    time_shown_s = 61
    div = time_shown_s / 10
    # define variables to carry over between readings

    points_taken = 10  # this is the number of points to take a moving average over
    while True:
        print('test')

        ###geting ICP values###
        if initial_icp.get() != '' and btn_pressed.get() == 'T':  # ensuring calibration number has been entered
            print(chan1.voltage)
            print(chan2.voltage)
            print(chan3.voltage)
            print(chan4.voltage)
            print(chan5.voltage)
            print(chan6.voltage)
            print('!')
            # getting voltage values from the channels
            num1 = round(chan1.voltage - initial1, 6)
            num2 = round(chan2.voltage - initial2, 6)
            num3 = round(chan3.voltage - initial3, 6)
            num4 = round(chan4.voltage - initial4, 6)
            num5 = round(chan5.voltage - initial5, 6)
            num6 = round(chan6.voltage - initial6, 6)

            sg1_val = int(sg1.get())
            sg2_val = int(sg2.get())
            sg3_val = int(sg3.get())
            sg4_val = int(sg4.get())
            sg5_val = int(sg5.get())
            sg6_val = int(sg6.get())

            pressure1 = num1
            pressure2 = num2
            pressure3 = num3
            pressure4 = num4
            pressure5 = num5
            pressure6 = num6
            # repeat for the remaining strain gauges

            average_val_initial = ((pressure1 * sg1_val) + (pressure2 * sg2_val) +
                                   (pressure3 * sg3_val) + (pressure4 * sg4_val) + (pressure5 * sg5_val) +
                                   (pressure6 * sg6_val)) / (sg1_val + sg2_val + sg3_val + sg4_val + sg5_val + sg6_val)

            average_val_final = round(average_val_initial, 6)

            if len(average_set) < points_taken - 1:  # this number is the number of points to take the average over
                average_set.append(average_val_final)
                moving_average = average_val_final
            if len(average_set) == points_taken - 1:
                average_set.append(average_val_final)
                moving_average = sum(average_set) / points_taken
            if len(average_set) > points_taken - 1:
                moving_average = moving_average + (average_val_final / points_taken) - (average_set[0] / points_taken)
                average_set.append(average_val_final)
                del average_set[0]
                moving_average_set.append(moving_average)

            # setting the string variables to the numbers so the label will update
            readout1_var.set(str(num1))
            readout2_var.set(str(num2))
            readout3_var.set(str(num3))
            readout4_var.set(str(num4))
            readout5_var.set(str(num5))
            readout6_var.set(str(num6))
            avg_icp.set(str(round(moving_average, 4)))


        else:  # if calibration value has not been entered
            readout1_var.set("-")
            readout2_var.set("-")
            readout3_var.set("-")
            readout4_var.set("-")
            readout5_var.set("-")
            readout6_var.set("-")
            avg_icp.set("-")

        ###Plotting graph###
        tick_marks = [*range(time_shown_s - 1, -1, -int(time_shown_s / div))]
        y = np.append(y, moving_average)
        end = len(y)
        new_y = y[max(0, end - (time_shown_s)): end]
        end2 = len(new_y)
        new_x = np.array(range(end2 - 1, -1, -1))
        p = datetime.now()
        p2 = np.append(p2, p.strftime("%I:%M:%S"))
        new_p2 = p2[max(0, end - (time_shown_s)): end]

        data = (new_x, new_y)
        plot[0].set(data=data)
        plt.ylim(min(y), max(y) + .1)
        plt.xlim(max(new_x), min(new_x) - (time_shown_s / 10))
        ax.set_xticks(tick_marks)
        final_p2 = sorted(new_p2, reverse=True)
        time_vals = np.pad(final_p2, (0, (time_shown_s) - len(new_p2)), 'constant', constant_values=0)
        ax.set_xticklabels(time_vals[tick_marks], rotation=67.5)
        ax.xaxis.set_tick_params(labelsize=12)
        ax.yaxis.set_tick_params(labelsize=12)
        figure.canvas.draw()
        figure.canvas.flush_events()

        time.sleep(.1)


# I2C Setup
i2c = board.I2C()
tca = adafruit_tca9548a.TCA9548A(i2c)

# 1 - white - 4
# 2 - black - 5
# 3 - yellow - 2
# 4 - red - 3
# 5 - blue - 7
# 6 - green - 6
ads1 = ADS.ADS1015(tca[5])
ads2 = ADS.ADS1015(tca[1])
ads3 = ADS.ADS1015(tca[3])
ads4 = ADS.ADS1015(tca[4])
ads5 = ADS.ADS1015(tca[2])
ads6 = ADS.ADS1015(tca[0])

chan1 = AnalogIn(ads1, ADS.P0)
chan2 = AnalogIn(ads2, ADS.P0)
chan3 = AnalogIn(ads3, ADS.P0)
chan4 = AnalogIn(ads4, ADS.P0)
chan5 = AnalogIn(ads5, ADS.P0)
chan6 = AnalogIn(ads6, ADS.P0)

# initial1 = chan1.voltage
# initial2 = chan2.voltage
# initial3 = chan3.voltage
# initial4 = chan4.voltage
# initial5 = chan5.voltage
# initial6 = chan6.voltage
global readout1_var, readout2_var, readout3_var, readout4_var, readout5_var, readout6_var
readout1_var = tk.StringVar()
readout1_var.set("-")
readout2_var = tk.StringVar()
readout2_var.set("-")
readout3_var = tk.StringVar()
readout3_var.set("-")
readout4_var = tk.StringVar()
readout4_var.set("-")
readout5_var = tk.StringVar()
readout5_var.set("-")
readout6_var = tk.StringVar()
readout6_var.set("-")

global sg1, sg2, sg3, sg4, sg5, sg6
sg1 = tk.StringVar()
sg2 = tk.StringVar()
sg3 = tk.StringVar()
sg4 = tk.StringVar()
sg5 = tk.StringVar()
sg6 = tk.StringVar()
sg1.set("1")
sg2.set("1")
sg3.set("1")
sg4.set("1")
sg5.set("1")
sg6.set("1")
global average_set  # this will be the set of instantaneous average readings to be moving averaged
global moving_average  # this will be the current moving average over the last points at any moment
global moving_average_set  # this is the set of moving averages to graph
global average_val_final
global btn_pressed, avg_readout
btn_pressed = tk.StringVar()
btn_pressed.set('F')
initial1 = 0
initial2 = 0
initial3 = 0
initial4 = 0
initial5 = 0
initial6 = 0

global initial_icp, avg_icp
initial_icp = tk.StringVar()
avg_icp = tk.StringVar()
avg_icp.set("-")

average_set = []  # this initializes the set of averages for the moving average
moving_average_set = []
moving_average = 0

root = tk.Tk()
root.configure(bg='white')

# finding the width and height of the window so application is fullscreen
width = root.winfo_screenwidth()
height = root.winfo_screenheight()
create_Main_Window()

##the following code is also what was used to plot the average icp graph
figure, ax = plt.subplots(1, 1, figsize=(12, 9))
plt.ion()
x = np.array([])
y = np.array([])
p2 = np.array([])
plt.ylim(0, 20)
plt.xlim(0, 20)
ax.set_xlabel("Time (s)", size=20)
ax.set_ylabel("ICP Value (mmHg)", size=20)
figure.set_tight_layout(True)
plot = ax.plot(x, y)
canvas = FigureCanvasTkAgg(figure, root)
canvas.draw()
canvas.get_tk_widget().place(relx=0, rely=.08)

# ani = animation.FuncAnimation(fig, animate, interval=500, frames = 100)


# initializing the TopLevel window for individual readouts
indiv_readouts = tk.Toplevel(root, background='white')

# hiding the window so that only the main one is showing until button is clicked
indiv_readouts.withdraw()
create_Indiv_ICP_Window(root)

print("about to get icp")
print("graph plotted")
main_fcn(p2, y)
print("got icp")
tk.mainloop()
