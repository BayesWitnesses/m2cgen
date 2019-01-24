from m2cgen import ast
from m2cgen import interpreters
from tests import utils


def test_if_expr():
    expr = ast.IfExpr(
        ast.CompExpr(ast.NumVal(1), ast.FeatureRef(0), ast.CompOpType.EQ),
        ast.NumVal(2),
        ast.NumVal(3))

    interpreter = interpreters.JavaInterpreter()

    expected_code = """
public class Model {

    public static double score(double[] input) {
        double var0;
        if ((1) == (input[0])) {
            var0 = 2;
        } else {
            var0 = 3;
        }
        return var0;
    }
}
"""

    utils.assert_code_equal(interpreter.interpret(expr)[0][1], expected_code)


def test_bin_num_expr():
    expr = ast.BinNumExpr(
        ast.BinNumExpr(
            ast.FeatureRef(0), ast.NumVal(-2), ast.BinNumOpType.DIV),
        ast.NumVal(2),
        ast.BinNumOpType.MUL)

    interpreter = interpreters.JavaInterpreter()

    expected_code = """
public class Model {

    public static double score(double[] input) {
        return ((input[0]) / (-2)) * (2);
    }
}"""

    utils.assert_code_equal(interpreter.interpret(expr)[0][1], expected_code)


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
public class Model {

    public static double score(double[] input) {
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
    }
}"""

    interpreter = interpreters.JavaInterpreter()

    utils.assert_code_equal(interpreter.interpret(expr)[0][1], expected_code)


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
public class Model {

    public static double score(double[] input) {
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
    }
}"""

    interpreter = interpreters.JavaInterpreter()
    utils.assert_code_equal(interpreter.interpret(expr)[0][1], expected_code)


def test_subroutine():
    expr = ast.BinNumExpr(
        ast.FeatureRef(0),
        ast.SubroutineExpr(
            ast.BinNumExpr(ast.NumVal(1), ast.NumVal(2), ast.BinNumOpType.ADD)),
        ast.BinNumOpType.MUL)

    expected_code = """
public class Model {

    public static double score(double[] input) {
        return (input[0]) * (subroutine0(input));
    }
    public static double subroutine0(double[] input) {
        return (1) + (2);
    }
}"""

    interpreter = interpreters.JavaInterpreter()
    utils.assert_code_equal(interpreter.interpret(expr)[0][1], expected_code)
