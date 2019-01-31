from m2cgen import ast
from m2cgen import interpreters
from tests import utils


def test_if_expr():
    expr = ast.IfExpr(
        ast.CompExpr(ast.NumVal(1), ast.FeatureRef(0), ast.CompOpType.EQ),
        ast.NumVal(2),
        ast.NumVal(3))

    interpreter = interpreters.CInterpreter()

    expected_code = """
double score(double * input) {
    double var0;
    if ((1) == (input[0])) {
        var0 = 2;
    } else {
        var0 = 3;
    }
    return var0;
}"""
    utils.assert_code_equal(interpreter.interpret(expr), expected_code)


def test_bin_num_expr():
    expr = ast.BinNumExpr(
        ast.BinNumExpr(
            ast.FeatureRef(0), ast.NumVal(-2), ast.BinNumOpType.DIV),
        ast.NumVal(2),
        ast.BinNumOpType.MUL)

    interpreter = interpreters.CInterpreter()

    expected_code = """
double score(double * input) {
    return ((input[0]) / (-2)) * (2);
}"""
    utils.assert_code_equal(interpreter.interpret(expr), expected_code)


def test_dependable_condition():
    left = ast.BinNumExpr(
        ast.IfExpr(
            ast.CompExpr(ast.NumVal(1),
                         ast.NumVal(1),
                         ast.CompOpType.EQ),
            ast.NumVal(1),
            ast.NumVal(2)),
        ast.NumVal(2),
        ast.BinNumOpType.ADD)

    right = ast.BinNumExpr(ast.NumVal(1), ast.NumVal(2), ast.BinNumOpType.DIV)
    bool_test = ast.CompExpr(left, right, ast.CompOpType.GTE)

    expr = ast.IfExpr(bool_test, ast.NumVal(1), ast.FeatureRef(0))

    expected_code = """
double score(double * input) {
    double var0;
    double var1;
    if ((1) == (1)) {
        var1 = 1;
    } else {
        var1 = 2;
    }
    if (((var1) + (2)) >= ((1) / (2))) {
        var0 = 1;
    } else {
        var0 = input[0];
    }
    return var0;
}"""

    interpreter = interpreters.CInterpreter()
    utils.assert_code_equal(interpreter.interpret(expr), expected_code)


def test_nested_condition():
    left = ast.BinNumExpr(
        ast.IfExpr(
            ast.CompExpr(ast.NumVal(1),
                         ast.NumVal(1),
                         ast.CompOpType.EQ),
            ast.NumVal(1),
            ast.NumVal(2)),
        ast.NumVal(2),
        ast.BinNumOpType.ADD)

    bool_test = ast.CompExpr(ast.NumVal(1), left, ast.CompOpType.EQ)

    expr_nested = ast.IfExpr(bool_test, ast.FeatureRef(2), ast.NumVal(2))

    expr = ast.IfExpr(bool_test, expr_nested, ast.NumVal(2))

    expected_code = """
double score(double * input) {
    double var0;
    double var1;
    if ((1) == (1)) {
        var1 = 1;
    } else {
        var1 = 2;
    }
    if ((1) == ((var1) + (2))) {
        double var2;
        if ((1) == (1)) {
            var2 = 1;
        } else {
            var2 = 2;
        }
        if ((1) == ((var2) + (2))) {
            var0 = input[2];
        } else {
            var0 = 2;
        }
    } else {
        var0 = 2;
    }
    return var0;
}"""
    interpreter = interpreters.CInterpreter()
    utils.assert_code_equal(interpreter.interpret(expr), expected_code)


def test_multi_output():
    expr = ast.SubroutineExpr(
        ast.IfExpr(
            ast.CompExpr(
                ast.NumVal(1),
                ast.NumVal(1),
                ast.CompOpType.EQ),
            ast.VectorVal([ast.NumVal(1), ast.NumVal(2)]),
            ast.VectorVal([ast.NumVal(3), ast.NumVal(4)])))

    expected_code = """
void assignArray(double *output, double input[], int size) {
    for(int i = 0; i < size; ++i)
        output[i] = input[i];
}
double * score(double * input) {
    static double var0[2];
    if ((1) == (1)) {
        double var1[2] = {1, 2};
        assignArray(var0, var1, 2);
    } else {
        double var2[2] = {3, 4};
        assignArray(var0, var2, 2);
    }
    return var0;
}"""
    interpreter = interpreters.CInterpreter()
    utils.assert_code_equal(interpreter.interpret(expr), expected_code)