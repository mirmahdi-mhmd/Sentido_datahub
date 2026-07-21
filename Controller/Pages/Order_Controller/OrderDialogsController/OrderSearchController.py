from View.Pages.Order_Page.Order_Dialogs.OrderSearchDialog import OrderSearchDialog
from Controller.Pages.Order_Controller.OrderDialogsController.OrderDtlPageController import OrderDtlPageController

class OrderSearchController:

    def __init__(self,theme,model):

        self.details_dialog = None
        self.is_dark = theme
        self.model = model
        self.view = None
        self.headers = ["Name","Tel","City","Address","date","Status","Order_ID","Comment"]
        self.edit_dialog = None

        self.setup_view()
        self.setup_signals()

    def setup_view(self):
        types = self.model.fetch_distinct_values("Name")
        self.view = OrderSearchDialog(self.is_dark, types,self.headers, None)

    def setup_signals(self):
        self.view.adv_search_requested.connect(self.adv_search_requested)
        self.view.close_requested.connect(self.view.close)
        self.view.name_changed.connect(self.add_comboboxes_items)
        self.view.tableview.row_selected.connect(self.open_details)

    def adv_search_requested(self):
        customer_name = self.none_if_empty(self.view.customer_name.currentText())
        customer_tel = self.none_if_empty(self.view.customer_tel.currentText())
        customer_city = self.none_if_empty(self.view.customer_city.currentText())
        if customer_name is None and customer_tel is None and customer_city is None:
            return
        else:
            result = self.model.adv_search(customer_name,customer_tel,customer_city)
            self.view.tableview.update_data(result)

    def open_details(self, data):
        self.details_dialog = OrderDtlPageController(self.is_dark,data[6],data[5])
        self.details_dialog.view.show()

    def add_comboboxes_items(self, customer_name: str):
        tels, cities,addresses = self.model.fetch_comboboxes_items(customer_name)
        self.view.add_comboboxes_items(tels, cities)

    @staticmethod
    def none_if_empty(text):
        if type(text) == str:
            text = text.strip()
        return None if text == "" else text

