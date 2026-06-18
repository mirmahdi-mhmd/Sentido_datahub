from PySide6.QtWidgets import QDialog, QPushButton, QVBoxLayout, QLineEdit, QLabel,      QApplication
from PySide6.QtCore import Signal,Qt
from PySide6.QtGui import QIcon

from


class LogInView(QDialog):
    login_signal = Signal()

    def __init__(self, theme):
        super().__init__()
        self.is_dark = theme
        self.setWindowTitle("Log In")
        self.username = QLineEdit(self)
        self.password = QLineEdit(self)

        self.login_button = QPushButton("Log In",self)

        self.setup_widgets()
        self.setup_style()

    def setup_widgets(self):
        v_layout = QVBoxLayout()
        font = self.font()
        font.setPointSize(35)

        signup_label = QLabel("Welcome!")
        signup_label.setFont(font)
        signup_label.setAlignment(Qt.AlignCenter)
        v_layout.addWidget(signup_label)

        font.setPointSize(15)
        self.username.setFont(font)
        self.username.setPlaceholderText("Username")
        self.username.setAlignment(Qt.AlignCenter)
        v_layout.addWidget(self.username)

        self.password.setFont(font)
        self.password.setPlaceholderText("Password")
        self.password.setAlignment(Qt.AlignCenter)
        v_layout.addWidget(self.password)

        self.login_button.setFont(font)
        v_layout.addWidget(self.login_button)

        v_layout.setAlignment(Qt.AlignCenter)
        self.setLayout(v_layout)

    def setup_signals(self):
        self.login_button.clicked.connect(self.login_signal.emit)

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
            self.setWindowIcon(QIcon(icon("Account_light.png")))
            theme_button_style = """
                        QPushButton {
                            background-color: #2f2f2f;
                            border: 1px solid #b03b02; 
                        }"""
            theme_lineedit_style = """ 
                        QLineEdit:focus {
                            border-bottom: 2px solid #b03b02;
                        }"""
        else:
            self.setWindowIcon(QIcon(icon("Account_dark.png")))
            theme_button_style = """
                        QPushButton {
                            background-color: white;
                            border: 1px solid #ff6f29; 
                        }"""
            theme_lineedit_style = """ 
                        QLineEdit:focus {
                            border-bottom: 2px solid #ff6f29;
                        }"""

        for lineedit in [self.username, self.password]:
            lineedit.setStyleSheet(base_lineedit_style + theme_lineedit_style)

        self.login_button.setStyleSheet(base_button_style + theme_button_style)

app = QApplication([])
window = LogInView("")
window.show()
app.exec()