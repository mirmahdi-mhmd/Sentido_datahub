from pyodbc import IntegrityError
from Model.Connection import Connection


class LOMPageModel:
    def __init__(self):
        self.conn = Connection.connect()

    def fetch_all_data(self):
        cursor = self.conn.cursor()
        cursor.execute("""
        SELECT P.Name, P.[Board/sheet], E.Part_number, E.Footprint, E.Manufacturer,
               L.Feeder, L.Nozzle, L.Count, L.Sign_list, L.Comment, L.PCB_ID, L.EC_ID 
        FROM tbl_LOM L 
        JOIN tbl_PCB P ON P.PCB_ID = L.PCB_ID 
        JOIN tbl_EC E ON E.EC_ID = L.EC_ID 
        """)
        result = cursor.fetchall()

        cursor.close()
        return list(result)

    def fetch_distinct_values(self,column_name,tbl):
        cursor = self.conn.cursor()
        if tbl == "PCB":
            cursor.execute(f"""
            SELECT DISTINCT {column_name} 
            FROM tbl_PCB 
            """)
        elif tbl == "EC":
            cursor.execute(f"""
            SELECT DISTINCT {column_name} 
            FROM tbl_EC  
            """)
        elif tbl == "LOM":
            cursor.execute(f"""
            SELECT DISTINCT {column_name} 
            FROM tbl_LOM
            """)
        list_distinct = cursor.fetchall()
        result = [i[0] for i in list_distinct]

        cursor.close()
        return result

    def search(self,pcb_name):
        cursor = self.conn.cursor()
        cursor.execute("""
        SELECT P.Name, P.[Board/sheet], E.Part_number, E.Footprint, E.Manufacturer,
               L.Feeder, L.Nozzle, L.Count, L.Sign_list, L.Comment, L.PCB_ID, L.EC_ID
        FROM tbl_LOM L 
        JOIN tbl_PCB P ON P.PCB_ID = L.PCB_ID 
        JOIN tbl_EC E ON E.EC_ID = L.EC_ID 
        WHERE P.Name = ?
        """,(pcb_name,))
        result = cursor.fetchall()

        cursor.close()
        return result

    def insert(self,pcb_name, pcb_board_per_sheet, pcb_color, pcb_finishing, pcb_thickness,
               ec_type, ec_part_number, ec_marking, ec_footprint, ec_manufacturer,
                lom_feeder, lom_nozzle, lom_count, lom_sign_list, lom_comment):
        cursor = self.conn.cursor()

        pcb_id = self.get_pcb_id(cursor,pcb_name, pcb_board_per_sheet, pcb_color, pcb_finishing, pcb_thickness)
        if pcb_id is None:
            cursor.close()
            return "No matching PCB found"

        ec_id = self.get_ec_id(cursor,ec_type, ec_part_number, ec_marking, ec_footprint, ec_manufacturer)
        if ec_id is None:
            cursor.close()
            return "No matching ec found"

        try:
            cursor.execute("""
            INSERT INTO tbl_LOM
            (EC_ID,PCB_ID,Feeder,Nozzle,Count,Sign_list,Comment)
            VALUES (?,?,?,?,?,?,?)
            """,(ec_id, pcb_id, lom_feeder, lom_nozzle, lom_count, lom_sign_list, lom_comment))

            self.conn.commit()
            return "Insert successful",1

        except IntegrityError:
            self.conn.rollback()
            return "Row exists",0

        finally:
            cursor.close()

    def remove(self,pcb_name, pcb_board_per_sheet, pcb_color, pcb_finishing, pcb_thickness,
               ec_type, ec_part_number, ec_marking, ec_footprint, ec_manufacturer):
        cursor = self.conn.cursor()

        pcb_id = self.get_pcb_id(cursor,pcb_name, pcb_board_per_sheet, pcb_color, pcb_finishing, pcb_thickness)
        if pcb_id is None:
            cursor.close()
            return "No pcb found",0

        ec_id = self.get_ec_id(cursor,ec_type, ec_part_number, ec_marking, ec_footprint, ec_manufacturer)
        if ec_id is None:
            cursor.close()
            return "No component found",0

        cursor.execute("""
        DELETE FROM tbl_LOM
        WHERE EC_ID=? AND PCB_ID=?
        """,(ec_id, pcb_id))

        if cursor.rowcount == 0:
            cursor.close()
            return "No matching row found",0

        self.conn.commit()
        cursor.close()
        return "Remove successful",1

    def adv_search(self, pcb_name, pcb_board_per_sheet, pcb_color, pcb_finishing, pcb_thickness,
                   ec_type, ec_part_number, ec_marking, ec_footprint, ec_manufacturer):
        cursor = self.conn.cursor()

        ec_command_list = [["Part_number=?", ec_part_number], ["Marking=?", ec_marking],
                           ["Footprint=?", ec_footprint],["Manufacturer=?", ec_manufacturer]]
        ec_value_list = [ec_type]
        ec_conditions_string = """
        SELECT EC_ID
        FROM Tbl_EC
        WHERE Type=?
        """
        for condition, value in ec_command_list:
            if value is not None:
                ec_conditions_string += f" AND {condition}"
                ec_value_list.append(value)

        pcb_command_list = [["[Board/sheet]=?", pcb_board_per_sheet], ["Color=?", pcb_color],
                            ["Finishing=?", pcb_finishing], ["Thickness=?", pcb_thickness]]
        pcb_value_list = [pcb_name]
        pcb_conditions_string = """
        SELECT PCB_ID
        FROM tbl_PCB
        WHERE Name=?
        """
        for condition, value in pcb_command_list:
            if value is not None:
                pcb_conditions_string += f" AND {condition}"
                pcb_value_list.append(value)

        condition_string = """
        SELECT P.Name, P.[Board/sheet], E.Part_number, E.Footprint, E.Manufacturer,
        L.Feeder, L.Nozzle, L.Count, L.Sign_list, L.Comment, L.PCB_ID, L.EC_ID  
        FROM tbl_LOM L 
        JOIN tbl_PCB P ON P.PCB_ID = L.PCB_ID 
        JOIN tbl_EC E ON E.EC_ID = L.EC_ID
        """
        if pcb_name is not None and ec_type is not None:
            cursor.execute(pcb_conditions_string, pcb_value_list)
            pcb_ids = [str(i[0]) for i in cursor.fetchall()] or ["0"]
            condition_string += f" WHERE L.PCB_ID IN ({','.join(pcb_ids)})"

            cursor.execute(ec_conditions_string, ec_value_list)
            ec_ids = [str(i[0]) for i in cursor.fetchall()] or ["0"]
            condition_string += f" AND L.EC_ID IN ({','.join(ec_ids)})"

        elif ec_type is not None:
            cursor.execute(ec_conditions_string, ec_value_list)
            ec_ids = [str(i[0]) for i in cursor.fetchall()] or ["0"]
            condition_string += f" WHERE L.EC_ID IN ({','.join(ec_ids)})"

        elif pcb_name is not None:
            cursor.execute(pcb_conditions_string, pcb_value_list)
            pcb_ids = [str(i[0]) for i in cursor.fetchall()] or ["0"]
            condition_string += f" WHERE L.PCB_ID IN ({','.join(pcb_ids)})"

        else:
            cursor.close()
            return "please fill EC type or PCB name"

        cursor.execute(condition_string)
        result = cursor.fetchall()
        cursor.close()
        return list(result)

    def fetch_lom_comboboxes_items(self):
        cursor = self.conn.cursor()

        cursor.execute("""
        SELECT DISTINCT
        Feeder,Nozzle
        FROM tbl_LOM
        """)

        rows = cursor.fetchall()
        cursor.close()
        return (sorted(list(set([i[0] for i in rows if i[0] is not None]))),
                sorted(list(set([i[1] for i in rows if i[1] is not None]))))

    def fetch_ec_comboboxes_items(self,ec_type):
        cursor = self.conn.cursor()

        cursor.execute("""
        SELECT DISTINCT
        Part_number, Marking, Footprint, Manufacturer
        FROM tbl_EC
        WHERE Type = ?
        """,(ec_type,))

        rows = cursor.fetchall()
        cursor.close()

        return (sorted(list(set([i[0] for i in rows if i[0] is not None]))),
                sorted(list(set([i[1] for i in rows if i[1] is not None]))),
                sorted(list(set([i[2] for i in rows if i[2] is not None]))),
                sorted(list(set([i[3] for i in rows if i[3] is not None]))))

    def fetch_pcb_comboboxes_items(self, pcb_name):
        cursor = self.conn.cursor()

        cursor.execute("""
        SELECT DISTINCT
        [Board/sheet],Color,Finishing,Thickness
        FROM tbl_PCB
        WHERE Name = ?
        """,(pcb_name,))

        rows = cursor.fetchall()
        cursor.close()

        return (sorted(list(set([i[0] for i in rows if i[0] is not None]))),
                sorted(list(set([i[1] for i in rows if i[1] is not None]))),
                sorted(list(set([i[2] for i in rows if i[2] is not None]))),
                sorted(list(set([i[3] for i in rows if i[3] is not None]))))

    def edit_data(self,pcb_id,ec_id,new_row):
        cursor = self.conn.cursor()

        try:
            new_pcb_id = self.get_pcb_id(cursor, new_row[0][0], new_row[0][1], new_row[0][2], new_row[0][3],new_row[0][4])
            new_ec_id = self.get_ec_id (cursor, new_row[1][0],new_row[1][1],new_row[1][2],new_row[1][3],new_row[1][4])

            if new_pcb_id is None or new_ec_id is None:
                cursor.close()
                return "No matching PCB or component found"

            cursor.execute("""
            UPDATE tbl_LOM
            SET PCB_ID=?, EC_ID=?, Feeder=?,Nozzle=?,Count=?,Sign_list=?,Comment=?
            WHERE PCB_ID=? AND EC_ID=?
            """,
            (new_pcb_id, new_ec_id,new_row[2][0],new_row[2][1],new_row[2][2],new_row[2][3],new_row[2][4],
             pcb_id,ec_id))

            self.conn.commit()
            return "Edit successful"

        except IntegrityError:
            self.conn.rollback()
            return "Row exists"

        finally:
            cursor.close()

    def add_suggestion(self):
        cursor = self.conn.cursor()
        cursor.execute(f"""
        SELECT DISTINCT P.Name 
        FROM tbl_PCB P
        JOIN tbl_LOM L ON P.PCB_ID = L.PCB_ID
        """)
        result = cursor.fetchall()

        cursor.close()
        return [i[0] for i in result]

    def check_stock(self,pcb_name, pcb_board_per_sheet, pcb_color, pcb_finishing, pcb_thickness, qty):
        pass

    def get_pcb_data (self,pcb_id):
        cursor = self.conn.cursor()
        cursor.execute("""
        SELECT Name,[Board/sheet],Color,Finishing,Thickness
        FROM tbl_PCB
        WHERE PCB_ID = ?
        """,pcb_id)
        result = cursor.fetchone()

        cursor.close()
        return result

    def get_ec_data (self,ec_id):
        cursor = self.conn.cursor()
        cursor.execute("""
        SELECT Type, Part_number, Marking, Footprint, Manufacturer
        FROM tbl_EC
        WHERE EC_ID = ?
        """,ec_id)
        result = cursor.fetchone()

        cursor.close()
        return result

    @staticmethod
    def get_ec_id (cursor, ec_type, ec_part_number, ec_marking, ec_footprint, ec_manufacturer):
        cursor.execute("""
        SELECT EC_ID
        FROM tbl_EC
        WHERE Type = ?
        AND Part_number = ?
        AND (Marking = ? OR (Marking IS NULL AND ? IS NULL))
        AND (Footprint = ? OR (Footprint IS NULL AND ? IS NULL))
        AND (Manufacturer = ? OR (Manufacturer IS NULL AND ? IS NULL))
        """,
        (ec_type, ec_part_number, ec_marking, ec_marking, ec_footprint, ec_footprint, ec_manufacturer,ec_manufacturer))

        row = cursor.fetchone()
        return row[0] if row else None

    @staticmethod
    def get_pcb_id (cursor, pcb_name, pcb_board_per_sheet, pcb_color, pcb_finishing, pcb_thickness):
        cursor.execute("""
        SELECT PCB_ID
        FROM tbl_PCB
        WHERE Name = ?
        AND [Board/sheet] = ?
        AND (Color = ? OR (Color IS NULL AND ? IS NULL))
        AND (Finishing = ? OR (Finishing IS NULL AND ? IS NULL))
        AND (Thickness = ? OR (Thickness IS NULL AND ? IS NULL))
        """, (pcb_name, pcb_board_per_sheet, pcb_color, pcb_color , pcb_finishing, pcb_finishing, pcb_thickness, pcb_thickness))

        row = cursor.fetchone()
        return row[0] if row else None
