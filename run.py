import argparse

from transpiler.cypher_generator import CypherGenerator


def main(filename: str):
    with open(filename) as f:
        content = f.read()

    generator = CypherGenerator()
    cypher = generator.generate(content)

    print(cypher)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="CLI for Switch")

    parser.add_argument("filename")

    args = parser.parse_args()

    main(args.filename)
