from m2cgen import ast


def cmp_exprs(left, right):
    """Recursively compares two ast expressions."""

    if not isinstance(left, ast.Expr) and not isinstance(right, ast.Expr):
        assert left == right
        return True

    if isinstance(left, ast.Expr) and isinstance(right, ast.Expr):
        assert isinstance(left, type(right)), (
            "Expected instance of {}, received {}".format(
                type(right), type(left)))

        # Only compare attributes which don't start with __
        attrs_to_compare = filter(
            lambda attr_name: not attr_name.startswith('__'), dir(left))

        for attr_name in attrs_to_compare:
            assert cmp_exprs(
                getattr(left, attr_name), getattr(right, attr_name))

        return True

    return False
