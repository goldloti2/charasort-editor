from view import View
from model import Model

class Controller:
    def __init__(self):
        window = View(self)
        self.window = window
    
    def start(self):
        self.open_file()
        self.window.start()
    
    def update_filters(self):
        flt_list = []
        for flt in self.model.flt_list:
            node = []
            node.append(("label", "name:", flt["name"]))
            node.append(("label", "key:", flt["key"]))
            node.append(("label", "tooltip:", flt.get("tooltip", "")))
            node.append(("label", "checked:", flt.get("checked", None)))
            if "sub" in flt:
                subs = [("name:", "key:")]
                for sub in flt["sub"]:
                    subs.append((sub["name"], sub["key"]))
                node.append(("sub_frame", "sub:", subs))
            flt_list.append(node)
        self.window.refresh_filters(flt_list)
    
    def update_characters(self):
        self.window.refresh_characters(self.model.chr_list)

    def open_file(self, path = "test.js"):
        self.model = Model(path)
        self.update_filters()
        self.update_characters()



if __name__ == "__main__":
    app = Controller()
    app.start()