from PySide6.QtCore import QObject, Signal

from Model.Pages.LOMPageModel import LOMPageModel
from View.Pages.LOM_Page.LOM_Dialogs.LOMSearchDialog import LOMSearchDialog
from Controller.Pages.LOM_Controller.LOMDialogsController.LOMEditController import LOMEditController


class LOMSearchController(QObject):
    refresh_requested = Signal()

    def __init__(self, theme, model):
        super(LOMSearchController, self).__init__()
        self.edit_dialog = None
        self.is_dark = theme
        self.model = LOMPageModel()
        self.headers = ["PCB-Name","PCB-B/S","EC-PN","EC-Footprint","EC-Manufacturer","Feeder","Nozzle","Count","Sign list","Comment","PCB_ID","EC_ID"]
        self.view = None

        self.setup_view()
        self.setup_signals()

    def setup_view(self):
        ec_types = self.model.fetch_distinct_values("Type", "EC")
        pcb_names = self.model.fetch_distinct_values("Name", "PCB")

        self.view = LOMSearchDialog(self.is_dark, ec_types, pcb_names,self.headers, None)

    def setup_signals(self):
        self.view.search_requested.connect(self.search)
        self.view.close_requested.connect(self.view.close)
        self.view.pcb_name_changed.connect(self.add_pcb_comboboxes_items)
        self.view.ec_type_changed.connect(self.add_ec_comboboxes_items)
        self.view.tableview.row_selected.connect(self.edit_requested)

    def search(self):
        data = [[self.none_if_empty(self.view.pcb_name.currentText()),
                 self.none_if_empty(self.view.pcb_board_per_sheet.currentText()),
                 self.none_if_empty(self.view.pcb_color.currentText()),
                 self.none_if_empty(self.view.pcb_finishing.currentText()),
                 self.none_if_empty(self.view.pcb_thickness.currentText())],

                [self.none_if_empty(self.view.ec_type.currentText()),
                 self.none_if_empty(self.view.ec_part_number.currentText()),
                 self.none_if_empty(self.view.ec_marking.currentText()),
                 self.none_if_empty(self.view.ec_footprint.currentText()),
                 self.none_if_empty(self.view.ec_manufacturer.currentText())]]

        if data[0][0] is None and data [1][0] is None:
            return
        else:
            if data[0][1] is not None:
                data[0][1] = int(data[0][1])

            result = self.model.adv_search(data[0][0], data[0][1], data[0][2], data[0][3], data[0][4],
                                  data[1][0], data[1][1], data[1][2], data[1][3], data[1][4])
            self.view.tableview.update_data(result)

    def edit_requested(self, data):
        self.edit_dialog = LOMEditController(self.is_dark,data,self.model)
        self.edit_dialog.view.show()
        self.edit_dialog.view.edit_button.clicked.connect(self.search)

    def add_pcb_comboboxes_items(self, pcb_name: str):
        board_per_sheets, colors, finishings, thicknesses = self.model.fetch_pcb_comboboxes_items(pcb_name)
        self.view.add_pcb_comboboxes_items(board_per_sheets, colors, finishings, thicknesses)

    def add_ec_comboboxes_items(self, ec_name: str):
        part_numbers, markings, footprints, manufacturers = self.model.fetch_ec_comboboxes_items(ec_name)
        self.view.add_ec_comboboxes_items(part_numbers, markings, footprints, manufacturers)

    @staticmethod
    def none_if_empty(text):
        if type(text) == str:
            text = text.strip()
        return None if text == "" else text


