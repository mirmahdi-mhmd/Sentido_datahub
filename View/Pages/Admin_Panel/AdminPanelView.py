from PySide6.QtWidgets import QVBoxLayout, QWidget

from View.MainElements.Searchbar import Searchbar
from View.MainElements.BasicToolbar import BasicToolbar
from View.MainElements.TableView import TableView


class AdminPanelView(QWidget):
    def __init__(self, theme,table_data,search_suggestions):
        super().__init__()

        self.panel_layout = QVBoxLayout(self)
        self.searchbar = Searchbar(theme, "Name", search_suggestions)
        self.toolbar = BasicToolbar(theme)
        self.tableview = TableView(theme, ["Name","Username","Tel","gmail"],table_data)

        self.setup_widgets()

    def setup_widgets(self):
        for widget in [self.searchbar, self.toolbar, self.tableview]:
            self.panel_layout.addWidget(widget)
