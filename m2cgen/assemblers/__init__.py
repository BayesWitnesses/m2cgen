from .linear import (SklearnLinearModelAssembler,
                     StatsmodelsLinearModelAssembler)
from .tree import TreeModelAssembler
from .ensemble import RandomForestModelAssembler
from .boosting import XGBoostModelAssembler, LightGBMModelAssembler
from .svm import SVMModelAssembler

__all__ = [
    SklearnLinearModelAssembler,
    StatsmodelsLinearModelAssembler,
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
    "LinearSVC": SklearnLinearModelAssembler,
    "LinearSVR": SklearnLinearModelAssembler,
    "SVR": SVMModelAssembler,
    "NuSVR": SVMModelAssembler,
    "SVC": SVMModelAssembler,
    "NuSVC": SVMModelAssembler,

    # Sklearn Linear Regressors
    "LinearRegression": SklearnLinearModelAssembler,
    "HuberRegressor": SklearnLinearModelAssembler,
    "ElasticNet": SklearnLinearModelAssembler,
    "ElasticNetCV": SklearnLinearModelAssembler,
    "TheilSenRegressor": SklearnLinearModelAssembler,
    "Lars": SklearnLinearModelAssembler,
    "LarsCV": SklearnLinearModelAssembler,
    "Lasso": SklearnLinearModelAssembler,
    "LassoCV": SklearnLinearModelAssembler,
    "LassoLars": SklearnLinearModelAssembler,
    "LassoLarsCV": SklearnLinearModelAssembler,
    "LassoLarsIC": SklearnLinearModelAssembler,
    "OrthogonalMatchingPursuit": SklearnLinearModelAssembler,
    "OrthogonalMatchingPursuitCV": SklearnLinearModelAssembler,
    "Ridge": SklearnLinearModelAssembler,
    "RidgeCV": SklearnLinearModelAssembler,
    "BayesianRidge": SklearnLinearModelAssembler,
    "ARDRegression": SklearnLinearModelAssembler,
    "SGDRegressor": SklearnLinearModelAssembler,
    "PassiveAggressiveRegressor": SklearnLinearModelAssembler,

    # Statsmodels Linear Regressors
    "RegressionResultsWrapper": StatsmodelsLinearModelAssembler,
    "RegularizedResultsWrapper": StatsmodelsLinearModelAssembler,

    # Logistic Regressors
    "LogisticRegression": SklearnLinearModelAssembler,
    "LogisticRegressionCV": SklearnLinearModelAssembler,
    "RidgeClassifier": SklearnLinearModelAssembler,
    "RidgeClassifierCV": SklearnLinearModelAssembler,
    "SGDClassifier": SklearnLinearModelAssembler,
    "PassiveAggressiveClassifier": SklearnLinearModelAssembler,

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

    return assembler_cls
