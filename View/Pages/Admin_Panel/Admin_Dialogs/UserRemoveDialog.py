from PySide6.QtCore import Signal
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QDialog, QComboBox, QPushButton, QHBoxLayout, QVBoxLayout, QLabel

from View.MainElements.IconPath import icon


class CustomerRemoveDialog(QDialog):
    remove_requested = Signal()
    close_requested = Signal()
    name_changed = Signal(str)

    def __init__(self, theme, name_list):
        super(CustomerRemoveDialog, self).__init__()
        self.is_dark = theme
        self.setWindowTitle("Remove (User)")
        self.setMinimumSize(500, 250)
        self.setMaximumSize(650, 350)

        self.user_name = QComboBox(self)
        self.user_username = QComboBox(self)
        self.user_tel = QComboBox(self)

        self.remove_button = QPushButton("Remove", self)
        self.close_button = QPushButton("Close", self)

        self.name_list = name_list

        layout = QVBoxLayout(self)
        self.setup_widgets(layout)
        self.setup_buttons(layout)
        self.setup_signals()
        self.setup_style()
        layout.insertStretch(1, 1)

    def setup_widgets(self, layout):
        h_layout = QHBoxLayout()
        font = self.font()
        font.setPointSize(12)

        self.user_name.addItems(self.name_list)
        self.user_name.setCurrentIndex(-1)

        for lineedit, text, num in [(self.user_name, "Name",1),(self.user_username, "Username",1),
                                    (self.user_tel, "Tel",1)]:
            lineedit.setFont(font)
            v_layout = QVBoxLayout()
            v_layout.addWidget(QLabel(text))
            v_layout.addWidget(lineedit)
            h_layout.addLayout(v_layout,num)

        layout.addLayout(h_layout)

    def setup_buttons(self,layout):
        h_layout = QHBoxLayout()
        h_layout.addWidget(self.remove_button)
        h_layout.addWidget(self.close_button)
        h_layout.insertStretch(0, 1)
        layout.addLayout(h_layout)

    def setup_signals(self):
        self.remove_button.clicked.connect(self.remove_requested.emit)
        self.close_button.clicked.connect(self.close_requested.emit)
        self.user_name.currentIndexChanged.connect(lambda _: self.name_changed.emit(self.user_name.currentText()))

    def setup_style(self):
        base_combobox_style = """
        QComboBox {
            padding-right: 0px; 
            border: none;
            border-bottom: 2px solid gray;
        }
        QComboBox QLineEdit {
            border: none;
            background: transparent;
            border-bottom: 2px solid gray;
        }
        QComboBox::down-arrow {
            width: 8px;
            height: 8px;
        }"""
        base_button_style = """
        QPushButton {
            padding: 3px 20px; 
            border-radius: 5px;
        }"""

        if self.is_dark:
            self.setWindowIcon(QIcon(icon("Minus_light.png")))
            theme_combobox_style = """
            QComboBox:focus {
            border-bottom: 2px solid #b03b02; 
            }
            QComboBox QLineEdit:focus {
            border-bottom: 2px solid #b03b02;
            }"""
            theme_button_style = """
            QPushButton {
                background-color: #2f2f2f;
                border: 1px solid #b03b02; 
            }"""

        else:
            self.setWindowIcon(QIcon(icon("Minus_dark.png")))
            theme_combobox_style = """
            QComboBox:focus {
            border-bottom: 2px solid #ff6f29; 
            }
            QComboBox QLineEdit:focus {
            border-bottom: 2px solid #ff6f29;
            }"""
            theme_button_style = """
            QPushButton {
                background-color: white;
                border: 1px solid #ff6f29; 
            }"""

        for combobox in [self.user_name, self.user_username,self.user_tel]:
            combobox.setStyleSheet(base_combobox_style + theme_combobox_style)

        self.remove_button.setStyleSheet(base_button_style + theme_button_style)

    def add_comboboxes_items(self,username,tel):
        for combobox, data in ((self.user_username, username),(self.user_tel, tel)):
            text = combobox.currentText()
            combobox.clear()
            combobox.addItems(data)
            combobox.setCurrentText(text)
