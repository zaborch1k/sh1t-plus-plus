# проводник между gui и main
import threading

class Server:
    def __init__(self):
        pass

    def gui_to_ser(self, data):
        self.gui_data = data
    
    def main_to_ser(self, data):
        self.main_data = data
    
    def ser_to_main(self):
        return self.gui_data
    
    def ser_to_gui(self):
        return self.main_data



