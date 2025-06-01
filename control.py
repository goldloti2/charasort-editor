from view import View
from model import Model

class Controller:
    def __init__(self):
        window = View(self)
        self.window = window
    
    def start(self):
        self.window.start()
    
    def update_filters(self):
        self.window.destroy_filters()
        self.window.add_filters(self.model.flt_list)
    
    def update_characters(self):
        self.window.destroy_characters()
        self.window.add_characters(self.model.chr_list)

    def open_file(self, path = "test.js"):
        self.model = Model(path)
        self.update_filters()
        self.update_characters()



if __name__ == "__main__":
    app = Controller()
    app.start()