import os

from m2cgen import assemblers
from m2cgen import interpreters


def export_to_java(model, output_file=None, package_name=None,
                   class_name="Model", indent=4):
    """
    Generates a Java code representation of the given model.

    Parameters
    ----------
    model : object
        The model object that should be transpiled into code.
    output_file : string, optional
        Path to a file in which the generated code should be written.
    package_name : string, optional
        Java package name. By default no package name is used.
    class_name : string, optional
        The name of the generated class.
    indent : int, optional
        The size of indents in the generated code.

    Returns
    -------
    code : string or None
    """
    interpreter = interpreters.JavaInterpreter(
        package_name=package_name,
        class_name=class_name,
        indent=indent)
    return _export(model, interpreter, output_file)


def export_to_python(model, output_file=None, indent=4):
    """
    Generates a Python code representation of the given model.

    Parameters
    ----------
    model : object
        The model object that should be transpiled into code.
    output_file : string, optional
        Path to a file in which the generated code should be written.
    indent : int, optional
        The size of indents in the generated code.

    Returns
    -------
    code : string or None
    """
    interpreter = interpreters.PythonInterpreter(indent=indent)
    return _export(model, interpreter, output_file)


def export_to_c(model, output_file=None, indent=4):
    """
    Generates a C code representation of the given model.

    Parameters
    ----------
    model : object
        The model object that should be transpiled into code.
    output_file : string, optional
        Path to a file in which the generated code should be written.
    indent : int, optional
        The size of indents in the generated code.

    Returns
    -------
    code : string or None
    """
    interpreter = interpreters.CInterpreter(indent=indent)
    return _export(model, interpreter, output_file)


def export_to_go(model, output_file=None, indent=4):
    """
    Generates a Go code representation of the given model.

    Parameters
    ----------
    model : object
        The model object that should be transpiled into code.
    output_file : string, optional
        Path to a file in which the generated code should be written.
    indent : int, optional
        The size of indents in the generated code.

    Returns
    -------
    code : string or None
    """
    interpreter = interpreters.GoInterpreter(indent=indent)
    return _export(model, interpreter, output_file)


def export_to_javascript(model, output_file=None, indent=4):
    """
    Generates a Javascript code representation of the given model.

    Parameters
    ----------
    model : object
        The model object that should be transpiled into code.
    output_file : string, optional
        Path to a file in which the generated code should be written.
    indent : int, optional
        The size of indents in the generated code.

    Returns
    -------
    code : string or None
    """
    interpreter = interpreters.JavascriptInterpreter(indent=indent)
    return _export(model, interpreter, output_file)


def _export(model, interpreter, output_file=None):
    assembler_cls = assemblers.get_assembler_cls(model)
    model_ast = assembler_cls(model).assemble()
    code = interpreter.interpret(model_ast)
    if output_file is None:
        return code
    else:
        directory = os.path.dirname(output_file)
        if directory and not os.path.exists(directory):
            os.makedirs(directory)
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(code)
