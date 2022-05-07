from collections import OrderedDict
from typing import Dict, List


def parse(filename: str) -> Dict[str, List[str]]:
    last_added = ""
    output = OrderedDict()
    with open(filename) as f:
        for row in f:
            row = row.strip()
            if not row:
                continue

            if row == "Token definitions:":
                break

            if row[0] != "|":
                head, body = row.split("::=")
                head = head.strip()

                last_added = head

                body = [b.strip() for b in body.split() if b.strip()]
                output[head] = body
            else:
                body = row.strip()
                body = [b.strip() for b in body.split() if b.strip()]
                output[last_added].extend(body)

    return output


if __name__ == "__main__":
    grammar = parse("grammar/07 - SELECT_SPARQL.grammar")
    print("Total starting keys: %s" % len(grammar.keys()))
    initial_keys = set(grammar.keys())

    initial = "QueryUnit"

    modified = True
    while modified:
        to_pop = []
        modified = False

        for key in grammar:
            found = False
            for curr_key, body in grammar.items():
                if curr_key == key:
                    continue

                if key in body:
                    found = True
                    break

            if not found and key != initial:
                to_pop.append(key)

        if to_pop:
            modified = True

        for key in to_pop:
            grammar.pop(key)

    print("Final keys: %s" % len(grammar.keys()))
    print("Removed keys:", initial_keys - set(grammar.keys()))

    max_key_len = max([len(key) for key in grammar.keys()])
    with open("grammar/08 - SELECT_SPARQL.grammar", "w") as f:
        for key, value in grammar.items():
            f.write(
                f'{key}{" " * (max_key_len - len(key))} ::= {" ".join(value)}\n'
            )
