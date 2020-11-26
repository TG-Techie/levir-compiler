import sys

import levir

checks = (
    'class.lvr',
    'struct.lvr',
    'old_grammar.lvr',
    'new_grammar.lvr',
)

for filename in checks:
    with open(f"examples/{filename}", 'r') as file:
        with open(f"outputs/{filename}.c", 'w') as output:
            mod = levir.translate_file(file, output)
    print(f"done with '{filename}' check")
