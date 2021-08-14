import numpy as np
from lightning.classification import KernelSVC

from m2cgen import ast
from m2cgen.assemblers import LightningSVMModelAssembler

from tests.assemblers import utils
from tests.utils import cmp_exprs


def test_cosine_kernel():
    estimator = KernelSVC(kernel="cosine", random_state=1, gamma=2.0)

    estimator.fit(np.array([[1], [2]]), [1, 2])

    assembler = LightningSVMModelAssembler(estimator)
    actual = assembler.assemble()

    expected = utils._create_expected_svm_single_output_ast(
        estimator.coef_, estimator.intercept_,
        [utils._svm_cosine_kernel_ast(1.0), utils._svm_cosine_kernel_ast(1.0)])

    assert cmp_exprs(actual, expected)


def test_norm_in_cosine_kernel():
    estimator = KernelSVC(kernel="cosine", random_state=1, gamma=2.0)

    estimator.fit(np.array([[0], [0]]), [1, 2])
    np.testing.assert_array_equal(estimator.support_vectors_, [[0], [0]])

    assembler = LightningSVMModelAssembler(estimator)
    actual = assembler.assemble()

    expected = utils._create_expected_svm_single_output_ast(
        estimator.coef_, estimator.intercept_,
        [utils._svm_cosine_kernel_ast(0.0), utils._svm_cosine_kernel_ast(0.0)])

    assert cmp_exprs(actual, expected)


def test_multi_class_rbf_kernel():
    estimator = KernelSVC(kernel="rbf", random_state=1, gamma=2.0)

    estimator.fit(np.array([[1], [2], [3]]), np.array([1, 2, 3]))

    assembler = LightningSVMModelAssembler(estimator)
    actual = assembler.assemble()

    kernels = [
        utils._svm_rbf_kernel_ast(estimator, float(i))
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

    assert cmp_exprs(actual, expected)
