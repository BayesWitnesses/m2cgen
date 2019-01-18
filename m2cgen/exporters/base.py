import numpy as np

from sklearn.metrics import mean_squared_error

from m2cgen.ast import assemblers


class BaseExporter:

    code_generator = None
    executor_cls = None

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

    def export(self, for_validation=False):
        self.code_generator.reset_state()

        model_ast = self.assembler.assemble()

        self.export_from_ast(model_ast, for_validation=for_validation)

        return self.code_generator.code

    def export_from_ast(self, model_ast, for_validation=False):
        raise NotImplementedError

    def validate(self, X):
        y_true = self.model.predict(X)
        y_predicted = self.predict(X)

        return mean_squared_error(y_true, y_predicted)

    def predict(self, X):
        assert self.executor_cls, "executor_cls is missing"

        executor = self.executor_cls(self)

        return np.array(executor.predict(X))
