from .linear import (SklearnLinearModelAssembler,
                     StatsmodelsLinearModelAssembler)
from .tree import TreeModelAssembler
from .ensemble import RandomForestModelAssembler
from .boosting import (XGBoostModelAssemblerSelector,
                       XGBoostTreeModelAssembler,
                       XGBoostLinearModelAssembler,
                       LightGBMModelAssembler)
from .svm import SVMModelAssembler
from .meta import RANSACModelAssembler

__all__ = [
    SklearnLinearModelAssembler,
    StatsmodelsLinearModelAssembler,
    RANSACModelAssembler,
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
    "lightgbm.sklearn.LGBMClassifier": LightGBMModelAssembler,
    "lightgbm.sklearn.LGBMRegressor": LightGBMModelAssembler,

    # XGBoost
    "xgboost.sklearn.XGBClassifier": XGBoostModelAssemblerSelector,
    "xgboost.sklearn.XGBRFClassifier": XGBoostModelAssemblerSelector,
    "xgboost.sklearn.XGBRegressor": XGBoostModelAssemblerSelector,
    "xgboost.sklearn.XGBRFRegressor": XGBoostModelAssemblerSelector,

    # Sklearn SVM
    "sklearn.svm.classes.LinearSVC": SklearnLinearModelAssembler,
    "sklearn.svm.classes.LinearSVR": SklearnLinearModelAssembler,
    "sklearn.svm.classes.NuSVC": SVMModelAssembler,
    "sklearn.svm.classes.NuSVR": SVMModelAssembler,
    "sklearn.svm.classes.SVC": SVMModelAssembler,
    "sklearn.svm.classes.SVR": SVMModelAssembler,

    # lightning SVM
    "lightning.impl.dual_cd.LinearSVC": SklearnLinearModelAssembler,
    "lightning.impl.dual_cd.LinearSVR": SklearnLinearModelAssembler,

    # Sklearn Linear Regressors
    "sklearn.linear_model.bayes.ARDRegression": SklearnLinearModelAssembler,
    "sklearn.linear_model.bayes.BayesianRidge": SklearnLinearModelAssembler,
    "sklearn.linear_model.coordinate_descent.ElasticNet":
        SklearnLinearModelAssembler,
    "sklearn.linear_model.coordinate_descent.ElasticNetCV":
        SklearnLinearModelAssembler,
    "sklearn.linear_model.huber.HuberRegressor": SklearnLinearModelAssembler,
    "sklearn.linear_model.least_angle.Lars": SklearnLinearModelAssembler,
    "sklearn.linear_model.least_angle.LarsCV": SklearnLinearModelAssembler,
    "sklearn.linear_model.coordinate_descent.Lasso":
        SklearnLinearModelAssembler,
    "sklearn.linear_model.coordinate_descent.LassoCV":
        SklearnLinearModelAssembler,
    "sklearn.linear_model.least_angle.LassoLars":
        SklearnLinearModelAssembler,
    "sklearn.linear_model.least_angle.LassoLarsCV":
        SklearnLinearModelAssembler,
    "sklearn.linear_model.least_angle.LassoLarsIC":
        SklearnLinearModelAssembler,
    "sklearn.linear_model.base.LinearRegression":
        SklearnLinearModelAssembler,
    "sklearn.linear_model.omp.OrthogonalMatchingPursuit":
        SklearnLinearModelAssembler,
    "sklearn.linear_model.omp.OrthogonalMatchingPursuitCV":
        SklearnLinearModelAssembler,
    "sklearn.linear_model.passive_aggressive.PassiveAggressiveRegressor":
        SklearnLinearModelAssembler,
    "sklearn.linear_model.ransac.RANSACRegressor": RANSACModelAssembler,
    "sklearn.linear_model.ridge.Ridge": SklearnLinearModelAssembler,
    "sklearn.linear_model.ridge.RidgeCV": SklearnLinearModelAssembler,
    "sklearn.linear_model.stochastic_gradient.SGDRegressor":
        SklearnLinearModelAssembler,
    "sklearn.linear_model.theil_sen.TheilSenRegressor":
        SklearnLinearModelAssembler,

    # Statsmodels Linear Regressors
    "statsmodels.regression.linear_model.RegressionResultsWrapper":
        StatsmodelsLinearModelAssembler,
    "statsmodels.base.elastic_net.RegularizedResultsWrapper":
        StatsmodelsLinearModelAssembler,

    # lightning Linear Regressors
    "lightning.impl.adagrad.AdaGradRegressor": SklearnLinearModelAssembler,
    "lightning.impl.primal_cd.CDRegressor": SklearnLinearModelAssembler,
    "lightning.impl.fista.FistaRegressor": SklearnLinearModelAssembler,
    "lightning.impl.sag.SAGARegressor": SklearnLinearModelAssembler,
    "lightning.impl.sag.SAGRegressor": SklearnLinearModelAssembler,
    "lightning.impl.sdca.SDCARegressor": SklearnLinearModelAssembler,

    # Sklearn Linear Classifiers
    "sklearn.linear_model.logistic.LogisticRegression":
        SklearnLinearModelAssembler,
    "sklearn.linear_model.logistic.LogisticRegressionCV":
        SklearnLinearModelAssembler,
    "sklearn.linear_model.passive_aggressive.PassiveAggressiveClassifier":
        SklearnLinearModelAssembler,
    "sklearn.linear_model.perceptron.Perceptron":
        SklearnLinearModelAssembler,
    "sklearn.linear_model.ridge.RidgeClassifier":
        SklearnLinearModelAssembler,
    "sklearn.linear_model.ridge.RidgeClassifierCV":
        SklearnLinearModelAssembler,
    "sklearn.linear_model.stochastic_gradient.SGDClassifier":
        SklearnLinearModelAssembler,

    # lightning Linear Classifiers
    "lightning.impl.adagrad.AdaGradClassifier": SklearnLinearModelAssembler,
    "lightning.impl.primal_cd.CDClassifier": SklearnLinearModelAssembler,
    "lightning.impl.fista.FistaClassifier": SklearnLinearModelAssembler,
    "lightning.impl.sag.SAGAClassifier": SklearnLinearModelAssembler,
    "lightning.impl.sag.SAGClassifier": SklearnLinearModelAssembler,
    "lightning.impl.sdca.SDCAClassifier": SklearnLinearModelAssembler,
    "lightning.impl.sgd.SGDClassifier": SklearnLinearModelAssembler,

    # Decision trees
    "sklearn.tree.tree.DecisionTreeClassifier": TreeModelAssembler,
    "sklearn.tree.tree.DecisionTreeRegressor": TreeModelAssembler,
    "sklearn.tree.tree.ExtraTreeClassifier": TreeModelAssembler,
    "sklearn.tree.tree.ExtraTreeRegressor": TreeModelAssembler,

    # Ensembles
    "sklearn.ensemble.forest.ExtraTreesClassifier":
        RandomForestModelAssembler,
    "sklearn.ensemble.forest.ExtraTreesRegressor":
        RandomForestModelAssembler,
    "sklearn.ensemble.forest.RandomForestClassifier":
        RandomForestModelAssembler,
    "sklearn.ensemble.forest.RandomForestRegressor":
        RandomForestModelAssembler,
}


def _get_full_model_name(model):
    type_name = type(model)
    return "{}.{}".format(type_name.__module__,
                          type_name.__name__)


def get_assembler_cls(model):
    model_name = _get_full_model_name(model)
    assembler_cls = SUPPORTED_MODELS.get(model_name)

    if not assembler_cls:
        raise NotImplementedError(
            "Model {} is not supported".format(model_name))

    return assembler_cls
