from .linear import LinearModelAssembler
from .tree import TreeModelAssembler
from .ensemble import RandomForestModelAssembler
from .boosting import (XGBoostModelAssemblerSelector,
                       XGBoostTreeModelAssembler,
                       XGBoostLinearModelAssembler,
                       LightGBMModelAssembler)
from .svm import SVMModelAssembler

__all__ = [
    LinearModelAssembler,
    TreeModelAssembler,
    RandomForestModelAssembler,
    XGBoostModelAssemblerSelector,
    XGBoostTreeModelAssembler,
    XGBoostLinearModelAssembler,
    LightGBMModelAssembler,
    SVMModelAssembler,
]


SUPPORTED_MODELS = {
    # LightGBM
    "LGBMClassifier": LightGBMModelAssembler,
    "LGBMRegressor": LightGBMModelAssembler,

    # XGBoost
    "XGBClassifier": XGBoostModelAssemblerSelector,
    "XGBRFClassifier": XGBoostModelAssemblerSelector,
    "XGBRegressor": XGBoostModelAssemblerSelector,
    "XGBRFRegressor": XGBoostModelAssemblerSelector,

    # SVM
    "LinearSVC": LinearModelAssembler,
    "LinearSVR": LinearModelAssembler,
    "NuSVC": SVMModelAssembler,
    "NuSVR": SVMModelAssembler,
    "SVC": SVMModelAssembler,
    "SVR": SVMModelAssembler,

    # Linear Regressors
    "ARDRegression": LinearModelAssembler,
    "BayesianRidge": LinearModelAssembler,
    "ElasticNet": LinearModelAssembler,
    "ElasticNetCV": LinearModelAssembler,
    "HuberRegressor": LinearModelAssembler,
    "Lars": LinearModelAssembler,
    "LarsCV": LinearModelAssembler,
    "Lasso": LinearModelAssembler,
    "LassoCV": LinearModelAssembler,
    "LassoLars": LinearModelAssembler,
    "LassoLarsCV": LinearModelAssembler,
    "LassoLarsIC": LinearModelAssembler,
    "LinearRegression": LinearModelAssembler,
    "OrthogonalMatchingPursuit": LinearModelAssembler,
    "OrthogonalMatchingPursuitCV": LinearModelAssembler,
    "PassiveAggressiveRegressor": LinearModelAssembler,
    "Ridge": LinearModelAssembler,
    "RidgeCV": LinearModelAssembler,
    "SGDRegressor": LinearModelAssembler,
    "TheilSenRegressor": LinearModelAssembler,

    # Linear Classifiers
    "LogisticRegression": LinearModelAssembler,
    "LogisticRegressionCV": LinearModelAssembler,
    "PassiveAggressiveClassifier": LinearModelAssembler,
    "Perceptron": LinearModelAssembler,
    "RidgeClassifier": LinearModelAssembler,
    "RidgeClassifierCV": LinearModelAssembler,
    "SGDClassifier": LinearModelAssembler,

    # Decision trees
    "DecisionTreeClassifier": TreeModelAssembler,
    "DecisionTreeRegressor": TreeModelAssembler,
    "ExtraTreeClassifier": TreeModelAssembler,
    "ExtraTreeRegressor": TreeModelAssembler,

    # Ensembles
    "ExtraTreesClassifier": RandomForestModelAssembler,
    "ExtraTreesRegressor": RandomForestModelAssembler,
    "RandomForestClassifier": RandomForestModelAssembler,
    "RandomForestRegressor": RandomForestModelAssembler,
}


def get_assembler_cls(model):
    model_name = type(model).__name__
    assembler_cls = SUPPORTED_MODELS.get(model_name)

    if not assembler_cls:
        raise NotImplementedError(
            "Model {} is not supported".format(model_name))

    return assembler_cls
