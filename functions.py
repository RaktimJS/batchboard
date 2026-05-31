"""
Contains several functions that can be called whenever and wherever needed
"""

import sqlite3




"""
        Utility functions
"""
# Query Executioner
def ask(query:str, db:str):
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


