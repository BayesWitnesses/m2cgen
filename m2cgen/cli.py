"""CLI for m2cgen.

Example usage:
    $ m2cgen <path_to_file> --language java --class_name MyModel \
             --package_name foo.bar.baz
    $ m2cgen --language java < <path_to_file>

Model can also be piped:
    # cat <path_to_file> | m2cgen --language java

"""
import pickle
import argparse
import sys
import numpy as np

import m2cgen


LANGUAGE_TO_EXPORTER = {
    "python": (m2cgen.export_to_python, ["indent"]),
    "java": (
        m2cgen.export_to_java, ["indent", "class_name", "package_name"]),
    "c": (m2cgen.export_to_c, ["indent"]),
    "go": (m2cgen.export_to_go, ["indent"]),
}


# The maximum recursion depth is represented by the maximum int32 value.
MAX_RECURSION_DEPTH = np.iinfo(np.intc).max


parser = argparse.ArgumentParser(
    prog="m2cgen",
    description="Generate code in native language for provided model")
parser.add_argument(
    "infile", type=argparse.FileType("rb"), nargs="?",
    default=sys.stdin.buffer,
    help="File with pickle representation of the model")
parser.add_argument(
    "--language", "-l", type=str,
    choices=LANGUAGE_TO_EXPORTER.keys(),
    help="Target language",
    required=True)
parser.add_argument(
    "--class_name", "-cn", dest="class_name", type=str,
    help="Name of the generated class (if supported by target language)")
parser.add_argument(
    "--package_name", "-pn", dest="package_name", type=str,
    help="Package name for the generated code "
         "(if supported by target language)")
parser.add_argument(
    "--indent", "-i", dest="indent", type=int,
    default=4,
    help="Indentation for the generated code")
parser.add_argument(
    "--recursion-limit", "-rl", type=int,
    help="Sets the maximum depth of the Python interpreter stack. "
         "No limit by default",
    default=MAX_RECURSION_DEPTH)


def parse_args(args):
    return parser.parse_args(args)


def generate_code(args):
    sys.setrecursionlimit(args.recursion_limit)

    with args.infile as f:
        model = pickle.load(f)

    exporter, supported_args = LANGUAGE_TO_EXPORTER[args.language]

    kwargs = {}
    for arg_name in supported_args:
        arg_value = getattr(args, arg_name)
        if arg_value is not None:
            kwargs[arg_name] = arg_value

    return exporter(model, **kwargs)


def main():
    args = parse_args(sys.argv[1:])
    print(generate_code(args))
