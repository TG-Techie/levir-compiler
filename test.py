import sys

import levir1

checks = (
    "class.lvr",
    "struct.lvr",
    "old_grammar.lvr",
    "new_grammar.lvr",
    "cond_old.lvr",
    "struct.lvr",
    # "methods.lvr",
)

for filename in checks:
    with open(f"examples/{filename}", "r") as file:
        with open(f"outputs/{filename}.c", "w") as output:
            mod = levir1.translate_file(file, output)
    print(f"done with '{filename}' check")
