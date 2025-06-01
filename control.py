from view import View
from model import Model

class Controller:
    def __init__(self):
        window = View(self)
        self.window = window
        self.update_view()
    
    def start(self):
        self.window.start()
    
    def update_view(self):
        self.window.add_filter("haha")
        self.window.add_filter("hihi")

    def open_file(self, path = "test.js"):
        self.model = Model(path)



if __name__ == "__main__":
    app = Controller()
    app.start()