import threading

class Server:
    def __init__(self):
        pass

    def do_thread(self, t):
        t.start()
    
    def join_thread(self, t):
        t.join()

    def gui_to_ser(self, data):
        self.gui_data = data
    
    def main_to_ser(self, data):
        self.main_data = data
    
    def ser_to_main(self):
        return self.gui_data
    
    def ser_to_gui(self):
        return self.main_data



