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

    utils.assert_code_equal(interpreter.interpret(expr), expected_code)


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
    utils.assert_code_equal(interpreter.interpret(expr), expected_code)


def test_package_name():
    expr = ast.NumVal(1)

    interpreter = interpreters.JavaInterpreter(package_name="foo.bar")

    expected_code = """
package foo.bar;
public class Model {
    public static double score(double[] input) {
        return 1;
    }
}"""

    utils.assert_code_equal(interpreter.interpret(expr), expected_code)


def test_ignores_subroutine_expr():
    expr = ast.BinNumExpr(
        ast.FeatureRef(0),
        ast.BinNumExpr(ast.NumVal(1), ast.NumVal(2), ast.BinNumOpType.ADD),
        ast.BinNumOpType.MUL)

    expected_code = """
public class Model {
    public static double score(double[] input) {
        return (input[0]) * ((1) + (2));
    }
}"""

    interpreter = interpreters.JavaInterpreter()
    utils.assert_code_equal(interpreter.interpret(expr), expected_code)


def test_raw_array():
    expr = ast.VectorVal([ast.NumVal(3), ast.NumVal(4)])

    expected_code = """
public class Model {
    public static double[] score(double[] input) {
        return new double[] {3, 4};
    }
}"""

    interpreter = interpreters.JavaInterpreter()
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
public class Model {
    public static double[] score(double[] input) {
        double[] var0;
        if ((1) == (1)) {
            var0 = new double[] {1, 2};
        } else {
            var0 = new double[] {3, 4};
        }
        return var0;
    }
}"""

    interpreter = interpreters.JavaInterpreter()
    utils.assert_code_equal(interpreter.interpret(expr), expected_code)


def test_bin_vector_expr():
    expr = ast.BinVectorExpr(
        ast.VectorVal([ast.NumVal(1), ast.NumVal(2)]),
        ast.VectorVal([ast.NumVal(3), ast.NumVal(4)]),
        ast.BinNumOpType.ADD)

    interpreter = interpreters.JavaInterpreter()

    expected_code = """
public class Model {
    public static double[] score(double[] input) {
        return addVectors(new double[] {1, 2}, new double[] {3, 4});
    }
    public static double[] addVectors(double[] v1, double[] v2) {
        double[] result = new double[v1.length];
        for (int i = 0; i < v1.length; i++) {
            result[i] = v1[i] + v2[i];
        }
        return result;
    }
    public static double[] mulVectorNumber(double[] v1, double num) {
        double[] result = new double[v1.length];
        for (int i = 0; i < v1.length; i++) {
            result[i] = v1[i] * num;
        }
        return result;
    }
}"""
    utils.assert_code_equal(interpreter.interpret(expr), expected_code)


def test_bin_vector_num_expr():
    expr = ast.BinVectorNumExpr(
        ast.VectorVal([ast.NumVal(1), ast.NumVal(2)]),
        ast.NumVal(1),
        ast.BinNumOpType.MUL)

    interpreter = interpreters.JavaInterpreter()

    expected_code = """
public class Model {
    public static double[] score(double[] input) {
        return mulVectorNumber(new double[] {1, 2}, 1);
    }
    public static double[] addVectors(double[] v1, double[] v2) {
        double[] result = new double[v1.length];
        for (int i = 0; i < v1.length; i++) {
            result[i] = v1[i] + v2[i];
        }
        return result;
    }
    public static double[] mulVectorNumber(double[] v1, double num) {
        double[] result = new double[v1.length];
        for (int i = 0; i < v1.length; i++) {
            result[i] = v1[i] * num;
        }
        return result;
    }
}"""
    utils.assert_code_equal(interpreter.interpret(expr), expected_code)


def test_abs_expr():
    expr = ast.AbsExpr(ast.NumVal(-1.0))

    interpreter = interpreters.JavaInterpreter()

    expected_code = """
public class Model {
    public static double score(double[] input) {
        return Math.abs(-1.0);
    }
}"""

    utils.assert_code_equal(interpreter.interpret(expr), expected_code)


def test_exp_expr():
    expr = ast.ExpExpr(ast.NumVal(1.0))

    interpreter = interpreters.JavaInterpreter()

    expected_code = """
public class Model {
    public static double score(double[] input) {
        return Math.exp(1.0);
    }
}"""

    utils.assert_code_equal(interpreter.interpret(expr), expected_code)


def test_pow_expr():
    expr = ast.PowExpr(ast.NumVal(2.0), ast.NumVal(3.0))

    interpreter = interpreters.JavaInterpreter()

    expected_code = """
public class Model {
    public static double score(double[] input) {
        return Math.pow(2.0, 3.0);
    }
}"""

    utils.assert_code_equal(interpreter.interpret(expr), expected_code)


def test_sqrt_expr():
    expr = ast.SqrtExpr(ast.NumVal(2.0))

    interpreter = interpreters.JavaInterpreter()

    expected_code = """
public class Model {
    public static double score(double[] input) {
        return Math.sqrt(2.0);
    }
}"""

    utils.assert_code_equal(interpreter.interpret(expr), expected_code)


def test_tanh_expr():
    expr = ast.TanhExpr(ast.NumVal(2.0))

    interpreter = interpreters.JavaInterpreter()

    expected_code = """
public class Model {
    public static double score(double[] input) {
        return Math.tanh(2.0);
    }
}"""

    utils.assert_code_equal(interpreter.interpret(expr), expected_code)


def test_reused_expr():
    reused_expr = ast.ExpExpr(ast.NumVal(1.0), to_reuse=True)
    expr = ast.BinNumExpr(reused_expr, reused_expr, ast.BinNumOpType.DIV)

    interpreter = interpreters.JavaInterpreter()

    expected_code = """
public class Model {
    public static double score(double[] input) {
        double var0;
        var0 = Math.exp(1.0);
        return (var0) / (var0);
    }
}"""

    utils.assert_code_equal(interpreter.interpret(expr), expected_code)


def test_depth_threshold_with_bin_expr():
    expr = ast.NumVal(1)
    for i in range(4):
        expr = ast.BinNumExpr(ast.NumVal(1), expr, ast.BinNumOpType.ADD)

    interpreter = interpreters.JavaInterpreter()
    interpreter.ast_size_check_frequency = 3
    interpreter.ast_size_per_subroutine_threshold = 1

    expected_code = """
public class Model {
    public static double score(double[] input) {
        return (1) + ((1) + (subroutine0(input)));
    }
    public static double subroutine0(double[] input) {
        return (1) + ((1) + (1));
    }
}"""

    utils.assert_code_equal(interpreter.interpret(expr), expected_code)


def test_depth_threshold_without_bin_expr():
    expr = ast.NumVal(1)
    for i in range(4):
        expr = ast.IfExpr(
            ast.CompExpr(
                ast.NumVal(1), ast.NumVal(1), ast.CompOpType.EQ),
            ast.NumVal(1),
            expr)

    interpreter = interpreters.JavaInterpreter()
    interpreter.ast_size_check_frequency = 2
    interpreter.ast_size_per_subroutine_threshold = 1

    expected_code = """
public class Model {
    public static double score(double[] input) {
        double var0;
        if ((1) == (1)) {
            var0 = 1;
        } else {
            if ((1) == (1)) {
                var0 = 1;
            } else {
                if ((1) == (1)) {
                    var0 = 1;
                } else {
                    if ((1) == (1)) {
                        var0 = 1;
                    } else {
                        var0 = 1;
                    }
                }
            }
        }
        return var0;
    }
}"""

    utils.assert_code_equal(interpreter.interpret(expr), expected_code)


def test_deep_mixed_exprs_not_reaching_threshold():
    expr = ast.NumVal(1)
    for i in range(4):
        inner = ast.NumVal(1)
        for _ in range(2):
            inner = ast.BinNumExpr(ast.NumVal(1), inner, ast.BinNumOpType.ADD)

        expr = ast.IfExpr(
            ast.CompExpr(
                inner, ast.NumVal(1), ast.CompOpType.EQ),
            ast.NumVal(1),
            expr)

    interpreter = interpreters.JavaInterpreter()
    interpreter.ast_size_check_frequency = 3
    interpreter.ast_size_per_subroutine_threshold = 1

    expected_code = """
public class Model {
    public static double score(double[] input) {
        double var0;
        if (((1) + ((1) + (1))) == (1)) {
            var0 = 1;
        } else {
            if (((1) + ((1) + (1))) == (1)) {
                var0 = 1;
            } else {
                if (((1) + ((1) + (1))) == (1)) {
                    var0 = 1;
                } else {
                    if (((1) + ((1) + (1))) == (1)) {
                        var0 = 1;
                    } else {
                        var0 = 1;
                    }
                }
            }
        }
        return var0;
    }
}"""

    utils.assert_code_equal(interpreter.interpret(expr), expected_code)


def test_deep_mixed_exprs_exceeding_threshold():
    expr = ast.NumVal(1)
    for i in range(4):
        inner = ast.NumVal(1)
        for i in range(4):
            inner = ast.BinNumExpr(ast.NumVal(1), inner, ast.BinNumOpType.ADD)

        expr = ast.IfExpr(
            ast.CompExpr(
                inner, ast.NumVal(1), ast.CompOpType.EQ),
            ast.NumVal(1),
            expr)

    interpreter = interpreters.JavaInterpreter()
    interpreter.ast_size_check_frequency = 3
    interpreter.ast_size_per_subroutine_threshold = 1

    expected_code = """
public class Model {
    public static double score(double[] input) {
        double var0;
        if (((1) + ((1) + (subroutine0(input)))) == (1)) {
            var0 = 1;
        } else {
            if (((1) + ((1) + (subroutine1(input)))) == (1)) {
                var0 = 1;
            } else {
                if (((1) + ((1) + (subroutine2(input)))) == (1)) {
                    var0 = 1;
                } else {
                    if (((1) + ((1) + (subroutine3(input)))) == (1)) {
                        var0 = 1;
                    } else {
                        var0 = 1;
                    }
                }
            }
        }
        return var0;
    }
    public static double subroutine0(double[] input) {
        return (1) + ((1) + (1));
    }
    public static double subroutine1(double[] input) {
        return (1) + ((1) + (1));
    }
    public static double subroutine2(double[] input) {
        return (1) + ((1) + (1));
    }
    public static double subroutine3(double[] input) {
        return (1) + ((1) + (1));
    }
}"""

    utils.assert_code_equal(interpreter.interpret(expr), expected_code)
