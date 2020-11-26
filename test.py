import sys

import levir

checks = (
    'old_grammar.lvr',
    'new_grammar.lvr',
    'class.lvr',
    'struct.lvr',
)

for filename in checks:
    with open(f"examples/{filename}", 'r') as file:
        with open(f"outputs/{filename}.c", 'w') as output:
            mod = levir.translate_file(file, output)
    print(f"done with '{filename}' check")
