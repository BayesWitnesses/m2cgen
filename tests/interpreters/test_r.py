from m2cgen import ast
from m2cgen.interpreters import RInterpreter
from tests import utils


def test_if_expr():
    expr = ast.IfExpr(
        ast.CompExpr(ast.NumVal(1), ast.FeatureRef(0), ast.CompOpType.EQ),
        ast.NumVal(2),
        ast.NumVal(3))

    expected_code = """
score <- function(input) {
    if ((1.0) == (input[1])) {
        var0 <- 2.0
    } else {
        var0 <- 3.0
    }
    return(var0)
}
"""

    interpreter = RInterpreter()
    utils.assert_code_equal(interpreter.interpret(expr), expected_code)


def test_bin_num_expr():
    expr = ast.BinNumExpr(
        ast.BinNumExpr(
            ast.FeatureRef(0), ast.NumVal(-2), ast.BinNumOpType.DIV),
        ast.NumVal(2),
        ast.BinNumOpType.MUL)

    expected_code = """
score <- function(input) {
    return(((input[1]) / (-2.0)) * (2.0))
}
"""

    interpreter = RInterpreter()
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
score <- function(input) {
    if ((1.0) == (1.0)) {
        var1 <- 1.0
    } else {
        var1 <- 2.0
    }
    if (((var1) + (2.0)) >= ((1.0) / (2.0))) {
        var0 <- 1.0
    } else {
        var0 <- input[1]
    }
    return(var0)
}
"""

    interpreter = RInterpreter()
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
score <- function(input) {
    if ((1.0) == (1.0)) {
        var1 <- 1.0
    } else {
        var1 <- 2.0
    }
    if ((1.0) == ((var1) + (2.0))) {
        if ((1.0) == (1.0)) {
            var2 <- 1.0
        } else {
            var2 <- 2.0
        }
        if ((1.0) == ((var2) + (2.0))) {
            var0 <- input[3]
        } else {
            var0 <- 2.0
        }
    } else {
        var0 <- 2.0
    }
    return(var0)
}
"""

    interpreter = RInterpreter()
    utils.assert_code_equal(interpreter.interpret(expr), expected_code)


def test_raw_array():
    expr = ast.VectorVal([ast.NumVal(3), ast.NumVal(4)])

    expected_code = """
score <- function(input) {
    return(c(3.0, 4.0))
}
"""

    interpreter = RInterpreter()
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
score <- function(input) {
    if ((1.0) == (1.0)) {
        var0 <- c(1.0, 2.0)
    } else {
        var0 <- c(3.0, 4.0)
    }
    return(var0)
}
"""

    interpreter = RInterpreter()
    utils.assert_code_equal(interpreter.interpret(expr), expected_code)


def test_bin_vector_expr():
    expr = ast.BinVectorExpr(
        ast.VectorVal([ast.NumVal(1), ast.NumVal(2)]),
        ast.VectorVal([ast.NumVal(3), ast.NumVal(4)]),
        ast.BinNumOpType.ADD)

    expected_code = """
score <- function(input) {
    return((c(1.0, 2.0)) + (c(3.0, 4.0)))
}
"""

    interpreter = RInterpreter()
    utils.assert_code_equal(interpreter.interpret(expr), expected_code)


def test_bin_vector_num_expr():
    expr = ast.BinVectorNumExpr(
        ast.VectorVal([ast.NumVal(1), ast.NumVal(2)]),
        ast.NumVal(1),
        ast.BinNumOpType.MUL)

    expected_code = """
score <- function(input) {
    return((c(1.0, 2.0)) * (1.0))
}
"""

    interpreter = RInterpreter()
    utils.assert_code_equal(interpreter.interpret(expr), expected_code)


class CustomRInterpreter(RInterpreter):
    bin_depth_threshold = 2


def test_depth_threshold_with_bin_expr():
    expr = ast.NumVal(1)
    for _ in range(4):
        expr = ast.BinNumExpr(ast.NumVal(1), expr, ast.BinNumOpType.ADD)

    interpreter = CustomRInterpreter()

    expected_code = """
score <- function(input) {
    var0 <- (1.0) + ((1.0) + (1.0))
    return((1.0) + ((1.0) + (var0)))
}
"""

    utils.assert_code_equal(interpreter.interpret(expr), expected_code)


def test_depth_threshold_without_bin_expr():
    expr = ast.NumVal(1)
    for _ in range(4):
        expr = ast.IfExpr(
            ast.CompExpr(
                ast.NumVal(1), ast.NumVal(1), ast.CompOpType.EQ),
            ast.NumVal(1),
            expr)

    interpreter = CustomRInterpreter()

    expected_code = """
score <- function(input) {
    if ((1.0) == (1.0)) {
        var0 <- 1.0
    } else {
        if ((1.0) == (1.0)) {
            var0 <- 1.0
        } else {
            if ((1.0) == (1.0)) {
                var0 <- 1.0
            } else {
                if ((1.0) == (1.0)) {
                    var0 <- 1.0
                } else {
                    var0 <- 1.0
                }
            }
        }
    }
    return(var0)
}
"""

    utils.assert_code_equal(interpreter.interpret(expr), expected_code)


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

    interpreter = CustomRInterpreter()

    expected_code = """
score <- function(input) {
    if (((1.0) + ((1.0) + (1.0))) == (1.0)) {
        var0 <- 1.0
    } else {
        if (((1.0) + ((1.0) + (1.0))) == (1.0)) {
            var0 <- 1.0
        } else {
            if (((1.0) + ((1.0) + (1.0))) == (1.0)) {
                var0 <- 1.0
            } else {
                if (((1.0) + ((1.0) + (1.0))) == (1.0)) {
                    var0 <- 1.0
                } else {
                    var0 <- 1.0
                }
            }
        }
    }
    return(var0)
}
"""

    utils.assert_code_equal(interpreter.interpret(expr), expected_code)


def test_deep_mixed_exprs_exceeding_threshold():
    expr = ast.NumVal(1)
    for i in range(4):
        inner = ast.NumVal(1)
        for j in range(4):
            inner = ast.BinNumExpr(ast.NumVal(i), inner, ast.BinNumOpType.ADD)

        expr = ast.IfExpr(
            ast.CompExpr(
                inner, ast.NumVal(j), ast.CompOpType.EQ),
            ast.NumVal(1),
            expr)

    interpreter = RInterpreter()
    interpreter.bin_depth_threshold = 1
    interpreter.ast_size_check_frequency = 2
    interpreter.ast_size_per_subroutine_threshold = 6

    expected_code = """
score <- function(input) {
    var1 <- subroutine0(input)
    if (((3.0) + (var1)) == (3.0)) {
        var0 <- 1.0
    } else {
        var2 <- subroutine1(input)
        if (((2.0) + (var2)) == (3.0)) {
            var0 <- 1.0
        } else {
            var3 <- subroutine2(input)
            if (((1.0) + (var3)) == (3.0)) {
                var0 <- 1.0
            } else {
                var4 <- subroutine3(input)
                if (((0.0) + (var4)) == (3.0)) {
                    var0 <- 1.0
                } else {
                    var0 <- 1.0
                }
            }
        }
    }
    return(var0)
}
subroutine0 <- function(input) {
    var0 <- (3.0) + (1.0)
    var1 <- (3.0) + (var0)
    return((3.0) + (var1))
}
subroutine1 <- function(input) {
    var0 <- (2.0) + (1.0)
    var1 <- (2.0) + (var0)
    return((2.0) + (var1))
}
subroutine2 <- function(input) {
    var0 <- (1.0) + (1.0)
    var1 <- (1.0) + (var0)
    return((1.0) + (var1))
}
subroutine3 <- function(input) {
    var0 <- (0.0) + (1.0)
    var1 <- (0.0) + (var0)
    return((0.0) + (var1))
}
"""

    utils.assert_code_equal(interpreter.interpret(expr), expected_code)


def test_abs_expr():
    expr = ast.AbsExpr(ast.NumVal(-1.0))

    expected_code = """
score <- function(input) {
    return(abs(-1.0))
}
"""

    interpreter = RInterpreter()
    utils.assert_code_equal(interpreter.interpret(expr), expected_code)


def test_exp_expr():
    expr = ast.ExpExpr(ast.NumVal(1.0))

    expected_code = """
score <- function(input) {
    return(exp(1.0))
}
"""

    interpreter = RInterpreter()
    utils.assert_code_equal(interpreter.interpret(expr), expected_code)


def test_pow_expr():
    expr = ast.PowExpr(ast.NumVal(2.0), ast.NumVal(3.0))

    expected_code = """
score <- function(input) {
    return((2.0) ^ (3.0))
}
"""

    interpreter = RInterpreter()
    utils.assert_code_equal(interpreter.interpret(expr), expected_code)


def test_sqrt_expr():
    expr = ast.SqrtExpr(ast.NumVal(2.0))

    expected_code = """
score <- function(input) {
    return(sqrt(2.0))
}
"""

    interpreter = RInterpreter()
    utils.assert_code_equal(interpreter.interpret(expr), expected_code)


def test_tanh_expr():
    expr = ast.TanhExpr(ast.NumVal(2.0))

    expected_code = """
score <- function(input) {
    return(tanh(2.0))
}
"""

    interpreter = RInterpreter()
    utils.assert_code_equal(interpreter.interpret(expr), expected_code)


def test_log_expr():
    expr = ast.LogExpr(ast.NumVal(2.0))

    expected_code = """
score <- function(input) {
    return(log(2.0))
}
"""

    interpreter = RInterpreter()
    utils.assert_code_equal(interpreter.interpret(expr), expected_code)


def test_log1p_expr():
    expr = ast.Log1pExpr(ast.NumVal(2.0))

    expected_code = """
score <- function(input) {
    return(log1p(2.0))
}
"""

    interpreter = RInterpreter()
    utils.assert_code_equal(interpreter.interpret(expr), expected_code)


def test_atan_expr():
    expr = ast.AtanExpr(ast.NumVal(2.0))

    expected_code = """
score <- function(input) {
    return(atan(2.0))
}
"""

    interpreter = RInterpreter()
    utils.assert_code_equal(interpreter.interpret(expr), expected_code)


def test_softmax_expr():
    expr = ast.SoftmaxExpr([ast.NumVal(2.0), ast.NumVal(3.0)])

    expected_code = """
softmax <- function (x) {
    m <- max(x)
    exps <- exp(x - m)
    s <- sum(exps)
    return(exps / s)
}
score <- function(input) {
    return(softmax(c(2.0, 3.0)))
}
"""

    interpreter = RInterpreter()
    utils.assert_code_equal(interpreter.interpret(expr), expected_code)


def test_sigmoid_expr():
    expr = ast.SigmoidExpr(ast.NumVal(2.0))

    expected_code = """
sigmoid <- function(x) {
    if (x < 0.0) {
        z <- exp(x)
        return(z / (1.0 + z))
    }
    return(1.0 / (1.0 + exp(-x)))
}
score <- function(input) {
    return(sigmoid(2.0))
}
"""

    interpreter = RInterpreter()
    utils.assert_code_equal(interpreter.interpret(expr), expected_code)


def test_reused_expr():
    reused_expr = ast.ExpExpr(ast.NumVal(1.0), to_reuse=True)
    expr = ast.BinNumExpr(reused_expr, reused_expr, ast.BinNumOpType.DIV)

    expected_code = """
score <- function(input) {
    var0 <- exp(1.0)
    return((var0) / (var0))
}
"""

    interpreter = RInterpreter()
    utils.assert_code_equal(interpreter.interpret(expr), expected_code)
