from tkinter import *

def run():
    global new_window
    new_window = Toplevel(root)
    new_window.title('New Window')

    global stop
    stop = Button(new_window, text='STOP', command=stop_window)
    stop.pack()

def stop_window():
    global new_window
    new_window.destroy()

root = Tk()
Button(root, text='RUN', command=run).pack()
root.mainloop()