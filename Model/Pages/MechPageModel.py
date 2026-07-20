from pyodbc import IntegrityError

from Model.Connection import Connection


class MechPageModel:
    def __init__(self):
        self.conn = Connection.connect()

    def fetch_all_data(self):
        cursor = self.conn.cursor()
        cursor.execute("""
        SELECT Type,Name,Color,Quantity,Comment
        FROM tbl_Mech_part
        ORDER BY Type
        """)
        result = cursor.fetchall()

        cursor.close()
        return list(result)

    def fetch_distinct_values(self,column_name):
        cursor = self.conn.cursor()

        cursor.execute(f"""
        SELECT DISTINCT {column_name} 
        FROM tbl_Mech_part  
        """)
        list_distinct = cursor.fetchall()
        result = [i[0] for i in list_distinct]

        cursor.close()
        return result

    def search(self,mech_name):
        cursor = self.conn.cursor()
        cursor.execute("""
        SELECT Type,Name,Color,Quantity,Comment
        FROM tbl_Mech_part
        WHERE Name=?
        """,(mech_name,))
        result = cursor.fetchall()

        cursor.close()
        return list(result)

    def insert(self,mech_type,mech_name,mech_color,mech_qty,mech_comment):
        cursor = self.conn.cursor()

        try:
            cursor.execute("""
            INSERT INTO tbl_Mech_part 
            (Type,Name,Color,Quantity,Comment)
            VALUES (?,?,?,?,?)
            """,(mech_type,mech_name,mech_color,mech_qty,mech_comment))

            self.conn.commit()
            return "Insert successful",1

        except IntegrityError:
            self.conn.rollback()
            return "mechanical part Exists",0

        finally:
            cursor.close()

    def remove(self,mech_type,mech_name,mech_color):
        cursor = self.conn.cursor()

        cursor.execute("""
        DELETE FROM tbl_Mech_part
        WHERE Type=?
        AND Name=?
        AND (Color = ? OR (Color IS NULL AND ? IS NULL))
        """,(mech_type, mech_name,mech_color,mech_color))

        if cursor.rowcount == 0:
            cursor.close()
            return "No mechanical part found",0

        self.conn.commit()
        cursor.close()
        return "Remove successful",1

    def adv_search(self, mech_type, mech_name, mech_color):
        cursor = self.conn.cursor()

        command_list = [["Name=?", mech_name], ["Color=?", mech_color]]
        value_list = [mech_type]
        conditions_string = """
        SELECT Type,Name,Color,Quantity,Comment
        FROM tbl_Mech_part
        WHERE Type=?
        """
        for condition, value in command_list:
            if value is not None:
                conditions_string += f" AND {condition}"
                value_list.append(value)

        cursor.execute(conditions_string,value_list)
        result = cursor.fetchall()

        cursor.close()
        return result

    def fetch_comboboxes_items(self,mech_type):
        cursor = self.conn.cursor()

        cursor.execute("""
        SELECT DISTINCT
        Name,Color
        FROM tbl_Mech_part
        WHERE Type = ?
        """,(mech_type,))

        rows = cursor.fetchall()
        cursor.close()

        return (sorted(list(set([i[0] for i in rows if i[0] is not None]))),
                sorted(list(set([i[1] for i in rows if i[1] is not None]))))

    def edit_data(self,current_row,new_row):
        cursor = self.conn.cursor()

        try:
            cursor.execute("""
            UPDATE tbl_Mech_part
            SET Type=?,Name=?,Color=?,Quantity=?,Comment=?
            WHERE Type=?
            AND Name=?
            AND (Color = ? OR (Color IS NULL AND ? IS NULL))
            """,
            (new_row[0],new_row[1],new_row[2],new_row[3],new_row[4],
            current_row[0],current_row[1],current_row[2],current_row[2]))
            self.conn.commit()
            return "Edit successful",1

        except IntegrityError:
            self.conn.rollback()
            return "mechanical part exists",0

        finally:
            cursor.close()
