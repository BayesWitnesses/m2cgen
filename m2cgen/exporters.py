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


def export_to_javascript(model, indent=4):
    """
    Generates a JavaScript code representation of the given model.

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
    interpreter = interpreters.JavascriptInterpreter(indent=indent)
    return _export(model, interpreter)


def export_to_visual_basic(model, module_name="Model", indent=4):
    """
    Generates a Visual Basic (also can be treated as VBA
    with some small manual changes, see a note below)
    code representation of the given model.

    .. note::

        The generated code representation can be easily used as VBA code.
        You simply need to remove the first (`Module Model`) and
        the last (`End Module`) lines, and manually adjust the code
        to meet the following limitations:
        - nested floating-point expressions have level limits,
          e.g. 8 in 32-bit environment
          (**expression too complex**:
          https://docs.microsoft.com/ru-ru/office/vba/language/reference/user-interface-help/expression-too-complex-error-16);
        - **fixed or static data can't be larger than 64K**:
          https://docs.microsoft.com/ru-ru/office/vba/language/reference/user-interface-help/fixed-or-static-data-can-t-be-larger-than-64k;
        - code line length cannot contain more than 1023 characters
          (**line too long**:
          https://docs.microsoft.com/ru-ru/office/vba/language/reference/user-interface-help/line-too-long);
        - segment boundaries are 64K
          (**out of memory**:
          https://docs.microsoft.com/ru-ru/office/vba/language/reference/user-interface-help/out-of-memory-error-7);
        - nested function calls have depth limit
          (**out of stack space**:
          https://docs.microsoft.com/ru-ru/office/vba/language/reference/user-interface-help/out-of-stack-space-error-28);
        - compiled procedure cannot exceed 64K size limit
          (**procedure too large**:
          https://docs.microsoft.com/ru-ru/office/vba/language/reference/user-interface-help/procedure-too-large);
        - project's name table is limited by 32768 names
          (**project contains too many procedure, variable,
          and constant names**:
          https://docs.microsoft.com/ru-ru/office/vba/language/reference/user-interface-help/project-contains-too-many-procedure-variable-and-constant-names);
        - statements cannot be extremely complex
          (**statement too complex**:
          https://docs.microsoft.com/ru-ru/office/vba/language/reference/user-interface-help/statement-too-complex);
        - there can't be more than 24 consecutive line-continuation characters
          (**too many line continuations**:
          https://docs.microsoft.com/ru-ru/office/vba/language/reference/user-interface-help/too-many-line-continuations);
        - procedure's local, nonstatic variables and
          compiler-generated temporary variables cannot exceed 32K size limit
          (**too many local, nonstatic variables**:
          https://docs.microsoft.com/ru-ru/office/vba/language/reference/user-interface-help/too-many-local-nonstatic-variables);
        - and some others...

    Parameters
    ----------
    model : object
        The model object that should be transpiled into code.
    module_name : string, optional
        The name of the generated module.
    indent : int, optional
        The size of indents in the generated code.

    Returns
    -------
    code : string
    """
    interpreter = interpreters.VisualBasicInterpreter(module_name=module_name,
                                                      indent=indent)
    return _export(model, interpreter)


def export_to_c_sharp(model, namespace="ML", class_name="Model", indent=4):
    """
    Generates a C# code representation of the given model.

    Parameters
    ----------
    model : object
        The model object that should be transpiled into code.
    namespace : string, optional
        The namespace for the generated code.
    class_name : string, optional
        The name of the generated class.
    indent : int, optional
        The size of indents in the generated code.

    Returns
    -------
    code : string
    """
    interpreter = interpreters.CSharpInterpreter(
        namespace=namespace,
        class_name=class_name,
        indent=indent)
    return _export(model, interpreter)


def _export(model, interpreter):
    assembler_cls = assemblers.get_assembler_cls(model)
    model_ast = assembler_cls(model).assemble()
    return interpreter.interpret(model_ast)
