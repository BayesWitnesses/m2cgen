from m2cgen import ast
from m2cgen.interpreters import CSharpInterpreter
from tests import utils


def test_if_expr():
    expr = ast.IfExpr(
        ast.CompExpr(ast.NumVal(1), ast.FeatureRef(0), ast.CompOpType.EQ),
        ast.NumVal(2),
        ast.NumVal(3))

    expected_code = """
namespace ML {
    public static class Model {
        public static double Score(double[] input) {
            double var0;
            if ((1) == (input[0])) {
                var0 = 2;
            } else {
                var0 = 3;
            }
            return var0;
        }
    }
}
"""

    interpreter = CSharpInterpreter()
    utils.assert_code_equal(interpreter.interpret(expr), expected_code)


def test_bin_num_expr():
    expr = ast.BinNumExpr(
        ast.BinNumExpr(
            ast.FeatureRef(0), ast.NumVal(-2), ast.BinNumOpType.DIV),
        ast.NumVal(2),
        ast.BinNumOpType.MUL)

    expected_code = """
namespace ML {
    public static class Model {
        public static double Score(double[] input) {
            return ((input[0]) / (-2)) * (2);
        }
    }
}
"""

    interpreter = CSharpInterpreter()
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
namespace ML {
    public static class Model {
        public static double Score(double[] input) {
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
}
"""

    interpreter = CSharpInterpreter()
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
namespace ML {
    public static class Model {
        public static double Score(double[] input) {
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
}
"""

    interpreter = CSharpInterpreter()
    utils.assert_code_equal(interpreter.interpret(expr), expected_code)


def test_namespace():
    expr = ast.NumVal(1)

    expected_code = """
namespace ML.Tests {
    public static class Model {
        public static double Score(double[] input) {
            return 1;
        }
    }
}
"""

    interpreter = CSharpInterpreter(namespace="ML.Tests")
    utils.assert_code_equal(interpreter.interpret(expr), expected_code)


def test_class_name():
    expr = ast.NumVal(1)

    expected_code = """
namespace ML {
    public static class TestModel {
        public static double Score(double[] input) {
            return 1;
        }
    }
}
"""

    interpreter = CSharpInterpreter(class_name="TestModel")
    utils.assert_code_equal(interpreter.interpret(expr), expected_code)


def test_raw_array():
    expr = ast.VectorVal([ast.NumVal(3), ast.NumVal(4)])

    expected_code = """
namespace ML {
    public static class Model {
        public static double[] Score(double[] input) {
            return new double[2] {3, 4};
        }
    }
}
"""

    interpreter = CSharpInterpreter()
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
namespace ML {
    public static class Model {
        public static double[] Score(double[] input) {
            double[] var0;
            if ((1) == (1)) {
                var0 = new double[2] {1, 2};
            } else {
                var0 = new double[2] {3, 4};
            }
            return var0;
        }
    }
}
"""

    interpreter = CSharpInterpreter()
    utils.assert_code_equal(interpreter.interpret(expr), expected_code)


def test_bin_vector_expr():
    expr = ast.BinVectorExpr(
        ast.VectorVal([ast.NumVal(1), ast.NumVal(2)]),
        ast.VectorVal([ast.NumVal(3), ast.NumVal(4)]),
        ast.BinNumOpType.ADD)

    expected_code = """
namespace ML {
    public static class Model {
        public static double[] Score(double[] input) {
            return AddVectors(new double[2] {1, 2}, new double[2] {3, 4});
        }
        private static double[] AddVectors(double[] v1, double[] v2) {
            double[] result = new double[v1.Length];
            for (int i = 0; i < v1.Length; ++i) {
                result[i] = v1[i] + v2[i];
            }
            return result;
        }
        private static double[] MulVectorNumber(double[] v1, double num) {
            double[] result = new double[v1.Length];
            for (int i = 0; i < v1.Length; ++i) {
                result[i] = v1[i] * num;
            }
            return result;
        }
    }
}
"""

    interpreter = CSharpInterpreter()
    utils.assert_code_equal(interpreter.interpret(expr), expected_code)


def test_bin_vector_num_expr():
    expr = ast.BinVectorNumExpr(
        ast.VectorVal([ast.NumVal(1), ast.NumVal(2)]),
        ast.NumVal(1),
        ast.BinNumOpType.MUL)

    expected_code = """
namespace ML {
    public static class Model {
        public static double[] Score(double[] input) {
            return MulVectorNumber(new double[2] {1, 2}, 1);
        }
        private static double[] AddVectors(double[] v1, double[] v2) {
            double[] result = new double[v1.Length];
            for (int i = 0; i < v1.Length; ++i) {
                result[i] = v1[i] + v2[i];
            }
            return result;
        }
        private static double[] MulVectorNumber(double[] v1, double num) {
            double[] result = new double[v1.Length];
            for (int i = 0; i < v1.Length; ++i) {
                result[i] = v1[i] * num;
            }
            return result;
        }
    }
}
"""

    interpreter = CSharpInterpreter()
    utils.assert_code_equal(interpreter.interpret(expr), expected_code)


def test_exp_expr():
    expr = ast.ExpExpr(ast.NumVal(1.0))

    expected_code = """
using static System.Math;
namespace ML {
    public static class Model {
        public static double Score(double[] input) {
            return Exp(1.0);
        }
    }
}
"""

    interpreter = CSharpInterpreter()
    utils.assert_code_equal(interpreter.interpret(expr), expected_code)


def test_pow_expr():
    expr = ast.PowExpr(ast.NumVal(2.0), ast.NumVal(3.0))

    expected_code = """
using static System.Math;
namespace ML {
    public static class Model {
        public static double Score(double[] input) {
            return Pow(2.0, 3.0);
        }
    }
}
"""

    interpreter = CSharpInterpreter()
    utils.assert_code_equal(interpreter.interpret(expr), expected_code)


def test_sqrt_expr():
    expr = ast.SqrtExpr(ast.NumVal(2.0))

    expected_code = """
using static System.Math;
namespace ML {
    public static class Model {
        public static double Score(double[] input) {
            return Sqrt(2.0);
        }
    }
}
"""

    interpreter = CSharpInterpreter()
    utils.assert_code_equal(interpreter.interpret(expr), expected_code)


def test_tanh_expr():
    expr = ast.TanhExpr(ast.NumVal(2.0))

    expected_code = """
using static System.Math;
namespace ML {
    public static class Model {
        public static double Score(double[] input) {
            return Tanh(2.0);
        }
    }
}
"""

    interpreter = CSharpInterpreter()
    utils.assert_code_equal(interpreter.interpret(expr), expected_code)


def test_reused_expr():
    reused_expr = ast.ExpExpr(ast.NumVal(1.0), to_reuse=True)
    expr = ast.BinNumExpr(reused_expr, reused_expr, ast.BinNumOpType.DIV)

    expected_code = """
using static System.Math;
namespace ML {
    public static class Model {
        public static double Score(double[] input) {
            double var0;
            var0 = Exp(1.0);
            return (var0) / (var0);
        }
    }
}
"""

    interpreter = CSharpInterpreter()
    utils.assert_code_equal(interpreter.interpret(expr), expected_code)
