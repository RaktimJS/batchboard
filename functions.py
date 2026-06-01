"""
Contains several functions that can be called whenever and wherever needed
"""

import sqlite3
from tabulate import tabulate




# formatting options
R = "\033[38;2;255;0;0m"
Y = "\033[38;2;255;255;0m"
B = "\033[38;2;0;0;255m"
W = "\033[38;2;212;212;212m"
LB = "\033[38;2;135;206;235m"
LY = "\033[38;2;255;255;153m"

b = "\033[1m"
B = "\033[1m"
I = "\033[3m"
U = "\033[4m"

n = "\033[0m"
N = "\033[0m"


"""
        Utility functions
"""
# Query Executioner
def ask(query:str, db:str):
def ask(query:str, db:str = "tuition.db"):
        database = sqlite3.connect(db)
        cur = database.cursor()
        cur.execute(query)
        data = cur.fetchall()
        database.close()
        return data

def fetchTable(name: str):
        db = sqlite3.connect("tuition.db")
        cur = db.cursor()

        cur.execute(f"SELECT * FROM {name};")
        row = cur.fetchall()
        cur.execute(f"PRAGMA table_info({name});")
        column = cur.fetchall()

        for i in range(0, len(column)):
                column[i] = column[i][1]

        db.close()
        return [row, column]

def getAllID(name:str):
        if name in ["Class", "Batch", "Student", "Session", "Test_Detail", "Fee_ID", "Payment_ID"]:
                db = sqlite3.connect("tuition.db")
                cur = db.cursor()

                cur.execute(f"SELECT * FROM {name};")
                data = cur.fetchall()

                id_list = []
                for i in data:
                        id_list.append(i[0])
                
                return id_list
        else:
                raise NameError

        conn = sqlite3.connect(db)
        cursor = conn.cursor()

                cursor.execute(f"SELECT * FROM {table_name}")

                rows = cursor.fetchall()
                headers = [column[0] for column in cursor.description]

                if rows:
                        print(tabulate(rows,
                                       headers=headers,
                                       tablefmt="psql"))
                else:
                        print(f"Table '{table_name}' is empty.")

        except sqlite3.Error as e:
                print(f"Error: {e}")
        finally:
                conn.close()

