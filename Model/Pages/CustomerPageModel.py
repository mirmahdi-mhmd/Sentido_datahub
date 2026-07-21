from pyodbc import IntegrityError

from Model.Connection import Connection


class CustomerPageModel:
    def __init__(self):
        self.conn = Connection.connect()

    def fetch_all_data(self):
        cursor = self.conn.cursor()
        cursor.execute("""
        SELECT Name,Tel,City,Address,Comment
        FROM tbl_Customer
        ORDER BY Name
        """)
        result = cursor.fetchall()

        cursor.close()
        return list(result)

    def fetch_distinct_values(self,column_name):
        cursor = self.conn.cursor()

        cursor.execute(f"""
        SELECT DISTINCT {column_name} 
        FROM tbl_Customer  
        """)
        list_distinct = cursor.fetchall()
        result = [i[0] for i in list_distinct]

        cursor.close()
        return result

    def search(self,customer_name):
        cursor = self.conn.cursor()
        cursor.execute("""
        SELECT Name,Tel,City,Address,Comment
        FROM tbl_Customer
        WHERE Name=?
        """,(customer_name,))
        result = cursor.fetchall()

        cursor.close()
        return result

    def insert(self,customer_name,customer_tel,customer_city,customer_address,customer_comment):
        cursor = self.conn.cursor()

        try:
            cursor.execute("""
            INSERT INTO tbl_Customer 
            (Name,Tel,City,Address,Comment)
            VALUES (?,?,?,?,?)
            """,(customer_name,customer_tel,customer_city,customer_address,customer_comment))

            self.conn.commit()
            return "Insert successful",1

        except IntegrityError:
            self.conn.rollback()
            return "Customer exists",0

        finally:
            cursor.close()

    def remove(self,customer_name,customer_tel,customer_city,customer_address):
        cursor = self.conn.cursor()
        try:
            cursor.execute("""
            DELETE FROM tbl_Customer
            WHERE Name=?
            AND Tel=?
            AND City=?
            AND Address=?
            """,( customer_name,customer_tel,customer_city,customer_address))

            if cursor.rowcount == 0:
                return "No customer found",0

            self.conn.commit()
            return "Remove successful",1

        except IntegrityError:
            self.conn.rollback()
            return "a reference exists in Order table", 0

        finally:
            cursor.close()

    def adv_search(self,customer_name, customer_tel, customer_city):
        cursor = self.conn.cursor()

        command_list = [["Name=?", customer_name],["Tel=?", customer_tel],["City=?", customer_city]]
        value_list = []
        conditions_string = """
        SELECT Name,Tel,City,Address,Comment
        FROM tbl_Customer
        WHERE 
        """
        for condition, value in command_list:
            if value is not None:
                conditions_string += f"{condition} AND "
                value_list.append(value)

        conditions_string += "Customer_ID is not null"
        cursor.execute(conditions_string,value_list)
        result = cursor.fetchall()

        cursor.close()
        return result

    def fetch_comboboxes_items(self,customer_name):
        cursor = self.conn.cursor()

        cursor.execute("""
        SELECT DISTINCT
        Tel,City,Address
        FROM tbl_Customer
        WHERE Name = ?
        """,(customer_name,))

        rows = cursor.fetchall()
        cursor.close()

        return (sorted(list(set([i[0] for i in rows if i[0] is not None]))),
                sorted(list(set([i[1] for i in rows if i[1] is not None]))),
                sorted(list(set([i[2] for i in rows if i[2] is not None]))))

    def edit_data(self,current_row,new_row):
        cursor = self.conn.cursor()

        try:
            cursor.execute("""
            UPDATE tbl_Customer
            SET Name=?,Tel=?,City=?,Address=?,Comment=?
            WHERE Name=?
            AND Tel=?
            AND City=?
            AND Address=?
            """,
            (new_row[0],new_row[1],new_row[2],new_row[3],new_row[4],
            current_row[0],current_row[1],current_row[2],current_row[3]))

            self.conn.commit()
            return "Edit successful",1

        except IntegrityError:
            self.conn.rollback()
            return "Customer exists",0

        finally:
            cursor.close()
