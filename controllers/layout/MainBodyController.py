

class MainBodyController:
    def __init__(self, this):
        self.this = this

    def redirect_to(self, view_name):
        if view_name in self.this.views:
            self.this.stack_widget.setCurrentWidget(self.this.views[view_name])