"""
Contains several functions that can be called whenever and wherever needed
"""




import sqlite3


# Query Executioner
def ask(query:str, cursorObj):
        cursorObj.execute(query)
        return cursorObj.fetchall()

