from sklearn import linear_model, ensemble
from sklearn.ensemble import forest
from sklearn.linear_model.base import LinearModel
from sklearn.tree import tree

from m2cgen import assemblers
from m2cgen import interpreters


SUPPORTED_MODELS = {
    "LinearRegression": assemblers.LinearModelAssembler,
    "LogisticRegression": assemblers.LinearModelAssembler,
    "DecisionTreeRegressor": assemblers.TreeModelAssembler,
    "DecisionTreeClassifier": assemblers.TreeModelAssembler,
    "RandomForestRegressor": assemblers.RandomForestModelAssembler,
    "RandomForestClassifier": assemblers.RandomForestModelAssembler,
}

UNSUPPORTED_MODELS = [ensemble.RandomTreesEmbedding]


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
    if isinstance(model, LinearModel):
        return assemblers.LinearModelAssembler

    if isinstance(model, linear_model.LogisticRegression):
        return assemblers.LinearModelAssembler

    if isinstance(model, tree.BaseDecisionTree):
        return assemblers.TreeModelAssembler

    if isinstance(model, forest.ForestRegressor):
        return assemblers.RandomForestModelAssembler

    if isinstance(model, forest.ForestClassifier):
        return assemblers.RandomForestModelAssembler

    raise NotImplementedError(
        "Model {} is not supported".format(model.__name__))
