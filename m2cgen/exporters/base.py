from m2cgen.ast import assemblers


class BaseExporter:

    code_generator = None

    models_to_assemblers = {
        "LinearRegression": assemblers.LinearRegressionAssembler,
        "DecisionTreeRegressor": assemblers.TreeModelAssembler,
    }

    def __init__(self, model):
        self.model = model
        self.assembler = self._get_assembler_cls(type(model).__name__)(model)
        assert self.code_generator, "code_generator is required"

    def _get_assembler_cls(self, model_name):
        assembler_cls = self.models_to_assemblers.get(model_name)

        if not assembler_cls:
            raise NotImplementedError(
                "Model {} is not supported".format(model_name))

        return assembler_cls

    def export(self):
        self.code_generator.reset_state()

        model_ast = self.assembler.assemble()

        self.export_from_ast(model_ast)

        return self.code_generator.code

    def export_from_ast(self, model_ast):
        raise NotImplementedError
