from m2cgen import assemblers
from m2cgen import interpreters


def export_to_java(model, package_name=None, class_name="Model", indent=4):
    """
    Generates a Java code representation of the given model.

    Parameters
    ----------
    model : object
        The model object that should be transpiled into code.
    package_name : string, optional
        Java package name. By default no package name is used.
    class_name : string, optional
        The name of the generated class.
    indent : int, optional
        The size of indents in the generated code.

    Returns
    -------
    code : string
    """
    interpreter = interpreters.JavaInterpreter(
        package_name=package_name,
        class_name=class_name,
        indent=indent)
    return _export(model, interpreter)


def export_to_python(model, indent=4):
    """
    Generates a Python code representation of the given model.

    Parameters
    ----------
    model : object
        The model object that should be transpiled into code.
    indent : int, optional
        The size of indents in the generated code.

    Returns
    -------
    code : string
    """
    interpreter = interpreters.PythonInterpreter(indent=indent)
    return _export(model, interpreter)


def export_to_c(model, indent=4):
    """
    Generates a C code representation of the given model.

    Parameters
    ----------
    model : object
        The model object that should be transpiled into code.
    indent : int, optional
        The size of indents in the generated code.

    Returns
    -------
    code : string
    """
    interpreter = interpreters.CInterpreter(indent=indent)
    return _export(model, interpreter)


def export_to_go(model, indent=4):
    """
    Generates a Go code representation of the given model.

    Parameters
    ----------
    model : object
        The model object that should be transpiled into code.
    indent : int, optional
        The size of indents in the generated code.

    Returns
    -------
    code : string
    """
    interpreter = interpreters.GoInterpreter(indent=indent)
    return _export(model, interpreter)


def _export(model, interpreter):
    assembler_cls = assemblers.get_assembler_cls(model)
    model_ast = assembler_cls(model).assemble()
    return interpreter.interpret(model_ast)
