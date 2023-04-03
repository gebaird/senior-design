"""
Created on Thu Mar 30 21:03:58 2023

@author: Grace Baird

Last update: 3/31/2023 10:29 PM

"""

import tkinter as tk
from tkinter import *
from tkinter import ttk
from matplotlib.figure import *
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg,
                                               NavigationToolbar2Tk)


def plot_main(master):  # creating a basic plot on the first page
    # will update with time-average after figuring that out

    fig = Figure(figsize=(2, 3), dpi=100)
    y = range(10)
    plot1 = fig.add_subplot(111)
    plot1.plot(y)

    canvas = FigureCanvasTkAgg(fig, master)
    canvas.draw()
    canvas.get_tk_widget().pack()
    main_graph = FigureCanvasTkAgg()

def new_plot(screen, offsetx, offsety):  # creating a basic plot on the first page
    # will update with time-average after figuring that out
    fig = Figure(figsize=(2, 2), dpi=100, facecolor= 'lightgreen')
    y = range(10)
    plot1 = fig.add_subplot(111)
    plot1.plot(y)

    canvas = FigureCanvasTkAgg(fig, master=screen)
    canvas.draw()
    canvas.get_tk_widget().place(relheight = 0.3, relwidth = 0.3, relx = 0.3* offsetx+0.05,
                              rely = 0.3*offsety + 0.03*(offsety+1))

def replot(offsetx, offsety):
    fig = Figure(figsize=(2, 2), dpi=100, facecolor='tomato')
    y = range(10)
    plot1 = fig.add_subplot(111)
    plot1.plot(y)
    canvas = FigureCanvasTkAgg(fig, master=indiv_readouts)
    canvas.draw()
    canvas.get_tk_widget().place(relheight=0.3, relwidth=0.3, relx=0.3 * offsetx + 0.05,
                                 rely=0.3 * offsety + 0.03 * (offsety + 1))

def graphButtons(master):
    addButton = tk.Button(master, text = "Add", heigh = 1, width = 5, state = DISABLED ) #command = lambda: addValue()
    addButton.place(relx = 0.10, rely = 0.33)
    removeButton = tk.Button(master, text = "Remove", height = 1, width = 10, command = lambda: removeValue(removeButton))
    removeButton.place(relx = 0.15, rely = 0.33)


def addValue(addButton, removeButton, xoff, yoff):
    removeButton['state'] = NORMAL
    addButton['state'] = DISABLED
    newreadout1 = new_plot(indiv_readouts, xoff, yoff)

def removeValue(addButton, removeButton, xoff, yoff):
    removeButton['state'] = DISABLED
    addButton['state'] = NORMAL
    newreadout1 = replot(xoff,yoff)


def openIndividualReadouts():
    root.withdraw()
    indiv_readouts.deiconify()


def mainMenu():  # deletes window when button is pushed after time
    indiv_readouts.withdraw()
    root.deiconify()


###############################################################################
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

#adding the 6 different plots using new_plot(master, xoffset, yoffset)
    readout1 = new_plot(indiv_readouts, 0, 0)
    readout2 = new_plot(indiv_readouts, 0, 1.5)
    readout3 = new_plot(indiv_readouts, 1, 0)
    readout4 = new_plot(indiv_readouts, 1, 1.5)
    readout5 = new_plot(indiv_readouts, 2, 0)
    readout6 = new_plot(indiv_readouts, 2, 1.5)

#adding the add buttons to the readouts
    #1
    addButton1 = tk.Button(indiv_readouts, text="Add", heigh=1, width=5, state=DISABLED,
                        command = lambda: addValue(addButton1, removeButton1, 0,0))
    addButton1.place(relx=0.10, rely=0.33)
    #2
    addButton2 = tk.Button(indiv_readouts, text="Add", heigh=1, width=5, state=DISABLED,
                          command=lambda: addValue(addButton2, removeButton2, 0, 1.5))
    addButton2.place(relx=0.10, rely=0.825)
    #3
    addButton3 = tk.Button(indiv_readouts, text="Add", heigh=1, width=5, state=DISABLED,
                           command=lambda: addValue(addButton3, removeButton3, 1, 0))
    addButton3.place(relx=0.40, rely=0.33)
    #4
    addButton4 = tk.Button(indiv_readouts, text="Add", heigh=1, width=5, state=DISABLED,
                           command=lambda: addValue(addButton4, removeButton4, 1, 1.5))
    addButton4.place(relx=0.40, rely=0.825)
    #5
    addButton5 = tk.Button(indiv_readouts, text="Add", heigh=1, width=5, state=DISABLED,
                           command=lambda: addValue(addButton5, removeButton5, 2, 0))
    addButton5.place(relx=0.70, rely=0.33)
    #6
    addButton6 = tk.Button(indiv_readouts, text="Add", heigh=1, width=5, state=DISABLED,
                           command=lambda: addValue(addButton6, removeButton6, 2, 1.5))
    addButton6.place(relx=0.70, rely=0.825)

#adding the remove buttons to the readouts
    #1
    removeButton1 = tk.Button(indiv_readouts, text="Remove", height=1, width=10,
                           command = lambda: removeValue(addButton1, removeButton1, 0, 0))
    removeButton1.place(relx=0.15, rely=0.33)
    #2
    removeButton2 = tk.Button(indiv_readouts, text="Remove", height=1, width=10,
                           command = lambda: removeValue(addButton2, removeButton2, 0, 1.5))
    removeButton2.place(relx=0.15, rely=0.825)
    #3
    removeButton3 = tk.Button(indiv_readouts, text="Remove", height=1, width=10,
                           command = lambda: removeValue(addButton3, removeButton3,1, 0))
    removeButton3.place(relx=0.45, rely=0.33)
    #4
    removeButton4 = tk.Button(indiv_readouts, text="Remove", height=1, width=10,
                           command = lambda: removeValue(addButton4, removeButton4, 1, 1.5))
    removeButton4.place(relx=0.45, rely=0.825)
    #5
    removeButton5 = tk.Button(indiv_readouts, text="Remove", height=1, width=10,
                           command = lambda: removeValue(addButton5, removeButton5, 2, 0))
    removeButton5.place(relx=0.75, rely=0.33)
    #6
    removeButton6 = tk.Button(indiv_readouts, text="Remove", height=1, width=10,
                           command = lambda: removeValue(addButton6, removeButton6, 2, 1.5))
    removeButton6.place(relx=0.75, rely=0.825)


# inidializing the first window
root = tk.Tk()
create_Main_Window()
#initializing the TopLevel window
indiv_readouts = tk.Toplevel(root)
#hiding the window so that only the main one is showing until button is clicked
indiv_readouts.withdraw()
create_Indiv_ICP_Window(root)
tk.mainloop()

quit()