from interp import Interp
import gui_v1 as gui
from serv import Server

server = Server()
gui.find_server(server)
gui.run_gui()
print(server.ser_to_main())
