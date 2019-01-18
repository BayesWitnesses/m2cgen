from m2cgen.ast import assemblers


class BaseExporter:

    interpreter = None

    models_to_assemblers = {
        "LinearRegression": assemblers.LinearRegressionAssembler,
        "DecisionTreeRegressor": assemblers.TreeModelAssembler,
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
