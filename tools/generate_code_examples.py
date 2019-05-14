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
from sklearn import linear_model, tree, ensemble, svm

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
]

EXAMPLE_MODELS = [
    (
        "regression", "linear",
        linear_model.LinearRegression(),
        utils.train_model_regression,
    ),
    (
        "classification", "linear",
        linear_model.LogisticRegression(random_state=RANDOM_SEED),
        utils.train_model_classification,
    ),
    (
        "regression", "decision_tree",
        tree.DecisionTreeRegressor(**TREE_PARAMS),
        utils.train_model_regression,
    ),
    (
        "classification", "decision_tree",
        tree.DecisionTreeClassifier(**TREE_PARAMS),
        utils.train_model_classification,
    ),
    (
        "regression", "random_forest",
        ensemble.RandomForestRegressor(**FOREST_PARAMS),
        utils.train_model_regression,
    ),
    (
        "classification", "random_forest",
        ensemble.RandomForestClassifier(**FOREST_PARAMS),
        utils.train_model_classification,
    ),
    (
        "regression", "xgboost",
        xgboost.XGBRegressor(**XGBOOST_PARAMS),
        utils.train_model_regression,
    ),
    (
        "classification", "xgboost",
        xgboost.XGBClassifier(**XGBOOST_PARAMS),
        utils.train_model_classification,
    ),
    (
        "regression", "lightgbm",
        lightgbm.LGBMRegressor(**LIGHT_GBM_PARAMS),
        utils.train_model_regression,
    ),
    (
        "classification", "lightgbm",
        lightgbm.LGBMClassifier(**LIGHT_GBM_PARAMS),
        utils.train_model_classification,
    ),
    (
        "regression", "svm",
        svm.NuSVR(nu=0.1),
        utils.train_model_regression,
    ),
    (
        "classification", "svm",
        svm.NuSVC(**SVC_PARAMS),
        utils.train_model_classification,
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
