from calmjs.parse import io, es5

def open_file(path):
    with open(path, "r") as file:
        tree = io.read(es5, file)
    return tree