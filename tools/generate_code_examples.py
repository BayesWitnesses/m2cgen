"""Simple util to export example code.

Example usage:

    $ python tools/generate_code_examples.py <path_to_folder>

The structure of the exported code will be:

<absolute_path_to_folder>/<language>/<model_type><model_name>.<language_ext>
"""
import os
import sys
import itertools

import lightgbm
import xgboost
from sklearn.linear_model import LinearRegression, LogisticRegression
from sklearn.tree import DecisionTreeRegressor, DecisionTreeClassifier
from sklearn.ensemble import RandomForestRegressor, RandomForestClassifier
from sklearn.svm import NuSVR, NuSVC

import m2cgen as m2c
from tests import utils


RECURSION_LIMIT = 5000

RANDOM_SEED = 1234
TREE_PARAMS = dict(random_state=RANDOM_SEED, max_leaf_nodes=5)
FOREST_PARAMS = dict(
    n_estimators=2, random_state=RANDOM_SEED, max_leaf_nodes=5)
XGBOOST_PARAMS = dict(n_estimators=2, random_state=RANDOM_SEED, max_depth=2)
LIGHT_GBM_PARAMS = dict(n_estimators=2, random_state=RANDOM_SEED, max_depth=2)
SVC_PARAMS = dict(kernel="rbf", nu=0.1, random_state=RANDOM_SEED)


EXAMPLE_LANGUAGES = [
    ("python", m2c.export_to_python, "py"),
    ("java", m2c.export_to_java, "java"),
    ("c", m2c.export_to_c, "c"),
    ("go", m2c.export_to_go, "go"),
    ("javascript", m2c.export_to_javascript, "js"),
    ("visual_basic", m2c.export_to_visual_basic, "vb"),
    ("c_sharp", m2c.export_to_c_sharp, "cs"),
    ("powershell", m2c.export_to_powershell, "ps1"),
    ("r", m2c.export_to_r, "r"),
    ("php", m2c.export_to_php, "php"),
    ("dart", m2c.export_to_dart, "dart"),
    ("haskell", m2c.export_to_haskell, "hs"),
]

EXAMPLE_MODELS = [
    (
        "regression", "linear",
        LinearRegression(),
        utils.get_regression_model_trainer(),
    ),
    (
        "classification", "linear",
        LogisticRegression(random_state=RANDOM_SEED),
        utils.get_classification_model_trainer(),
    ),
    (
        "regression", "decision_tree",
        DecisionTreeRegressor(**TREE_PARAMS),
        utils.get_regression_model_trainer(),
    ),
    (
        "classification", "decision_tree",
        DecisionTreeClassifier(**TREE_PARAMS),
        utils.get_classification_model_trainer(),
    ),
    (
        "regression", "random_forest",
        RandomForestRegressor(**FOREST_PARAMS),
        utils.get_regression_model_trainer(),
    ),
    (
        "classification", "random_forest",
        RandomForestClassifier(**FOREST_PARAMS),
        utils.get_classification_model_trainer(),
    ),
    (
        "regression", "xgboost",
        xgboost.XGBRegressor(**XGBOOST_PARAMS),
        utils.get_regression_model_trainer(),
    ),
    (
        "classification", "xgboost",
        xgboost.XGBClassifier(**XGBOOST_PARAMS),
        utils.get_classification_model_trainer(),
    ),
    (
        "regression", "lightgbm",
        lightgbm.LGBMRegressor(**LIGHT_GBM_PARAMS),
        utils.get_regression_model_trainer(),
    ),
    (
        "classification", "lightgbm",
        lightgbm.LGBMClassifier(**LIGHT_GBM_PARAMS),
        utils.get_classification_model_trainer(),
    ),
    (
        "regression", "svm",
        NuSVR(nu=0.1),
        utils.get_regression_model_trainer(),
    ),
    (
        "classification", "svm",
        NuSVC(**SVC_PARAMS),
        utils.get_classification_model_trainer(),
    ),
]


if __name__ == "__main__":
    sys.setrecursionlimit(RECURSION_LIMIT)

    if len(sys.argv) != 2:
        print("Path to the export folder is required")
        sys.exit(1)

    export_folder = os.path.abspath(sys.argv[1])

    prod = itertools.product(EXAMPLE_LANGUAGES, EXAMPLE_MODELS)
    for (language, exporter, file_ext), (mtype, mname, model, trainer) in prod:
        trainer(model)

        # Make sure path exists, create if doesn't.
        folder = os.path.join(export_folder, language, mtype)
        os.makedirs(folder, exist_ok=True)

        model_filename = "{}.{}".format(mname, file_ext)
        model_path = os.path.join(folder, model_filename)

        with open(model_path, "w") as f:
            f.write(exporter(model))
