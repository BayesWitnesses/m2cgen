from .linear import LinearModelAssembler
from .tree import TreeModelAssembler
from .ensemble import RandomForestModelAssembler

__all__ = [
    LinearModelAssembler,
    TreeModelAssembler,
    RandomForestModelAssembler
]


SUPPORTED_MODELS = {
    "LinearRegression": LinearModelAssembler,
    "LogisticRegression": LinearModelAssembler,
    "DecisionTreeRegressor": TreeModelAssembler,
    "DecisionTreeClassifier": TreeModelAssembler,
    "RandomForestRegressor": RandomForestModelAssembler,
    "RandomForestClassifier": RandomForestModelAssembler,
}


def get_assembler_cls(model):
    model_name = type(model).__name__
    assembler_cls = SUPPORTED_MODELS.get(model_name)

    if not assembler_cls:
        raise NotImplementedError(
            "Model {} is not supported".format(model_name))

    return assembler_cls
