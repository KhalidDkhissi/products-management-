import os

class Config:
    def __init__(self):
        self.path = os.getcwd()

    def get_path(self, *paths):
        path = ""

        for p in paths:
            path += str(p) + "\\"

        return os.path.join(self.path, path.rstrip("\\"))

    