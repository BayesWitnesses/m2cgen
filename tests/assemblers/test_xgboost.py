import xgboost
import numpy as np
import os
from tests import utils
from m2cgen import assemblers, ast


def test_binary_classification():
    estimator = xgboost.XGBClassifier(n_estimators=2, random_state=1,
                                      max_depth=1)
    utils.get_binary_classification_model_trainer()(estimator)

    assembler = assemblers.XGBoostModelAssemblerSelector(estimator)
    actual = assembler.assemble()

    sigmoid = ast.BinNumExpr(
        ast.NumVal(1),
        ast.BinNumExpr(
            ast.NumVal(1),
            ast.ExpExpr(
                ast.BinNumExpr(
                    ast.NumVal(0),
                    ast.BinNumExpr(
                        ast.IfExpr(
                            ast.CompExpr(
                                ast.FeatureRef(20),
                                ast.NumVal(16.7950001),
                                ast.CompOpType.GTE),
                            ast.NumVal(-0.519171),
                            ast.NumVal(0.49032259)),
                        ast.IfExpr(
                            ast.CompExpr(
                                ast.FeatureRef(27),
                                ast.NumVal(0.142349988),
                                ast.CompOpType.GTE),
                            ast.NumVal(-0.443304211),
                            ast.NumVal(0.391988248)),
                        ast.BinNumOpType.ADD),
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

    assembler = assemblers.XGBoostModelAssemblerSelector(estimator)
    actual = assembler.assemble()

    exponent = ast.ExpExpr(
        ast.BinNumExpr(
            ast.NumVal(0.5),
            ast.NumVal(0.0),
            ast.BinNumOpType.ADD),
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
    utils.get_regression_model_trainer()(estimator)

    assembler = assemblers.XGBoostModelAssemblerSelector(estimator)
    actual = assembler.assemble()

    expected = ast.BinNumExpr(
        ast.NumVal(base_score),
        ast.BinNumExpr(
            ast.IfExpr(
                ast.CompExpr(
                    ast.FeatureRef(12),
                    ast.NumVal(9.725),
                    ast.CompOpType.GTE),
                ast.NumVal(4.98425627),
                ast.NumVal(8.75091362)),
            ast.IfExpr(
                ast.CompExpr(
                    ast.FeatureRef(5),
                    ast.NumVal(6.941),
                    ast.CompOpType.GTE),
                ast.NumVal(8.34557438),
                ast.NumVal(3.9141891)),
            ast.BinNumOpType.ADD),
        ast.BinNumOpType.ADD)

    assert utils.cmp_exprs(actual, expected)


def test_regression_best_ntree_limit():
    base_score = 0.6
    estimator = xgboost.XGBRegressor(n_estimators=3, random_state=1,
                                     max_depth=1, base_score=base_score)

    estimator.best_ntree_limit = 2

    utils.get_regression_model_trainer()(estimator)

    assembler = assemblers.XGBoostModelAssemblerSelector(estimator)
    actual = assembler.assemble()

    expected = ast.BinNumExpr(
        ast.NumVal(base_score),
        ast.BinNumExpr(
            ast.IfExpr(
                ast.CompExpr(
                    ast.FeatureRef(12),
                    ast.NumVal(9.72500038),
                    ast.CompOpType.GTE),
                ast.NumVal(4.98425627),
                ast.NumVal(8.75091362)),
            ast.IfExpr(
                ast.CompExpr(
                    ast.FeatureRef(5),
                    ast.NumVal(6.94099998),
                    ast.CompOpType.GTE),
                ast.NumVal(8.34557438),
                ast.NumVal(3.9141891)),
            ast.BinNumOpType.ADD),
        ast.BinNumOpType.ADD)

    assert utils.cmp_exprs(actual, expected)


def test_multi_class_best_ntree_limit():
    base_score = 0.5
    estimator = xgboost.XGBClassifier(n_estimators=100, random_state=1,
                                      max_depth=1, base_score=base_score)

    estimator.best_ntree_limit = 1

    utils.get_classification_model_trainer()(estimator)

    assembler = assemblers.XGBoostModelAssemblerSelector(estimator)
    actual = assembler.assemble()

    estimator_exp_class1 = ast.ExpExpr(
        ast.BinNumExpr(
            ast.NumVal(0.5),
            ast.IfExpr(
                ast.CompExpr(
                    ast.FeatureRef(2),
                    ast.NumVal(2.45000005),
                    ast.CompOpType.GTE),
                ast.NumVal(-0.219950154),
                ast.NumVal(0.430243909)),
            ast.BinNumOpType.ADD),
        to_reuse=True)

    estimator_exp_class2 = ast.ExpExpr(
        ast.BinNumExpr(
            ast.NumVal(0.5),
            ast.IfExpr(
                ast.CompExpr(
                    ast.FeatureRef(2),
                    ast.NumVal(2.45000005),
                    ast.CompOpType.GTE),
                ast.NumVal(0.103241883),
                ast.NumVal(-0.215121984)),
            ast.BinNumOpType.ADD),
        to_reuse=True)

    estimator_exp_class3 = ast.ExpExpr(
        ast.BinNumExpr(
            ast.NumVal(0.5),
            ast.IfExpr(
                ast.CompExpr(
                    ast.FeatureRef(3),
                    ast.NumVal(1.6500001),
                    ast.CompOpType.GTE),
                ast.NumVal(0.402985066),
                ast.NumVal(-0.193333372)),
            ast.BinNumOpType.ADD),
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
    utils.get_regression_model_trainer()(estimator)

    with utils.tmp_dir() as tmp_dirpath:
        filename = os.path.join(tmp_dirpath, "tmp.file")
        estimator.save_model(filename)
        estimator = xgboost.XGBRegressor(base_score=base_score)
        estimator.load_model(filename)

    assembler = assemblers.XGBoostModelAssemblerSelector(estimator)
    actual = assembler.assemble()

    expected = ast.BinNumExpr(
        ast.NumVal(base_score),
        ast.BinNumExpr(
            ast.IfExpr(
                ast.CompExpr(
                    ast.FeatureRef(12),
                    ast.NumVal(9.72500038),
                    ast.CompOpType.GTE),
                ast.NumVal(4.98425627),
                ast.NumVal(8.75091362)),
            ast.IfExpr(
                ast.CompExpr(
                    ast.FeatureRef(5),
                    ast.NumVal(6.94099998),
                    ast.CompOpType.GTE),
                ast.NumVal(8.34557438),
                ast.NumVal(3.9141891)),
            ast.BinNumOpType.ADD),
        ast.BinNumOpType.ADD)

    assert utils.cmp_exprs(actual, expected)


def test_linear_model():
    # Default updater ("shotgun") is nondeterministic
    estimator = xgboost.XGBRegressor(n_estimators=2, random_state=1,
                                     updater="coord_descent",
                                     feature_selector="shuffle",
                                     booster="gblinear")
    utils.get_regression_model_trainer()(estimator)

    assembler = assemblers.XGBoostModelAssemblerSelector(estimator)
    actual = assembler.assemble()

    feature_weight_mul = [
        ast.BinNumExpr(
            ast.FeatureRef(0),
            ast.NumVal(-0.151436),
            ast.BinNumOpType.MUL),
        ast.BinNumExpr(
            ast.FeatureRef(1),
            ast.NumVal(0.084474),
            ast.BinNumOpType.MUL),
        ast.BinNumExpr(
            ast.FeatureRef(2),
            ast.NumVal(-0.10035),
            ast.BinNumOpType.MUL),
        ast.BinNumExpr(
            ast.FeatureRef(3),
            ast.NumVal(4.71537),
            ast.BinNumOpType.MUL),
        ast.BinNumExpr(
            ast.FeatureRef(4),
            ast.NumVal(1.39071),
            ast.BinNumOpType.MUL),
        ast.BinNumExpr(
            ast.FeatureRef(5),
            ast.NumVal(0.330592),
            ast.BinNumOpType.MUL),
        ast.BinNumExpr(
            ast.FeatureRef(6),
            ast.NumVal(0.0610453),
            ast.BinNumOpType.MUL),
        ast.BinNumExpr(
            ast.FeatureRef(7),
            ast.NumVal(0.476255),
            ast.BinNumOpType.MUL),
        ast.BinNumExpr(
            ast.FeatureRef(8),
            ast.NumVal(-0.0677851),
            ast.BinNumOpType.MUL),
        ast.BinNumExpr(
            ast.FeatureRef(9),
            ast.NumVal(-0.000543615),
            ast.BinNumOpType.MUL),
        ast.BinNumExpr(
            ast.FeatureRef(10),
            ast.NumVal(0.0717916),
            ast.BinNumOpType.MUL),
        ast.BinNumExpr(
            ast.FeatureRef(11),
            ast.NumVal(0.010832),
            ast.BinNumOpType.MUL),
        ast.BinNumExpr(
            ast.FeatureRef(12),
            ast.NumVal(-0.139375),
            ast.BinNumOpType.MUL),
    ]

    expected = ast.BinNumExpr(
        ast.NumVal(0.5),
        assemblers.utils.apply_op_to_expressions(
            ast.BinNumOpType.ADD,
            ast.NumVal(11.1287),
            *feature_weight_mul),
        ast.BinNumOpType.ADD)

    assert utils.cmp_exprs(actual, expected)


def test_regression_random_forest():
    base_score = 0.6
    estimator = xgboost.XGBRFRegressor(n_estimators=2, random_state=1,
                                       max_depth=1, base_score=base_score)
    utils.get_regression_model_trainer()(estimator)

    assembler = assemblers.XGBoostModelAssemblerSelector(estimator)
    actual = assembler.assemble()

    expected = ast.BinNumExpr(
        ast.NumVal(base_score),
        ast.BinNumExpr(
            ast.IfExpr(
                ast.CompExpr(
                    ast.FeatureRef(5),
                    ast.NumVal(6.94099998),
                    ast.CompOpType.GTE),
                ast.NumVal(18.1008453),
                ast.NumVal(9.60167599)),
            ast.IfExpr(
                ast.CompExpr(
                    ast.FeatureRef(5),
                    ast.NumVal(6.79699993),
                    ast.CompOpType.GTE),
                ast.NumVal(17.780262),
                ast.NumVal(9.51712894)),
            ast.BinNumOpType.ADD),
        ast.BinNumOpType.ADD)

    assert utils.cmp_exprs(actual, expected)
