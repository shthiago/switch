"""Read a grammar and generate de PLY files"""
import re
import sys

import jinja2

template = jinja2.Environment().from_string(
    '''def p_{{ funcname }}(p):
    """{{ production }}"""
    # TODO



'''
)

output = ""
with open(sys.argv[1]) as fp:
    for i, row in enumerate(fp):
        prod = row.strip()
        if not prod:
            continue

        prod = re.sub(" +", " ", prod)

        output += template.render(funcname=f"production_{i}", production=prod)

with open("output.py", "w") as f:
    f.write(output)
