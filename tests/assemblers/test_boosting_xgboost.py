import numpy as np
import xgboost as xgb

from m2cgen import ast
from m2cgen.assemblers import XGBoostModelAssemblerSelector
from m2cgen.assemblers.utils import apply_op_to_expressions

from tests import utils


def test_binary_classification():
    estimator = xgb.XGBClassifier(n_estimators=2, random_state=1, max_depth=1)
    utils.get_binary_classification_model_trainer()(estimator)

    assembler = XGBoostModelAssemblerSelector(estimator)
    actual = assembler.assemble()

    sigmoid = ast.SigmoidExpr(
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
        to_reuse=True)

    expected = ast.VectorVal([
        ast.BinNumExpr(ast.NumVal(1), sigmoid, ast.BinNumOpType.SUB),
        sigmoid])

    assert utils.cmp_exprs(actual, expected)


def test_multi_class():
    estimator = xgb.XGBClassifier(n_estimators=1, random_state=1, max_depth=1)
    estimator.fit(np.array([[1], [2], [3]]), np.array([0, 1, 2]))

    assembler = XGBoostModelAssemblerSelector(estimator)
    actual = assembler.assemble()

    num_expr = ast.BinNumExpr(
        ast.NumVal(0.5),
        ast.NumVal(-7.663454759665456e-09),
        ast.BinNumOpType.ADD)
    expected = ast.SoftmaxExpr([num_expr] * 3)

    assert utils.cmp_exprs(actual, expected)


def test_regression_multioutput():
    base_score = 0.6
    estimator = xgb.XGBRegressor(n_estimators=1, random_state=1, max_depth=1, base_score=base_score)
    utils.get_multioutput_regression_model_trainer()(estimator)

    assembler = XGBoostModelAssemblerSelector(estimator)
    actual = assembler.assemble()

    expected = ast.VectorVal([
        ast.BinNumExpr(ast.NumVal(base_score),
                       ast.IfExpr(
                           ast.CompExpr(
                               ast.FeatureRef(4),
                               ast.NumVal(0.09817435592412949),
                               ast.CompOpType.GTE),
                           ast.NumVal(22.866134643554688),
                           ast.NumVal(-10.487930297851562)),
                       ast.BinNumOpType.ADD),
        ast.BinNumExpr(ast.NumVal(base_score),
                       ast.IfExpr(
                           ast.CompExpr(
                               ast.FeatureRef(1),
                               ast.NumVal(0.031133096665143967),
                               ast.CompOpType.GTE),
                           ast.NumVal(13.26490592956543),
                           ast.NumVal(-11.912125587463379)),
                       ast.BinNumOpType.ADD),
        ast.BinNumExpr(ast.NumVal(base_score),
                       ast.IfExpr(
                           ast.CompExpr(
                               ast.FeatureRef(4),
                               ast.NumVal(-0.42966189980506897),
                               ast.CompOpType.GTE),
                           ast.NumVal(17.365192413330078),
                           ast.NumVal(-24.488313674926758)),
                       ast.BinNumOpType.ADD)])

    assert utils.cmp_exprs(actual, expected)


def test_regression():
    base_score = 0.6
    estimator = xgb.XGBRegressor(n_estimators=2, random_state=1, max_depth=1, base_score=base_score)
    utils.get_regression_model_trainer()(estimator)

    assembler = XGBoostModelAssemblerSelector(estimator)
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
    estimator = xgb.XGBRegressor(n_estimators=3, random_state=1, max_depth=1, base_score=base_score)

    utils.get_regression_model_trainer()(estimator)

    estimator.get_booster().best_ntree_limit = 2

    assembler = XGBoostModelAssemblerSelector(estimator)
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
    estimator = xgb.XGBClassifier(n_estimators=100, random_state=1, max_depth=1, base_score=base_score)

    utils.get_classification_model_trainer()(estimator)

    estimator.get_booster().best_ntree_limit = 1

    assembler = XGBoostModelAssemblerSelector(estimator)
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
    estimator = xgb.XGBRegressor(n_estimators=2, random_state=1, max_depth=1, base_score=base_score)
    utils.get_regression_model_trainer()(estimator)

    with utils.tmp_dir() as tmp_dirpath:
        filename = tmp_dirpath / "tmp.file"
        estimator.save_model(filename)
        estimator = xgb.XGBRegressor(base_score=base_score)
        estimator.load_model(filename)

    assembler = XGBoostModelAssemblerSelector(estimator)
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
    estimator = xgb.XGBRegressor(n_estimators=2, random_state=1, updater="coord_descent",
                                 feature_selector="shuffle", booster="gblinear")
    utils.get_regression_model_trainer()(estimator)

    assembler = XGBoostModelAssemblerSelector(estimator)
    actual = assembler.assemble()

    feature_weight_mul = [
        ast.BinNumExpr(
            ast.FeatureRef(0),
            ast.NumVal(-0.168701),
            ast.BinNumOpType.MUL),
        ast.BinNumExpr(
            ast.FeatureRef(1),
            ast.NumVal(0.0759076),
            ast.BinNumOpType.MUL),
        ast.BinNumExpr(
            ast.FeatureRef(2),
            ast.NumVal(-0.0433617),
            ast.BinNumOpType.MUL),
        ast.BinNumExpr(
            ast.FeatureRef(3),
            ast.NumVal(5.57671),
            ast.BinNumOpType.MUL),
        ast.BinNumExpr(
            ast.FeatureRef(4),
            ast.NumVal(1.48913),
            ast.BinNumOpType.MUL),
        ast.BinNumExpr(
            ast.FeatureRef(5),
            ast.NumVal(0.245112),
            ast.BinNumOpType.MUL),
        ast.BinNumExpr(
            ast.FeatureRef(6),
            ast.NumVal(0.00765347),
            ast.BinNumOpType.MUL),
        ast.BinNumExpr(
            ast.FeatureRef(7),
            ast.NumVal(0.366748),
            ast.BinNumOpType.MUL),
        ast.BinNumExpr(
            ast.FeatureRef(8),
            ast.NumVal(-0.037578),
            ast.BinNumOpType.MUL),
        ast.BinNumExpr(
            ast.FeatureRef(9),
            ast.NumVal(-0.00171953),
            ast.BinNumOpType.MUL),
        ast.BinNumExpr(
            ast.FeatureRef(10),
            ast.NumVal(0.275619),
            ast.BinNumOpType.MUL),
        ast.BinNumExpr(
            ast.FeatureRef(11),
            ast.NumVal(0.00959933),
            ast.BinNumOpType.MUL),
        ast.BinNumExpr(
            ast.FeatureRef(12),
            ast.NumVal(-0.13406),
            ast.BinNumOpType.MUL),
    ]

    expected = ast.BinNumExpr(
        ast.NumVal(0.5),
        apply_op_to_expressions(
            ast.BinNumOpType.ADD,
            ast.NumVal(11.5264),
            *feature_weight_mul),
        ast.BinNumOpType.ADD)

    assert utils.cmp_exprs(actual, expected)


def test_regression_random_forest():
    base_score = 0.6
    estimator = xgb.XGBRFRegressor(n_estimators=2, random_state=1, max_depth=1, base_score=base_score)
    utils.get_regression_model_trainer()(estimator)

    assembler = XGBoostModelAssemblerSelector(estimator)
    actual = assembler.assemble()

    expected = ast.BinNumExpr(
        ast.NumVal(base_score),
        ast.BinNumExpr(
            ast.IfExpr(
                ast.CompExpr(
                    ast.FeatureRef(5),
                    ast.NumVal(6.940999984741211),
                    ast.CompOpType.GTE),
                ast.NumVal(18.381247),
                ast.NumVal(9.772658348083496)),
            ast.IfExpr(
                ast.CompExpr(
                    ast.FeatureRef(5),
                    ast.NumVal(6.971499919891357),
                    ast.CompOpType.GTE),
                ast.NumVal(18.84648895263672),
                ast.NumVal(9.71530532836914)),
            ast.BinNumOpType.ADD),
        ast.BinNumOpType.ADD)

    assert utils.cmp_exprs(actual, expected)
