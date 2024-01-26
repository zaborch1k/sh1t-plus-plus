# графика (backup)
# баги: не работает повторный запуск проги
import arcade
import threading
import tkinter as tk
import tkinter.filedialog as tfd
import tkinter.messagebox as tmb


SCREEN_WIDTH = 500
SCREEN_HEIGHT = 500
SCREEN_TITLE = "*performing field* (pls touch this window to update)"


prog_space = tk.Tk()
prog_space.title("interp") #тут менять название
prog_space.geometry("500x500")
prog_space.resizable(False, False)
window = None
file_name = ""
first = True
def create_polygon():
    global window
    window = Polygon(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    
def run_polygon():
    global t
    global first
    if first == True:
        create_polygon()
        first = False
    t = threading.Thread(target=arcade.run, daemon=True)
    t.start()

def kill_polygon():
    global window
    global t
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
    with open(file_name,  encoding="utf-8") as bobr:
        content_text.insert(1.0, bobr.read())

content_text = tk.Text(prog_space, wrap="word")
content_text.place(x=0, y=70, relheight=1, relwidth=1)

stop_button = tk.Button(prog_space, text="STOP", width=10, height=2, command=kill_polygon)
stop_button.place(x=60, y=20)

start_button = tk.Button(prog_space, text="START", width=10, height=2, command=run_polygon)
start_button.place(x=160, y=20)

save_button = tk.Button(prog_space, text="SAVE", width=10, height=2, command=save_file)
save_button.place(x=260, y=20)

open_button = tk.Button(prog_space, text="OPEN", width=10, height=2, command=open_file)
open_button.place(x=360, y=20)


class Performer(arcade.Sprite):
    def __init__(self, window):
        super().__init__("норм точка.png", 0.1)
        # один шаг в любую сторону - 47.25
        self.center_x = 250 
        self.center_y = 250 

    def update(self, dir, num):
        # добавить проверку на границы экрана
        step = 23.625
        w = 486.25
        h = 486.25
        if self.center_x + step * num <= w and dir == 'RIGHT':
            self.center_x += step * num

        elif self.center_x - step * num > 0 and dir == 'LEFT':
            self.center_x -= step * num

        elif self.center_y + step * num <= w and dir == 'UP':
            self.center_y += step * num

        elif self.center_y - step * num > 0 and dir == 'DOWN':
            self.center_y -= step * num
        else:
            pass # вызов исключения 'попытка выйти за границы поля'

class Polygon(arcade.Window):
    def __init__(self, width, height, title):
        super().__init__(width, height, title)
        self.bg = arcade.load_texture("мош_фон.jpeg") 
        self.performer = Performer(self)

    def on_draw(self):
        self.clear()
        arcade.draw_texture_rectangle(SCREEN_WIDTH / 2,
                                      SCREEN_HEIGHT / 2,
                                      SCREEN_WIDTH,
                                      SCREEN_HEIGHT,
                                      self.bg)
        self.performer.draw()

    def update(self, delta_time: float):
        global data # должно быть полчучение data от interp -> (ex) ['RIGHT', 3]
        if len(data) >= 1:
            self.performer.update('UP', data[0])
            del data[0]
        print(self.performer.center_x)

data = [10]
prog_space.mainloop()