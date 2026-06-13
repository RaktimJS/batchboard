"""
Contains several functions that can be called whenever and wherever needed
"""

import sqlite3
from tabulate import tabulate




# formatting options
R = "\033[38;2;255;0;0m"
Y = "\033[38;2;255;255;0m"
BL = "\033[38;2;0;0;255m"
W = "\033[38;2;212;212;212m"
LB = "\033[38;2;135;206;235m"
LY = "\033[38;2;255;255;153m"

B = "\033[1m"
I = "\033[3m"
U = "\033[4m"

N = "\033[0m"


"""
    Utility functions
"""
# Query Executioner
def ask(query:str, db:str = "tuition.db"):
    database = sqlite3.connect(db)
    cur = database.cursor()
    cur.execute(query)
    data = cur.fetchall()
    database.close()

    if data != None:
        return data


def drawTable(query: str, db: str = "tuition.db"):
    conn = sqlite3.connect(db)
    cursor = conn.cursor()
    
    try:
        cursor.execute(query)
        rows = cursor.fetchall()

        if not cursor.description:
            return None

        headers = [column[0] for column in cursor.description]

        return tabulate(rows, headers=headers, tablefmt="psql")
    except sqlite3.Error as e:
        print(f"Error: {e}")
        return None
    finally:
        conn.close()





        print(f"{BL}{B}Timing{N}")
        print(f"{Y}  Rules{LY}")
        print(f"    Use 24-hour clock system")
        print(f"    Format: ___ ___ ___ ___ ({I}{U}{LY} Hrs {N} {I}{U}{LY} Hrs {N} {I}{U}{LY} Min {N} {I}{U}{LY} Min {N}{LY}){N}\n")

        i = 0

        # Seperate function ot handle time inputs
        def isTimeValid(time:str):
            try:
                int(time)
                if len(time) != 4:
                    return f"{R}Invalid Time Format: Should be 4 characters, all being digits in HHMM format{N}"
                else:
                    if time[0] == "-":
                        return f"{R}Invalid Character Found: Time cannot be negative{N}"
                    if int(time[:2]) >= 0 and int(time[:2]) <= 23:
                        if int(time[2:]) >= 0 and int(time[2:]) <= 59:
                            return True
                        else:
                            return f"{R}Invalid Time Format: Minute should be either 0 or an integer between 1 and 59, written with a preceding \"0\" if single digit{N}"
                    else:
                        return f"{R}Invalid Time Format: Hour should be either 0 or an integer from 1 to 23, written with a preceding \"0\" if single digit{N}"
            except ValueError:
                return f"{R}Invalid Character Found{N}"

        def addTime(time1:str, time2:str):
            minList = [int(time1[2:]), int(time2[2:])]

            hrs = int(time1[:2]) + int(time2[:2])
            min = sum(minList)

            if min >= 60:
                hrs += 1
            
            hrs = str(hrs)
            min = str(min)

            if len(min) == 1:
                min = "0"+min            

            if len(hrs) == 1:
                hrs = "0"+hrs            

            return hrs + min

        dayTimeData = ask(f"SELECT Batch_ID, Name, Time, Duration FROM Batch NATURAL JOIN Batch_Schedule WHERE Day = '{dayList[i]}' ORDER BY Time;")

        if len(dayTimeData) > 0:
            i = 0
            while i in range (len(dayList)):
                print(f"  {Y}{dayList[i]}{W}")

                # Time definition
                while True:
                    time = input(f"    Time: {Y}")
                    print(N, end="")
                    verifiedTime = isTimeValid(time)

                    if verifiedTime == True:
                        for j in dayTimeData:
                            if int(time) in range(int(j[2]), int(addTime(j[2], j[3]))):
                                isSlotOccupied = True
                                break

                        if isSlotOccupied == False:
                            break
                        else:
                            print(f"      {R}Conflict Detected{W}")
                            print(f"      -----------------{LY}")
                            print(f"\t{int(j[2][:2])}:{j[2][2:]}{W} to {LY}{int(addTime(j[2], j[3])[:2])}:{addTime(j[2], j[3])[2:]}{W} ::: {LY}{j[1]}{W} (ID: {LY}{j[0]}{W})")
                            print(f"      -----------------")
                            print()
                            isSlotOccupied = False
                    else:
                        print("\t", verifiedTime, sep="")
                
                # --------------------------------------------------
    
                # Duration definition
                while True:
                    duration = input(f"    Duration: {Y}")
                    print(N, end="")
                    verifiedDuration = isTimeValid(duration)

                    if verifiedDuration == True:
                        for j in dayTimeData:
                            if int(addTime(time, duration)) in range(int(j[2])+1, int(addTime(j[2], j[3]))):
                                isSlotOccupied = True
                                break

                        if isSlotOccupied == False:
                            break
                        else:
                            print(f"      {R}Conflict Detected{W}")
                            print(f"      -----------------{LY}")
                            print(f"\t{int(j[2][:2])}:{j[2][2:]}{W} to {LY}{int(addTime(j[2], j[3])[:2])}:{addTime(j[2], j[3])[2:]}{W} ::: {LY}{j[1]}{W} (ID: {LY}{j[0]}{W})")
                            print(f"      -----------------")
                            print()
                            isSlotOccupied = False
                    else:
                        print("\t", verifiedDuration, sep="")

                dayTimeList.append((dayList[i], time, duration))
                i += 1
        else:
            i = 0
            while i in range (len(dayList)):
                while True:
                    time = input(f"    Time: {Y}")
                    print(N, end="")
                    verifiedTime = isTimeValid(time)

                    if verifiedTime == True:
                        break
                    else:
                        print("\t", verifiedTime, sep="")
                
                while True:
                    duration = input(f"    Duration: {Y}")
                    print(N, end="")
                    verifiedDuration = isTimeValid(duration)

                    if verifiedDuration == True:
                        break
                    else:
                        print("\t", verifiedDuration, sep="")
                
                dayTimeList.append((dayList[i], time, duration))
                i += 1

        try:
            cur.execute(f"INSERT INTO Batch (Batch_ID, Class_ID, Name) VALUES ('{b_id}', '{c_id}', '{b_name}')")

            for i in dayTimeList:
                cur.execute(f"INSERT INTO Batch_Schedule (Batch_ID, Day, Time, Duration) VALUES ('{b_id}', '{i[0]}', '{i[1]}', '{i[2]}')")

            db.commit()
            db.close()
            break
        except Exception as e:
            print("\nAn error occured:", e)
            print("Please try again\n")
            input("Hit ENTER to continue... ")
            __import__('os').system('cls')
addNewBatch()
