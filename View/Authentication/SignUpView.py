from PySide6.QtWidgets import QDialog, QPushButton, QHBoxLayout, QVBoxLayout, QLineEdit
from PySide6.QtCore import Signal


class SignUpView(QDialog):
    signup_signal = Signal()
