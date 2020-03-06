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
    if ((1) == (input[1])) {
        var0 <- 2
    } else {
        var0 <- 3
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
    return(((input[1]) / (-2)) * (2))
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
    if ((1) == (1)) {
        var1 <- 1
    } else {
        var1 <- 2
    }
    if (((var1) + (2)) >= ((1) / (2))) {
        var0 <- 1
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
    if ((1) == (1)) {
        var1 <- 1
    } else {
        var1 <- 2
    }
    if ((1) == ((var1) + (2))) {
        if ((1) == (1)) {
            var2 <- 1
        } else {
            var2 <- 2
        }
        if ((1) == ((var2) + (2))) {
            var0 <- input[3]
        } else {
            var0 <- 2
        }
    } else {
        var0 <- 2
    }
    return(var0)
}
"""

    interpreter = RInterpreter()
    utils.assert_code_equal(interpreter.interpret(expr), expected_code)


def test_subroutine():
    expr = ast.BinNumExpr(
        ast.FeatureRef(0),
        ast.SubroutineExpr(
            ast.BinNumExpr(
                ast.NumVal(1), ast.NumVal(2), ast.BinNumOpType.ADD)),
        ast.BinNumOpType.MUL)

    expected_code = """
score <- function(input) {
    return((input[1]) * (subroutine0(input)))
}
subroutine0 <- function(input) {
    return((1) + (2))
}
"""

    interpreter = RInterpreter()
    utils.assert_code_equal(interpreter.interpret(expr), expected_code)


def test_raw_array():
    expr = ast.VectorVal([ast.NumVal(3), ast.NumVal(4)])

    expected_code = """
score <- function(input) {
    return(c(3, 4))
}
"""

    interpreter = RInterpreter()
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
score <- function(input) {
    return(subroutine0(input))
}
subroutine0 <- function(input) {
    if ((1) == (1)) {
        var0 <- c(1, 2)
    } else {
        var0 <- c(3, 4)
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
    return((c(1, 2)) + (c(3, 4)))
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
    return((c(1, 2)) * (1))
}
"""

    interpreter = RInterpreter()
    utils.assert_code_equal(interpreter.interpret(expr), expected_code)


class CustomRInterpreter(RInterpreter):
    bin_depth_threshold = 2


def test_depth_threshold_with_bin_expr():
    expr = ast.NumVal(1)
    for i in range(4):
        expr = ast.BinNumExpr(ast.NumVal(1), expr, ast.BinNumOpType.ADD)

    interpreter = CustomRInterpreter()

    expected_code = """
score <- function(input) {
    var0 <- (1) + ((1) + (1))
    return((1) + ((1) + (var0)))
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

    interpreter = CustomRInterpreter()

    expected_code = """
score <- function(input) {
    if ((1) == (1)) {
        var0 <- 1
    } else {
        if ((1) == (1)) {
            var0 <- 1
        } else {
            if ((1) == (1)) {
                var0 <- 1
            } else {
                if ((1) == (1)) {
                    var0 <- 1
                } else {
                    var0 <- 1
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
    for i in range(4):
        inner = ast.NumVal(1)
        for i in range(2):
            inner = ast.BinNumExpr(ast.NumVal(1), inner, ast.BinNumOpType.ADD)

        expr = ast.IfExpr(
            ast.CompExpr(
                inner, ast.NumVal(1), ast.CompOpType.EQ),
            ast.NumVal(1),
            expr)

    interpreter = CustomRInterpreter()

    expected_code = """
score <- function(input) {
    if (((1) + ((1) + (1))) == (1)) {
        var0 <- 1
    } else {
        if (((1) + ((1) + (1))) == (1)) {
            var0 <- 1
        } else {
            if (((1) + ((1) + (1))) == (1)) {
                var0 <- 1
            } else {
                if (((1) + ((1) + (1))) == (1)) {
                    var0 <- 1
                } else {
                    var0 <- 1
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
        for i in range(4):
            inner = ast.BinNumExpr(ast.NumVal(1), inner, ast.BinNumOpType.ADD)

        expr = ast.IfExpr(
            ast.CompExpr(
                inner, ast.NumVal(1), ast.CompOpType.EQ),
            ast.NumVal(1),
            expr)

    interpreter = CustomRInterpreter()

    expected_code = """
score <- function(input) {
    var1 <- (1) + ((1) + (1))
    if (((1) + ((1) + (var1))) == (1)) {
        var0 <- 1
    } else {
        var2 <- (1) + ((1) + (1))
        if (((1) + ((1) + (var2))) == (1)) {
            var0 <- 1
        } else {
            var3 <- (1) + ((1) + (1))
            if (((1) + ((1) + (var3))) == (1)) {
                var0 <- 1
            } else {
                var4 <- (1) + ((1) + (1))
                if (((1) + ((1) + (var4))) == (1)) {
                    var0 <- 1
                } else {
                    var0 <- 1
                }
            }
        }
    }
    return(var0)
}
"""

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
