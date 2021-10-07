from lightning.classification import AdaGradClassifier
from lightning.regression import AdaGradRegressor

from m2cgen import assemblers, ast

from tests import utils


def test_regression():
    estimator = AdaGradRegressor(random_state=1)
    utils.get_regression_model_trainer()(estimator)

    assembler = assemblers.SklearnLinearModelAssembler(estimator)
    actual = assembler.assemble()

    feature_weight_mul = [
        ast.BinNumExpr(
            ast.FeatureRef(0),
            ast.NumVal(-0.08558826944690746),
            ast.BinNumOpType.MUL),
        ast.BinNumExpr(
            ast.FeatureRef(1),
            ast.NumVal(0.0803724696787377),
            ast.BinNumOpType.MUL),
        ast.BinNumExpr(
            ast.FeatureRef(2),
            ast.NumVal(-0.03516743076774846),
            ast.BinNumOpType.MUL),
        ast.BinNumExpr(
            ast.FeatureRef(3),
            ast.NumVal(0.26469178947134087),
            ast.BinNumOpType.MUL),
        ast.BinNumExpr(
            ast.FeatureRef(4),
            ast.NumVal(0.15651985221012488),
            ast.BinNumOpType.MUL),
        ast.BinNumExpr(
            ast.FeatureRef(5),
            ast.NumVal(1.5186399078028587),
            ast.BinNumOpType.MUL),
        ast.BinNumExpr(
            ast.FeatureRef(6),
            ast.NumVal(0.10089874009193693),
            ast.BinNumOpType.MUL),
        ast.BinNumExpr(
            ast.FeatureRef(7),
            ast.NumVal(-0.011426237067026246),
            ast.BinNumOpType.MUL),
        ast.BinNumExpr(
            ast.FeatureRef(8),
            ast.NumVal(0.0861987777487293),
            ast.BinNumOpType.MUL),
        ast.BinNumExpr(
            ast.FeatureRef(9),
            ast.NumVal(-0.0057791506839322574),
            ast.BinNumOpType.MUL),
        ast.BinNumExpr(
            ast.FeatureRef(10),
            ast.NumVal(0.3357752757550913),
            ast.BinNumOpType.MUL),
        ast.BinNumExpr(
            ast.FeatureRef(11),
            ast.NumVal(0.020189965076849486),
            ast.BinNumOpType.MUL),
        ast.BinNumExpr(
            ast.FeatureRef(12),
            ast.NumVal(-0.7390647599317609),
            ast.BinNumOpType.MUL),
    ]

    expected = assemblers.utils.apply_op_to_expressions(
        ast.BinNumOpType.ADD,
        ast.NumVal(0.0),
        *feature_weight_mul)

    assert utils.cmp_exprs(actual, expected)


def test_binary_class():
    estimator = AdaGradClassifier(random_state=1)
    utils.get_binary_classification_model_trainer()(estimator)

    assembler = assemblers.SklearnLinearModelAssembler(estimator)
    actual = assembler.assemble()

    feature_weight_mul = [
        ast.BinNumExpr(
            ast.FeatureRef(0),
            ast.NumVal(0.16218889967390476),
            ast.BinNumOpType.MUL),
        ast.BinNumExpr(
            ast.FeatureRef(1),
            ast.NumVal(0.10012761963766906),
            ast.BinNumOpType.MUL),
        ast.BinNumExpr(
            ast.FeatureRef(2),
            ast.NumVal(0.6289276652681673),
            ast.BinNumOpType.MUL),
        ast.BinNumExpr(
            ast.FeatureRef(3),
            ast.NumVal(0.17618420156072845),
            ast.BinNumOpType.MUL),
        ast.BinNumExpr(
            ast.FeatureRef(4),
            ast.NumVal(0.0010492096607182045),
            ast.BinNumOpType.MUL),
        ast.BinNumExpr(
            ast.FeatureRef(5),
            ast.NumVal(-0.0029135563693806913),
            ast.BinNumOpType.MUL),
        ast.BinNumExpr(
            ast.FeatureRef(6),
            ast.NumVal(-0.005923882409142498),
            ast.BinNumOpType.MUL),
        ast.BinNumExpr(
            ast.FeatureRef(7),
            ast.NumVal(-0.0023293599172479755),
            ast.BinNumOpType.MUL),
        ast.BinNumExpr(
            ast.FeatureRef(8),
            ast.NumVal(0.0020808828960210517),
            ast.BinNumOpType.MUL),
        ast.BinNumExpr(
            ast.FeatureRef(9),
            ast.NumVal(0.0009846430705550103),
            ast.BinNumOpType.MUL),
        ast.BinNumExpr(
            ast.FeatureRef(10),
            ast.NumVal(0.0010399810925427265),
            ast.BinNumOpType.MUL),
        ast.BinNumExpr(
            ast.FeatureRef(11),
            ast.NumVal(0.011203056917272093),
            ast.BinNumOpType.MUL),
        ast.BinNumExpr(
            ast.FeatureRef(12),
            ast.NumVal(-0.007271351370867731),
            ast.BinNumOpType.MUL),
        ast.BinNumExpr(
            ast.FeatureRef(13),
            ast.NumVal(-0.26333437096804224),
            ast.BinNumOpType.MUL),
        ast.BinNumExpr(
            ast.FeatureRef(14),
            ast.NumVal(1.8533543368532444e-05),
            ast.BinNumOpType.MUL),
        ast.BinNumExpr(
            ast.FeatureRef(15),
            ast.NumVal(-0.0008266341686278445),
            ast.BinNumOpType.MUL),
        ast.BinNumExpr(
            ast.FeatureRef(16),
            ast.NumVal(-0.0011090316301215724),
            ast.BinNumOpType.MUL),
        ast.BinNumExpr(
            ast.FeatureRef(17),
            ast.NumVal(-0.0001910857095336291),
            ast.BinNumOpType.MUL),
        ast.BinNumExpr(
            ast.FeatureRef(18),
            ast.NumVal(0.00010735116208006556),
            ast.BinNumOpType.MUL),
        ast.BinNumExpr(
            ast.FeatureRef(19),
            ast.NumVal(-4.076097659514017e-05),
            ast.BinNumOpType.MUL),
        ast.BinNumExpr(
            ast.FeatureRef(20),
            ast.NumVal(0.15300712110146406),
            ast.BinNumOpType.MUL),
        ast.BinNumExpr(
            ast.FeatureRef(21),
            ast.NumVal(0.06316277258339074),
            ast.BinNumOpType.MUL),
        ast.BinNumExpr(
            ast.FeatureRef(22),
            ast.NumVal(0.495291178977687),
            ast.BinNumOpType.MUL),
        ast.BinNumExpr(
            ast.FeatureRef(23),
            ast.NumVal(-0.29589136204657845),
            ast.BinNumOpType.MUL),
        ast.BinNumExpr(
            ast.FeatureRef(24),
            ast.NumVal(0.000771932729567487),
            ast.BinNumOpType.MUL),
        ast.BinNumExpr(
            ast.FeatureRef(25),
            ast.NumVal(-0.011877978242492428),
            ast.BinNumOpType.MUL),
        ast.BinNumExpr(
            ast.FeatureRef(26),
            ast.NumVal(-0.01678004536869617),
            ast.BinNumOpType.MUL),
        ast.BinNumExpr(
            ast.FeatureRef(27),
            ast.NumVal(-0.004070431062579625),
            ast.BinNumOpType.MUL),
        ast.BinNumExpr(
            ast.FeatureRef(28),
            ast.NumVal(0.001158641497209262),
            ast.BinNumOpType.MUL),
        ast.BinNumExpr(
            ast.FeatureRef(29),
            ast.NumVal(0.00010737287732588742),
            ast.BinNumOpType.MUL),
    ]

    expected = assemblers.utils.apply_op_to_expressions(
        ast.BinNumOpType.ADD,
        ast.NumVal(0.0),
        *feature_weight_mul)

    assert utils.cmp_exprs(actual, expected)


def test_multi_class():
    estimator = AdaGradClassifier(random_state=1)
    utils.get_classification_model_trainer()(estimator)

    assembler = assemblers.SklearnLinearModelAssembler(estimator)
    actual = assembler.assemble()

    expected = ast.VectorVal([
        ast.BinNumExpr(
            ast.BinNumExpr(
                ast.BinNumExpr(
                    ast.BinNumExpr(
                        ast.NumVal(0.0),
                        ast.BinNumExpr(
                            ast.FeatureRef(0),
                            ast.NumVal(0.09686334892116512),
                            ast.BinNumOpType.MUL),
                        ast.BinNumOpType.ADD),
                    ast.BinNumExpr(
                        ast.FeatureRef(1),
                        ast.NumVal(0.32572202133211947),
                        ast.BinNumOpType.MUL),
                    ast.BinNumOpType.ADD),
                ast.BinNumExpr(
                    ast.FeatureRef(2),
                    ast.NumVal(-0.48444233646554424),
                    ast.BinNumOpType.MUL),
                ast.BinNumOpType.ADD),
            ast.BinNumExpr(
                ast.FeatureRef(3),
                ast.NumVal(-0.219719145605816),
                ast.BinNumOpType.MUL),
            ast.BinNumOpType.ADD),
        ast.BinNumExpr(
            ast.BinNumExpr(
                ast.BinNumExpr(
                    ast.BinNumExpr(
                        ast.NumVal(0.0),
                        ast.BinNumExpr(
                            ast.FeatureRef(0),
                            ast.NumVal(-0.1089136473832088),
                            ast.BinNumOpType.MUL),
                        ast.BinNumOpType.ADD),
                    ast.BinNumExpr(
                        ast.FeatureRef(1),
                        ast.NumVal(-0.16956003333433572),
                        ast.BinNumOpType.MUL),
                    ast.BinNumOpType.ADD),
                ast.BinNumExpr(
                    ast.FeatureRef(2),
                    ast.NumVal(0.0365531256007199),
                    ast.BinNumOpType.MUL),
                ast.BinNumOpType.ADD),
            ast.BinNumExpr(
                ast.FeatureRef(3),
                ast.NumVal(-0.01016100116780896),
                ast.BinNumOpType.MUL),
            ast.BinNumOpType.ADD),
        ast.BinNumExpr(
            ast.BinNumExpr(
                ast.BinNumExpr(
                    ast.BinNumExpr(
                        ast.NumVal(0.0),
                        ast.BinNumExpr(
                            ast.FeatureRef(0),
                            ast.NumVal(-0.16690339219780817),
                            ast.BinNumOpType.MUL),
                        ast.BinNumOpType.ADD),
                    ast.BinNumExpr(
                        ast.FeatureRef(1),
                        ast.NumVal(-0.19466284646233858),
                        ast.BinNumOpType.MUL),
                    ast.BinNumOpType.ADD),
                ast.BinNumExpr(
                    ast.FeatureRef(2),
                    ast.NumVal(0.2953585236360389),
                    ast.BinNumOpType.MUL),
                ast.BinNumOpType.ADD),
            ast.BinNumExpr(
                ast.FeatureRef(3),
                ast.NumVal(0.21288203082531384),
                ast.BinNumOpType.MUL),
            ast.BinNumOpType.ADD)])

    assert utils.cmp_exprs(actual, expected)
