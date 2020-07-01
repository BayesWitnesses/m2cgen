import contextlib

from m2cgen.interpreters.code_generator import CLikeCodeGenerator


class CSharpCodeGenerator(CLikeCodeGenerator):

    scalar_type = "double"
    vector_type = "double[]"

    def add_class_def(self, class_name, modifier="public"):
        class_def = f"{modifier} static class {class_name} {{"
        self.add_code_line(class_def)
        self.increase_indent()

    def add_method_def(self, name, args, is_vector_output,
                       modifier="private"):
        return_type = self._get_var_declare_type(is_vector_output)
        func_args = ",".join([
            f"{self._get_var_declare_type(is_vector)} {n}"
            for is_vector, n in args])
        method_def = f"{modifier} static {return_type} {name}({func_args}) {{"
        self.add_code_line(method_def)
        self.increase_indent()

    def add_namespace_def(self, namespace):
        namespace_def = f"namespace {namespace} {{"
        self.add_code_line(namespace_def)
        self.increase_indent()

    @contextlib.contextmanager
    def class_definition(self, class_name, modifier="public"):
        self.add_class_def(class_name, modifier=modifier)
        yield
        self.add_block_termination()

    @contextlib.contextmanager
    def method_definition(self, name, args, is_vector_output,
                          modifier="private"):
        self.add_method_def(name, args, is_vector_output, modifier=modifier)
        yield
        self.add_block_termination()

    @contextlib.contextmanager
    def namespace_definition(self, namespace):
        self.add_namespace_def(namespace)
        yield
        self.add_block_termination()

    def vector_init(self, values):
        return (f"new double[{len(values)}] {{{', '.join(values)}}}")

    def _get_var_declare_type(self, is_vector):
        return (
            self.vector_type if is_vector
            else self.scalar_type)

    def add_dependency(self, dep, modifier="static"):
        self.prepend_code_line(f"using {modifier} {dep};")
