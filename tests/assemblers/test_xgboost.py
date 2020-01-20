import xgboost
import numpy as np
import os
from tests import utils
from m2cgen import assemblers, ast


def test_binary_classification():
    estimator = xgboost.XGBClassifier(n_estimators=2, random_state=1,
                                      max_depth=1)
    utils.train_model_classification_binary(estimator)

    assembler = assemblers.XGBoostTreeModelAssembler(estimator)
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
                                ast.SubroutineExpr(
                                    ast.IfExpr(
                                        ast.CompExpr(
                                            ast.FeatureRef(20),
                                            ast.NumVal(16.7950001),
                                            ast.CompOpType.GTE),
                                        ast.NumVal(-0.173057005),
                                        ast.NumVal(0.163440868))),
                                ast.BinNumOpType.ADD),
                            ast.SubroutineExpr(
                                ast.IfExpr(
                                    ast.CompExpr(
                                        ast.FeatureRef(27),
                                        ast.NumVal(0.142349988),
                                        ast.CompOpType.GTE),
                                    ast.NumVal(-0.161026895),
                                    ast.NumVal(0.149405137))),
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

    assembler = assemblers.XGBoostTreeModelAssembler(estimator)
    actual = assembler.assemble()

    exponent = ast.ExpExpr(
        ast.SubroutineExpr(
            ast.BinNumExpr(
                ast.NumVal(0.5),
                ast.SubroutineExpr(
                    ast.NumVal(0.0)),
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

    assembler = assemblers.XGBoostTreeModelAssembler(estimator)
    actual = assembler.assemble()

    expected = ast.SubroutineExpr(
        ast.BinNumExpr(
            ast.BinNumExpr(
                ast.NumVal(base_score),
                ast.SubroutineExpr(
                    ast.IfExpr(
                        ast.CompExpr(
                            ast.FeatureRef(12),
                            ast.NumVal(9.72500038),
                            ast.CompOpType.GTE),
                        ast.NumVal(1.6614188),
                        ast.NumVal(2.91697121))),
                ast.BinNumOpType.ADD),
            ast.SubroutineExpr(
                ast.IfExpr(
                    ast.CompExpr(
                        ast.FeatureRef(5),
                        ast.NumVal(6.94099998),
                        ast.CompOpType.GTE),
                    ast.NumVal(3.33810854),
                    ast.NumVal(1.71813202))),
            ast.BinNumOpType.ADD))

    assert utils.cmp_exprs(actual, expected)


def test_regression_best_ntree_limit():
    base_score = 0.6
    estimator = xgboost.XGBRegressor(n_estimators=3, random_state=1,
                                     max_depth=1, base_score=base_score)

    estimator.best_ntree_limit = 2

    utils.train_model_regression(estimator)

    assembler = assemblers.XGBoostTreeModelAssembler(estimator)
    actual = assembler.assemble()

    expected = ast.SubroutineExpr(
        ast.BinNumExpr(
            ast.BinNumExpr(
                ast.NumVal(base_score),
                ast.SubroutineExpr(
                    ast.IfExpr(
                        ast.CompExpr(
                            ast.FeatureRef(12),
                            ast.NumVal(9.72500038),
                            ast.CompOpType.GTE),
                        ast.NumVal(1.6614188),
                        ast.NumVal(2.91697121))),
                ast.BinNumOpType.ADD),
            ast.SubroutineExpr(
                ast.IfExpr(
                    ast.CompExpr(
                        ast.FeatureRef(5),
                        ast.NumVal(6.94099998),
                        ast.CompOpType.GTE),
                    ast.NumVal(3.33810854),
                    ast.NumVal(1.71813202))),
            ast.BinNumOpType.ADD))

    assert utils.cmp_exprs(actual, expected)


def test_multi_class_best_ntree_limit():
    base_score = 0.5
    estimator = xgboost.XGBClassifier(n_estimators=100, random_state=1,
                                      max_depth=1, base_score=base_score)

    estimator.best_ntree_limit = 1

    utils.train_model_classification(estimator)

    assembler = assemblers.XGBoostTreeModelAssembler(estimator)
    actual = assembler.assemble()

    estimator_exp_class1 = ast.ExpExpr(
        ast.SubroutineExpr(
            ast.BinNumExpr(
                ast.NumVal(0.5),
                ast.SubroutineExpr(
                    ast.IfExpr(
                        ast.CompExpr(
                            ast.FeatureRef(2),
                            ast.NumVal(2.45000005),
                            ast.CompOpType.GTE),
                        ast.NumVal(-0.0733167157),
                        ast.NumVal(0.143414631))),
                ast.BinNumOpType.ADD)),
        to_reuse=True)

    estimator_exp_class2 = ast.ExpExpr(
        ast.SubroutineExpr(
            ast.BinNumExpr(
                ast.NumVal(0.5),
                ast.SubroutineExpr(
                    ast.IfExpr(
                        ast.CompExpr(
                            ast.FeatureRef(2),
                            ast.NumVal(2.45000005),
                            ast.CompOpType.GTE),
                        ast.NumVal(0.0344139598),
                        ast.NumVal(-0.0717073306))),
                ast.BinNumOpType.ADD)),
        to_reuse=True)

    estimator_exp_class3 = ast.ExpExpr(
        ast.SubroutineExpr(
            ast.BinNumExpr(
                ast.NumVal(0.5),
                ast.SubroutineExpr(
                    ast.IfExpr(
                        ast.CompExpr(
                            ast.FeatureRef(3),
                            ast.NumVal(1.6500001),
                            ast.CompOpType.GTE),
                        ast.NumVal(0.13432835),
                        ast.NumVal(-0.0644444525))),
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
    base_score = 0.6
    estimator = xgboost.XGBRegressor(n_estimators=2, random_state=1,
                                     max_depth=1, base_score=base_score)
    utils.train_model_regression(estimator)

    with utils.tmp_dir() as tmp_dirpath:
        filename = os.path.join(tmp_dirpath, "tmp.file")
        estimator.save_model(filename)
        estimator = xgboost.XGBRegressor(base_score=base_score)
        estimator.load_model(filename)

    assembler = assemblers.XGBoostTreeModelAssembler(estimator)
    actual = assembler.assemble()

    expected = ast.SubroutineExpr(
        ast.BinNumExpr(
            ast.BinNumExpr(
                ast.NumVal(base_score),
                ast.SubroutineExpr(
                    ast.IfExpr(
                        ast.CompExpr(
                            ast.FeatureRef(12),
                            ast.NumVal(9.72500038),
                            ast.CompOpType.GTE),
                        ast.NumVal(1.6614188),
                        ast.NumVal(2.91697121))),
                ast.BinNumOpType.ADD),
            ast.SubroutineExpr(
                ast.IfExpr(
                    ast.CompExpr(
                        ast.FeatureRef(5),
                        ast.NumVal(6.94099998),
                        ast.CompOpType.GTE),
                    ast.NumVal(3.33810854),
                    ast.NumVal(1.71813202))),
            ast.BinNumOpType.ADD))

    assert utils.cmp_exprs(actual, expected)


def test_leaves_cutoff_threshold():
    estimator = xgboost.XGBClassifier(n_estimators=2, random_state=1,
                                      max_depth=1)
    utils.train_model_classification_binary(estimator)

    assembler = assemblers.XGBoostTreeModelAssembler(estimator,
                                                     leaves_cutoff_threshold=1)
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
                                ast.SubroutineExpr(
                                    ast.SubroutineExpr(
                                        ast.IfExpr(
                                            ast.CompExpr(
                                                ast.FeatureRef(20),
                                                ast.NumVal(16.7950001),
                                                ast.CompOpType.GTE),
                                            ast.NumVal(-0.173057005),
                                            ast.NumVal(0.163440868)))),
                                ast.BinNumOpType.ADD),
                            ast.SubroutineExpr(
                                ast.SubroutineExpr(
                                    ast.IfExpr(
                                        ast.CompExpr(
                                            ast.FeatureRef(27),
                                            ast.NumVal(0.142349988),
                                            ast.CompOpType.GTE),
                                        ast.NumVal(-0.161026895),
                                        ast.NumVal(0.149405137)))),
                            ast.BinNumOpType.ADD)),
                    ast.BinNumOpType.SUB)),
            ast.BinNumOpType.ADD),
        ast.BinNumOpType.DIV,
        to_reuse=True)

    expected = ast.VectorVal([
        ast.BinNumExpr(ast.NumVal(1), sigmoid, ast.BinNumOpType.SUB),
        sigmoid])

    assert utils.cmp_exprs(actual, expected)


def test_linear_model():
    estimator = xgboost.XGBRegressor(n_estimators=2, random_state=1,
                                     feature_selector="shuffle",
                                     booster="gblinear")
    utils.train_model_regression(estimator)

    assembler = assemblers.XGBoostLinearModelAssembler(estimator)
    actual = assembler.assemble()

    feature_weight_mul = [
        ast.BinNumExpr(
            ast.FeatureRef(0),
            ast.NumVal(-0.00999326),
            ast.BinNumOpType.MUL),
        ast.BinNumExpr(
            ast.FeatureRef(1),
            ast.NumVal(0.0520094),
            ast.BinNumOpType.MUL),
        ast.BinNumExpr(
            ast.FeatureRef(2),
            ast.NumVal(0.10447),
            ast.BinNumOpType.MUL),
        ast.BinNumExpr(
            ast.FeatureRef(3),
            ast.NumVal(0.17387),
            ast.BinNumOpType.MUL),
        ast.BinNumExpr(
            ast.FeatureRef(4),
            ast.NumVal(0.691745),
            ast.BinNumOpType.MUL),
        ast.BinNumExpr(
            ast.FeatureRef(5),
            ast.NumVal(0.296357),
            ast.BinNumOpType.MUL),
        ast.BinNumExpr(
            ast.FeatureRef(6),
            ast.NumVal(0.0288206),
            ast.BinNumOpType.MUL),
        ast.BinNumExpr(
            ast.FeatureRef(7),
            ast.NumVal(0.417822),
            ast.BinNumOpType.MUL),
        ast.BinNumExpr(
            ast.FeatureRef(8),
            ast.NumVal(0.0551116),
            ast.BinNumOpType.MUL),
        ast.BinNumExpr(
            ast.FeatureRef(9),
            ast.NumVal(0.00242449),
            ast.BinNumOpType.MUL),
        ast.BinNumExpr(
            ast.FeatureRef(10),
            ast.NumVal(0.109585),
            ast.BinNumOpType.MUL),
        ast.BinNumExpr(
            ast.FeatureRef(11),
            ast.NumVal(0.00744202),
            ast.BinNumOpType.MUL),
        ast.BinNumExpr(
            ast.FeatureRef(12),
            ast.NumVal(0.0731089),
            ast.BinNumOpType.MUL),
    ]

    expected = ast.SubroutineExpr(
        ast.BinNumExpr(
            ast.NumVal(0.5),
            assemblers.utils.apply_op_to_expressions(
                ast.BinNumOpType.ADD,
                ast.NumVal(3.13109),
                *feature_weight_mul),
            ast.BinNumOpType.ADD))

    assert utils.cmp_exprs(actual, expected)
