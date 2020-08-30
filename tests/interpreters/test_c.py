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
    if ((1.0) == (input[0])) {
        var0 = 2.0;
    } else {
        var0 = 3.0;
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
    return ((input[0]) / (-2.0)) * (2.0);
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
    if ((1.0) == (1.0)) {
        var1 = 1.0;
    } else {
        var1 = 2.0;
    }
    if (((var1) + (2.0)) >= ((1.0) / (2.0))) {
        var0 = 1.0;
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
    if ((1.0) == (1.0)) {
        var1 = 1.0;
    } else {
        var1 = 2.0;
    }
    if ((1.0) == ((var1) + (2.0))) {
        double var2;
        if ((1.0) == (1.0)) {
            var2 = 1.0;
        } else {
            var2 = 2.0;
        }
        if ((1.0) == ((var2) + (2.0))) {
            var0 = input[2];
        } else {
            var0 = 2.0;
        }
    } else {
        var0 = 2.0;
    }
    return var0;
}"""
    interpreter = interpreters.CInterpreter()
    utils.assert_code_equal(interpreter.interpret(expr), expected_code)


def test_raw_array():
    expr = ast.VectorVal([ast.NumVal(3), ast.NumVal(4)])

    expected_code = """
#include <string.h>
void score(double * input, double * output) {
    memcpy(output, (double[]){3.0, 4.0}, 2 * sizeof(double));
}"""
    interpreter = interpreters.CInterpreter()
    utils.assert_code_equal(interpreter.interpret(expr), expected_code)


def test_multi_output():
    expr = ast.IfExpr(
        ast.CompExpr(
            ast.NumVal(1),
            ast.NumVal(1),
            ast.CompOpType.EQ),
        ast.VectorVal([ast.NumVal(1), ast.NumVal(2)]),
        ast.VectorVal([ast.NumVal(3), ast.NumVal(4)]))

    expected_code = """
#include <string.h>
void score(double * input, double * output) {
    double var0[2];
    if ((1.0) == (1.0)) {
        memcpy(var0, (double[]){1.0, 2.0}, 2 * sizeof(double));
    } else {
        memcpy(var0, (double[]){3.0, 4.0}, 2 * sizeof(double));
    }
    memcpy(output, var0, 2 * sizeof(double));
}"""
    interpreter = interpreters.CInterpreter()
    utils.assert_code_equal(interpreter.interpret(expr), expected_code)


def test_bin_vector_expr():
    expr = ast.BinVectorExpr(
        ast.VectorVal([ast.NumVal(1), ast.NumVal(2)]),
        ast.VectorVal([ast.NumVal(3), ast.NumVal(4)]),
        ast.BinNumOpType.ADD)

    interpreter = interpreters.CInterpreter()

    expected_code = """
#include <string.h>
void add_vectors(double *v1, double *v2, int size, double *result) {
    for(int i = 0; i < size; ++i)
        result[i] = v1[i] + v2[i];
}
void mul_vector_number(double *v1, double num, int size, double *result) {
    for(int i = 0; i < size; ++i)
        result[i] = v1[i] * num;
}
void score(double * input, double * output) {
    double var0[2];
    add_vectors((double[]){1.0, 2.0}, (double[]){3.0, 4.0}, 2, var0);
    memcpy(output, var0, 2 * sizeof(double));
}"""
    utils.assert_code_equal(interpreter.interpret(expr), expected_code)


def test_bin_vector_num_expr():
    expr = ast.BinVectorNumExpr(
        ast.VectorVal([ast.NumVal(1), ast.NumVal(2)]),
        ast.NumVal(1),
        ast.BinNumOpType.MUL)

    interpreter = interpreters.CInterpreter()

    expected_code = """
#include <string.h>
void add_vectors(double *v1, double *v2, int size, double *result) {
    for(int i = 0; i < size; ++i)
        result[i] = v1[i] + v2[i];
}
void mul_vector_number(double *v1, double num, int size, double *result) {
    for(int i = 0; i < size; ++i)
        result[i] = v1[i] * num;
}
void score(double * input, double * output) {
    double var0[2];
    mul_vector_number((double[]){1.0, 2.0}, 1.0, 2, var0);
    memcpy(output, var0, 2 * sizeof(double));
}"""
    utils.assert_code_equal(interpreter.interpret(expr), expected_code)


def test_abs_expr():
    expr = ast.AbsExpr(ast.NumVal(-1.0))

    interpreter = interpreters.CInterpreter()

    expected_code = """
#include <math.h>
double score(double * input) {
    return fabs(-1.0);
}"""

    utils.assert_code_equal(interpreter.interpret(expr), expected_code)


def test_exp_expr():
    expr = ast.ExpExpr(ast.NumVal(1.0))

    interpreter = interpreters.CInterpreter()

    expected_code = """
#include <math.h>
double score(double * input) {
    return exp(1.0);
}"""

    utils.assert_code_equal(interpreter.interpret(expr), expected_code)


def test_pow_expr():
    expr = ast.PowExpr(ast.NumVal(2.0), ast.NumVal(3.0))

    interpreter = interpreters.CInterpreter()

    expected_code = """
#include <math.h>
double score(double * input) {
    return pow(2.0, 3.0);
}"""

    utils.assert_code_equal(interpreter.interpret(expr), expected_code)


def test_sqrt_expr():
    expr = ast.SqrtExpr(ast.NumVal(2.0))

    interpreter = interpreters.CInterpreter()

    expected_code = """
#include <math.h>
double score(double * input) {
    return sqrt(2.0);
}"""

    utils.assert_code_equal(interpreter.interpret(expr), expected_code)


def test_tanh_expr():
    expr = ast.TanhExpr(ast.NumVal(2.0))

    interpreter = interpreters.CInterpreter()

    expected_code = """
#include <math.h>
double score(double * input) {
    return tanh(2.0);
}"""

    utils.assert_code_equal(interpreter.interpret(expr), expected_code)


def test_log_expr():
    expr = ast.LogExpr(ast.NumVal(2.0))

    interpreter = interpreters.CInterpreter()

    expected_code = """
#include <math.h>
double score(double * input) {
    return log(2.0);
}"""

    utils.assert_code_equal(interpreter.interpret(expr), expected_code)


def test_log1p_expr():
    expr = ast.Log1pExpr(ast.NumVal(2.0))

    interpreter = interpreters.CInterpreter()

    expected_code = """
#include <math.h>
double score(double * input) {
    return log1p(2.0);
}"""

    utils.assert_code_equal(interpreter.interpret(expr), expected_code)


def test_atan_expr():
    expr = ast.AtanExpr(ast.NumVal(2.0))

    interpreter = interpreters.CInterpreter()

    expected_code = """
#include <math.h>
double score(double * input) {
    return atan(2.0);
}"""

    utils.assert_code_equal(interpreter.interpret(expr), expected_code)


def test_reused_expr():
    reused_expr = ast.ExpExpr(ast.NumVal(1.0), to_reuse=True)
    expr = ast.BinNumExpr(reused_expr, reused_expr, ast.BinNumOpType.DIV)

    interpreter = interpreters.CInterpreter()

    expected_code = """
#include <math.h>
double score(double * input) {
    double var0;
    var0 = exp(1.0);
    return (var0) / (var0);
}"""

    utils.assert_code_equal(interpreter.interpret(expr), expected_code)
