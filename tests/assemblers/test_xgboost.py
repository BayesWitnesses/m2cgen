import sys
import xgboost
import m2cgen as m2c
from tests import utils
from m2cgen import assemblers, ast


def test_xgboost():
    sys.setrecursionlimit(5000)
    estimator = xgboost.XGBClassifier(n_estimators=5)
    utils.train_model_classification(estimator)
    code = m2c.export_to_java(estimator)
    with open("Model.java", "w") as fd:
        fd.write(code)
    assembler = assemblers.XGBoostModelAssembler(estimator)
    # print(assembler.assemble())
