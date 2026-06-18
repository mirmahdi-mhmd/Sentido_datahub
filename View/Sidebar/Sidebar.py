"""
Sidebar widget for the application.
This module defines the NavBar class, a QWidget-based vertical Side panel with three buttons: Components, PCBs, and Pages.
Each button is checkable, grouped exclusively, and emits a 'page_selected' signal with a string identifier when clicked.
The widget adapts its style and icons based on the system theme (dark/light).
"""
from PySide6.QtWidgets import QWidget,QVBoxLayout,QPushButton,QButtonGroup
from PySide6.QtCore import QSize, Signal, QPropertyAnimation, QEasingCurve, Qt
from PySide6.QtGui import QIcon

from View.MainElements.IconPath import icon


class Sidebar(QWidget):
    page_selected = Signal(str)

    def __init__(self,theme):
        super().__init__()
        self.dark_theme = theme

        self.expanded_width = 190
        self.collapsed_width = 56
        self.expanded = True

        self.setMinimumWidth(self.expanded_width)
        self.setMaximumWidth(self.expanded_width)
        self.setAttribute(Qt.WA_StyledBackground, True)

        self.anim_min = QPropertyAnimation(self, b"minimumWidth")
        self.anim_max = QPropertyAnimation(self, b"maximumWidth")

        for anim in (self.anim_min, self.anim_max):
            anim.setDuration(220)
            anim.setEasingCurve(QEasingCurve.OutCubic)

        self.toggle_button = QPushButton(self)
        self.toggle_button.setFixedSize(56,50)

        self.button_group = QButtonGroup(self)
        self.product_button = QPushButton("  Product")
        self.ec_button = QPushButton("  Electronic\n  component")
        self.pcb_button = QPushButton("  PCB")
        self.lom_button = QPushButton("  LOM")
        self.serial_button = QPushButton("  Serial")
        self.customer_button = QPushButton("  Customer")
        self.order_button = QPushButton("  Order")
        self.mech_button = QPushButton("  Mechanical\n  component")
        self.setup_widgets()
        self.setup_signals()
        self.setup_style()

    def setup_widgets(self):
        layout = QVBoxLayout(self)
        layout.addWidget(self.toggle_button)

        for btn in [self.product_button, self.serial_button, self.customer_button, self.order_button,self.mech_button,self.ec_button, self.pcb_button, self.lom_button]:
            btn.setCheckable(True)
            self.button_group.addButton(btn)
            layout.addWidget(btn)

        self.button_group.setExclusive(True)
        self.product_button.setChecked(True)

        layout.addStretch()
        layout.setContentsMargins(0, 9, 0, 9)

    def setup_signals(self):
        self.toggle_button.clicked.connect(self.toggle)

        self.ec_button.clicked.connect(lambda _:self.page_selected.emit("Component"))
        self.pcb_button.clicked.connect(lambda _: self.page_selected.emit("PCB"))
        self.lom_button.clicked.connect(lambda _: self.page_selected.emit("LOM"))
        self.product_button.clicked.connect(lambda _: self.page_selected.emit("Product"))
        self.customer_button.clicked.connect(lambda _: self.page_selected.emit("Customer"))
        self.serial_button.clicked.connect(lambda _: self.page_selected.emit("Serial"))
        self.order_button.clicked.connect(lambda _: self.page_selected.emit("Order"))
        self.mech_button.clicked.connect(lambda _: self.page_selected.emit("Mech"))

    def toggle(self):
        self.anim_min.stop()
        self.anim_max.stop()

        if self.expanded:
            start = self.expanded_width
            end = self.collapsed_width
            self.anim_max.finished.connect(self._hide_text_once)
        else:
            start = self.collapsed_width
            end = self.expanded_width
            self.anim_max.finished.connect(self._show_text_once)

        self.anim_min.setStartValue(start)
        self.anim_min.setEndValue(end)

        self.anim_max.setStartValue(start)
        self.anim_max.setEndValue(end)

        self.anim_min.start()
        self.anim_max.start()

        self.expanded = not self.expanded

    def _hide_text(self):
        for btn in self.button_group.buttons():
            btn.setToolTip(btn.text().strip())
            btn.setText("")

    def _show_text(self):
        labels = {
            self.ec_button: "  Electronic\n  component",
            self.pcb_button: "  PCB",
            self.lom_button: "  LOM",
            self.product_button: "  Product",
            self.serial_button: "  Serial",
            self.customer_button: "  Customer",
            self.order_button: "  Order",
            self.mech_button: "  Mechanical\n  component"}

        for btn, text in labels.items():
            btn.setText(text)
            btn.setToolTip("")

    def _hide_text_once(self):
        self.anim_max.finished.disconnect(self._hide_text_once)
        self._hide_text()

    def _show_text_once(self):
        self.anim_max.finished.disconnect(self._show_text_once)
        self._show_text()

    def setup_style(self):
        base_style = """
        QPushButton:hover {
            background-color: #A0A0A0;
        }
        QPushButton {
            background-color: transparent;
            border: none;
            padding: 10px;
            padding-left: 10px;
            padding-right: 20px;
            text-align: left;
            font-size: 18px;
            font-weight: bold;
            border-radius: 6px;
            margin: 0px;
        }"""

        if self.dark_theme:
            menu_icon = icon("Menu_light")
            ec_icon = icon("Component_light.png")
            pcb_icon = icon("PCB_light.png")
            lom_icon = icon("LOM_light.png")
            product_icon = icon("Product_light.png")
            customer_icon = icon("Customer_light.png")
            serial_icon = icon("Serial_light.png")
            order_icon = icon("Order_light.png")
            mech_icon = icon("Mech_light.png")
            theme_style = """
            QPushButton {
                color: white;
            }
            QPushButton:checked {
                background-color: #b03b02;
                color: white;
            }"""

        else:
            menu_icon = icon("Menu_dark")
            ec_icon = icon("Component_dark.png")
            pcb_icon = icon("PCB_dark.png")
            lom_icon = icon("LOM_dark.png")
            product_icon = icon("Product_dark.png")
            customer_icon = icon("Customer_dark.png")
            serial_icon = icon("Serial_dark.png")
            order_icon = icon("Order_dark.png")
            mech_icon = icon("Mech_dark.png")
            theme_style = """
            QPushButton {
                color: black;
            }
            QPushButton:checked {
                background-color: #ff6f29;
                color: black;
            }"""

        self.setStyleSheet(base_style + theme_style)

        for btn, icons in [(self.toggle_button,menu_icon),(self.ec_button, ec_icon), (self.pcb_button, pcb_icon),
                           (self.lom_button, lom_icon),(self.product_button,product_icon),(self.customer_button, customer_icon),
                           (self.serial_button, serial_icon),(self.order_button, order_icon),(self.mech_button, mech_icon)]:
            btn.setIcon(QIcon(icons))
            btn.setIconSize(QSize(37,37))
