from m2cgen import assemblers


class BaseMetaAssembler(assemblers.base.ModelAssembler):

    def assemble(self):
        base_model = self._get_base_model()
        return assemblers.get_assembler_cls(base_model)(base_model).assemble()

    def _get_base_model(self):
        raise NotImplementedError


class RANSACModelAssembler(BaseMetaAssembler):

    def _get_base_model(self):
        return self.model.estimator_
