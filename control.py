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

    def open_file(self, path = "test.js"):
        self.model = Model(path)
        self.update_filters()



if __name__ == "__main__":
    app = Controller()
    app.start()