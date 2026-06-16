from PySide6.QtCore import QObject,Signal

from View.MainElements.MessageDialog import MessageDialog
from View.Pages.LOM_Page.LOM_Dialogs.LOMInsertDialog import LOMInsertDialog


class LOMInsertController(QObject):
    refresh_requested = Signal()

    def __init__(self,theme,model):
        super(LOMInsertController, self).__init__()
        self.message = None
        self.is_dark = theme
        self.model = model
        self.view = None

        self.setup_view()
        self.setup_signals()

    def setup_view(self):
        ec_types = self.model.fetch_distinct_values("Type","EC")
        pcb_names = self.model.fetch_distinct_values("Name","PCB")
        feeders,nozzles = self.model.fetch_lom_comboboxes_items()

        self.view = LOMInsertDialog(self.is_dark, ec_types, pcb_names, feeders, nozzles)

        self.view.add_comboboxes_items()

    def setup_signals(self):
        self.view.insert_requested.connect(self.insert)
        self.view.close_requested.connect(self.view.close)
        self.view.pcb_name_changed.connect(self.add_pcb_comboboxes_items)
        self.view.ec_type_changed.connect(self.add_ec_comboboxes_items)

    def insert(self):
        new_data = [[self.none_if_empty(self.view.pcb_name.currentText()),
                    self.none_if_empty(self.view.pcb_board_per_sheet.currentText()),
                    self.none_if_empty(self.view.pcb_color.currentText()),
                    self.none_if_empty(self.view.pcb_finishing.currentText()),
                    self.none_if_empty(self.view.pcb_thickness.currentText())],

                    [self.none_if_empty(self.view.ec_type.currentText()),
                    self.none_if_empty(self.view.ec_part_number.currentText()),
                    self.none_if_empty(self.view.ec_marking.currentText()),
                    self.none_if_empty(self.view.ec_footprint.currentText()),
                    self.none_if_empty(self.view.ec_manufacturer.currentText())],

                    [self.none_if_empty(self.view.lom_feeder.currentText()),
                    self.none_if_empty(self.view.lom_nozzle.currentText()),
                    self.none_if_empty(self.view.lom_count.value()),
                    self.none_if_empty(self.view.lom_sign.text()),
                    self.none_if_empty(self.view.lom_comment.text())]]

        if new_data[0][0] is None or new_data[0][1] is None or new_data[1][0] is None or new_data[1][1] is None:
            self.message = MessageDialog(self.is_dark,"Please fill the required fields", 0)
            self.message.show()
            return
        new_data[0][1] = int(new_data[0][1])

        result,success = self.model.insert(new_data[0][0],new_data[0][1],new_data[0][2],new_data[0][3],new_data[0][4],
                          new_data[1][0],new_data[1][1],new_data[1][2],new_data[1][3],new_data[1][4],
                          new_data[2][0],new_data[2][1],new_data[2][2],new_data[2][3],new_data[2][4])

        self.message = MessageDialog(self.is_dark, result,success)
        self.message.show()

        self.refresh_requested.emit()

    def add_pcb_comboboxes_items(self, pcb_name: str):
        board_per_sheets, colors, finishings, thicknesses = self.model.fetch_pcb_comboboxes_items(pcb_name)
        self.view.add_pcb_comboboxes_items(board_per_sheets, colors, finishings, thicknesses)

    def add_ec_comboboxes_items(self, ec_name: str):
        part_numbers, markings, footprints, manufacturers = self.model.fetch_ec_comboboxes_items(ec_name)
        self.view.add_ec_comboboxes_items(part_numbers,markings,footprints,manufacturers)

    @staticmethod
    def none_if_empty(text):
        if type(text) == str:
            text = text.strip()
        return None if text == "" else text


