"""Simple util to export example code.

Example usage:

    $ python tools/generate_code_examples.py <path_to_folder>

The structure of the exported code will be:

<absolute_path_to_folder>/<language>/<model_name>.<language_ext>
"""

import os
import sys
import itertools
from sklearn import linear_model, tree, ensemble

import m2cgen as m2c
from tests import utils


RANDOM_SEED = 1234
TREE_PARAMS = dict(random_state=RANDOM_SEED)
FOREST_PARAMS = dict(n_estimators=10, random_state=RANDOM_SEED)


EXAMPLE_LANGUAGES = [
    ("python", m2c.export_to_python, "py"),
    ("java", m2c.export_to_java, "java"),
    ("c", m2c.export_to_c, "c"),
]

EXAMPLE_MODELS = [
    (
        "linear_regression",
        linear_model.LinearRegression(),
        utils.train_model_regression,
    ),
    (
        "linear_classification",
        linear_model.LogisticRegression(random_state=RANDOM_SEED),
        utils.train_model_classification,
    ),
    (
        "decision_tree_regression",
        tree.DecisionTreeRegressor(**TREE_PARAMS),
        utils.train_model_regression,
    ),
    (
        "decision_tree_classification",
        tree.DecisionTreeClassifier(**TREE_PARAMS),
        utils.train_model_classification,
    ),
    (
        "random_forest_regression",
        ensemble.RandomForestRegressor(**FOREST_PARAMS),
        utils.train_model_regression,
    ),
    (
        "random_forest_classification",
        ensemble.RandomForestClassifier(**FOREST_PARAMS),
        utils.train_model_classification,
    ),
]


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Path to the export folder is required")
        sys.exit(1)

    export_folder = os.path.abspath(sys.argv[1])

    prod = itertools.product(EXAMPLE_LANGUAGES, EXAMPLE_MODELS)
    for (language, exporter, file_ext), (model_name, model, trainer) in prod:
        trainer(model)

        # Make sure path exists, create if doesn't.
        language_path = os.path.join(export_folder, language)
        os.makedirs(language_path, exist_ok=True)

        model_filename = "{}.{}".format(model_name, file_ext)
        model_path = os.path.join(language_path, model_filename)

        with open(model_path, "w") as f:
            f.write(exporter(model))
