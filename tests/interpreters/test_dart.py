from m2cgen import ast
from m2cgen.interpreters import DartInterpreter
from tests import utils


def test_if_expr():
    expr = ast.IfExpr(
        ast.CompExpr(ast.NumVal(1), ast.FeatureRef(0), ast.CompOpType.EQ),
        ast.NumVal(2),
        ast.NumVal(3))

    expected_code = """
double score(List<double> input) {
    double var0;
    if ((1) == (input[0])) {
        var0 = 2;
    } else {
        var0 = 3;
    }
    return var0;
}
"""

    interpreter = DartInterpreter()
    utils.assert_code_equal(interpreter.interpret(expr), expected_code)


def test_bin_num_expr():
    expr = ast.BinNumExpr(
        ast.BinNumExpr(
            ast.FeatureRef(0), ast.NumVal(-2), ast.BinNumOpType.DIV),
        ast.NumVal(2),
        ast.BinNumOpType.MUL)

    expected_code = """
double score(List<double> input) {
    return ((input[0]) / (-2)) * (2);
}
"""

    interpreter = DartInterpreter()
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
double score(List<double> input) {
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
"""

    interpreter = DartInterpreter()
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
double score(List<double> input) {
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
"""

    interpreter = DartInterpreter()
    utils.assert_code_equal(interpreter.interpret(expr), expected_code)


def test_raw_array():
    expr = ast.VectorVal([ast.NumVal(3), ast.NumVal(4)])

    expected_code = """
List<double> score(List<double> input) {
    return [3, 4];
}
"""

    interpreter = DartInterpreter()
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
List<double> score(List<double> input) {
    List<double> var0;
    if ((1) == (1)) {
        var0 = [1, 2];
    } else {
        var0 = [3, 4];
    }
    return var0;
}
"""

    interpreter = DartInterpreter()
    utils.assert_code_equal(interpreter.interpret(expr), expected_code)


def test_bin_vector_expr():
    expr = ast.BinVectorExpr(
        ast.VectorVal([ast.NumVal(1), ast.NumVal(2)]),
        ast.VectorVal([ast.NumVal(3), ast.NumVal(4)]),
        ast.BinNumOpType.ADD)

    expected_code = """
List<double> score(List<double> input) {
    return addVectors([1, 2], [3, 4]);
}
List<double> addVectors(List<double> v1, List<double> v2) {
    List<double> result = new List<double>(v1.length);
    for (int i = 0; i < v1.length; i++) {
        result[i] = v1[i] + v2[i];
    }
    return result;
}
List<double> mulVectorNumber(List<double> v1, double num) {
    List<double> result = new List<double>(v1.length);
    for (int i = 0; i < v1.length; i++) {
        result[i] = v1[i] * num;
    }
    return result;
}
"""

    interpreter = DartInterpreter()
    utils.assert_code_equal(interpreter.interpret(expr), expected_code)


def test_bin_vector_num_expr():
    expr = ast.BinVectorNumExpr(
        ast.VectorVal([ast.NumVal(1), ast.NumVal(2)]),
        ast.NumVal(1),
        ast.BinNumOpType.MUL)

    expected_code = """
List<double> score(List<double> input) {
    return mulVectorNumber([1, 2], 1);
}
List<double> addVectors(List<double> v1, List<double> v2) {
    List<double> result = new List<double>(v1.length);
    for (int i = 0; i < v1.length; i++) {
        result[i] = v1[i] + v2[i];
    }
    return result;
}
List<double> mulVectorNumber(List<double> v1, double num) {
    List<double> result = new List<double>(v1.length);
    for (int i = 0; i < v1.length; i++) {
        result[i] = v1[i] * num;
    }
    return result;
}
"""

    interpreter = DartInterpreter()
    utils.assert_code_equal(interpreter.interpret(expr), expected_code)


class CustomDartInterpreter(DartInterpreter):
    bin_depth_threshold = 2


def test_depth_threshold_with_bin_expr():
    expr = ast.NumVal(1)
    for i in range(4):
        expr = ast.BinNumExpr(ast.NumVal(1), expr, ast.BinNumOpType.ADD)

    interpreter = CustomDartInterpreter()

    expected_code = """
double score(List<double> input) {
    double var0;
    var0 = (1) + ((1) + (1));
    return (1) + ((1) + (var0));
}
"""

    utils.assert_code_equal(interpreter.interpret(expr), expected_code)


def test_depth_threshold_without_bin_expr():
    expr = ast.NumVal(1)
    for i in range(4):
        expr = ast.IfExpr(
            ast.CompExpr(
                ast.NumVal(1), ast.NumVal(1), ast.CompOpType.EQ),
            ast.NumVal(1),
            expr)

    interpreter = CustomDartInterpreter()

    expected_code = """
double score(List<double> input) {
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
"""

    utils.assert_code_equal(interpreter.interpret(expr), expected_code)


def test_deep_mixed_exprs_not_reaching_threshold():
    expr = ast.NumVal(1)
    for i in range(4):
        inner = ast.NumVal(1)
        for i in range(2):
            inner = ast.BinNumExpr(ast.NumVal(1), inner, ast.BinNumOpType.ADD)

        expr = ast.IfExpr(
            ast.CompExpr(
                inner, ast.NumVal(1), ast.CompOpType.EQ),
            ast.NumVal(1),
            expr)

    interpreter = CustomDartInterpreter()

    expected_code = """
double score(List<double> input) {
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
"""

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

    interpreter = CustomDartInterpreter()

    expected_code = """
double score(List<double> input) {
    double var0;
    double var1;
    var1 = (1) + ((1) + (1));
    if (((1) + ((1) + (var1))) == (1)) {
        var0 = 1;
    } else {
        double var2;
        var2 = (1) + ((1) + (1));
        if (((1) + ((1) + (var2))) == (1)) {
            var0 = 1;
        } else {
            double var3;
            var3 = (1) + ((1) + (1));
            if (((1) + ((1) + (var3))) == (1)) {
                var0 = 1;
            } else {
                double var4;
                var4 = (1) + ((1) + (1));
                if (((1) + ((1) + (var4))) == (1)) {
                    var0 = 1;
                } else {
                    var0 = 1;
                }
            }
        }
    }
    return var0;
}
"""

    utils.assert_code_equal(interpreter.interpret(expr), expected_code)


def test_exp_expr():
    expr = ast.ExpExpr(ast.NumVal(1.0))

    expected_code = """
import 'dart:math';
double score(List<double> input) {
    return exp(1.0);
}
"""

    interpreter = DartInterpreter()
    utils.assert_code_equal(interpreter.interpret(expr), expected_code)


def test_pow_expr():
    expr = ast.PowExpr(ast.NumVal(2.0), ast.NumVal(3.0))

    expected_code = """
import 'dart:math';
double score(List<double> input) {
    return pow(2.0, 3.0);
}
"""

    interpreter = DartInterpreter()
    utils.assert_code_equal(interpreter.interpret(expr), expected_code)


def test_sqrt_expr():
    expr = ast.SqrtExpr(ast.NumVal(2.0))

    expected_code = """
import 'dart:math';
double score(List<double> input) {
    return sqrt(2.0);
}
"""

    interpreter = DartInterpreter()
    utils.assert_code_equal(interpreter.interpret(expr), expected_code)


def test_tanh_expr():
    expr = ast.TanhExpr(ast.NumVal(2.0))

    expected_code = """
import 'dart:math';
double score(List<double> input) {
    return tanh(2.0);
}
double tanh(double x) {
    if (x > 22.0)
        return 1.0;
    if (x < -22.0)
        return -1.0;
    return ((exp(2*x) - 1)/(exp(2*x) + 1));
}
"""
    interpreter = DartInterpreter()
    utils.assert_code_equal(interpreter.interpret(expr), expected_code)


def test_log_expr():
    expr = ast.LogExpr(ast.NumVal(2.0))

    expected_code = """
import 'dart:math';
double score(List<double> input) {
    return log(2.0);
}
"""
    interpreter = DartInterpreter()
    utils.assert_code_equal(interpreter.interpret(expr), expected_code)


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
    utils.assert_code_equal(interpreter.interpret(expr), expected_code)


def test_reused_expr():
    reused_expr = ast.ExpExpr(ast.NumVal(1.0), to_reuse=True)
    expr = ast.BinNumExpr(reused_expr, reused_expr, ast.BinNumOpType.DIV)

    expected_code = """
import 'dart:math';
double score(List<double> input) {
    double var0;
    var0 = exp(1.0);
    return (var0) / (var0);
}
"""

    interpreter = DartInterpreter()
    utils.assert_code_equal(interpreter.interpret(expr), expected_code)
