
class BaseCodeGenerator:

    code = None

    def __init__(self):
        self.reset_state()

    def reset_state(self):
        raise NotImplementedError
