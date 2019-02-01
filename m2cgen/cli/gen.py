"""CLI for m2cgen.

Example usage:

    ./gen <path_to_file> --language java
"""
import pickle
import argparse

import m2cgen


LANGUAGE_TO_EXPRTER = {
    "python": m2cgen.export_to_python,
    "java": m2cgen.export_to_java,
}


parser = argparse.ArgumentParser(
    description="Generate code in native language for provided model")
parser.add_argument("infile", type=argparse.FileType("rb"),
                    help="File with pickle representation of the model")
parser.add_argument("--language", dest="language", type=str,
                    choices=LANGUAGE_TO_EXPRTER.keys(), help="Target language",
                    required=True)


def main():
    args = parser.parse_args()

    with args.infile as f:
        model = pickle.load(f)

    exporter = LANGUAGE_TO_EXPRTER[args.language]
    print(exporter(model))