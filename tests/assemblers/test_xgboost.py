import xgboost
import numpy as np
from tests import utils
from m2cgen import assemblers, ast


def test_binary_classification():
    estimator = xgboost.XGBClassifier(n_estimators=2, random_state=1,
                                      max_depth=1)
    utils.train_model_classification_binary(estimator)

    assembler = assemblers.XGBoostModelAssembler(estimator)
    actual = assembler.assemble()

    sigmoid = ast.BinNumExpr(
        ast.NumVal(1),
        ast.BinNumExpr(
            ast.NumVal(1),
            ast.ExpExpr(
                ast.BinNumExpr(
                    ast.NumVal(0),
                    ast.SubroutineExpr(
                        ast.BinNumExpr(
                            ast.BinNumExpr(
                                ast.NumVal(-0.0),
                                ast.IfExpr(
                                    ast.CompExpr(
                                        ast.FeatureRef(20),
                                        ast.NumVal(16.7950001),
                                        ast.CompOpType.GTE),
                                    ast.NumVal(-0.17062147),
                                    ast.NumVal(0.1638484)),
                                ast.BinNumOpType.ADD),
                            ast.IfExpr(
                                ast.CompExpr(
                                    ast.FeatureRef(27),
                                    ast.NumVal(0.142349988),
                                    ast.CompOpType.GTE),
                                ast.NumVal(-0.16087772),
                                ast.NumVal(0.149866998)),
                            ast.BinNumOpType.ADD)),
                    ast.BinNumOpType.SUB)),
            ast.BinNumOpType.ADD),
        ast.BinNumOpType.DIV,
        to_reuse=True)

    expected = ast.VectorVal([
        ast.BinNumExpr(ast.NumVal(1), sigmoid, ast.BinNumOpType.SUB),
        sigmoid])

    assert utils.cmp_exprs(actual, expected)


def test_multi_class():
    estimator = xgboost.XGBClassifier(n_estimators=1, random_state=1,
                                      max_depth=1)
    estimator.fit(np.array([[1], [2], [3]]), np.array([1, 2, 3]))

    assembler = assemblers.XGBoostModelAssembler(estimator)
    actual = assembler.assemble()

    exponent = ast.ExpExpr(
        ast.SubroutineExpr(
            ast.BinNumExpr(
                ast.NumVal(0.5),
                ast.NumVal(0.0),
                ast.BinNumOpType.ADD)),
        to_reuse=True)

    exponent_sum = ast.BinNumExpr(
        ast.BinNumExpr(exponent, exponent, ast.BinNumOpType.ADD),
        exponent,
        ast.BinNumOpType.ADD,
        to_reuse=True)

    softmax = ast.BinNumExpr(exponent, exponent_sum, ast.BinNumOpType.DIV)

    expected = ast.VectorVal([softmax] * 3)

    assert utils.cmp_exprs(actual, expected)


def test_regression():
    base_score = 0.6
    estimator = xgboost.XGBRegressor(n_estimators=2, random_state=1,
                                     max_depth=1, base_score=base_score)
    utils.train_model_regression(estimator)

    assembler = assemblers.XGBoostModelAssembler(estimator)
    actual = assembler.assemble()

    expected = ast.SubroutineExpr(
        ast.BinNumExpr(
            ast.BinNumExpr(
                ast.NumVal(base_score),
                ast.IfExpr(
                    ast.CompExpr(
                        ast.FeatureRef(12),
                        ast.NumVal(9.72500038),
                        ast.CompOpType.GTE),
                    ast.NumVal(1.67318344),
                    ast.NumVal(2.92757893)),
                ast.BinNumOpType.ADD),
            ast.IfExpr(
                ast.CompExpr(
                    ast.FeatureRef(5),
                    ast.NumVal(6.94099998),
                    ast.CompOpType.GTE),
                ast.NumVal(3.3400948),
                ast.NumVal(1.72118247)),
            ast.BinNumOpType.ADD))

    assert utils.cmp_exprs(actual, expected)


def test_regression_best_ntree_limit():
    base_score = 0.6
    estimator = xgboost.XGBRegressor(n_estimators=3, random_state=1,
                                     max_depth=1, base_score=base_score)

    estimator.best_ntree_limit = 2

    utils.train_model_regression(estimator)

    assembler = assemblers.XGBoostModelAssembler(estimator)
    actual = assembler.assemble()

    expected = ast.SubroutineExpr(
        ast.BinNumExpr(
            ast.BinNumExpr(
                ast.NumVal(base_score),
                ast.IfExpr(
                    ast.CompExpr(
                        ast.FeatureRef(12),
                        ast.NumVal(9.72500038),
                        ast.CompOpType.GTE),
                    ast.NumVal(1.67318344),
                    ast.NumVal(2.92757893)),
                ast.BinNumOpType.ADD),
            ast.IfExpr(
                ast.CompExpr(
                    ast.FeatureRef(5),
                    ast.NumVal(6.94099998),
                    ast.CompOpType.GTE),
                ast.NumVal(3.3400948),
                ast.NumVal(1.72118247)),
            ast.BinNumOpType.ADD))

    assert utils.cmp_exprs(actual, expected)


def test_multi_class_best_ntree_limit():
    base_score = 0.5
    estimator = xgboost.XGBClassifier(n_estimators=100, random_state=1,
                                      max_depth=1, base_score=base_score)

    estimator.best_ntree_limit = 1

    utils.train_model_classification(estimator)

    assembler = assemblers.XGBoostModelAssembler(estimator)
    actual = assembler.assemble()

    estimator_exp_class1 = ast.ExpExpr(
        ast.SubroutineExpr(
            ast.BinNumExpr(
                ast.NumVal(0.5),
                ast.IfExpr(
                    ast.CompExpr(
                        ast.FeatureRef(2),
                        ast.NumVal(2.5999999),
                        ast.CompOpType.GTE),
                    ast.NumVal(-0.0731707439),
                    ast.NumVal(0.142857149)),
                ast.BinNumOpType.ADD)),
        to_reuse=True)

    estimator_exp_class2 = ast.ExpExpr(
        ast.SubroutineExpr(
            ast.BinNumExpr(
                ast.NumVal(0.5),
                ast.IfExpr(
                    ast.CompExpr(
                        ast.FeatureRef(2),
                        ast.NumVal(2.5999999),
                        ast.CompOpType.GTE),
                    ast.NumVal(0.0341463387),
                    ast.NumVal(-0.0714285821)),
                ast.BinNumOpType.ADD)),
        to_reuse=True)

    estimator_exp_class3 = ast.ExpExpr(
        ast.SubroutineExpr(
            ast.BinNumExpr(
                ast.NumVal(0.5),
                ast.IfExpr(
                    ast.CompExpr(
                        ast.FeatureRef(2),
                        ast.NumVal(4.85000038),
                        ast.CompOpType.GTE),
                    ast.NumVal(0.129441619),
                    ast.NumVal(-0.0681440532)),
                ast.BinNumOpType.ADD)),
        to_reuse=True)

    exp_sum = ast.BinNumExpr(
        ast.BinNumExpr(
            estimator_exp_class1,
            estimator_exp_class2,
            ast.BinNumOpType.ADD),
        estimator_exp_class3,
        ast.BinNumOpType.ADD,
        to_reuse=True)

    expected = ast.VectorVal([
        ast.BinNumExpr(
            estimator_exp_class1,
            exp_sum,
            ast.BinNumOpType.DIV),
        ast.BinNumExpr(
            estimator_exp_class2,
            exp_sum,
            ast.BinNumOpType.DIV),
        ast.BinNumExpr(
            estimator_exp_class3,
            exp_sum,
            ast.BinNumOpType.DIV)
    ])

    assert utils.cmp_exprs(actual, expected)


def test_regression_saved_without_feature_names():
    import os

    base_score = 0.6
    estimator = xgboost.XGBRegressor(n_estimators=2, random_state=1,
                                     max_depth=1, base_score=base_score)
    utils.train_model_regression(estimator)

    filename = "tmp.file"
    if os.path.exists(filename):
        raise OSError("File is already exist")
    estimator.save_model(filename)
    estimator = xgboost.XGBRegressor(base_score=base_score)
    estimator.load_model(filename)
    if os.path.exists(filename):
        os.remove(filename)

    assembler = assemblers.XGBoostModelAssembler(estimator)
    actual = assembler.assemble()

    expected = ast.SubroutineExpr(
        ast.BinNumExpr(
            ast.BinNumExpr(
                ast.NumVal(base_score),
                ast.IfExpr(
                    ast.CompExpr(
                        ast.FeatureRef(12),
                        ast.NumVal(9.72500038),
                        ast.CompOpType.GTE),
                    ast.NumVal(1.67318344),
                    ast.NumVal(2.92757893)),
                ast.BinNumOpType.ADD),
            ast.IfExpr(
                ast.CompExpr(
                    ast.FeatureRef(5),
                    ast.NumVal(6.94099998),
                    ast.CompOpType.GTE),
                ast.NumVal(3.3400948),
                ast.NumVal(1.72118247)),
            ast.BinNumOpType.ADD))

    assert utils.cmp_exprs(actual, expected)
