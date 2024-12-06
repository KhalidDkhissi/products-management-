from config.Static import Static


class ProductsController:
    def __init__(self, this):
        self.this = this

        self._static_ = Static()