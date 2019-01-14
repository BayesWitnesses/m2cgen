from m2cgen.interpreter.base import BaseInterpreter


class JavaGenerator(BaseInterpreter):
    def __init__(self, package_name=None, model_name='Model'):
        self._var_idx = 0
        self._code = ''
        self._package_name = package_name
        self._model_name = model_name

    def interpret(self, expr):
        self._code = ''
        self._var_idx = 0
        if self._package_name:
            self._code += 'package ' + self._package_name + ';\n'
        self._add_class_def(self._model_name)
        self._add_method_def(name='score',
                             args=[('double[]', 'input')],
                             return_type='double')
        last_result = self._do_interpret(expr)
        self._code += 'return ' + last_result + ';\n'
        self._code += '}\n'  # Close method.
        self._code += '}\n'  # Close class.
        return self._code

    def interpret_num_val(self, expr):
        return str(expr.value)

    def interpret_bin_num_expr(self, expr):
        left_val = self._do_interpret(expr.left)
        right_val = self._do_interpret(expr.right)
        expr = left_val + ' ' + expr.op.value + ' ' + right_val
        return self._add_var_def(expr)

    def interpret_feature_ref(self, expr):
        index = expr.index
        return 'input[' + str(index) + ']'

    def _add_class_def(self, class_name, modifier='public'):
        class_def = ''
        class_def += modifier + ' class ' + class_name + ' {\n'
        class_def += '\n'
        self._code += class_def

    def _add_method_def(self, name, args, return_type, modifier='public'):
        method_def = modifier + ' ' + return_type + ' ' + name + '('
        method_def += ','.join([t + ' ' + n for t, n in args])
        method_def += ') {\n'
        self._code += method_def

    def _add_var_def(self, expr, var_type = 'double'):
        var_name = 'var' + str(self._var_idx)
        self._var_idx += 1
        self._code += var_type + ' ' + var_name + ' = ' + expr + ';\n'
        return var_name
