from calmjs.parse import io, es5
from calmjs.parse import asttypes
from calmjs.parse.unparsers.es5 import pretty_print
from calmjs.parse.walkers import Walker

import controls

walker = Walker()

try:
    ast = controls.open_file("test.js")
except FileNotFoundError:
    raise IOError("haha")

# with open("out1.js", "w") as out1:
#     print(pretty_print(parsed, indent_str = "    "), file = out1)

# with open("out3", "w") as out3:
#     for i in walker.walk(ast):
#         print(type(i), file = out3)
#         print(i, file = out3)

for F_node in walker.filter(ast, lambda node: (
        isinstance(node, asttypes.Assign) and
        isinstance(node.left, asttypes.DotAccessor) and
        node.left.identifier.value == "options")):
    F_array = F_node.right
    for F_opt in F_array.children():
        is_type = False
        for prop in F_opt.properties:
            if isinstance(prop.right, asttypes.String) and prop.right.value == "\"type\"":
                prop.right.value = "\"TEST\""
                is_type = True
            if isinstance(prop.left, asttypes.PropIdentifier) and prop.left.value == "sub":
                type_sub = prop
        if is_type:
            # print(type(type_sub.right.children()))
            type_sub.right.children().append(asttypes.String("AAA"))
            # print(type_sub.right.children())
    temp = F_array.children()[0]
    F_array.children()[0] = F_array.children()[1]
    F_array.children()[1] = temp

with open("out4.js", "w") as out4:
    print(pretty_print(ast, indent_str = "    "), file = out4)