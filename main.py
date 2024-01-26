# главный файл, в котором по идее должна быть реализована связь gui и interp, т.е. работа всей программы
from interp import Interp
import gui_v1 as gui
from serv import Server
import threading

server = Server()
gui.find_server(server)
gui.run_gui()