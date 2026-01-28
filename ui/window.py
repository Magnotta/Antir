from PyQt6.QtWidgets import (
    QMainWindow,
    QTabWidget,
    QWidget
)

from ui.home_tab import HomeTab

class Window(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Antir, otários")
        self.resize(800, 600)

        self.tabs = QTabWidget()
        self.setCentralWidget(self.tabs)

        # Tabs
        self.home_tab = HomeTab()

        self.tabs.addTab(self.home_tab, "Home")