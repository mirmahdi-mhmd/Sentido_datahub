from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QMainWindow, QHBoxLayout, QWidget

from View.MainElements.IconPath import icon
from View.Pages.PagesStack import PagesStack
from View.Sidebar.Sidebar import Sidebar

class MainWindow(QMainWindow):
    def __init__(self,theme,*pages):
        super().__init__()
        self.is_dark = theme
        self.setMinimumWidth(850)
        self.setMinimumHeight(600)
        self.setWindowTitle("Sentido datahub")
        self.set_icon()

        self.navbar = Sidebar(self.is_dark)
        self.stack = PagesStack(*pages)

        self.setup_widgets()

    def setup_widgets(self):
        main_widget = QWidget()
        main_layout = QHBoxLayout(main_widget)
        main_layout.addWidget(self.navbar)
        main_layout.addWidget(self.stack)
        self.setCentralWidget(main_widget)

    def set_icon(self):
        if self.is_dark:
            self.setWindowIcon(QIcon(icon("Sentido_dark.jpg")))
        else:
            self.setWindowIcon(QIcon(icon("Sentido_light.jpg")))