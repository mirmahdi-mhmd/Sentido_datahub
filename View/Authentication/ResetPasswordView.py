from PySide6.QtWidgets import QDialog, QPushButton, QVBoxLayout, QLineEdit, QHBoxLayout
from PySide6.QtCore import Signal,Qt
from PySide6.QtGui import QIcon

from View.MainElements.IconPath import icon


import sys
from PySide6.QtWidgets import QApplication


class ResetPasswordView(QDialog):
    send_code_signal = Signal()
    confirm_code_signal = Signal()
    change_password_signal = Signal()

    def __init__(self, theme):
        super().__init__()
        self.is_dark = theme
        self.setWindowTitle("Create a new password")
        self.setFixedSize(300, 240)
        self.username = QLineEdit(self)
        self.code = QLineEdit(self)
        self.password = QLineEdit(self)
        self.confirm_password = QLineEdit(self)

        self.visibility_button = QPushButton(self)
        self.send_code_button = QPushButton("Send code", self)
        self.confirm_code_button = QPushButton("Confirm", self)
        self.change_password_button = QPushButton("Reset password", self)

        self.setup_widgets()
        self.setup_signals()
        self.setup_style()

    def setup_widgets(self):
        v_layout = QVBoxLayout()
        font = self.font()
        font.setPointSize(13)

        h_layout = QHBoxLayout()
        self.username.setFont(font)
        self.username.setPlaceholderText("Username")
        h_layout.addWidget(self.username)
        h_layout.setContentsMargins(0, 0, 0, 0)
        h_layout.setSpacing(0)

        self.send_code_button.setFixedSize(90, 26)
        h_layout.addWidget(self.send_code_button)
        v_layout.addLayout(h_layout)

        h_layout = QHBoxLayout()
        self.code.setFont(font)
        self.code.setPlaceholderText("Code")
        h_layout.addWidget(self.code)
        h_layout.setContentsMargins(0, 0, 0, 0)
        h_layout.setSpacing(0)

        self.confirm_code_button.setFixedSize(90, 26)
        h_layout.addWidget(self.confirm_code_button)
        v_layout.addLayout(h_layout)

        h_layout = QHBoxLayout()
        self.password.setFont(font)
        self.password.setPlaceholderText("New password")
        self.password.setEchoMode(QLineEdit.EchoMode.Password)
        h_layout.addWidget(self.password)
        h_layout.setContentsMargins(0, 0, 0, 0)
        h_layout.setSpacing(0)

        self.visibility_button.setFixedSize(26, 26)
        self.visibility_button.setCheckable(True)
        self.visibility_button.setChecked(False)
        h_layout.addWidget(self.visibility_button)
        v_layout.addLayout(h_layout)

        self.confirm_password.setFont(font)
        self.confirm_password.setPlaceholderText("Confirm password")
        self.confirm_password.setEchoMode(QLineEdit.EchoMode.Password)
        v_layout.addWidget(self.confirm_password)

        self.change_password_button.setFont(font)
        v_layout.addWidget(self.change_password_button)

        v_layout.setAlignment(Qt.AlignCenter)
        v_layout.insertStretch(2, 1)
        v_layout.insertStretch(5,1)
        self.setLayout(v_layout)

    def setup_signals(self):
        self.send_code_button.clicked.connect(self.send_code_signal.emit)
        self.confirm_code_button.clicked.connect(self.confirm_code_signal.emit)
        self.change_password_button.clicked.connect(self.change_password_signal.emit)
        self.visibility_button.toggled.connect(self.change_visibility)

    def change_visibility(self, visible: bool):
        if visible:
            self.password.setEchoMode(QLineEdit.EchoMode.Normal)
            self.confirm_password.setEchoMode(QLineEdit.EchoMode.Normal)
            if self.is_dark:
                self.visibility_button.setIcon(QIcon(icon("Visible_light.png")))
            else:
                self.visibility_button.setIcon(QIcon(icon("Visible_dark.png")))
        else:
            self.password.setEchoMode(QLineEdit.EchoMode.Password)
            self.confirm_password.setEchoMode(QLineEdit.EchoMode.Password)
            if self.is_dark:
                self.visibility_button.setIcon(QIcon(icon("Invisible_light.png")))
            else:
                self.visibility_button.setIcon(QIcon(icon("Invisible_dark.png")))

    def setup_style(self):
        base_button_style = """
                QPushButton {
                    padding: 3px 20px; 
                    border-radius: 5px;
                }"""

        base_lineedit_style = """
                QLineEdit {
                    border-radius: 0px;
                    border-bottom: 2px solid gray;
                }"""
        if self.is_dark:
            self.setWindowIcon(QIcon(icon("Account_light.png")))
            self.visibility_button.setIcon(QIcon(icon("Invisible_light.png")))
            action_button_style = """
            QPushButton {
                background-color: #2f2f2f;
                border: 1px solid #b03b02; 
            }"""
            theme_lineedit_style = """ 
            QLineEdit:focus {
                border-bottom: 2px solid #b03b02;
                background-color: #2f2f2f;
            }"""
            visibility_button_style = """
            QPushButton {
                border: None;
                background-color: #2f2f2f;
            }"""
            secondary_button_style = """
            QPushButton {
                border: 2px solid #808080;
            }
            QPushButton:hover {
                border-color: #b03b02;
            }"""
        else:
            self.setWindowIcon(QIcon(icon("Account_dark.png")))
            self.visibility_button.setIcon(QIcon(icon("Invisible_dark.png")))
            action_button_style = """
            QPushButton {
                border: 1px solid #ff6f29; 
            }"""
            theme_lineedit_style = """ 
            QLineEdit:focus {
                border-bottom: 2px solid #ff6f29;
            }"""
            visibility_button_style = """
            QPushButton {
                border: None;
            }"""
            secondary_button_style = """
            QPushButton {
                border: None;
            }
            QPushButton:hover {
                border-color: #ff6f29;
            }"""

        for lineedit in [self.username, self.code, self.password, self.confirm_password]:
            lineedit.setStyleSheet(base_lineedit_style + theme_lineedit_style)

        self.change_password_button.setStyleSheet(base_button_style + action_button_style)
        self.visibility_button.setStyleSheet(visibility_button_style)

        for button in (self.send_code_button, self.confirm_code_button):
            button.setStyleSheet(secondary_button_style)

def main() -> int:
    app = QApplication(sys.argv)

    view = ResetPasswordView(True)
    view.show()

    return app.exec()


if __name__ == "__main__":
    sys.exit(main())
