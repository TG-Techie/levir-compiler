import sys

import levir1

checks = (
    "class.lv1",
    "struct.lv1",
    "old_grammar.lv1",
    "new_grammar.lv1",
    "cond_old.lv1",
    "struct.lv1",
    "cond_new.lv1",
    "trycalls.lv1",
    # "methods.lv1",
)

for filename in checks:
    with open(f"examples/{filename}", "r") as file:
        with open(f"outputs/{filename}.c", "w") as output:
            mod = levir1.translate_file(file, output)
    print(f"done with '{filename}' check")
