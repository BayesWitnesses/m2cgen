import numpy as np
import pytest
from sklearn.svm import SVC

from m2cgen import ast
from m2cgen.assemblers import SklearnSVMModelAssembler

from tests.assemblers import utils
from tests.utils import cmp_exprs


def test_rbf_kernel():
    estimator = SVC(kernel="rbf", random_state=1, gamma=2.0)

    estimator.fit([[1], [2]], [1, 2])

    assembler = SklearnSVMModelAssembler(estimator)
    actual = assembler.assemble()

    kernels = [utils._svm_rbf_kernel_ast(estimator, 1.), utils._svm_rbf_kernel_ast(estimator, 2.)]
    expected = utils._create_expected_svm_single_output_ast(
        estimator.dual_coef_, estimator.intercept_, kernels)

    assert cmp_exprs(actual, expected)


def test_linear_kernel():
    estimator = SVC(kernel="linear", random_state=1)

    estimator.fit([[1], [2]], [1, 2])

    assembler = SklearnSVMModelAssembler(estimator)
    actual = assembler.assemble()

    def kernel_ast(sup_vec_value):
        return ast.BinNumExpr(
            ast.NumVal(sup_vec_value),
            ast.FeatureRef(0),
            ast.BinNumOpType.MUL)

    expected = utils._create_expected_svm_single_output_ast(
        estimator.dual_coef_, estimator.intercept_,
        [kernel_ast(1.0), kernel_ast(2.0)])

    assert cmp_exprs(actual, expected)


def test_sigmoid_kernel():
    estimator = SVC(kernel="sigmoid", random_state=1, gamma=2.0)

    estimator.fit([[1], [2]], [1, 2])

    assembler = SklearnSVMModelAssembler(estimator)
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

    expected = utils._create_expected_svm_single_output_ast(
        estimator.dual_coef_, estimator.intercept_,
        [kernel_ast(1.0), kernel_ast(2.0)])

    assert cmp_exprs(actual, expected)


def test_poly_kernel():
    estimator = SVC(kernel="poly", random_state=1, gamma=2.0, degree=2)

    estimator.fit([[1], [2]], [1, 2])

    assembler = SklearnSVMModelAssembler(estimator)
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

    expected = utils._create_expected_svm_single_output_ast(
        estimator.dual_coef_, estimator.intercept_,
        [kernel_ast(1.0), kernel_ast(2.0)])

    assert cmp_exprs(actual, expected)


def test_unknown_kernel():
    estimator = SVC(kernel=lambda x, y: np.transpose(x) * y)
    estimator.fit([[1], [2]], [1, 2])

    with pytest.raises(ValueError,
                       match="Unsupported kernel type '<function test_unknown_kernel.<locals>.<lambda> at .*"):
        SklearnSVMModelAssembler(estimator)


def test_multi_class_rbf_kernel():
    estimator = SVC(kernel="rbf", random_state=1, gamma=2.0)

    estimator.fit([[1], [2], [3]], [1, 2, 3])

    assembler = SklearnSVMModelAssembler(estimator)
    actual = assembler.assemble()

    kernels = [
        utils._svm_rbf_kernel_ast(estimator, float(i), to_reuse=True)
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

    assert cmp_exprs(actual, expected)
