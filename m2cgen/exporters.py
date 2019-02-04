from m2cgen import assemblers
from m2cgen import interpreters


def export_to_java(model, package_name=None, class_name="Model", indent=4):
    interpreter = interpreters.JavaInterpreter(
        package_name=package_name,
        class_name=class_name,
        indent=indent)
    return _export(model, interpreter)


def export_to_python(model, indent=4):
    interpreter = interpreters.PythonInterpreter(indent=indent)
    return _export(model, interpreter)


def export_to_c(model, indent=4):
    interpreter = interpreters.CInterpreter(indent=indent)
    return _export(model, interpreter)


def _export(model, interpreter):
    assembler_cls = assemblers.get_assembler_cls(model)
    model_ast = assembler_cls(model).assemble()
    return interpreter.interpret(model_ast)
