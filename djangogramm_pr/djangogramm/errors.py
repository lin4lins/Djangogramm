class InvalidFormException(Exception):
    def __init__(self, form=None):
        self.form = form
        super().__init__()
