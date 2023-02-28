"""Simple util to export example code.

Example usage:

    $ python tools/generate_code_examples.py <path_to_folder>

The structure of the exported code will be:

<absolute_path_to_folder>/<language>/<model_type><model_name>.<language_ext>
"""
import sys
from itertools import product
from pathlib import Path

import lightgbm as lgb
import xgboost as xgb
from sklearn import ensemble, linear_model, svm, tree

import m2cgen as m2c

from tests import utils

RECURSION_LIMIT = 5000

RANDOM_SEED = 1234
TREE_PARAMS = dict(random_state=RANDOM_SEED, max_leaf_nodes=5)
FOREST_PARAMS = dict(n_estimators=2, random_state=RANDOM_SEED, max_leaf_nodes=5)
XGBOOST_PARAMS = dict(n_estimators=2, random_state=RANDOM_SEED, max_depth=2)
LIGHTGBM_PARAMS = dict(n_estimators=2, random_state=RANDOM_SEED, max_depth=2)
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
    ("ruby", m2c.export_to_ruby, "rb"),
    ("f_sharp", m2c.export_to_f_sharp, "fs"),
    ("rust", m2c.export_to_rust, "rs"),
    ("elixir", m2c.export_to_elixir, "ex"),
    ("fortran", m2c.export_to_fortran, "fo"),
]

EXAMPLE_MODELS = [
    (
        "regression", "linear",
        linear_model.LinearRegression(),
        utils.get_regression_model_trainer(),
    ),
    (
        "classification", "linear",
        linear_model.LogisticRegression(random_state=RANDOM_SEED),
        utils.get_classification_model_trainer(),
    ),
    (
        "regression", "decision_tree",
        tree.DecisionTreeRegressor(**TREE_PARAMS),
        utils.get_regression_model_trainer(),
    ),
    (
        "classification", "decision_tree",
        tree.DecisionTreeClassifier(**TREE_PARAMS),
        utils.get_classification_model_trainer(),
    ),
    (
        "regression", "random_forest",
        ensemble.RandomForestRegressor(**FOREST_PARAMS),
        utils.get_regression_model_trainer(),
    ),
    (
        "classification", "random_forest",
        ensemble.RandomForestClassifier(**FOREST_PARAMS),
        utils.get_classification_model_trainer(),
    ),
    (
        "regression", "xgboost",
        xgb.XGBRegressor(**XGBOOST_PARAMS),
        utils.get_regression_model_trainer(),
    ),
    (
        "classification", "xgboost",
        xgb.XGBClassifier(**XGBOOST_PARAMS),
        utils.get_classification_model_trainer(),
    ),
    (
        "regression", "lightgbm",
        lgb.LGBMRegressor(**LIGHTGBM_PARAMS),
        utils.get_regression_model_trainer(),
    ),
    (
        "classification", "lightgbm",
        lgb.LGBMClassifier(**LIGHTGBM_PARAMS),
        utils.get_classification_model_trainer(),
    ),
    (
        "regression", "svm",
        svm.NuSVR(nu=0.1),
        utils.get_regression_model_trainer(),
    ),
    (
        "classification", "svm",
        svm.NuSVC(**SVC_PARAMS),
        utils.get_classification_model_trainer(),
    ),
]


if __name__ == "__main__":
    sys.setrecursionlimit(RECURSION_LIMIT)

    if len(sys.argv) != 2:
        print("Path to the export folder is required")
        sys.exit(1)

    export_folder = Path(sys.argv[1]).absolute()

    prod = product(EXAMPLE_LANGUAGES, EXAMPLE_MODELS)
    for (language, exporter, file_ext), (mtype, mname, model, trainer) in prod:
        trainer(model)

        # Make sure path exists, create if doesn't.
        folder = export_folder / language / mtype
        folder.mkdir(parents=True, exist_ok=True)

        model_path = folder / f"{mname}.{file_ext}"
        model_path.write_text(exporter(model), encoding="utf-8")
