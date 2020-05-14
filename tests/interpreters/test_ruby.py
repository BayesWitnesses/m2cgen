from m2cgen import ast
from m2cgen.interpreters import RubyInterpreter
from tests import utils


def test_if_expr():
    expr = ast.IfExpr(
        ast.CompExpr(ast.NumVal(1), ast.FeatureRef(0), ast.CompOpType.EQ),
        ast.NumVal(2),
        ast.NumVal(3))

    expected_code = """
def score(input)
    if (1) == (input[0])
        var0 = 2
    else
        var0 = 3
    end
    var0
end
"""

    interpreter = RubyInterpreter()
    utils.assert_code_equal(interpreter.interpret(expr), expected_code)


def test_bin_num_expr():
    expr = ast.BinNumExpr(
        ast.BinNumExpr(
            ast.FeatureRef(0), ast.NumVal(-2), ast.BinNumOpType.DIV),
        ast.NumVal(2),
        ast.BinNumOpType.MUL)

    expected_code = """
def score(input)
    ((input[0]).fdiv(-2)) * (2)
end
"""

    interpreter = RubyInterpreter()
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
def score(input)
    if (1) == (1)
        var1 = 1
    else
        var1 = 2
    end
    if ((var1) + (2)) >= ((1).fdiv(2))
        var0 = 1
    else
        var0 = input[0]
    end
    var0
end
"""

    interpreter = RubyInterpreter()
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
def score(input)
    if (1) == (1)
        var1 = 1
    else
        var1 = 2
    end
    if (1) == ((var1) + (2))
        if (1) == (1)
            var2 = 1
        else
            var2 = 2
        end
        if (1) == ((var2) + (2))
            var0 = input[2]
        else
            var0 = 2
        end
    else
        var0 = 2
    end
    var0
end
"""

    interpreter = RubyInterpreter()
    utils.assert_code_equal(interpreter.interpret(expr), expected_code)


def test_raw_array():
    expr = ast.VectorVal([ast.NumVal(3), ast.NumVal(4)])

    expected_code = """
def score(input)
    [3, 4]
end
"""

    interpreter = RubyInterpreter()
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
def score(input)
    if (1) == (1)
        var0 = [1, 2]
    else
        var0 = [3, 4]
    end
    var0
end
"""

    interpreter = RubyInterpreter()
    utils.assert_code_equal(interpreter.interpret(expr), expected_code)


def test_bin_vector_expr():
    expr = ast.BinVectorExpr(
        ast.VectorVal([ast.NumVal(1), ast.NumVal(2)]),
        ast.VectorVal([ast.NumVal(3), ast.NumVal(4)]),
        ast.BinNumOpType.ADD)

    expected_code = """
def add_vectors(v1, v2)
    v1.zip(v2).map { |x, y| x + y }
end
def mul_vector_number(v1, num)
    v1.map { |i| i * num }
end
def score(input)
    add_vectors([1, 2], [3, 4])
end
"""

    interpreter = RubyInterpreter()
    utils.assert_code_equal(interpreter.interpret(expr), expected_code)


def test_bin_vector_num_expr():
    expr = ast.BinVectorNumExpr(
        ast.VectorVal([ast.NumVal(1), ast.NumVal(2)]),
        ast.NumVal(1),
        ast.BinNumOpType.MUL)

    expected_code = """
def add_vectors(v1, v2)
    v1.zip(v2).map { |x, y| x + y }
end
def mul_vector_number(v1, num)
    v1.map { |i| i * num }
end
def score(input)
    mul_vector_number([1, 2], 1)
end
"""

    interpreter = RubyInterpreter()
    utils.assert_code_equal(interpreter.interpret(expr), expected_code)


def test_exp_expr():
    expr = ast.ExpExpr(ast.NumVal(1.0))

    expected_code = """
def score(input)
    Math.exp(1.0)
end
"""

    interpreter = RubyInterpreter()
    utils.assert_code_equal(interpreter.interpret(expr), expected_code)


def test_pow_expr():
    expr = ast.PowExpr(ast.NumVal(2.0), ast.NumVal(3.0))

    expected_code = """
def score(input)
    (2.0) ** (3.0)
end
"""

    interpreter = RubyInterpreter()
    utils.assert_code_equal(interpreter.interpret(expr), expected_code)


def test_sqrt_expr():
    expr = ast.SqrtExpr(ast.NumVal(2.0))

    expected_code = """
def score(input)
    Math.sqrt(2.0)
end
"""

    interpreter = RubyInterpreter()
    utils.assert_code_equal(interpreter.interpret(expr), expected_code)


def test_tanh_expr():
    expr = ast.TanhExpr(ast.NumVal(2.0))

    expected_code = """
def score(input)
    Math.tanh(2.0)
end
"""

    interpreter = RubyInterpreter()
    utils.assert_code_equal(interpreter.interpret(expr), expected_code)


def test_reused_expr():
    reused_expr = ast.ExpExpr(ast.NumVal(1.0), to_reuse=True)
    expr = ast.BinNumExpr(reused_expr, reused_expr, ast.BinNumOpType.DIV)

    expected_code = """
def score(input)
    var0 = Math.exp(1.0)
    (var0).fdiv(var0)
end
"""

    interpreter = RubyInterpreter()
    utils.assert_code_equal(interpreter.interpret(expr), expected_code)
