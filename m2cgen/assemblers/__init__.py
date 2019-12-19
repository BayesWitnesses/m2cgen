import json

from .linear import LinearModelAssembler
from .tree import TreeModelAssembler
from .ensemble import RandomForestModelAssembler
from .boosting import (XGBoostModelAssembler, XGBoostLinearModelAssembler,
                       LightGBMModelAssembler)
from .svm import SVMModelAssembler

__all__ = [
    LinearModelAssembler,
    TreeModelAssembler,
    RandomForestModelAssembler,
    XGBoostModelAssembler,
    LightGBMModelAssembler,
    SVMModelAssembler,
]


SUPPORTED_MODELS = {
    # LightGBM
    "LGBMRegressor": LightGBMModelAssembler,
    "LGBMClassifier": LightGBMModelAssembler,

    # XGBoost
    "XGBClassifier": XGBoostModelAssembler,
    "XGBRegressor": XGBoostModelAssembler,

    # SVM
    "LinearSVC": LinearModelAssembler,
    "LinearSVR": LinearModelAssembler,
    "SVR": SVMModelAssembler,
    "NuSVR": SVMModelAssembler,
    "SVC": SVMModelAssembler,
    "NuSVC": SVMModelAssembler,

    # Linear Regressors
    "LinearRegression": LinearModelAssembler,
    "HuberRegressor": LinearModelAssembler,
    "ElasticNet": LinearModelAssembler,
    "ElasticNetCV": LinearModelAssembler,
    "TheilSenRegressor": LinearModelAssembler,
    "Lars": LinearModelAssembler,
    "LarsCV": LinearModelAssembler,
    "Lasso": LinearModelAssembler,
    "LassoCV": LinearModelAssembler,
    "LassoLars": LinearModelAssembler,
    "LassoLarsCV": LinearModelAssembler,
    "LassoLarsIC": LinearModelAssembler,
    "OrthogonalMatchingPursuit": LinearModelAssembler,
    "OrthogonalMatchingPursuitCV": LinearModelAssembler,
    "Ridge": LinearModelAssembler,
    "RidgeCV": LinearModelAssembler,
    "BayesianRidge": LinearModelAssembler,
    "ARDRegression": LinearModelAssembler,
    "SGDRegressor": LinearModelAssembler,
    "PassiveAggressiveRegressor": LinearModelAssembler,

    # Logistic Regressors
    "LogisticRegression": LinearModelAssembler,
    "LogisticRegressionCV": LinearModelAssembler,
    "RidgeClassifier": LinearModelAssembler,
    "RidgeClassifierCV": LinearModelAssembler,
    "SGDClassifier": LinearModelAssembler,
    "PassiveAggressiveClassifier": LinearModelAssembler,

    # Decision trees
    "DecisionTreeRegressor": TreeModelAssembler,
    "DecisionTreeClassifier": TreeModelAssembler,
    "ExtraTreeRegressor": TreeModelAssembler,
    "ExtraTreeClassifier": TreeModelAssembler,

    # Ensembles
    "RandomForestRegressor": RandomForestModelAssembler,
    "RandomForestClassifier": RandomForestModelAssembler,
    "ExtraTreesRegressor": RandomForestModelAssembler,
    "ExtraTreesClassifier": RandomForestModelAssembler,
}


def get_assembler_cls(model):
    model_name = type(model).__name__
    assembler_cls = SUPPORTED_MODELS.get(model_name)

    if not assembler_cls:
        raise NotImplementedError(
            "Model {} is not supported".format(model_name))

    if assembler_cls is XGBoostModelAssembler:
        model_dump = model.get_booster().get_dump(dump_format="json")
        if len(model_dump) == 1 and all(i in json.loads(model_dump[0])
                                        for i in ("weight", "bias")):
            assembler_cls = XGBoostLinearModelAssembler

    return assembler_cls
