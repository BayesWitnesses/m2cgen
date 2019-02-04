import sys
import xgboost
import m2cgen as m2c
from tests import utils
from m2cgen import assemblers, ast


def test_xgboost():
    sys.setrecursionlimit(5000)
    estimator = xgboost.XGBClassifier(n_estimators=100)
    utils.train_model_classification_binary(estimator)
    code = m2c.export_to_python(estimator)
    with open("test.py", "w") as fd:
        fd.write(code)
    assembler = assemblers.XGBoostModelAssembler(estimator)
    # print(assembler.assemble())
