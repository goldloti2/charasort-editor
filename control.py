from model import Model
from view import View


class Controller:
    def __init__(self):
        window = View(self)
        self.window = window

    def start(self):
        self.open_file()
        self.window.start()

    def open_file(self, path="test.js"):
        self.path = path
        self.model = Model(path)
        self.update_filters()
        self.update_characters()

    def save_file(self, path=""):
        if not path:
            self.model.save_file(self.path)
        else:
            self.path = path
            self.model.save_file(path)

    def delete(self, index: int, tab: str):
        self.model.delete(index, tab)
        if tab == "filter":
            self.update_filters()
        elif tab == "character":
            self.update_characters()

    def move_filter(self, index: int, direction: str):
        self.model.move_filter(index, direction)
        self.update_filters()

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
        if flt_list:
            self.window.refresh_tabs(flt_list, "filter")
        else:
            self.window.destroy_tabs("filter")

    def update_characters(self):
        chr_list = []
        for chr in self.model.chr_list:
            node = []
            node.append(("label", "name:", chr["name"]))
            node.append(("label", "img:", chr["img"]))
            opts = [("filter key:", "option:")]
            chr_opts = chr["opts"]
            for opt in chr_opts:
                opts.append((opt, chr_opts[opt]))
            node.append(("sub_frame", "filter options:", opts))
            chr_list.append(node)
        if chr_list:
            self.window.refresh_tabs(chr_list, "character")
        else:
            self.window.destroy_tabs("character")


if __name__ == "__main__":
    app = Controller()
    app.start()
