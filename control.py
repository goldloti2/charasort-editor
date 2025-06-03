from model import Model
from view import View


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
        self.window.refresh_tabs(flt_list, "filter")

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
        self.window.refresh_tabs(chr_list, "character")

    def open_file(self, path="test.js"):
        self.model = Model(path)
        self.update_filters()
        self.update_characters()


if __name__ == "__main__":
    app = Controller()
    app.start()
