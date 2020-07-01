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
import inspect
import numpy as np

import m2cgen


LANGUAGE_TO_EXPORTER = {
    "python": (m2cgen.export_to_python, ["indent", "function_name"]),
    "java": (m2cgen.export_to_java, ["indent", "class_name", "package_name",
                                     "function_name"]),
    "c": (m2cgen.export_to_c, ["indent", "function_name"]),
    "go": (m2cgen.export_to_go, ["indent", "function_name"]),
    "javascript": (m2cgen.export_to_javascript, ["indent", "function_name"]),
    "visual_basic": (m2cgen.export_to_visual_basic,
                     ["module_name", "indent", "function_name"]),
    "c_sharp": (m2cgen.export_to_c_sharp,
                ["indent", "class_name", "namespace", "function_name"]),
    "powershell": (m2cgen.export_to_powershell, ["indent", "function_name"]),
    "r": (m2cgen.export_to_r, ["indent", "function_name"]),
    "php": (m2cgen.export_to_php, ["indent", "function_name"]),
    "dart": (m2cgen.export_to_dart, ["indent", "function_name"]),
    "haskell": (m2cgen.export_to_haskell,
                ["module_name", "indent", "function_name"]),
    "ruby": (m2cgen.export_to_ruby, ["indent", "function_name"]),
    "f_sharp": (m2cgen.export_to_f_sharp, ["indent", "function_name"]),
}


# The maximum recursion depth is represented by the maximum int32 value.
MAX_RECURSION_DEPTH = np.iinfo(np.intc).max


parser = argparse.ArgumentParser(
    prog="m2cgen",
    description="Generate code in native language for provided model.")
parser.add_argument(
    "infile", type=argparse.FileType("rb"), nargs="?",
    default=sys.stdin.buffer,
    help="File with pickle representation of the model.")
parser.add_argument(
    "--language", "-l", type=str,
    choices=LANGUAGE_TO_EXPORTER.keys(),
    help="Target language.",
    required=True)
parser.add_argument(
    "--function_name", "-fn", dest="function_name", type=str,
    # The default value is conditional and will be set in the argument's
    # post-processing, based on the signature of the `export` function
    # that belongs to the specified target language.
    default=None,
    help="Name of the function in the generated code.")
parser.add_argument(
    "--class_name", "-cn", dest="class_name", type=str,
    help="Name of the generated class (if supported by target language).")
parser.add_argument(
    "--package_name", "-pn", dest="package_name", type=str,
    help="Package name for the generated code "
         "(if supported by target language).")
parser.add_argument(
    "--module_name", "-mn", dest="module_name", type=str,
    help="Module name for the generated code "
         "(if supported by target language).")
parser.add_argument(
    "--namespace", "-ns", dest="namespace", type=str,
    help="Namespace for the generated code "
         "(if supported by target language).")
parser.add_argument(
    "--indent", "-i", dest="indent", type=int,
    default=4,
    help="Indentation for the generated code.")
parser.add_argument(
    "--recursion-limit", "-rl", type=int,
    help="Sets the maximum depth of the Python interpreter stack. "
         "No limit by default",
    default=MAX_RECURSION_DEPTH)
parser.add_argument(
    "--version", "-v", action="version",
    version=f"%(prog)s {m2cgen.__version__}")


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

        # Special handling for the function_name parameter, which needs to be
        # the same as the default value of the keyword argument of the exporter
        # (this is due to languages like C# which prefer their method names to
        # follow PascalCase unlike all the other supported languages -- see
        # https://github.com/BayesWitnesses/m2cgen/pull/166#discussion_r379867601
        # for more).
        if arg_name == 'function_name' and arg_value is None:
            param = inspect.signature(exporter).parameters['function_name']
            kwargs[arg_name] = param.default

    return exporter(model, **kwargs)


def main():
    args = parse_args(sys.argv[1:])
    print(generate_code(args))
