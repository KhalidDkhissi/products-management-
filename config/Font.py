from PyQt5.QtGui import QFont

class Font:
    def __init__(self):
        self.family = "Lucida Sans Typewriter"
        self.italic = False
    
    def setFont(self, size=12, weight=300):
        return QFont(self.family, size, weight, self.italic)
