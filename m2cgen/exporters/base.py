from m2cgen.ast import assemblers


class BaseExporter:

    models_to_assemblers = {
        "LinearRegression": assemblers.LinearRegressionAssembler,
        "DecisionTreeRegressor": assemblers.TreeModelAssembler,
    }

    def __init__(self, model):
        self.model = model
        self.assembler = self._get_assembler_cls(type(model).__name__)(model)

    def _get_assembler_cls(self, model_name):
        assembler_cls = self.models_to_assemblers.get(model_name)

        if not assembler_cls:
            raise NotImplementedError(
                "Model {} is not supported".format(model_name))

        return assembler_cls

    def export(self):
        model_ast = self.assembler.assemble()
        return self.export_from_ast(model_ast)

    def export_from_ast(self, model_ast):
        raise NotImplementedError
