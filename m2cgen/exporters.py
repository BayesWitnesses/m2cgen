from m2cgen import assemblers
from m2cgen import interpreters


SUPPORTED_MODELS = {
    # Linear Regressors
    "LinearRegression": assemblers.LinearModelAssembler,
    "HuberRegressor": assemblers.LinearModelAssembler,
    "ElasticNet": assemblers.LinearModelAssembler,
    "ElasticNetCV": assemblers.LinearModelAssembler,
    "TheilSenRegressor": assemblers.LinearModelAssembler,
    "Lars": assemblers.LinearModelAssembler,
    "LarsCV": assemblers.LinearModelAssembler,
    "Lasso": assemblers.LinearModelAssembler,
    "LassoCV": assemblers.LinearModelAssembler,
    "LassoLars": assemblers.LinearModelAssembler,
    "LassoLarsIC": assemblers.LinearModelAssembler,

    # Logistic Regressors
    "LogisticRegression": assemblers.LinearModelAssembler,
    "LogisticRegressionCV": assemblers.LinearModelAssembler,

    # Decision trees
    "DecisionTreeRegressor": assemblers.TreeModelAssembler,
    "DecisionTreeClassifier": assemblers.TreeModelAssembler,
    "ExtraTreeRegressor": assemblers.TreeModelAssembler,
    "ExtraTreeClassifier": assemblers.TreeModelAssembler,

    # Ensembles
    "RandomForestRegressor": assemblers.RandomForestModelAssembler,
    "RandomForestClassifier": assemblers.RandomForestModelAssembler,
    "ExtraTreesRegressor": assemblers.RandomForestModelAssembler,
    "ExtraTreesClassifier": assemblers.RandomForestModelAssembler,
}


def export_to_java(model, package_name=None, model_name="Model", indent=4):
    interpreter = interpreters.JavaInterpreter(
        package_name=package_name,
        model_name=model_name,
        indent=indent)
    return _export(model, interpreter)


def export_to_python(model, indent=4):
    interpreter = interpreters.PythonInterpreter(indent=indent)
    return _export(model, interpreter)


def export_to_c(model, indent=4):
    interpreter = interpreters.CInterpreter(indent=indent)
    return _export(model, interpreter)


def _export(model, interpreter):
    assembler_cls = _get_assembler_cls(model)
    model_ast = assembler_cls(model).assemble()
    return interpreter.interpret(model_ast)


def _get_assembler_cls(model):
    model_name = type(model).__name__
    assembler_cls = SUPPORTED_MODELS.get(model_name)

    if not assembler_cls:
        raise NotImplementedError(
            "Model {} is not supported".format(model_name))

    return assembler_cls
