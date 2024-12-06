from config.Static import Static


class OrdersController:
    def __init__(self, this):
        self.this = this

        self._static_ = Static()