from m2cgen import ast
from m2cgen.interpreters import DartInterpreter
from tests import utils


def test_if_expr():
    expr = ast.IfExpr(
        ast.CompExpr(ast.NumVal(1), ast.FeatureRef(0), ast.CompOpType.EQ),
        ast.NumVal(2),
        ast.NumVal(3))

    expected_code = """
class Model {
    static double score(List<double> input) {
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

    interpreter = DartInterpreter()
    utils.assert_code_equal(interpreter.interpret(expr), expected_code)


def test_bin_num_expr():
    expr = ast.BinNumExpr(
        ast.BinNumExpr(
            ast.FeatureRef(0), ast.NumVal(-2), ast.BinNumOpType.DIV),
        ast.NumVal(2),
        ast.BinNumOpType.MUL)

    expected_code = """
class Model {
    static double score(List<double> input) {
        return ((input[0]) / (-2)) * (2);
    }
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
class Model {
    static double score(List<double> input) {
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
class Model {
    static double score(List<double> input) {
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
}
"""

    interpreter = DartInterpreter()
    utils.assert_code_equal(interpreter.interpret(expr), expected_code)


def test_class_name():
    expr = ast.NumVal(1)

    expected_code = """
class TestModel {
    static double score(List<double> input) {
        return 1;
    }
}
"""

    interpreter = DartInterpreter(class_name="TestModel")
    utils.assert_code_equal(interpreter.interpret(expr), expected_code)


def test_raw_array():
    expr = ast.VectorVal([ast.NumVal(3), ast.NumVal(4)])

    expected_code = """
class Model {
    static List<double> score(List<double> input) {
        return [3, 4];
    }
}
"""

    interpreter = DartInterpreter()
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
class Model {
    static List<double> score(List<double> input) {
        List<double> var0;
        if ((1) == (1)) {
            var0 = [1, 2];
        } else {
            var0 = [3, 4];
        }
        return var0;
    }
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
class Model {
    static List<double> score(List<double> input) {
        return addVectors([1, 2], [3, 4]);
    }
    static List<double> addVectors(List<double> v1, List<double> v2) {
        List<double> result = new List<double>(v1.length);
        for (int i = 0; i < v1.length; i++) {
            result[i] = v1[i] + v2[i];
        }
        return result;
    }
    static List<double> mulVectorNumber(List<double> v1, double num) {
        List<double> result = new List<double>(v1.length);
        for (int i = 0; i < v1.length; i++) {
            result[i] = v1[i] * num;
        }
        return result;
    }
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
class Model {
    static List<double> score(List<double> input) {
        return mulVectorNumber([1, 2], 1);
    }
    static List<double> addVectors(List<double> v1, List<double> v2) {
        List<double> result = new List<double>(v1.length);
        for (int i = 0; i < v1.length; i++) {
            result[i] = v1[i] + v2[i];
        }
        return result;
    }
    static List<double> mulVectorNumber(List<double> v1, double num) {
        List<double> result = new List<double>(v1.length);
        for (int i = 0; i < v1.length; i++) {
            result[i] = v1[i] * num;
        }
        return result;
    }
}
"""

    interpreter = DartInterpreter()
    utils.assert_code_equal(interpreter.interpret(expr), expected_code)


def test_exp_expr():
    expr = ast.ExpExpr(ast.NumVal(1.0))

    expected_code = """
import 'dart:math';
class Model {
    static double score(List<double> input) {
        return exp(1.0);
    }
}
"""

    interpreter = DartInterpreter()
    utils.assert_code_equal(interpreter.interpret(expr), expected_code)


def test_pow_expr():
    expr = ast.PowExpr(ast.NumVal(2.0), ast.NumVal(3.0))

    expected_code = """
import 'dart:math';
class Model {
    static double score(List<double> input) {
        return pow(2.0, 3.0);
    }
}
"""

    interpreter = DartInterpreter()
    utils.assert_code_equal(interpreter.interpret(expr), expected_code)


def test_tanh_expr():
    expr = ast.TanhExpr(ast.NumVal(2.0))

    expected_code = """
import 'dart:math';
class Model {
    static double score(List<double> input) {
        return tanh(2.0);
    }
    static double tanh(double x) {
        if (x > 22.0)
            return 1.0;
        if (x < -22.0)
            return -1.0;
        return ((exp(2*x) - 1)/(exp(2*x) + 1));
    }
}
"""
    interpreter = DartInterpreter()
    utils.assert_code_equal(interpreter.interpret(expr), expected_code)


def test_reused_expr():
    reused_expr = ast.ExpExpr(ast.NumVal(1.0), to_reuse=True)
    expr = ast.BinNumExpr(reused_expr, reused_expr, ast.BinNumOpType.DIV)

    expected_code = """
import 'dart:math';
class Model {
    static double score(List<double> input) {
        double var0;
        var0 = exp(1.0);
        return (var0) / (var0);
    }
}
"""

    interpreter = DartInterpreter()
    utils.assert_code_equal(interpreter.interpret(expr), expected_code)
