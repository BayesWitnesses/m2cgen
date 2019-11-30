import contextlib

from m2cgen.interpreters.code_generator import CLikeCodeGenerator


class CSharpCodeGenerator(CLikeCodeGenerator):

    scalar_type = "double"
    vector_type = "double[]"

    def __init__(self, *args, **kwargs):
        super(CSharpCodeGenerator, self).__init__(*args, **kwargs)

    def add_class_def(self, class_name, modifier="public"):
        class_def = modifier + " static class " + class_name + " {"
        self.add_code_line(class_def)
        self.increase_indent()

    def add_method_def(self, name, args, is_vector_output,
                       modifier="private"):
        return_type = self._get_var_declare_type(is_vector_output)
        method_def = modifier + " static " + return_type + " " + name + "("
        method_def += ",".join([
            self._get_var_declare_type(is_vector) + " " + n
            for is_vector, n in args])
        method_def += ") {"
        self.add_code_line(method_def)
        self.increase_indent()

    def add_namespace_def(self, namespace):
        namespace_def = "namespace " + namespace + " {"
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
        return ("new double[{}] {{".format(len(values)) +
                ", ".join(values) + "}")

    def _get_var_declare_type(self, is_vector):
        return (
            self.vector_type if is_vector
            else self.scalar_type)

    def add_dependency(self, dep, modifier="static"):
        dep_str = "using {0} {1};".format(modifier, dep)
        self.prepend_code_line(dep_str)
