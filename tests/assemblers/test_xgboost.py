import xgboost
import numpy as np
import os

from m2cgen import assemblers, ast
from tests import utils


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
                                ast.NumVal(16.795),
                                ast.CompOpType.GTE),
                            ast.NumVal(-0.5178947448730469),
                            ast.NumVal(0.4880000054836273)),
                        ast.IfExpr(
                            ast.CompExpr(
                                ast.FeatureRef(27),
                                ast.NumVal(0.142349988),
                                ast.CompOpType.GTE),
                            ast.NumVal(-0.4447747468948364),
                            ast.NumVal(0.39517202973365784)),
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

    num_expr = ast.BinNumExpr(
        ast.NumVal(0.5),
        ast.NumVal(-7.663454759665456e-09),
        ast.BinNumOpType.ADD)
    expected = ast.SoftmaxExpr([num_expr] * 3)

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
                    ast.NumVal(9.725000381469727),
                    ast.CompOpType.GTE),
                ast.NumVal(4.995625019073486),
                ast.NumVal(8.715502738952637)),
            ast.IfExpr(
                ast.CompExpr(
                    ast.FeatureRef(5),
                    ast.NumVal(6.941),
                    ast.CompOpType.GTE),
                ast.NumVal(8.309040069580078),
                ast.NumVal(3.930694580078125)),
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
                ast.NumVal(4.995625019073486),
                ast.NumVal(8.715502738952637)),
            ast.IfExpr(
                ast.CompExpr(
                    ast.FeatureRef(5),
                    ast.NumVal(6.94099998),
                    ast.CompOpType.GTE),
                ast.NumVal(8.309040069580078),
                ast.NumVal(3.930694580078125)),
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

    estimator_class1 = ast.BinNumExpr(
        ast.NumVal(0.5),
        ast.IfExpr(
            ast.CompExpr(
                ast.FeatureRef(2),
                ast.NumVal(2.450000047683716),
                ast.CompOpType.GTE),
            ast.NumVal(-0.21995015442371368),
            ast.NumVal(0.43024390935897827)),
        ast.BinNumOpType.ADD)

    estimator_class2 = ast.BinNumExpr(
        ast.NumVal(0.5),
        ast.IfExpr(
            ast.CompExpr(
                ast.FeatureRef(2),
                ast.NumVal(2.450000047683716),
                ast.CompOpType.GTE),
            ast.NumVal(0.10324188321828842),
            ast.NumVal(-0.21512198448181152)),
        ast.BinNumOpType.ADD)

    estimator_class3 = ast.BinNumExpr(
        ast.NumVal(0.5),
        ast.IfExpr(
            ast.CompExpr(
                ast.FeatureRef(3),
                ast.NumVal(1.6500000953674316),
                ast.CompOpType.GTE),
            ast.NumVal(0.4029850661754608),
            ast.NumVal(-0.19333337247371674)),
        ast.BinNumOpType.ADD)

    expected = ast.SoftmaxExpr([
        estimator_class1,
        estimator_class2,
        estimator_class3])

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
                ast.NumVal(4.995625019073486),
                ast.NumVal(8.715502738952637)),
            ast.IfExpr(
                ast.CompExpr(
                    ast.FeatureRef(5),
                    ast.NumVal(6.94099998),
                    ast.CompOpType.GTE),
                ast.NumVal(8.309040069580078),
                ast.NumVal(3.930694580078125)),
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
            ast.NumVal(-0.154567),
            ast.BinNumOpType.MUL),
        ast.BinNumExpr(
            ast.FeatureRef(1),
            ast.NumVal(0.0815865),
            ast.BinNumOpType.MUL),
        ast.BinNumExpr(
            ast.FeatureRef(2),
            ast.NumVal(-0.0979713),
            ast.BinNumOpType.MUL),
        ast.BinNumExpr(
            ast.FeatureRef(3),
            ast.NumVal(4.80472),
            ast.BinNumOpType.MUL),
        ast.BinNumExpr(
            ast.FeatureRef(4),
            ast.NumVal(1.35478),
            ast.BinNumOpType.MUL),
        ast.BinNumExpr(
            ast.FeatureRef(5),
            ast.NumVal(0.327222),
            ast.BinNumOpType.MUL),
        ast.BinNumExpr(
            ast.FeatureRef(6),
            ast.NumVal(0.0610654),
            ast.BinNumOpType.MUL),
        ast.BinNumExpr(
            ast.FeatureRef(7),
            ast.NumVal(0.46989),
            ast.BinNumOpType.MUL),
        ast.BinNumExpr(
            ast.FeatureRef(8),
            ast.NumVal(-0.0674318),
            ast.BinNumOpType.MUL),
        ast.BinNumExpr(
            ast.FeatureRef(9),
            ast.NumVal(-0.000506212),
            ast.BinNumOpType.MUL),
        ast.BinNumExpr(
            ast.FeatureRef(10),
            ast.NumVal(0.0732867),
            ast.BinNumOpType.MUL),
        ast.BinNumExpr(
            ast.FeatureRef(11),
            ast.NumVal(0.0108842),
            ast.BinNumOpType.MUL),
        ast.BinNumExpr(
            ast.FeatureRef(12),
            ast.NumVal(-0.140096),
            ast.BinNumOpType.MUL),
    ]

    expected = ast.BinNumExpr(
        ast.NumVal(0.5),
        assemblers.utils.apply_op_to_expressions(
            ast.BinNumOpType.ADD,
            ast.NumVal(11.138),
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
                ast.NumVal(18.38124656677246),
                ast.NumVal(9.772658348083496)),
            ast.IfExpr(
                ast.CompExpr(
                    ast.FeatureRef(12),
                    ast.NumVal(9.539999961853027),
                    ast.CompOpType.GTE),
                ast.NumVal(8.342499732971191),
                ast.NumVal(15.027499198913574)),
            ast.BinNumOpType.ADD),
        ast.BinNumOpType.ADD)

    assert utils.cmp_exprs(actual, expected)
