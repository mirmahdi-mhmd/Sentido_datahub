from PySide6.QtCore import Signal, QSize
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QDialog, QComboBox, QPushButton, QHBoxLayout, QVBoxLayout, QLabel

from View.MainElements.IconPath import icon
from View.MainElements.TableView import TableView

class UserSearchDialog(QDialog):
    adv_search_requested = Signal()
    close_requested = Signal()
    name_changed = Signal(str)

    def __init__(self, theme, name_list, username_list, tel_list, gmail_list, headers, info):
        super(UserSearchDialog, self).__init__()
        self.is_dark = theme
        self.setWindowTitle("ADV Search (User)")
        self.setMinimumSize(700, 300)

        self.user_name = QComboBox(self)
        self.user_username = QComboBox(self)
        self.user_tel = QComboBox(self)
        self.user_gmail = QComboBox(self)

        self.tableview = TableView(self.is_dark, headers, info)

        self.adv_search_button = QPushButton("Search", self)
        self.close_button = QPushButton("Close", self)

        self.names = name_list
        self.usernames = username_list
        self.tels = tel_list
        self.gmails = gmail_list

        layout = QVBoxLayout(self)
        self.setup_comboboxes(layout)
        layout.addWidget(self.tableview)
        self.setup_buttons(layout)
        self.setup_signals()
        self.setup_style()

    def setup_comboboxes(self,layout):
        h_layout = QHBoxLayout()
        font = self.font()
        font.setPointSize(12)

        for combobox,items in ((self.user_name,self.names),(self.user_username,self.usernames),
                               (self.user_tel,self.tels),(self.user_gmail,self.gmails)):
            combobox.addItems(items)
            combobox.setCurrentIndex(-1)

        for combobox, text, num in [(self.user_name, "Name",1),(self.user_username, "Username",1),
                                    (self.user_tel, "Tel",1),(self.user_gmail, "Gmail",1)]:
            combobox.setEditable(True)
            combobox.setFont(font)
            combobox.setMaxVisibleItems(5)
            combobox.setFixedSize(QSize(130,27))
            v_layout = QVBoxLayout()
            v_layout.addWidget(QLabel(text))
            v_layout.addWidget(combobox)
            h_layout.addLayout(v_layout,num)

        h_layout.addStretch()
        layout.addLayout(h_layout)

    def setup_buttons(self,layout):
        h_layout = QHBoxLayout()
        h_layout.addWidget(self.adv_search_button)
        h_layout.addWidget(self.close_button)
        h_layout.insertStretch(0, 1)
        layout.addLayout(h_layout)

    def setup_signals(self):
        self.adv_search_button.clicked.connect(self.adv_search_requested.emit)
        self.close_button.clicked.connect(self.close_requested.emit)
        self.user_name.currentIndexChanged.connect(lambda _:self.name_changed.emit(self.user_name.currentText()))

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
            self.setWindowIcon(QIcon(icon("ADVSearch_light.png")))
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
            self.setWindowIcon(QIcon(icon("ADVSearch_dark.png")))
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

        for combobox in [self.user_name, self.user_username, self.user_tel,self.user_gmail]:
            combobox.setStyleSheet(base_combobox_style + theme_combobox_style)

        self.adv_search_button.setStyleSheet(base_button_style + theme_button_style)

    def add_comboboxes_items(self, usernames, tels, gmails):
        for combobox, data in ((self.user_username,usernames),(self.user_tel, tels),(self.user_gmail, gmails)):
            text = combobox.currentText()
            combobox.clear()
            combobox.addItems(data)
            combobox.setCurrentText(text)
