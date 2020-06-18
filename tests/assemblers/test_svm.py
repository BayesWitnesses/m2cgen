import pytest
import numpy as np
from sklearn import svm
from lightning.classification import KernelSVC
from m2cgen import assemblers, ast
from tests import utils


def test_rbf_kernel():
    estimator = svm.SVC(kernel="rbf", random_state=1, gamma=2.0)

    estimator.fit([[1], [2]], [1, 2])

    assembler = assemblers.SklearnSVMModelAssembler(estimator)
    actual = assembler.assemble()

    kernels = [_rbf_kernel_ast(estimator, 1.), _rbf_kernel_ast(estimator, 2.)]
    expected = _create_expected_single_output_ast(
        estimator.dual_coef_, estimator.intercept_, kernels)

    assert utils.cmp_exprs(actual, expected)


def test_linear_kernel():
    estimator = svm.SVC(kernel="linear", random_state=1)

    estimator.fit([[1], [2]], [1, 2])

    assembler = assemblers.SklearnSVMModelAssembler(estimator)
    actual = assembler.assemble()

    def kernel_ast(sup_vec_value):
        return ast.BinNumExpr(
            ast.NumVal(sup_vec_value),
            ast.FeatureRef(0),
            ast.BinNumOpType.MUL)

    expected = _create_expected_single_output_ast(
        estimator.dual_coef_, estimator.intercept_,
        [kernel_ast(1.0), kernel_ast(2.0)])

    assert utils.cmp_exprs(actual, expected)


def test_sigmoid_kernel():
    estimator = svm.SVC(kernel="sigmoid", random_state=1, gamma=2.0)

    estimator.fit([[1], [2]], [1, 2])

    assembler = assemblers.SklearnSVMModelAssembler(estimator)
    actual = assembler.assemble()

    def kernel_ast(sup_vec_value):
        return ast.TanhExpr(
            ast.BinNumExpr(
                ast.BinNumExpr(
                    ast.NumVal(estimator.gamma),
                    ast.BinNumExpr(
                        ast.NumVal(sup_vec_value),
                        ast.FeatureRef(0),
                        ast.BinNumOpType.MUL),
                    ast.BinNumOpType.MUL),
                ast.NumVal(0.0),
                ast.BinNumOpType.ADD))

    expected = _create_expected_single_output_ast(
        estimator.dual_coef_, estimator.intercept_,
        [kernel_ast(1.0), kernel_ast(2.0)])

    assert utils.cmp_exprs(actual, expected)


def test_poly_kernel():
    estimator = svm.SVC(kernel="poly", random_state=1, gamma=2.0, degree=2)

    estimator.fit([[1], [2]], [1, 2])

    assembler = assemblers.SklearnSVMModelAssembler(estimator)
    actual = assembler.assemble()

    def kernel_ast(sup_vec_value):
        return ast.PowExpr(
            ast.BinNumExpr(
                ast.BinNumExpr(
                    ast.NumVal(estimator.gamma),
                    ast.BinNumExpr(
                        ast.NumVal(sup_vec_value),
                        ast.FeatureRef(0),
                        ast.BinNumOpType.MUL),
                    ast.BinNumOpType.MUL),
                ast.NumVal(0.0),
                ast.BinNumOpType.ADD),
            ast.NumVal(estimator.degree))

    expected = _create_expected_single_output_ast(
        estimator.dual_coef_, estimator.intercept_,
        [kernel_ast(1.0), kernel_ast(2.0)])

    assert utils.cmp_exprs(actual, expected)


def test_cosine_kernel():
    estimator = KernelSVC(kernel="cosine", random_state=1, gamma=2.0)

    estimator.fit(np.array([[1], [2]]), [1, 2])

    assembler = assemblers.LightningSVMModelAssembler(estimator)
    actual = assembler.assemble()

    def kernel_ast(sup_vec_value):
        feature_norm = ast.SqrtExpr(
            ast.BinNumExpr(
                ast.FeatureRef(0),
                ast.FeatureRef(0),
                ast.BinNumOpType.MUL),
            to_reuse=True)
        return ast.BinNumExpr(
            ast.BinNumExpr(
                ast.NumVal(sup_vec_value),
                ast.FeatureRef(0),
                ast.BinNumOpType.MUL),
            ast.IfExpr(
                ast.CompExpr(
                    feature_norm,
                    ast.NumVal(0.0),
                    ast.CompOpType.EQ),
                ast.NumVal(1.0),
                feature_norm),
            ast.BinNumOpType.DIV)

    expected = _create_expected_single_output_ast(
        estimator.coef_, estimator.intercept_,
        [kernel_ast(1.0), kernel_ast(1.0)])

    assert utils.cmp_exprs(actual, expected)


@pytest.mark.xfail(raises=ValueError, strict=True)
def test_unknown_kernel():
    estimator = svm.SVC(kernel=lambda x, y: np.transpose(x) * y)

    estimator.fit([[1], [2]], [1, 2])

    assembler = assemblers.SklearnSVMModelAssembler(estimator)
    assembler.assemble()


def test_multi_class_rbf_kernel():
    estimator = svm.SVC(kernel="rbf", random_state=1, gamma=2.0)

    estimator.fit([[1], [2], [3]], [1, 2, 3])

    assembler = assemblers.SklearnSVMModelAssembler(estimator)
    actual = assembler.assemble()

    kernels = [
        _rbf_kernel_ast(estimator, float(i), to_reuse=True)
        for i in range(1, 4)
    ]

    expected = ast.VectorVal([
        ast.BinNumExpr(
            ast.BinNumExpr(
                ast.NumVal(0.0),
                ast.BinNumExpr(
                    kernels[1],
                    ast.NumVal(-1.0),
                    ast.BinNumOpType.MUL),
                ast.BinNumOpType.ADD),
            ast.BinNumExpr(
                kernels[0],
                ast.NumVal(1.0),
                ast.BinNumOpType.MUL),
            ast.BinNumOpType.ADD),
        ast.BinNumExpr(
            ast.BinNumExpr(
                ast.NumVal(0.0),
                ast.BinNumExpr(
                    kernels[2],
                    ast.NumVal(-1.0),
                    ast.BinNumOpType.MUL),
                ast.BinNumOpType.ADD),
            ast.BinNumExpr(
                kernels[0],
                ast.NumVal(1.0),
                ast.BinNumOpType.MUL),
            ast.BinNumOpType.ADD),
        ast.BinNumExpr(
            ast.BinNumExpr(
                ast.NumVal(0.0),
                ast.BinNumExpr(
                    kernels[2],
                    ast.NumVal(-1.0),
                    ast.BinNumOpType.MUL),
                ast.BinNumOpType.ADD),
            ast.BinNumExpr(
                kernels[1],
                ast.NumVal(1.0),
                ast.BinNumOpType.MUL),
            ast.BinNumOpType.ADD)])

    assert utils.cmp_exprs(actual, expected)


def test_lightning_multi_class_rbf_kernel():
    estimator = KernelSVC(kernel="rbf", random_state=1, gamma=2.0)

    estimator.fit(np.array([[1], [2], [3]]), np.array([1, 2, 3]))

    assembler = assemblers.LightningSVMModelAssembler(estimator)
    actual = assembler.assemble()

    kernels = [
        _rbf_kernel_ast(estimator, float(i))
        for i in range(1, 4)
    ]

    expected = ast.VectorVal([
        ast.BinNumExpr(
            ast.BinNumExpr(
                ast.BinNumExpr(
                    ast.NumVal(0.0),
                    ast.BinNumExpr(
                        kernels[0],
                        ast.NumVal(0.5342246289),
                        ast.BinNumOpType.MUL),
                    ast.BinNumOpType.ADD),
                ast.BinNumExpr(
                    kernels[1],
                    ast.NumVal(-0.5046204480),
                    ast.BinNumOpType.MUL),
                ast.BinNumOpType.ADD),
            ast.BinNumExpr(
                kernels[2],
                ast.NumVal(-0.4659431306),
                ast.BinNumOpType.MUL),
            ast.BinNumOpType.ADD),
        ast.BinNumExpr(
            ast.BinNumExpr(
                ast.BinNumExpr(
                    ast.NumVal(0.0),
                    ast.BinNumExpr(
                        kernels[0],
                        ast.NumVal(-0.5386765707),
                        ast.BinNumOpType.MUL),
                    ast.BinNumOpType.ADD),
                ast.BinNumExpr(
                    kernels[1],
                    ast.NumVal(0.5729019463),
                    ast.BinNumOpType.MUL),
                ast.BinNumOpType.ADD),
            ast.BinNumExpr(
                kernels[2],
                ast.NumVal(-0.5386765707),
                ast.BinNumOpType.MUL),
            ast.BinNumOpType.ADD),
        ast.BinNumExpr(
            ast.BinNumExpr(
                ast.BinNumExpr(
                    ast.NumVal(0.0),
                    ast.BinNumExpr(
                        kernels[0],
                        ast.NumVal(-0.4659431306),
                        ast.BinNumOpType.MUL),
                    ast.BinNumOpType.ADD),
                ast.BinNumExpr(
                    kernels[1],
                    ast.NumVal(-0.5046204480),
                    ast.BinNumOpType.MUL),
                ast.BinNumOpType.ADD),
            ast.BinNumExpr(
                kernels[2],
                ast.NumVal(0.5342246289),
                ast.BinNumOpType.MUL),
            ast.BinNumOpType.ADD)])

    assert utils.cmp_exprs(actual, expected)


def _create_expected_single_output_ast(coef, intercept, kernels_ast):
    return ast.BinNumExpr(
        ast.BinNumExpr(
            ast.NumVal(intercept[0]),
            ast.BinNumExpr(
                kernels_ast[0],
                ast.NumVal(coef[0][0]),
                ast.BinNumOpType.MUL),
            ast.BinNumOpType.ADD),
        ast.BinNumExpr(
            kernels_ast[1],
            ast.NumVal(coef[0][1]),
            ast.BinNumOpType.MUL),
        ast.BinNumOpType.ADD)


def _rbf_kernel_ast(estimator, sup_vec_value, to_reuse=False):
    return ast.ExpExpr(
        ast.BinNumExpr(
            ast.NumVal(-estimator.gamma),
            ast.PowExpr(
                ast.BinNumExpr(
                    ast.NumVal(sup_vec_value),
                    ast.FeatureRef(0),
                    ast.BinNumOpType.SUB),
                ast.NumVal(2)),
            ast.BinNumOpType.MUL),
        to_reuse=to_reuse)
