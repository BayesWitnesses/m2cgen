from m2cgen.assemblers.base import ModelAssembler


class BaseMetaAssembler(ModelAssembler):

    def assemble(self):
        # import here to avoid circular import error
        from m2cgen.assemblers import get_assembler_cls
        base_model = self._get_base_model()
        return get_assembler_cls(base_model)(base_model).assemble()

    def _get_base_model(self):
        raise NotImplementedError


class RANSACModelAssembler(BaseMetaAssembler):

    def _get_base_model(self):
        return self.model.estimator_
