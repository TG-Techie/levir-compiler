import sys

import levir

checks = (
    "exclass.lvr",
    "exstruct.lvr",
    #'old_grammar.lvr',
    "combo_struct_class.lvr",
    "excond.lvr",
    "exmethods.lvr",
)

for filename in checks:
    with open(f"examples/{filename}", "r") as file:
        with open(f"outputs/{filename}.c", "w") as output:
            print(f"'{file.name}'... ", end="")
            try:
                mod = levir.lexer_parser.parse_str(file.read())
            except Exception as e:
                raise Exception(f"{filename}:\n{type(e).__name__}:{e}")
    print(f"done parsing")
print("switching to takin")
for filename in checks:
    with open(f"examples/{filename}", "r") as file:
        with open(f"outputs/{filename}.c", "w") as output:
            print(f"'{file.name}'... ", end="")
            # try:
            mod = levir.translate_file(file, output)
            # except Exception as e:
            #    raise Exception(f"{filename}:\n{type(e).__name__}:{e}")
    print(f"done tout intaking")
