from m2cgen import ast


def _create_expected_svm_single_output_ast(coef, intercept, kernels_ast):
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


def _svm_rbf_kernel_ast(estimator, sup_vec_value, to_reuse=False):
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


def _svm_cosine_kernel_ast(sup_vec_value):
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
