from .linear import (SklearnLinearModelAssembler,
                     StatsmodelsLinearModelAssembler)
from .tree import TreeModelAssembler
from .ensemble import RandomForestModelAssembler
from .boosting import (XGBoostModelAssemblerSelector,
                       XGBoostTreeModelAssembler,
                       XGBoostLinearModelAssembler,
                       LightGBMModelAssembler)
from .svm import SVMModelAssembler

__all__ = [
    SklearnLinearModelAssembler,
    StatsmodelsLinearModelAssembler,
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
    "LinearSVC": SklearnLinearModelAssembler,
    "LinearSVR": SklearnLinearModelAssembler,
    "NuSVC": SVMModelAssembler,
    "NuSVR": SVMModelAssembler,
    "SVC": SVMModelAssembler,
    "SVR": SVMModelAssembler,

    # Sklearn Linear Regressors
    "ARDRegression": SklearnLinearModelAssembler,
    "BayesianRidge": SklearnLinearModelAssembler,
    "ElasticNet": SklearnLinearModelAssembler,
    "ElasticNetCV": SklearnLinearModelAssembler,
    "HuberRegressor": SklearnLinearModelAssembler,
    "Lars": SklearnLinearModelAssembler,
    "LarsCV": SklearnLinearModelAssembler,
    "Lasso": SklearnLinearModelAssembler,
    "LassoCV": SklearnLinearModelAssembler,
    "LassoLars": SklearnLinearModelAssembler,
    "LassoLarsCV": SklearnLinearModelAssembler,
    "LassoLarsIC": SklearnLinearModelAssembler,
    "LinearRegression": SklearnLinearModelAssembler,
    "OrthogonalMatchingPursuit": SklearnLinearModelAssembler,
    "OrthogonalMatchingPursuitCV": SklearnLinearModelAssembler,
    "PassiveAggressiveRegressor": SklearnLinearModelAssembler,
    "Ridge": SklearnLinearModelAssembler,
    "RidgeCV": SklearnLinearModelAssembler,
    "SGDRegressor": SklearnLinearModelAssembler,
    "TheilSenRegressor": SklearnLinearModelAssembler,

    # Statsmodels Linear Regressors
    "RegressionResultsWrapper": StatsmodelsLinearModelAssembler,
    "RegularizedResultsWrapper": StatsmodelsLinearModelAssembler,

    # Linear Classifiers
    "LogisticRegression": SklearnLinearModelAssembler,
    "LogisticRegressionCV": SklearnLinearModelAssembler,
    "PassiveAggressiveClassifier": SklearnLinearModelAssembler,
    "Perceptron": SklearnLinearModelAssembler,
    "RidgeClassifier": SklearnLinearModelAssembler,
    "RidgeClassifierCV": SklearnLinearModelAssembler,
    "SGDClassifier": SklearnLinearModelAssembler,

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
