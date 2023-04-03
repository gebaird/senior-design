"""
Created on Thu Mar 30 21:03:58 2023

@author: Grace Baird

Last update: 3/31/2023 1:28 PM

"""

import tkinter as tk
from tkinter import *
from tkinter import ttk
from matplotlib.figure import *
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg,
                                               NavigationToolbar2Tk)
import random
import time
def rand_num_generator(): #using to test to see if the label will update
    if initial_icp.get() != '':
        num1 = random.randint(1, int(round(float(initial_icp.get()))))
        num2 = random.randint(1, int(round(float(initial_icp.get()))))
        num3 = random.randint(1, int(round(float(initial_icp.get()))))
        num4 = random.randint(1, int(round(float(initial_icp.get()))))
        num5 = random.randint(1, int(round(float(initial_icp.get()))))
        num6 = random.randint(1, int(round(float(initial_icp.get()))))
        readout1_var.set(str(num1))
        readout2_var.set(str(num2))
        readout3_var.set(str(num3))
        readout4_var.set(str(num4))
        readout5_var.set(str(num5))
        readout6_var.set(str(num6))
    else:
        readout1_var.set("0")
        readout2_var.set("0")
        readout3_var.set("0")
        readout4_var.set("0")
        readout5_var.set("0")
        readout6_var.set("0")
    indiv_readouts.after(1000, rand_num_generator)


def mainMenu():  # deletes window when button is pushed after time
    indiv_readouts.withdraw()
    root.deiconify()
def create_Main_Window():
    root.title("GAMIX ICP MONITOR")
    global width, height
    #finding the width and height of the window so application is fullscreen
    width = root.winfo_screenwidth()
    height = root.winfo_screenheight()
    root.geometry("%dx%d" % (width, height))

    #creating actual plot with label
    plot_label = tk.Label(root, text="test plot")
    plot_label.pack(anchor="s")
    root_plot = plot_main(root)

    #creating button to go to the individual ICP page
    next_button = tk.Button(root, text="Individual ICP Readouts",
                         height = 1, width = 20,
                         command=openIndividualReadouts)
    next_button.pack(side ="top")

    #creating text box for calibration input
    global initial_icp
    initial_icp= tk.StringVar()
    print(initial_icp.get())
    label_calib= tk.Label(root, text = "Please input initial ICP value then press ''Calibrate''")
    label_calib.pack(anchor = 's')
    calib_input = tk.Entry(root, textvariable=initial_icp)
    calib_input.pack(anchor = 's')
    recalib_btn = tk.Button(root, text="Recalibrate", state = DISABLED,
                        command=lambda: recalibrate(calib_input, calib_btn, recalib_btn))
    calib_btn = tk.Button(root, text = "Calibrate", state = NORMAL,
                           command = lambda: calibrate(calib_input, calib_btn, recalib_btn))
    calib_btn.pack(anchor = 's')
def plot_main(master):  # creating a basic plot on the first page
    # will update with time-average after figuring that out

    fig = Figure(figsize=(6, 6), dpi=100)
    y = range(10)
    plot1 = fig.add_subplot(111)
    plot1.plot(y)

    canvas = FigureCanvasTkAgg(fig, master)
    canvas.draw()
    canvas.get_tk_widget().pack()
    main_graph = FigureCanvasTkAgg()

def create_Indiv_ICP_Window(master):
#geometry and title
    indiv_readouts.title("INDIVIDUAL ICP READOUTS")
    indiv_readouts.geometry("%dx%d" % (width, height))

#main menu button to go back to main page
    mainMenu_button = tk.Button(indiv_readouts, text="Main Menu",
                             heigh=1, width=10,
                             command=lambda: mainMenu())
    mainMenu_button.pack(anchor="c")
    # if you dont add the lambda it will assign the command value to the return
    # from the mainMenu function which will immediately close the window
    # the lambda function assigns a callable object which will only execute
    # when given an input

#adding the 6 different labels with string variables that will be the latest value
    global readout1_var, readout2_var, readout3_var, readout4_var, readout5_var, readout6_var
    readout1_var = tk.StringVar()
    readout1_var.set("1")
    readout2_var = tk.StringVar()
    readout2_var.set("2")
    readout3_var = tk.StringVar()
    readout3_var.set("3")
    readout4_var = tk.StringVar()
    readout4_var.set("4")
    readout5_var = tk.StringVar()
    readout5_var.set("5")
    readout6_var = tk.StringVar()
    readout6_var.set("6")

    readout1 = tk.Label(indiv_readouts, textvariable = readout1_var, bg= 'lightgreen',
                        height = 5, width = 10,
                        name = "readout1", font = ("Arial", 30))
    readout1.place(relx=0.1, rely = 0.1)

    readout2 = tk.Label(indiv_readouts, textvariable = readout2_var, bg= 'lightgreen',
                        height = 5, width = 10,
                        name = "readout2", font = ("Arial", 30))
    readout2.place(relx=0.1, rely = 0.6)

    readout3 = tk.Label(indiv_readouts, textvariable = readout3_var, bg= 'lightgreen',
                        height = 5, width = 10,
                        name = "readout3", font = ("Arial", 30))
    readout3.place(relx=0.4, rely = 0.1)

    readout4 = tk.Label(indiv_readouts, textvariable = readout4_var, bg= 'lightgreen',
                        height = 5, width = 10,
                        name = "readout4", font = ("Arial", 30))
    readout4.place(relx=0.4, rely = 0.6)

    readout5 = tk.Label(indiv_readouts, textvariable = readout5_var, bg= 'lightgreen',
                        height =5, width = 10,
                        name = "readout5", font = ("Arial", 30))
    readout5.place(relx=0.7, rely = 0.1)

    readout6 = tk.Label(indiv_readouts, textvariable = readout6_var, bg = 'lightgreen',
                        height = 5, width = 10,
                        name = "readout6", font = ("Arial", 30))
    readout6.place(relx=.7, rely = 0.6)

#adding the add buttons to the readouts
    #1
    addButton1 = tk.Button(indiv_readouts, text="Add", heigh=1, width=5, state=DISABLED,
                        command = lambda: addBtn(addButton1, removeButton1, readout1))
    addButton1.place(relx=0.10, rely=0.33)
    #2
    addButton2 = tk.Button(indiv_readouts, text="Add", heigh=1, width=5, state=DISABLED,
                           command=lambda: addBtn(addButton2, removeButton2, readout2))
    addButton2.place(relx=0.10, rely=0.825)
    #3
    addButton3 = tk.Button(indiv_readouts, text="Add", heigh=1, width=5, state=DISABLED,
                           command=lambda: addBtn(addButton3, removeButton3, readout3))
    addButton3.place(relx=0.40, rely=0.33)
    #4
    addButton4 = tk.Button(indiv_readouts, text="Add", heigh=1, width=5, state=DISABLED,
                           command=lambda: addBtn(addButton4, removeButton4, readout4))
    addButton4.place(relx=0.40, rely=0.825)
    #5
    addButton5 = tk.Button(indiv_readouts, text="Add", heigh=1, width=5, state=DISABLED,
                           command=lambda: addBtn(addButton5, removeButton5, readout5))
    addButton5.place(relx=0.70, rely=0.33)
    #6
    addButton6 = tk.Button(indiv_readouts, text="Add", heigh=1, width=5, state=DISABLED,
                           command=lambda: addBtn(addButton6, removeButton6, readout6))
    addButton6.place(relx=0.70, rely=0.825)

#adding the remove buttons to the readouts
    #1
    removeButton1 = tk.Button(indiv_readouts, text="Remove", height=1, width=10,
                              command = lambda: removeBtn(addButton1, removeButton1, readout1))
    removeButton1.place(relx=0.15, rely=0.33)
    #2
    removeButton2 = tk.Button(indiv_readouts, text="Remove", height=1, width=10,
                              command = lambda: removeBtn(addButton2, removeButton2, readout2))
    removeButton2.place(relx=0.15, rely=0.825)
    #3
    removeButton3 = tk.Button(indiv_readouts, text="Remove", height=1, width=10,
                              command = lambda: removeBtn(addButton3, removeButton3, readout3))
    removeButton3.place(relx=0.45, rely=0.33)
    #4
    removeButton4 = tk.Button(indiv_readouts, text="Remove", height=1, width=10,
                              command = lambda: removeBtn(addButton4, removeButton4, readout4))
    removeButton4.place(relx=0.45, rely=0.825)
    #5
    removeButton5 = tk.Button(indiv_readouts, text="Remove", height=1, width=10,
                              command = lambda: removeBtn(addButton5, removeButton5, readout5))
    removeButton5.place(relx=0.75, rely=0.33)
    #6
    removeButton6 = tk.Button(indiv_readouts, text="Remove", height=1, width=10,
                              command = lambda: removeBtn(addButton6, removeButton6, readout6))
    removeButton6.place(relx=0.75, rely=0.825)

def openIndividualReadouts():
    root.withdraw()
    indiv_readouts.deiconify()

def addBtn(addButton, removeButton, readout):
    removeButton['state'] = NORMAL
    addButton['state'] = DISABLED
    readout['bg'] = 'lightgreen'
    readout['fg'] = 'black'

def removeBtn(addButton, removeButton, readout):
    removeButton['state'] = DISABLED
    addButton['state'] = NORMAL
    readout['bg'] = 'tomato'
    readout['fg'] = 'gray'

def calibrate(box, calib_btn, recalib_btn):
    if box.get() != "":
        calib_btn['state']= DISABLED
        box['state'] = DISABLED
        popup = tk.Tk()
        success_message = tk.Label(popup, text = "Calibration successful!")
        success_message.pack()
        recalib_btn.pack()
        if recalib_btn['state'] == DISABLED:
            recalib_btn['state'] = NORMAL
    else:
        popup = tk.Tk()
        warning_message = tk.Label(popup, text="Please enter calibration value and try again!")
        warning_message.pack()

def recalibrate(box, calib_btn, recalib_btn):
    box['state'] = NORMAL
    box.after(10, box.delete(0, END))
    calib_btn['state'] = NORMAL
    recalib_btn['state'] = DISABLED

# inidializing the first window
root = tk.Tk()
create_Main_Window()
#initializing the TopLevel window
indiv_readouts = tk.Toplevel(root)
#hiding the window so that only the main one is showing until button is clicked
indiv_readouts.withdraw()
create_Indiv_ICP_Window(root)
rand_num_generator()
tk.mainloop()