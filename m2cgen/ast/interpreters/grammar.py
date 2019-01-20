from string import Template


class GrammarExpression:
    """
    Simple wrapper around string.Template to provide readable
    __str__ method.
    """

    def __init__(self, template):
        self._template = template
        self.template = Template(template)

    def __call__(self, **kwargs):
        return self.template.substitute(**kwargs)

    def __str__(self):
        return "GrammarExpression: {}".format(self.template)


class GrammarMetaclass(type):
    """
    Probably overengineering. Just to make attributes of grammar
    implicitly templates.
    """

    def __init__(self, *args, **kwargs):
        super(GrammarMetaclass, self).__init__(*args, **kwargs)

    def __new__(cls, name, bases, namespace):
        new_dict = {}

        if name == "BaseGrammar":
            return super().__new__(cls, name, bases, namespace)

        for name, value in namespace.items():
            if name.startswith("__"):
                new_dict[name] = value
                continue
            new_dict[name] = GrammarExpression(value)

        return super().__new__(cls, name, bases, new_dict)


class BaseGrammar(metaclass=GrammarMetaclass):
    num_value = NotImplemented
    comp_expression = NotImplemented
    bin_num_expression = NotImplemented
    return_statement = NotImplemented
    if_statement = NotImplemented
    array_index_access = NotImplemented
