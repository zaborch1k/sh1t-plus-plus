# графика
import arcade
import threading
import tkinter as tk
import tkinter.filedialog as tfd
import tkinter.messagebox as tmb


SCREEN_WIDTH = 500
SCREEN_HEIGHT = 500
SCREEN_TITLE = "Пробник"


prog_space = tk.Tk()
prog_space.title("Имя") #тут менять название
prog_space.geometry("500x500")
prog_space.resizable(False, False)
window = None
file_name = ""
def create_polygon():
    global window
    window = Polygon(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    t = threading.Thread(target=arcade.run)
    t.start()

def kill_polygon():
    global window
    window.performer.center_x = 300 #тута пошали с координатами
    window.performer.center_y = 300 #тута пошали с координатами

def save_file():
    tmb.showinfo(title="Сохранение файла", message="Ожидайте сохранения файла")
    global file_name
    file_name = tfd.asksaveasfilename(filetypes=(("text files", "*.txt"),)) + ".txt"
    content = content_text.get(1.0, "end")
    with open(file_name, "w", encoding="utf-8") as bobr:
        bobr.write(content)

def open_file():
    tmb.showinfo(title="Открытие файла", message="Ожидайте открытия файла")
    global file_name
    file_name = tfd.askopenfilename()
    content_text.delete(1.0, "end")
    with open(file_name,  encoding="utf-8") as bobr:
        content_text.insert(1.0, bobr.read())

content_text = tk.Text(prog_space, wrap="word")
content_text.place(x=0, y=70, relheight=1, relwidth=1)

stop_button = tk.Button(prog_space, text="STOP", width=10, height=2, command=kill_polygon)
stop_button.place(x=60, y=20) #если есть неровность пошали с координатами

start_button = tk.Button(prog_space, text="START", width=10, height=2, command=create_polygon)
start_button.place(x=160, y=20) #если есть неровность пошали с координатами

save_button = tk.Button(prog_space, text="SAVE", width=10, height=2, command=save_file)
save_button.place(x=260, y=20) #если есть неровность пошали с координатами

open_button = tk.Button(prog_space, text="OPEN", width=10, height=2, command=open_file)
open_button.place(x=360, y=20) #если есть неровность пошали с координатами


class Performer(arcade.Sprite):
    def __init__(self, window):
        super().__init__("норм точка.png", 0.5)
        self.center_x = 250 #тута пошали с координатами
        self.center_y = 250 #тута пошали с координатами


class Polygon(arcade.Window):
    def __init__(self, width, height, title):
        super().__init__(width, height, title)
        self.bg = arcade.load_texture("мош_фон.jpeg") #тута качаем фон
        self.performer = Performer(self)

    def on_draw(self):
        self.clear()
        arcade.draw_texture_rectangle(SCREEN_WIDTH / 2,
                                      SCREEN_HEIGHT / 2,
                                      SCREEN_WIDTH,
                                      SCREEN_HEIGHT,
                                      self.bg) #тута рисуем фон
        self.performer.draw()


    def update(self, delta_time: float):
        self.performer.update()




prog_space.mainloop()