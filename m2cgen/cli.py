"""CLI for m2cgen.

Example usage:
    ./gen <path_to_file> --language java
    gen --language java < <path_to_file>

Model can also be piped:
    cat <path_to_file> | gen --language java

"""
import pickle
import argparse
import sys

import m2cgen


LANGUAGE_TO_EXPORTER = {
    "python": m2cgen.export_to_python,
    "java": m2cgen.export_to_java,
}


parser = argparse.ArgumentParser(
    description="Generate code in native language for provided model")
parser.add_argument("infile", type=argparse.FileType("rb"), nargs="?",
                    default=sys.stdin.buffer,
                    help="File with pickle representation of the model")
parser.add_argument("--language", dest="language", type=str,
                    choices=LANGUAGE_TO_EXPORTER.keys(),
                    help="Target language",
                    required=True)


def parse_args(args):
    args = parser.parse_args(args)
    return args.infile, args.language


def generate_code(infile, language):
    with infile as f:
        model = pickle.load(f)

    exporter = LANGUAGE_TO_EXPORTER[language]
    return exporter(model)


def main():
    infile, language = parse_args(sys.argv[1:])
    print(generate_code(infile, language))
