import pytest
import numpy as np
from sklearn import svm
from m2cgen import assemblers, ast
from tests import utils


def test_rbf_kernel():
    estimator = svm.SVC(kernel="rbf", random_state=1, gamma=2.0)

    estimator.fit([[1], [2]], [1, 2])

    assembler = assemblers.SVMModelAssembler(estimator)
    actual = assembler.assemble()

    kernels = [_rbf_kernel_ast(estimator, 1.), _rbf_kernel_ast(estimator, 2.)]
    expected = _create_expected_single_output_ast(estimator, kernels)

    assert utils.cmp_exprs(actual, expected)


def test_linear_kernel():
    estimator = svm.SVC(kernel="linear", random_state=1)

    estimator.fit([[1], [2]], [1, 2])

    assembler = assemblers.SVMModelAssembler(estimator)
    actual = assembler.assemble()

    def kernel_ast(sup_vec_value):
        return ast.SubroutineExpr(
            ast.BinNumExpr(
                ast.NumVal(sup_vec_value),
                ast.FeatureRef(0),
                ast.BinNumOpType.MUL))

    expected = _create_expected_single_output_ast(
        estimator, [kernel_ast(1.0), kernel_ast(2.0)])

    assert utils.cmp_exprs(actual, expected)


def test_sigmoid_kernel():
    estimator = svm.SVC(kernel="sigmoid", random_state=1, gamma=2.0)

    estimator.fit([[1], [2]], [1, 2])

    assembler = assemblers.SVMModelAssembler(estimator)
    actual = assembler.assemble()

    def kernel_ast(sup_vec_value):
        return ast.SubroutineExpr(
            ast.TanhExpr(
                ast.BinNumExpr(
                    ast.BinNumExpr(
                        ast.NumVal(estimator.gamma),
                        ast.BinNumExpr(
                            ast.NumVal(sup_vec_value),
                            ast.FeatureRef(0),
                            ast.BinNumOpType.MUL),
                        ast.BinNumOpType.MUL),
                    ast.NumVal(0.0),
                    ast.BinNumOpType.ADD)))

    expected = _create_expected_single_output_ast(
        estimator, [kernel_ast(1.0), kernel_ast(2.0)])

    assert utils.cmp_exprs(actual, expected)


def test_poly_kernel():
    estimator = svm.SVC(kernel="poly", random_state=1, gamma=2.0, degree=2)

    estimator.fit([[1], [2]], [1, 2])

    assembler = assemblers.SVMModelAssembler(estimator)
    actual = assembler.assemble()

    def kernel_ast(sup_vec_value):
        return ast.SubroutineExpr(
            ast.PowExpr(
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
                ast.NumVal(estimator.degree)))

    expected = _create_expected_single_output_ast(
        estimator, [kernel_ast(1.0), kernel_ast(2.0)])

    assert utils.cmp_exprs(actual, expected)


@pytest.mark.xfail(raises=ValueError, strict=True)
def test_unknown_kernel():
    estimator = svm.SVC(kernel=lambda x, y: np.transpose(x) * y)

    estimator.fit([[1], [2]], [1, 2])

    assembler = assemblers.SVMModelAssembler(estimator)
    assembler.assemble()


def test_multi_class_rbf_kernel():
    estimator = svm.SVC(kernel="rbf", random_state=1, gamma=2.0)

    estimator.fit([[1], [2], [3]], [1, 2, 3])

    assembler = assemblers.SVMModelAssembler(estimator)
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

    # expected = _create_expected_single_output_ast(
    #     estimator, [kernel_ast(1.0), kernel_ast(2.0), kernel_ast(3.0)])

    assert utils.cmp_exprs(actual, expected)


def _create_expected_single_output_ast(svm_model, kernels_ast):
    return ast.BinNumExpr(
        ast.BinNumExpr(
            ast.NumVal(svm_model.intercept_[0]),
            ast.BinNumExpr(
                kernels_ast[0],
                ast.NumVal(svm_model.dual_coef_[0][0]),
                ast.BinNumOpType.MUL),
            ast.BinNumOpType.ADD),
        ast.BinNumExpr(
            kernels_ast[1],
            ast.NumVal(svm_model.dual_coef_[0][1]),
            ast.BinNumOpType.MUL),
        ast.BinNumOpType.ADD)


def _rbf_kernel_ast(estimator, sup_vec_value, to_reuse=False):
    negative_gamma_ast = ast.BinNumExpr(
        ast.NumVal(0),
        ast.NumVal(estimator.gamma),
        ast.BinNumOpType.SUB,
        to_reuse=True)

    return ast.SubroutineExpr(
        ast.ExpExpr(
            ast.BinNumExpr(
                negative_gamma_ast,
                ast.PowExpr(
                    ast.BinNumExpr(
                        ast.NumVal(sup_vec_value),
                        ast.FeatureRef(0),
                        ast.BinNumOpType.SUB),
                    ast.NumVal(2)),
                ast.BinNumOpType.MUL)),
        to_reuse=to_reuse)
