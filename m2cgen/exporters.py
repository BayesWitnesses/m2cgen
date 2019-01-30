from m2cgen import assemblers
from m2cgen import interpreters


class BaseExporter:

    interpreter = None

    models_to_assemblers = {
        "LinearRegression": assemblers.LinearModelAssembler,
        "LogisticRegression": assemblers.LinearModelAssembler,
        "DecisionTreeRegressor": assemblers.TreeModelAssembler,
        "DecisionTreeClassifier": assemblers.TreeModelAssembler,
        "RandomForestRegressor": assemblers.RandomForestModelAssembler,
    }

    def __init__(self, model):
        self.model = model
        self.assembler = self._get_assembler_cls(type(model).__name__)(model)
        assert self.interpreter, "interpreter is required"

    def _get_assembler_cls(self, model_name):
        assembler_cls = self.models_to_assemblers.get(model_name)

        if not assembler_cls:
            raise NotImplementedError(
                "Model {} is not supported".format(model_name))

        return assembler_cls

    def export(self):
        model_ast = self.assembler.assemble()
        return self.interpreter.interpret(model_ast)


class JavaExporter(BaseExporter):

    def __init__(self, model, package_name=None, model_name="Model", indent=4):
        self.interpreter = interpreters.JavaInterpreter(
            package_name=package_name,
            model_name=model_name,
            indent=indent)
        super(JavaExporter, self).__init__(model)


class PythonExporter(BaseExporter):

    def __init__(self, model, indent=4):
        self.interpreter = interpreters.PythonInterpreter(indent=indent)
        super(PythonExporter, self).__init__(model)


class CExporter(BaseExporter):

    def __init__(self, model, indent=4):
        self.interpreter = interpreters.CInterpreter(indent=indent)
        super(CExporter, self).__init__(model)
