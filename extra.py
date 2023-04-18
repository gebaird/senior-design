
import tkinter as tk


def switchButtonState():
    if (button1['state'] == tk.NORMAL):
        button1['state'] = tk.DISABLED
    else:
        button1['state'] = tk.NORMAL



def buttons():
    button1 = tk.Button(app, text="Python Button 1", state=tk.DISABLED)
    button2 = tk.Button(app, text="EN/DISABLE Button 1", command=switchButtonState)
    button1.pack()
    button2.pack()

app = tk.Tk()
app.geometry("200x200")
buttons()
app.mainloop()