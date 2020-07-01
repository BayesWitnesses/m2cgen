from .linear import (SklearnLinearModelAssembler,
                     StatsmodelsLinearModelAssembler,
                     ProcessMLEModelAssembler,
                     StatsmodelsGLMModelAssembler,
                     StatsmodelsModelAssemblerSelector,
                     SklearnGLMModelAssembler)
from .tree import TreeModelAssembler
from .ensemble import RandomForestModelAssembler
from .boosting import (XGBoostModelAssemblerSelector,
                       XGBoostTreeModelAssembler,
                       XGBoostLinearModelAssembler,
                       LightGBMModelAssembler)
from .svm import SklearnSVMModelAssembler, LightningSVMModelAssembler
from .meta import RANSACModelAssembler

__all__ = [
    SklearnLinearModelAssembler,
    StatsmodelsLinearModelAssembler,
    ProcessMLEModelAssembler,
    RANSACModelAssembler,
    TreeModelAssembler,
    RandomForestModelAssembler,
    XGBoostModelAssemblerSelector,
    XGBoostTreeModelAssembler,
    XGBoostLinearModelAssembler,
    LightGBMModelAssembler,
    SklearnSVMModelAssembler,
    LightningSVMModelAssembler,
    StatsmodelsGLMModelAssembler,
    StatsmodelsModelAssemblerSelector,
    SklearnGLMModelAssembler,
]


SUPPORTED_MODELS = {
    # LightGBM
    "lightgbm_LGBMClassifier": LightGBMModelAssembler,
    "lightgbm_LGBMRegressor": LightGBMModelAssembler,

    # XGBoost
    "xgboost_XGBClassifier": XGBoostModelAssemblerSelector,
    "xgboost_XGBRFClassifier": XGBoostModelAssemblerSelector,
    "xgboost_XGBRegressor": XGBoostModelAssemblerSelector,
    "xgboost_XGBRFRegressor": XGBoostModelAssemblerSelector,

    # Sklearn SVM
    "sklearn_LinearSVC": SklearnLinearModelAssembler,
    "sklearn_LinearSVR": SklearnLinearModelAssembler,
    "sklearn_NuSVC": SklearnSVMModelAssembler,
    "sklearn_NuSVR": SklearnSVMModelAssembler,
    "sklearn_SVC": SklearnSVMModelAssembler,
    "sklearn_SVR": SklearnSVMModelAssembler,

    # Lightning SVM
    "lightning_KernelSVC": LightningSVMModelAssembler,
    "lightning_LinearSVC": SklearnLinearModelAssembler,
    "lightning_LinearSVR": SklearnLinearModelAssembler,

    # Sklearn Linear Regressors
    "sklearn_ARDRegression": SklearnLinearModelAssembler,
    "sklearn_BayesianRidge": SklearnLinearModelAssembler,
    "sklearn_ElasticNet": SklearnLinearModelAssembler,
    "sklearn_ElasticNetCV": SklearnLinearModelAssembler,
    "sklearn_GammaRegressor": SklearnGLMModelAssembler,
    "sklearn_HuberRegressor": SklearnLinearModelAssembler,
    "sklearn_Lars": SklearnLinearModelAssembler,
    "sklearn_LarsCV": SklearnLinearModelAssembler,
    "sklearn_Lasso": SklearnLinearModelAssembler,
    "sklearn_LassoCV": SklearnLinearModelAssembler,
    "sklearn_LassoLars": SklearnLinearModelAssembler,
    "sklearn_LassoLarsCV": SklearnLinearModelAssembler,
    "sklearn_LassoLarsIC": SklearnLinearModelAssembler,
    "sklearn_LinearRegression": SklearnLinearModelAssembler,
    "sklearn_OrthogonalMatchingPursuit": SklearnLinearModelAssembler,
    "sklearn_OrthogonalMatchingPursuitCV": SklearnLinearModelAssembler,
    "sklearn_PassiveAggressiveRegressor": SklearnLinearModelAssembler,
    "sklearn_PoissonRegressor": SklearnGLMModelAssembler,
    "sklearn_RANSACRegressor": RANSACModelAssembler,
    "sklearn_Ridge": SklearnLinearModelAssembler,
    "sklearn_RidgeCV": SklearnLinearModelAssembler,
    "sklearn_SGDRegressor": SklearnLinearModelAssembler,
    "sklearn_TheilSenRegressor": SklearnLinearModelAssembler,
    "sklearn_TweedieRegressor": SklearnGLMModelAssembler,

    # Statsmodels Linear Regressors
    "statsmodels_GLMResultsWrapper": StatsmodelsGLMModelAssembler,
    "statsmodels_ProcessMLEResults": ProcessMLEModelAssembler,
    "statsmodels_RegressionResultsWrapper": StatsmodelsLinearModelAssembler,
    "statsmodels_RegularizedResultsWrapper": StatsmodelsModelAssemblerSelector,

    # Lightning Linear Regressors
    "lightning_AdaGradRegressor": SklearnLinearModelAssembler,
    "lightning_CDRegressor": SklearnLinearModelAssembler,
    "lightning_FistaRegressor": SklearnLinearModelAssembler,
    "lightning_SAGARegressor": SklearnLinearModelAssembler,
    "lightning_SAGRegressor": SklearnLinearModelAssembler,
    "lightning_SDCARegressor": SklearnLinearModelAssembler,

    # Sklearn Linear Classifiers
    "sklearn_LogisticRegression": SklearnLinearModelAssembler,
    "sklearn_LogisticRegressionCV": SklearnLinearModelAssembler,
    "sklearn_PassiveAggressiveClassifier": SklearnLinearModelAssembler,
    "sklearn_Perceptron": SklearnLinearModelAssembler,
    "sklearn_RidgeClassifier": SklearnLinearModelAssembler,
    "sklearn_RidgeClassifierCV": SklearnLinearModelAssembler,
    "sklearn_SGDClassifier": SklearnLinearModelAssembler,

    # Lightning Linear Classifiers
    "lightning_AdaGradClassifier": SklearnLinearModelAssembler,
    "lightning_CDClassifier": SklearnLinearModelAssembler,
    "lightning_FistaClassifier": SklearnLinearModelAssembler,
    "lightning_SAGAClassifier": SklearnLinearModelAssembler,
    "lightning_SAGClassifier": SklearnLinearModelAssembler,
    "lightning_SDCAClassifier": SklearnLinearModelAssembler,
    "lightning_SGDClassifier": SklearnLinearModelAssembler,

    # Decision trees
    "sklearn_DecisionTreeClassifier": TreeModelAssembler,
    "sklearn_DecisionTreeRegressor": TreeModelAssembler,
    "sklearn_ExtraTreeClassifier": TreeModelAssembler,
    "sklearn_ExtraTreeRegressor": TreeModelAssembler,

    # Ensembles
    "sklearn_ExtraTreesClassifier": RandomForestModelAssembler,
    "sklearn_ExtraTreesRegressor": RandomForestModelAssembler,
    "sklearn_RandomForestClassifier": RandomForestModelAssembler,
    "sklearn_RandomForestRegressor": RandomForestModelAssembler,
}


def _get_full_model_name(model):
    type_name = type(model)
    return f"{type_name.__module__.split('.')[0]}_{type_name.__name__}"


def get_assembler_cls(model):
    model_name = _get_full_model_name(model)
    assembler_cls = SUPPORTED_MODELS.get(model_name)

    if not assembler_cls:
        raise NotImplementedError(f"Model '{model_name}' is not supported")

    return assembler_cls
