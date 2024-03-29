# just a gui. a really ordinary one
import arcade
import threading
import tkinter as tk
import tkinter.filedialog as tfd
import tkinter.messagebox as tmb

import os
import sys

def resource_path(relative_path):
    if getattr(sys, 'frozen', False):
        base_path = sys._MEIPASS
    else:
        base_path = os.getcwd()
    return os.path.join(base_path, relative_path)


SCREEN_WIDTH = 500
SCREEN_HEIGHT = 500
SCREEN_TITLE = "*performing field* (pls touch this window to update)"

prog_space = tk.Tk()
prog_space.title("interp") 
prog_space.geometry("500x500")
prog_space.resizable(False, False)
prog_space.iconbitmap(resource_path('sh1t.ico'))
window = None
file_name = ""
first = True

def create_polygon():
    global window
    window = Polygon(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)

def run_polygon():
    from interp import get_data
    global t, first, window
    mdata = None
    err = None

    if first:
        create_polygon()
        first = False
        t = threading.Thread(target=window.run, daemon=True)
        t.start()
        oldc = None

    window.performer.center_x = 250
    window.performer.center_y = 250

    code = content_text.get(1.0, "end")

    data = get_data(code)
    
    mdata = data[0]
    err = data[1]
    pos = data[2]

    for i in mdata:
        window.performer.update(i[0], i[1])
    if err:
        error_msg(err)
    
def kill_polygon():
    global window, t
    window.performer.center_x = 250
    window.performer.center_y = 250
    t.join()

def save_file():
    tmb.showinfo(title="*сохранение файла*", message="Вы точно хотите сохранить файл?")
    global file_name
    file_name = tfd.asksaveasfilename(filetypes=(("text files", "*.txt"),)) + ".txt"
    content = content_text.get(1.0, "end")
    with open(file_name, "w", encoding="utf-8") as bobr:
        bobr.write(content)

def open_file():
    tmb.showinfo(title="*открытие файла*", message="Вы точно хотите открыть новый файл? \n(все несохраненные данные будут УТЕРЯНЫ НАВСЕГДА)")
    global file_name
    file_name = tfd.askopenfilename()
    content_text.delete(1.0, "end")
    try:
        with open(file_name,  encoding="utf-8") as bobr:
            content_text.insert(1.0, bobr.read())
    except:
        error_msg('ошибка при попытке открытия файла')


def error_msg(txt):
    tmb.showinfo(title="oops error :(", message=f'Error: {txt}')

content_text = tk.Text(prog_space, wrap="word")
content_text.place(x=0, y=70, relheight=1, relwidth=1)

stop_button = tk.Button(prog_space, text="STOP", width=10, height=2, command=kill_polygon)
stop_button.place(x=60, y=20)

start_button = tk.Button(prog_space, text="RUN", width=10, height=2, command=run_polygon)
start_button.place(x=160, y=20)

save_button = tk.Button(prog_space, text="SAVE", width=10, height=2, command=save_file)
save_button.place(x=260, y=20)

open_button = tk.Button(prog_space, text="OPEN", width=10, height=2, command=open_file)
open_button.place(x=360, y=20)


class Performer(arcade.Sprite):
    def __init__(self, window):
        super().__init__("C:\\Users\\user\\Documents\\GitHub\\interp\\норм точка.png", 0.1)
        self.center_x = 250 
        self.center_y = 250 

    def update(self, dir, num):
        step = 23.625
        m = 486.25
        if dir == 'RIGHT':
            self.center_x += step * num

        elif dir == 'LEFT':
            self.center_x -= step * num

        elif  dir == 'UP':
            self.center_y += step * num

        elif dir == 'DOWN':
            self.center_y -= step * num
            

class Polygon(arcade.Window):
    def __init__(self, width, height, title):
        super().__init__(width, height, title)
        self.bg = arcade.load_texture("C:\\Users\\user\\Documents\\GitHub\\interp\\мош_фон.jpeg") 
        self.performer = Performer(self)

    def on_draw(self):
        self.clear()
        arcade.draw_texture_rectangle(SCREEN_WIDTH / 2,
                                      SCREEN_HEIGHT / 2,
                                      SCREEN_WIDTH,
                                      SCREEN_HEIGHT,
                                      self.bg)
        self.performer.draw()

if __name__ == '__main__':
    prog_space.mainloop()
    