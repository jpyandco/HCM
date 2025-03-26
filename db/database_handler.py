import oracledb
import configparser

from hcm.const import CONFIG


class DatabaseHandler:
    def __init__(self) -> None:
        # as singleton?
        self.config = configparser.ConfigParser()
        self.config.read(CONFIG)
        self.user = self.config["DB"]["user"]
        self.pwd = self.config["DB"]["pwd"]
        self.dsn = self.config["DB"]["dsn"]

    def select_from_db(self, tbl) -> list[dict]:
        sql = f"select * from {tbl}"
        formatted_rows = None

        try:
            connection = oracledb.connect(user=self.user, password=self.pwd, dsn=self.dsn)
            cursor = connection.cursor()
            cursor.execute(sql)

            rows = cursor.fetchall()
            # Get column names from the cursor description
            column_names = [desc[0].lower() for desc in cursor.description]
            # Format rows as a list of dictionaries
            formatted_rows = [dict(zip(column_names, row)) for row in rows]
            # for row in formatted_rows:
            #     print(row)
        except Exception as e:
            print(e)
            print(f"Error in {tbl}\n")

        finally:
            cursor.close()
            connection.close()

        return formatted_rows
