from View.Pages.Customer_Page.Customer_Dialogs.CustomerSearchDialog import CustomerSearchDialog
from Controller.Pages.Customer_Controller.CustomerDialogsController.CustomerEditController import CustomerEditController


class CustomerSearchController:

    def __init__(self,theme,model):

        self.is_dark = theme
        self.model = model
        self.view = None
        self.headers = ["Name","Tel","City","Address","Comment"]
        self.edit_dialog = None

        self.setup_view()
        self.setup_signals()

    def setup_view(self):
        names = self.model.fetch_distinct_values("Name")
        tels = self.model.fetch_distinct_values("Tel")
        cities = self.model.fetch_distinct_values("City")
        self.view = CustomerSearchDialog(self.is_dark, names,tels,cities,self.headers, None)

    def setup_signals(self):
        self.view.adv_search_requested.connect(self.adv_search_requested)
        self.view.close_requested.connect(self.view.close)
        self.view.name_changed.connect(self.add_comboboxes_items)
        self.view.tableview.row_selected.connect(self.edit_requested)

    def adv_search_requested(self):
        customer_name = self.none_if_empty(self.view.customer_name.currentText())
        customer_tel = self.none_if_empty(self.view.customer_tel.currentText())
        customer_city = self.none_if_empty(self.view.customer_city.currentText())
        if customer_name is None and customer_tel is None and customer_city is None:
            return
        else:
            result = self.model.adv_search(customer_name,customer_tel,customer_city)
            self.view.tableview.update_data(result)

    def edit_requested(self, data):
        self.edit_dialog = CustomerEditController(self.is_dark,data,self.model)
        self.edit_dialog.view.show()
        self.edit_dialog.view.edit_button.clicked.connect(self.adv_search_requested)

    def add_comboboxes_items(self, customer_name: str):
        tels, cities,addresses = self.model.fetch_comboboxes_items(customer_name)
        self.view.add_comboboxes_items(tels, cities)

    @staticmethod
    def none_if_empty(text):
        if type(text) == str:
            text = text.strip()
        return None if text == "" else text

