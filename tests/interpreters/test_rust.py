from itertools import product

import pytest

from m2cgen import ast
from m2cgen.interpreters import RustInterpreter

from tests.utils import assert_code_equal


def test_if_expr():
    expr = ast.IfExpr(
        ast.CompExpr(ast.NumVal(1), ast.FeatureRef(0), ast.CompOpType.EQ),
        ast.NumVal(2),
        ast.NumVal(3))

    expected_code = """
fn score(input: Vec<f64>) -> f64 {
    let var0: f64;
    if 1.0_f64 == input[0] {
        var0 = 2.0_f64;
    } else {
        var0 = 3.0_f64;
    }
    var0
}
"""

    interpreter = RustInterpreter()
    assert_code_equal(interpreter.interpret(expr), expected_code)


def test_bin_num_expr():
    expr = ast.BinNumExpr(
        ast.BinNumExpr(
            ast.FeatureRef(0), ast.NumVal(-2), ast.BinNumOpType.DIV),
        ast.NumVal(2),
        ast.BinNumOpType.MUL)

    expected_code = """
fn score(input: Vec<f64>) -> f64 {
    input[0] / -2.0_f64 * 2.0_f64
}
"""

    interpreter = RustInterpreter()
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
        op_code_line = f"1.0_f64 {op1.value} 1.0_f64 {op2.value} 1.0_f64"
    else:
        op_code_line = f"1.0_f64 {op1.value} (1.0_f64 {op2.value} 1.0_f64)"
    expected_code1 = f"""
fn score(input: Vec<f64>) -> f64 {{
    {op_code_line}
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
fn score(input: Vec<f64>) -> f64 {{
    1.0_f64 {op1.value} 1.0_f64 {op2.value} 1.0_f64
}}
"""

    interpreter = RustInterpreter()
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
fn score(input: Vec<f64>) -> f64 {
    let var0: f64;
    let var1: f64;
    if 1.0_f64 == 1.0_f64 {
        var1 = 1.0_f64;
    } else {
        var1 = 2.0_f64;
    }
    if var1 + 2.0_f64 >= 1.0_f64 / 2.0_f64 {
        var0 = 1.0_f64;
    } else {
        var0 = input[0];
    }
    var0
}
"""

    interpreter = RustInterpreter()
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
fn score(input: Vec<f64>) -> f64 {
    let var0: f64;
    let var1: f64;
    if 1.0_f64 == 1.0_f64 {
        var1 = 1.0_f64;
    } else {
        var1 = 2.0_f64;
    }
    if 1.0_f64 == var1 + 2.0_f64 {
        let var2: f64;
        if 1.0_f64 == 1.0_f64 {
            var2 = 1.0_f64;
        } else {
            var2 = 2.0_f64;
        }
        if 1.0_f64 == var2 + 2.0_f64 {
            var0 = input[2];
        } else {
            var0 = 2.0_f64;
        }
    } else {
        var0 = 2.0_f64;
    }
    var0
}
"""

    interpreter = RustInterpreter()
    assert_code_equal(interpreter.interpret(expr), expected_code)


def test_raw_array():
    expr = ast.VectorVal([ast.NumVal(3), ast.NumVal(4)])

    expected_code = """
fn score(input: Vec<f64>) -> Vec<f64> {
    vec![3.0_f64, 4.0_f64]
}
"""

    interpreter = RustInterpreter()
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
fn score(input: Vec<f64>) -> Vec<f64> {
    let var0: Vec<f64>;
    if 1.0_f64 != 1.0_f64 {
        var0 = vec![1.0_f64, 2.0_f64];
    } else {
        var0 = vec![3.0_f64, 4.0_f64];
    }
    var0
}
"""

    interpreter = RustInterpreter()
    assert_code_equal(interpreter.interpret(expr), expected_code)


def test_bin_vector_expr():
    expr = ast.BinVectorExpr(
        ast.VectorVal([ast.NumVal(1), ast.NumVal(2)]),
        ast.VectorVal([ast.NumVal(3), ast.NumVal(4)]),
        ast.BinNumOpType.ADD)

    expected_code = """
fn score(input: Vec<f64>) -> Vec<f64> {
    add_vectors(vec![1.0_f64, 2.0_f64], vec![3.0_f64, 4.0_f64])
}
fn add_vectors(v1: Vec<f64>, v2: Vec<f64>) -> Vec<f64> {
    v1.iter().zip(v2.iter()).map(|(&x, &y)| x + y).collect::<Vec<f64>>()
}
fn mul_vector_number(v1: Vec<f64>, num: f64) -> Vec<f64> {
    v1.iter().map(|&i| i * num).collect::<Vec<f64>>()
}
"""

    interpreter = RustInterpreter()
    assert_code_equal(interpreter.interpret(expr), expected_code)


def test_bin_vector_num_expr():
    expr = ast.BinVectorNumExpr(
        ast.VectorVal([ast.NumVal(1), ast.NumVal(2)]),
        ast.NumVal(1),
        ast.BinNumOpType.MUL)

    expected_code = """
fn score(input: Vec<f64>) -> Vec<f64> {
    mul_vector_number(vec![1.0_f64, 2.0_f64], 1.0_f64)
}
fn add_vectors(v1: Vec<f64>, v2: Vec<f64>) -> Vec<f64> {
    v1.iter().zip(v2.iter()).map(|(&x, &y)| x + y).collect::<Vec<f64>>()
}
fn mul_vector_number(v1: Vec<f64>, num: f64) -> Vec<f64> {
    v1.iter().map(|&i| i * num).collect::<Vec<f64>>()
}
"""

    interpreter = RustInterpreter()
    assert_code_equal(interpreter.interpret(expr), expected_code)


def test_abs_expr():
    expr = ast.AbsExpr(ast.NumVal(-1.0))

    expected_code = """
fn score(input: Vec<f64>) -> f64 {
    f64::abs(-1.0_f64)
}
"""

    interpreter = RustInterpreter()
    assert_code_equal(interpreter.interpret(expr), expected_code)


def test_exp_expr():
    expr = ast.ExpExpr(ast.NumVal(1.0))

    expected_code = """
fn score(input: Vec<f64>) -> f64 {
    f64::exp(1.0_f64)
}
"""

    interpreter = RustInterpreter()
    assert_code_equal(interpreter.interpret(expr), expected_code)


def test_pow_expr():
    expr = ast.PowExpr(ast.NumVal(2.0), ast.NumVal(3.0))

    expected_code = """
fn score(input: Vec<f64>) -> f64 {
    f64::powf(2.0_f64, 3.0_f64)
}
"""

    interpreter = RustInterpreter()
    assert_code_equal(interpreter.interpret(expr), expected_code)


def test_sqrt_expr():
    expr = ast.SqrtExpr(ast.NumVal(2.0))

    expected_code = """
fn score(input: Vec<f64>) -> f64 {
    f64::sqrt(2.0_f64)
}
"""

    interpreter = RustInterpreter()
    assert_code_equal(interpreter.interpret(expr), expected_code)


def test_tanh_expr():
    expr = ast.TanhExpr(ast.NumVal(2.0))

    expected_code = """
fn score(input: Vec<f64>) -> f64 {
    f64::tanh(2.0_f64)
}
"""

    interpreter = RustInterpreter()
    assert_code_equal(interpreter.interpret(expr), expected_code)


def test_log_expr():
    expr = ast.LogExpr(ast.NumVal(2.0))

    expected_code = """
fn score(input: Vec<f64>) -> f64 {
    f64::ln(2.0_f64)
}
"""

    interpreter = RustInterpreter()
    assert_code_equal(interpreter.interpret(expr), expected_code)


def test_log1p_expr():
    expr = ast.Log1pExpr(ast.NumVal(2.0))

    expected_code = """
fn score(input: Vec<f64>) -> f64 {
    f64::ln_1p(2.0_f64)
}
"""

    interpreter = RustInterpreter()
    assert_code_equal(interpreter.interpret(expr), expected_code)


def test_atan_expr():
    expr = ast.AtanExpr(ast.NumVal(2.0))

    expected_code = """
fn score(input: Vec<f64>) -> f64 {
    f64::atan(2.0_f64)
}
"""

    interpreter = RustInterpreter()
    assert_code_equal(interpreter.interpret(expr), expected_code)


def test_softmax_expr():
    expr = ast.SoftmaxExpr([ast.NumVal(2.0), ast.NumVal(3.0)])

    expected_code = """
fn score(input: Vec<f64>) -> Vec<f64> {
    softmax(vec![2.0_f64, 3.0_f64])
}
fn softmax(x: Vec<f64>) -> Vec<f64> {
    let size: usize = x.len();
    let m: f64 = x.iter().fold(std::f64::MIN, |a, b| a.max(*b));
    let mut exps: Vec<f64> = vec![0.0_f64; size];
    let mut s: f64 = 0.0_f64;
    for (i, &v) in x.iter().enumerate() {
        exps[i] = (v - m).exp();
        s += exps[i];
    }
    exps.iter().map(|&i| i / s).collect::<Vec<f64>>()
}
"""

    interpreter = RustInterpreter()
    assert_code_equal(interpreter.interpret(expr), expected_code)


def test_sigmoid_expr():
    expr = ast.SigmoidExpr(ast.NumVal(2.0))

    expected_code = """
fn score(input: Vec<f64>) -> f64 {
    sigmoid(2.0_f64)
}
fn sigmoid(x: f64) -> f64 {
    if x < 0.0_f64 {
        let z: f64 = x.exp();
        return z / (1.0_f64 + z);
    }
    1.0_f64 / (1.0_f64 + (-x).exp())
}
"""

    interpreter = RustInterpreter()
    assert_code_equal(interpreter.interpret(expr), expected_code)


def test_reused_expr():
    reused_expr = ast.ExpExpr(ast.NumVal(1.0), to_reuse=True)
    expr = ast.BinNumExpr(reused_expr, reused_expr, ast.BinNumOpType.DIV)

    expected_code = """
fn score(input: Vec<f64>) -> f64 {
    let var0: f64;
    var0 = f64::exp(1.0_f64);
    var0 / var0
}
"""

    interpreter = RustInterpreter()
    assert_code_equal(interpreter.interpret(expr), expected_code)


def test_unsupported_exprs():
    interpreter = RustInterpreter()

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
