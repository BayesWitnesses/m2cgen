from itertools import product

import pytest

from m2cgen import ast
from m2cgen.interpreters import DartInterpreter

from tests.utils import assert_code_equal


def test_if_expr():
    expr = ast.IfExpr(
        ast.CompExpr(ast.NumVal(1), ast.FeatureRef(0), ast.CompOpType.EQ),
        ast.NumVal(2),
        ast.NumVal(3))

    expected_code = """
double score(List<double> input) {
    double var0;
    if (1.0 == input[0]) {
        var0 = 2.0;
    } else {
        var0 = 3.0;
    }
    return var0;
}
"""

    interpreter = DartInterpreter()
    assert_code_equal(interpreter.interpret(expr), expected_code)


def test_bin_num_expr():
    expr = ast.BinNumExpr(
        ast.BinNumExpr(
            ast.FeatureRef(0), ast.NumVal(-2), ast.BinNumOpType.DIV),
        ast.NumVal(2),
        ast.BinNumOpType.MUL)

    expected_code = """
double score(List<double> input) {
    return input[0] / -2.0 * 2.0;
}
"""

    interpreter = DartInterpreter()
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
double score(List<double> input) {{
    return {op_code_line};
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
double score(List<double> input) {{
    return 1.0 {op1.value} 1.0 {op2.value} 1.0;
}}
"""

    interpreter = DartInterpreter()
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
double score(List<double> input) {
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
"""

    interpreter = DartInterpreter()
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
double score(List<double> input) {
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
"""

    interpreter = DartInterpreter()
    assert_code_equal(interpreter.interpret(expr), expected_code)


def test_raw_array():
    expr = ast.VectorVal([ast.NumVal(3), ast.NumVal(4)])

    expected_code = """
List<double> score(List<double> input) {
    return [3.0, 4.0];
}
"""

    interpreter = DartInterpreter()
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
List<double> score(List<double> input) {
    List<double> var0;
    if (1.0 != 1.0) {
        var0 = [1.0, 2.0];
    } else {
        var0 = [3.0, 4.0];
    }
    return var0;
}
"""

    interpreter = DartInterpreter()
    assert_code_equal(interpreter.interpret(expr), expected_code)


def test_bin_vector_expr():
    expr = ast.BinVectorExpr(
        ast.VectorVal([ast.NumVal(1), ast.NumVal(2)]),
        ast.VectorVal([ast.NumVal(3), ast.NumVal(4)]),
        ast.BinNumOpType.ADD)

    expected_code = """
List<double> score(List<double> input) {
    return addVectors([1.0, 2.0], [3.0, 4.0]);
}
List<double> addVectors(List<double> v1, List<double> v2) {
    List<double> result = new List<double>.filled(v1.length, 0.0);
    for (int i = 0; i < v1.length; i++) {
        result[i] = v1[i] + v2[i];
    }
    return result;
}
List<double> mulVectorNumber(List<double> v1, double num) {
    List<double> result = new List<double>.filled(v1.length, 0.0);
    for (int i = 0; i < v1.length; i++) {
        result[i] = v1[i] * num;
    }
    return result;
}
"""

    interpreter = DartInterpreter()
    assert_code_equal(interpreter.interpret(expr), expected_code)


def test_bin_vector_num_expr():
    expr = ast.BinVectorNumExpr(
        ast.VectorVal([ast.NumVal(1), ast.NumVal(2)]),
        ast.NumVal(1),
        ast.BinNumOpType.MUL)

    expected_code = """
List<double> score(List<double> input) {
    return mulVectorNumber([1.0, 2.0], 1.0);
}
List<double> addVectors(List<double> v1, List<double> v2) {
    List<double> result = new List<double>.filled(v1.length, 0.0);
    for (int i = 0; i < v1.length; i++) {
        result[i] = v1[i] + v2[i];
    }
    return result;
}
List<double> mulVectorNumber(List<double> v1, double num) {
    List<double> result = new List<double>.filled(v1.length, 0.0);
    for (int i = 0; i < v1.length; i++) {
        result[i] = v1[i] * num;
    }
    return result;
}
"""

    interpreter = DartInterpreter()
    assert_code_equal(interpreter.interpret(expr), expected_code)


class CustomDartInterpreter(DartInterpreter):
    bin_depth_threshold = 2


def test_depth_threshold_with_bin_expr():
    expr = ast.NumVal(1)
    for _ in range(4):
        expr = ast.BinNumExpr(ast.NumVal(1), expr, ast.BinNumOpType.ADD)

    expected_code = """
double score(List<double> input) {
    double var0;
    var0 = 1.0 + 1.0 + 1.0;
    return 1.0 + 1.0 + var0;
}
"""

    interpreter = CustomDartInterpreter()
    assert_code_equal(interpreter.interpret(expr), expected_code)


def test_depth_threshold_with_reused_bin_expr():
    reused_expr = ast.BinNumExpr(ast.NumVal(1), ast.NumVal(1), ast.BinNumOpType.ADD, to_reuse=True)
    expr = ast.BinNumExpr(ast.NumVal(1), reused_expr, ast.BinNumOpType.ADD)
    expr = ast.BinNumExpr(expr, expr, ast.BinNumOpType.ADD)

    expected_code = """
double score(List<double> input) {
    double var0;
    var0 = 1.0 + 1.0;
    double var1;
    var1 = var0;
    return 1.0 + var1 + 1.0 + var0;
}
"""

    interpreter = CustomDartInterpreter()
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
double score(List<double> input) {
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
"""

    interpreter = CustomDartInterpreter()
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
double score(List<double> input) {
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
"""

    interpreter = CustomDartInterpreter()
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
double score(List<double> input) {
    double var0;
    double var1;
    var1 = 3.0 + 3.0 + 1.0;
    if (3.0 + 3.0 + var1 == 1.0) {
        var0 = 1.0;
    } else {
        double var2;
        var2 = 2.0 + 2.0 + 1.0;
        if (2.0 + 2.0 + var2 == 1.0) {
            var0 = 1.0;
        } else {
            double var3;
            var3 = 1.0 + 1.0 + 1.0;
            if (1.0 + 1.0 + var3 == 1.0) {
                var0 = 1.0;
            } else {
                double var4;
                var4 = 0.0 + 0.0 + 1.0;
                if (0.0 + 0.0 + var4 == 1.0) {
                    var0 = 1.0;
                } else {
                    var0 = 1.0;
                }
            }
        }
    }
    return var0;
}
"""

    interpreter = CustomDartInterpreter()
    assert_code_equal(interpreter.interpret(expr), expected_code)


def test_abs_expr():
    expr = ast.AbsExpr(ast.NumVal(-1.0))

    expected_code = """
double score(List<double> input) {
    return (-1.0).abs();
}
"""

    interpreter = DartInterpreter()
    assert_code_equal(interpreter.interpret(expr), expected_code)


def test_exp_expr():
    expr = ast.ExpExpr(ast.NumVal(1.0))

    expected_code = """
import 'dart:math';
double score(List<double> input) {
    return exp(1.0);
}
"""

    interpreter = DartInterpreter()
    assert_code_equal(interpreter.interpret(expr), expected_code)


def test_pow_expr():
    expr = ast.PowExpr(ast.NumVal(2.0), ast.NumVal(3.0))

    expected_code = """
import 'dart:math';
double score(List<double> input) {
    return (pow(2.0, 3.0)).toDouble();
}
"""

    interpreter = DartInterpreter()
    assert_code_equal(interpreter.interpret(expr), expected_code)


def test_sqrt_expr():
    expr = ast.SqrtExpr(ast.NumVal(2.0))

    expected_code = """
import 'dart:math';
double score(List<double> input) {
    return sqrt(2.0);
}
"""

    interpreter = DartInterpreter()
    assert_code_equal(interpreter.interpret(expr), expected_code)


def test_tanh_expr():
    expr = ast.TanhExpr(ast.NumVal(2.0))

    expected_code = """
import 'dart:math';
double score(List<double> input) {
    return tanh(2.0);
}
double tanh(double x) {
    // Implementation is taken from
    // https://github.com/golang/go/blob/master/src/math/tanh.go
    double z;
    z = x.abs();
    if (z > 0.440148459655565271479942397125e+2) {
        if (x < 0) {
            return -1.0;
        }
        return 1.0;
    }
    if (z >= 0.625) {
        z = 1 - 2 / (exp(2 * z) + 1);
        if (x < 0) {
            z = -z;
        }
        return z;
    }
    if (x == 0) {
        return 0.0;
    }
    double s;
    s = x * x;
    z = x + x * s
        * ((-0.964399179425052238628e+0 * s + -0.992877231001918586564e+2)
        * s + -0.161468768441708447952e+4) / (((s + 0.112811678491632931402e+3)
        * s + 0.223548839060100448583e+4) * s + 0.484406305325125486048e+4);
    return z;
}
"""

    interpreter = DartInterpreter()
    assert_code_equal(interpreter.interpret(expr), expected_code)


def test_log_expr():
    expr = ast.LogExpr(ast.NumVal(2.0))

    expected_code = """
import 'dart:math';
double score(List<double> input) {
    return log(2.0);
}
"""

    interpreter = DartInterpreter()
    assert_code_equal(interpreter.interpret(expr), expected_code)


def test_log1p_expr():
    expr = ast.Log1pExpr(ast.NumVal(2.0))

    expected_code = """
import 'dart:math';
double score(List<double> input) {
    return log1p(2.0);
}
double log1p(double x) {
    if (x == 0.0)
        return 0.0;
    if (x == -1.0)
        return double.negativeInfinity;
    if (x < -1.0)
        return double.nan;
    double xAbs = x.abs();
    if (xAbs < 0.5 * 4.94065645841247e-324)
        return x;
    if ((x > 0.0 && x < 1e-8) || (x > -1e-9 && x < 0.0))
        return x * (1.0 - x * 0.5);
    if (xAbs < 0.375) {
        List<double> coeffs = [
             0.10378693562743769800686267719098e+1,
            -0.13364301504908918098766041553133e+0,
             0.19408249135520563357926199374750e-1,
            -0.30107551127535777690376537776592e-2,
             0.48694614797154850090456366509137e-3,
            -0.81054881893175356066809943008622e-4,
             0.13778847799559524782938251496059e-4,
            -0.23802210894358970251369992914935e-5,
             0.41640416213865183476391859901989e-6,
            -0.73595828378075994984266837031998e-7,
             0.13117611876241674949152294345011e-7,
            -0.23546709317742425136696092330175e-8,
             0.42522773276034997775638052962567e-9,
            -0.77190894134840796826108107493300e-10,
             0.14075746481359069909215356472191e-10,
            -0.25769072058024680627537078627584e-11,
             0.47342406666294421849154395005938e-12,
            -0.87249012674742641745301263292675e-13,
             0.16124614902740551465739833119115e-13,
            -0.29875652015665773006710792416815e-14,
             0.55480701209082887983041321697279e-15,
            -0.10324619158271569595141333961932e-15];
        return x * (1.0 - x * chebyshevBroucke(x / 0.375, coeffs));
    }
    return log(1.0 + x);
}
double chebyshevBroucke(double x, List<double> coeffs) {
    double b0, b1, b2, x2;
    b2 = b1 = b0 = 0.0;
    x2 = x * 2;
    for (int i = coeffs.length - 1; i >= 0; --i) {
        b2 = b1;
        b1 = b0;
        b0 = x2 * b1 - b2 + coeffs[i];
    }
    return (b0 - b2) * 0.5;
}
"""

    interpreter = DartInterpreter()
    assert_code_equal(interpreter.interpret(expr), expected_code)


def test_atan_expr():
    expr = ast.AtanExpr(ast.NumVal(2.0))

    expected_code = """
import 'dart:math';
double score(List<double> input) {
    return atan(2.0);
}
"""

    interpreter = DartInterpreter()
    assert_code_equal(interpreter.interpret(expr), expected_code)


def test_softmax_expr():
    expr = ast.SoftmaxExpr([ast.NumVal(2.0), ast.NumVal(3.0)])

    expected_code = """
import 'dart:math';
List<double> score(List<double> input) {
    return softmax([2.0, 3.0]);
}
List<double> softmax(List<double> x) {
    int size = x.length;
    List<double> result = new List<double>.filled(size, 0.0);
    double maxElem = x.reduce(max);
    double sum = 0.0;
    for (int i = 0; i < size; ++i) {
        result[i] = exp(x[i] - maxElem);
        sum += result[i];
    }
    for (int i = 0; i < size; ++i)
        result[i] /= sum;
    return result;
}
"""

    interpreter = DartInterpreter()
    assert_code_equal(interpreter.interpret(expr), expected_code)


def test_sigmoid_expr():
    expr = ast.SigmoidExpr(ast.NumVal(2.0))

    expected_code = """
import 'dart:math';
double score(List<double> input) {
    return sigmoid(2.0);
}
double sigmoid(double x) {
    if (x < 0.0) {
        double z = exp(x);
        return z / (1.0 + z);
    }
    return 1.0 / (1.0 + exp(-x));
}
"""

    interpreter = DartInterpreter()
    assert_code_equal(interpreter.interpret(expr), expected_code)


def test_reused_expr():
    reused_expr = ast.ExpExpr(ast.NumVal(1.0), to_reuse=True)
    expr = ast.BinNumExpr(reused_expr, reused_expr, ast.BinNumOpType.DIV)

    expected_code = """
import 'dart:math';
double score(List<double> input) {
    double var0;
    var0 = exp(1.0);
    return var0 / var0;
}
"""

    interpreter = DartInterpreter()
    assert_code_equal(interpreter.interpret(expr), expected_code)


def test_unsupported_exprs():
    interpreter = DartInterpreter()

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
