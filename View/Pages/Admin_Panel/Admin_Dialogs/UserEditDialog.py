from PySide6.QtCore import Signal
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QDialog, QPushButton, QHBoxLayout, QVBoxLayout, QLabel, QLineEdit

from View.MainElements.IconPath import icon


class CustomerEditDialog(QDialog):
    edit_requested = Signal()
    close_requested = Signal()

    def __init__(self, theme):
        super(CustomerEditDialog, self).__init__()
        self.is_dark = theme
        self.setWindowTitle("Edit (Customer)")
        self.setMinimumSize(500, 250)
        self.setMaximumSize(650, 350)

        self.user_name = QLineEdit(self)
        self.user_username = QLineEdit(self)
        self.user_tel = QLineEdit(self)
        self.user_gmail = QLineEdit(self)

        self.edit_button = QPushButton("Edit", self)
        self.close_button = QPushButton("Close", self)

        layout = QVBoxLayout(self)
        self.setup_widgets(layout)
        self.setup_buttons(layout)
        self.setup_signals()
        self.setup_style()
        layout.insertStretch(2, 1)

    def setup_widgets(self, layout):
        h_layout = QHBoxLayout()
        font = self.font()
        font.setPointSize(12)

        for lineedit, text, num in [(self.user_name,"Name",1),(self.user_username,"Username",1),
                                        (self.user_tel, "Tel",1),(self.user_gmail,"Gmail",None)]:
            lineedit.setFont(font)
            v_layout = QVBoxLayout()
            v_layout.addWidget(QLabel(text))
            v_layout.addWidget(lineedit)
            if num:
                h_layout.addLayout(v_layout, num)

        layout.addLayout(h_layout)
        layout.addLayout(v_layout)

    def setup_buttons(self,layout):
        h_layout = QHBoxLayout()
        h_layout.addWidget(self.edit_button)
        h_layout.addWidget(self.close_button)
        h_layout.insertStretch(0, 1)
        layout.addLayout(h_layout)

    def setup_signals(self):
        self.edit_button.clicked.connect(self.edit_requested.emit)
        self.close_button.clicked.connect(self.close_requested.emit)

    def setup_style(self):
        base_button_style = """
        QPushButton {
            padding: 3px 20px; 
            border-radius: 5px;
        }"""
        base_lineedit_style = """
        QLineEdit {
            border: none;
            border-bottom: 2px solid gray;
        }"""

        if self.is_dark:
            self.setWindowIcon(QIcon(icon("Edit_light.png")))
            theme_button_style = """
            QPushButton {
                background-color: #2f2f2f;
                border: 1px solid #b03b02; 
            }"""
            theme_lineedit_style=""" 
            QLineEdit:focus {
                border-bottom: 2px solid #b03b02;
            }"""

        else:
            self.setWindowIcon(QIcon(icon("Edit_dark.png")))
            theme_button_style = """
            QPushButton {
                background-color: white;
                border: 1px solid #ff6f29; 
            }"""
            theme_lineedit_style = """ 
            QLineEdit:focus {
                border-bottom: 2px solid #ff6f29;
            }"""

        for lineedit in [self.user_name, self.user_username, self.user_tel,self.user_gmail]:
            lineedit.setStyleSheet(base_lineedit_style + theme_lineedit_style)

        self.edit_button.setStyleSheet(base_button_style + theme_button_style)
