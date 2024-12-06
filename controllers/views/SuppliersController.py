from config.Static import Static


class SuppliersController:
    def __init__(self, this):
        self.this = this

        self._static_ = Static()