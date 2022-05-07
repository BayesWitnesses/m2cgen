from itertools import product

import pytest

from m2cgen import ast
from m2cgen.interpreters import JavaInterpreter

from tests.utils import assert_code_equal


def test_if_expr():
    expr = ast.IfExpr(
        ast.CompExpr(ast.NumVal(1), ast.FeatureRef(0), ast.CompOpType.EQ),
        ast.NumVal(2),
        ast.NumVal(3))

    expected_code = """
public class Model {
    public static double score(double[] input) {
        double var0;
        if (1.0 == input[0]) {
            var0 = 2.0;
        } else {
            var0 = 3.0;
        }
        return var0;
    }
}
"""

    interpreter = JavaInterpreter()
    assert_code_equal(interpreter.interpret(expr), expected_code)


def test_bin_num_expr():
    expr = ast.BinNumExpr(
        ast.BinNumExpr(
            ast.FeatureRef(0), ast.NumVal(-2), ast.BinNumOpType.DIV),
        ast.NumVal(2),
        ast.BinNumOpType.MUL)

    expected_code = """
public class Model {
    public static double score(double[] input) {
        return input[0] / -2.0 * 2.0;
    }
}
"""

    interpreter = JavaInterpreter()
    assert_code_equal(interpreter.interpret(expr), expected_code)


@pytest.mark.parametrize("op1, op2", [
    *product((ast.BinNumOpType.ADD, ast.BinNumOpType.SUB), repeat=2),
    *product((ast.BinNumOpType.MUL, ast.BinNumOpType.DIV), repeat=2)
])
def test_associativity_in_bin_num_expr(op1, op2):
    expr1 = ast.BinNumExpr(
        left=ast.NumVal(1.0),
        right=ast.BinNumExpr(
            left=ast.NumVal(1.0),
            right=ast.NumVal(1.0),
            op=op2
        ),
        op=op1
    )
    if op1 in {ast.BinNumOpType.ADD, ast.BinNumOpType.MUL}:
        op_code_line = f"1.0 {op1.value} 1.0 {op2.value} 1.0"
    else:
        op_code_line = f"1.0 {op1.value} (1.0 {op2.value} 1.0)"
    expected_code1 = f"""
public class Model {{
    public static double score(double[] input) {{
        return {op_code_line};
    }}
}}
"""

    expr2 = ast.BinNumExpr(
        left=ast.BinNumExpr(
            left=ast.NumVal(1.0),
            right=ast.NumVal(1.0),
            op=op1
        ),
        right=ast.NumVal(1.0),
        op=op2
    )
    expected_code2 = f"""
public class Model {{
    public static double score(double[] input) {{
        return 1.0 {op1.value} 1.0 {op2.value} 1.0;
    }}
}}
"""

    interpreter = JavaInterpreter()
    assert_code_equal(interpreter.interpret(expr1), expected_code1)
    assert_code_equal(interpreter.interpret(expr2), expected_code2)


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
        if (1.0 == 1.0) {
            var1 = 1.0;
        } else {
            var1 = 2.0;
        }
        if (var1 + 2.0 >= 1.0 / 2.0) {
            var0 = 1.0;
        } else {
            var0 = input[0];
        }
        return var0;
    }
}
"""

    interpreter = JavaInterpreter()
    assert_code_equal(interpreter.interpret(expr), expected_code)


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
        if (1.0 == 1.0) {
            var1 = 1.0;
        } else {
            var1 = 2.0;
        }
        if (1.0 == var1 + 2.0) {
            double var2;
            if (1.0 == 1.0) {
                var2 = 1.0;
            } else {
                var2 = 2.0;
            }
            if (1.0 == var2 + 2.0) {
                var0 = input[2];
            } else {
                var0 = 2.0;
            }
        } else {
            var0 = 2.0;
        }
        return var0;
    }
}
"""

    interpreter = JavaInterpreter()
    assert_code_equal(interpreter.interpret(expr), expected_code)


def test_package_name():
    expr = ast.NumVal(1)

    expected_code = """
package foo.bar;
public class Model {
    public static double score(double[] input) {
        return 1.0;
    }
}
"""

    interpreter = JavaInterpreter(package_name="foo.bar")
    assert_code_equal(interpreter.interpret(expr), expected_code)


def test_ignores_subroutine_expr():
    expr = ast.BinNumExpr(
        ast.FeatureRef(0),
        ast.BinNumExpr(ast.NumVal(1), ast.NumVal(2), ast.BinNumOpType.ADD),
        ast.BinNumOpType.MUL)

    expected_code = """
public class Model {
    public static double score(double[] input) {
        return input[0] * (1.0 + 2.0);
    }
}
"""

    interpreter = JavaInterpreter()
    assert_code_equal(interpreter.interpret(expr), expected_code)


def test_raw_array():
    expr = ast.VectorVal([ast.NumVal(3), ast.NumVal(4)])

    expected_code = """
public class Model {
    public static double[] score(double[] input) {
        return new double[] {3.0, 4.0};
    }
}
"""

    interpreter = JavaInterpreter()
    assert_code_equal(interpreter.interpret(expr), expected_code)


def test_multi_output():
    expr = ast.IfExpr(
        ast.CompExpr(
            ast.NumVal(1),
            ast.NumVal(1),
            ast.CompOpType.NOT_EQ),
        ast.VectorVal([ast.NumVal(1), ast.NumVal(2)]),
        ast.VectorVal([ast.NumVal(3), ast.NumVal(4)]))

    expected_code = """
public class Model {
    public static double[] score(double[] input) {
        double[] var0;
        if (1.0 != 1.0) {
            var0 = new double[] {1.0, 2.0};
        } else {
            var0 = new double[] {3.0, 4.0};
        }
        return var0;
    }
}
"""

    interpreter = JavaInterpreter()
    assert_code_equal(interpreter.interpret(expr), expected_code)


def test_bin_vector_expr():
    expr = ast.BinVectorExpr(
        ast.VectorVal([ast.NumVal(1), ast.NumVal(2)]),
        ast.VectorVal([ast.NumVal(3), ast.NumVal(4)]),
        ast.BinNumOpType.ADD)

    expected_code = """
public class Model {
    public static double[] score(double[] input) {
        return addVectors(new double[] {1.0, 2.0}, new double[] {3.0, 4.0});
    }
    private static double[] addVectors(double[] v1, double[] v2) {
        double[] result = new double[v1.length];
        for (int i = 0; i < v1.length; i++) {
            result[i] = v1[i] + v2[i];
        }
        return result;
    }
    private static double[] mulVectorNumber(double[] v1, double num) {
        double[] result = new double[v1.length];
        for (int i = 0; i < v1.length; i++) {
            result[i] = v1[i] * num;
        }
        return result;
    }
}
"""

    interpreter = JavaInterpreter()
    assert_code_equal(interpreter.interpret(expr), expected_code)


def test_bin_vector_num_expr():
    expr = ast.BinVectorNumExpr(
        ast.VectorVal([ast.NumVal(1), ast.NumVal(2)]),
        ast.NumVal(1),
        ast.BinNumOpType.MUL)

    expected_code = """
public class Model {
    public static double[] score(double[] input) {
        return mulVectorNumber(new double[] {1.0, 2.0}, 1.0);
    }
    private static double[] addVectors(double[] v1, double[] v2) {
        double[] result = new double[v1.length];
        for (int i = 0; i < v1.length; i++) {
            result[i] = v1[i] + v2[i];
        }
        return result;
    }
    private static double[] mulVectorNumber(double[] v1, double num) {
        double[] result = new double[v1.length];
        for (int i = 0; i < v1.length; i++) {
            result[i] = v1[i] * num;
        }
        return result;
    }
}
"""

    interpreter = JavaInterpreter()
    assert_code_equal(interpreter.interpret(expr), expected_code)


class CustomJavaInterpreter(JavaInterpreter):
    ast_size_check_frequency = 3
    ast_size_per_subroutine_threshold = 1


def test_depth_threshold_with_bin_expr():
    expr = ast.NumVal(1)
    for _ in range(4):
        expr = ast.BinNumExpr(ast.NumVal(1), expr, ast.BinNumOpType.ADD)

    expected_code = """
public class Model {
    public static double score(double[] input) {
        return 1.0 + 1.0 + subroutine0(input);
    }
    public static double subroutine0(double[] input) {
        return 1.0 + 1.0 + 1.0;
    }
}
"""

    interpreter = CustomJavaInterpreter()
    assert_code_equal(interpreter.interpret(expr), expected_code)


def test_depth_threshold_with_reused_bin_expr():
    reused_expr = ast.BinNumExpr(ast.NumVal(1), ast.NumVal(1), ast.BinNumOpType.ADD, to_reuse=True)
    expr = ast.BinNumExpr(ast.NumVal(1), reused_expr, ast.BinNumOpType.ADD)
    for _ in range(2):
        expr = ast.BinNumExpr(expr, expr, ast.BinNumOpType.ADD)

    expected_code = """
public class Model {
    public static double score(double[] input) {
        return subroutine0(input) + subroutine1(input) + subroutine2(input) + subroutine3(input);
    }
    public static double subroutine0(double[] input) {
        double var0;
        var0 = 1.0 + 1.0;
        return 1.0 + var0;
    }
    public static double subroutine1(double[] input) {
        double var0;
        var0 = 1.0 + 1.0;
        return 1.0 + var0;
    }
    public static double subroutine2(double[] input) {
        double var0;
        var0 = 1.0 + 1.0;
        return 1.0 + var0;
    }
    public static double subroutine3(double[] input) {
        double var0;
        var0 = 1.0 + 1.0;
        return 1.0 + var0;
    }
}
"""

    interpreter = CustomJavaInterpreter()
    assert_code_equal(interpreter.interpret(expr), expected_code)


def test_depth_threshold_without_bin_expr():
    expr = ast.NumVal(1)
    for _ in range(4):
        expr = ast.IfExpr(
            ast.CompExpr(
                ast.NumVal(1), ast.NumVal(1), ast.CompOpType.EQ),
            ast.NumVal(1),
            expr)

    expected_code = """
public class Model {
    public static double score(double[] input) {
        double var0;
        if (1.0 == 1.0) {
            var0 = 1.0;
        } else {
            if (1.0 == 1.0) {
                var0 = 1.0;
            } else {
                if (1.0 == 1.0) {
                    var0 = 1.0;
                } else {
                    if (1.0 == 1.0) {
                        var0 = 1.0;
                    } else {
                        var0 = 1.0;
                    }
                }
            }
        }
        return var0;
    }
}
"""

    interpreter = CustomJavaInterpreter()
    interpreter.ast_size_check_frequency = 2
    assert_code_equal(interpreter.interpret(expr), expected_code)


def test_deep_mixed_exprs_not_reaching_threshold():
    expr = ast.NumVal(1)
    for _ in range(4):
        inner = ast.NumVal(1)
        for __ in range(2):
            inner = ast.BinNumExpr(ast.NumVal(1), inner, ast.BinNumOpType.ADD)
        expr = ast.IfExpr(
            ast.CompExpr(
                inner, ast.NumVal(1), ast.CompOpType.EQ),
            ast.NumVal(1),
            expr)

    expected_code = """
public class Model {
    public static double score(double[] input) {
        double var0;
        if (1.0 + 1.0 + 1.0 == 1.0) {
            var0 = 1.0;
        } else {
            if (1.0 + 1.0 + 1.0 == 1.0) {
                var0 = 1.0;
            } else {
                if (1.0 + 1.0 + 1.0 == 1.0) {
                    var0 = 1.0;
                } else {
                    if (1.0 + 1.0 + 1.0 == 1.0) {
                        var0 = 1.0;
                    } else {
                        var0 = 1.0;
                    }
                }
            }
        }
        return var0;
    }
}
"""

    interpreter = CustomJavaInterpreter()
    assert_code_equal(interpreter.interpret(expr), expected_code)


def test_deep_mixed_exprs_exceeding_threshold():
    expr = ast.NumVal(1)
    for i in range(4):
        inner = ast.NumVal(1)
        for _ in range(4):
            inner = ast.BinNumExpr(ast.NumVal(i), inner, ast.BinNumOpType.ADD)
        expr = ast.IfExpr(
            ast.CompExpr(
                inner, ast.NumVal(1), ast.CompOpType.EQ),
            ast.NumVal(1),
            expr)

    expected_code = """
public class Model {
    public static double score(double[] input) {
        double var0;
        if (3.0 + 3.0 + subroutine0(input) == 1.0) {
            var0 = 1.0;
        } else {
            if (2.0 + 2.0 + subroutine1(input) == 1.0) {
                var0 = 1.0;
            } else {
                if (1.0 + 1.0 + subroutine2(input) == 1.0) {
                    var0 = 1.0;
                } else {
                    if (0.0 + 0.0 + subroutine3(input) == 1.0) {
                        var0 = 1.0;
                    } else {
                        var0 = 1.0;
                    }
                }
            }
        }
        return var0;
    }
    public static double subroutine0(double[] input) {
        return 3.0 + 3.0 + 1.0;
    }
    public static double subroutine1(double[] input) {
        return 2.0 + 2.0 + 1.0;
    }
    public static double subroutine2(double[] input) {
        return 1.0 + 1.0 + 1.0;
    }
    public static double subroutine3(double[] input) {
        return 0.0 + 0.0 + 1.0;
    }
}
"""

    interpreter = CustomJavaInterpreter()
    assert_code_equal(interpreter.interpret(expr), expected_code)


def test_abs_expr():
    expr = ast.AbsExpr(ast.NumVal(-1.0))

    expected_code = """
public class Model {
    public static double score(double[] input) {
        return Math.abs(-1.0);
    }
}
"""

    interpreter = JavaInterpreter()
    assert_code_equal(interpreter.interpret(expr), expected_code)


def test_exp_expr():
    expr = ast.ExpExpr(ast.NumVal(1.0))

    expected_code = """
public class Model {
    public static double score(double[] input) {
        return Math.exp(1.0);
    }
}
"""

    interpreter = JavaInterpreter()
    assert_code_equal(interpreter.interpret(expr), expected_code)


def test_pow_expr():
    expr = ast.PowExpr(ast.NumVal(2.0), ast.NumVal(3.0))

    expected_code = """
public class Model {
    public static double score(double[] input) {
        return Math.pow(2.0, 3.0);
    }
}
"""

    interpreter = JavaInterpreter()
    assert_code_equal(interpreter.interpret(expr), expected_code)


def test_sqrt_expr():
    expr = ast.SqrtExpr(ast.NumVal(2.0))

    expected_code = """
public class Model {
    public static double score(double[] input) {
        return Math.sqrt(2.0);
    }
}
"""

    interpreter = JavaInterpreter()
    assert_code_equal(interpreter.interpret(expr), expected_code)


def test_tanh_expr():
    expr = ast.TanhExpr(ast.NumVal(2.0))

    expected_code = """
public class Model {
    public static double score(double[] input) {
        return Math.tanh(2.0);
    }
}
"""

    interpreter = JavaInterpreter()
    assert_code_equal(interpreter.interpret(expr), expected_code)


def test_log_expr():
    expr = ast.LogExpr(ast.NumVal(2.0))

    expected_code = """
public class Model {
    public static double score(double[] input) {
        return Math.log(2.0);
    }
}
"""

    interpreter = JavaInterpreter()
    assert_code_equal(interpreter.interpret(expr), expected_code)


def test_log1p_expr():
    expr = ast.Log1pExpr(ast.NumVal(2.0))

    expected_code = """
public class Model {
    public static double score(double[] input) {
        return Math.log1p(2.0);
    }
}
"""

    interpreter = JavaInterpreter()
    assert_code_equal(interpreter.interpret(expr), expected_code)


def test_atan_expr():
    expr = ast.AtanExpr(ast.NumVal(2.0))

    expected_code = """
public class Model {
    public static double score(double[] input) {
        return Math.atan(2.0);
    }
}
"""

    interpreter = JavaInterpreter()
    assert_code_equal(interpreter.interpret(expr), expected_code)


def test_softmax_expr():
    expr = ast.SoftmaxExpr([ast.NumVal(2.0), ast.NumVal(3.0)])

    expected_code = """
public class Model {
    public static double[] score(double[] input) {
        return softmax(new double[] {2.0, 3.0});
    }
    private static double[] softmax(double[] x) {
        int size = x.length;
        double[] result = new double[size];
        double max = x[0];
        for (int i = 1; i < size; ++i) {
            if (x[i] > max)
                max = x[i];
        }
        double sum = 0.0;
        for (int i = 0; i < size; ++i) {
            result[i] = Math.exp(x[i] - max);
            sum += result[i];
        }
        for (int i = 0; i < size; ++i)
            result[i] /= sum;
        return result;
    }
}
"""

    interpreter = JavaInterpreter()
    assert_code_equal(interpreter.interpret(expr), expected_code)


def test_sigmoid_expr():
    expr = ast.SigmoidExpr(ast.NumVal(2.0))

    expected_code = """
public class Model {
    public static double score(double[] input) {
        return sigmoid(2.0);
    }
    private static double sigmoid(double x) {
        if (x < 0.0) {
            double z = Math.exp(x);
            return z / (1.0 + z);
        }
        return 1.0 / (1.0 + Math.exp(-x));
    }
}
"""

    interpreter = JavaInterpreter()
    assert_code_equal(interpreter.interpret(expr), expected_code)


def test_reused_expr():
    reused_expr = ast.ExpExpr(ast.NumVal(1.0), to_reuse=True)
    expr = ast.BinNumExpr(reused_expr, reused_expr, ast.BinNumOpType.DIV)

    expected_code = """
public class Model {
    public static double score(double[] input) {
        double var0;
        var0 = Math.exp(1.0);
        return var0 / var0;
    }
}
"""

    interpreter = JavaInterpreter()
    assert_code_equal(interpreter.interpret(expr), expected_code)


def test_unsupported_exprs():
    interpreter = JavaInterpreter()

    expr = ast.Expr()
    with pytest.raises(NotImplementedError, match="No handler found for 'Expr'"):
        interpreter.interpret(expr)

    expr = ast.BinVectorNumExpr(
        ast.VectorVal([ast.NumVal(1), ast.NumVal(2)]),
        ast.NumVal(1),
        ast.BinNumOpType.ADD)
    with pytest.raises(NotImplementedError, match="Op 'ADD' is unsupported"):
        interpreter.interpret(expr)

    expr = ast.BinVectorExpr(
        ast.VectorVal([ast.NumVal(1), ast.NumVal(2)]),
        ast.VectorVal([ast.NumVal(3), ast.NumVal(4)]),
        ast.BinNumOpType.MUL)
    with pytest.raises(NotImplementedError, match="Op 'MUL' is unsupported"):
        interpreter.interpret(expr)
