from m2cgen.interpreter.base import BaseInterpreter
from m2cgen.ast import BinNumOpType


class BasicInterpreter(BaseInterpreter):

    def interpret_num_val(self, expr):
        return expr.value

    def interpret_bin_num_expr(self, expr):
        left_val = self._do_interpret(expr.left)
        right_val = self._do_interpret(expr.right)
        ops = {
            BinNumOpType.ADD: lambda x, y: x + y,
            BinNumOpType.SUB: lambda x, y: x - y,
            BinNumOpType.MUL: lambda x, y: x * y,
            BinNumOpType.DIV: lambda x, y: x / y,
        }
        return ops[expr.op](left_val, right_val)
