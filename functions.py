"""
Contains several functions that can be called whenever and wherever needed
"""

import sqlite3, time
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




"""
    Core functions
"""

# New Batch Creator
def addNewBatch():
    db = sqlite3.connect("tuition.db")
    cur = db.cursor()
    
    while True:
        isSlotOccupied = False
        dayTimeList = []

        # Generate an ID for the batch
        cur.execute("SELECT * FROM Batch")
        batchNum = str(len(cur.fetchall()) + 1)

        if len(batchNum) == 1:
            batchNum = "0" + batchNum

        b_id = "BAT-" + batchNum
        print(f"Batch ID: {Y}{b_id}{N}")


        # Fetching Class ID
        while True:
            try:
                standard = int(input(f"Enter class (11 or 12 only): {Y}"))
                print(W, end="")

                if standard in [11, 12]:
                    break
                else:
                    print(f"{W}Out of range\n")
            except ValueError:
                print(f"{W}Invalid Input\n")
            except EOFError:
                print(f"{W}Invalid Input\n")
        standard = str(standard)

        cur.execute(f"SELECT Class_ID FROM Class WHERE Class_Name = \"Class {standard}\";")
        c_id = cur.fetchall()[0][0]

        # Batch Name
        b_name = input(f"Enter the batch name: {Y}")
        print(W, end="")

        print("\n----------------------------------------\n")

        print(f"{BL}{B}Day Selection{N}")
        print("  Sunday")
        print("  Monday")
        print("  Tueday")
        print("  Wednesday")
        print("  Thursday")
        print("  Friday")
        print("  Saturday\n")

        print("Enter the day of the week to select (or deselect) it\n")

        dayList = []
        i = 0
        while True:
            day = input(f"Select a day of the week (Type 'END' to end): {Y}").capitalize().strip()
            print(W, end="")

            if day == "End":
                if len(dayList) < 1:
                    print(f"{LB}Choose at least one day for the batch{W}\n")
                else:
                    break
            else:
                if day in ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]:
                    if day in dayList:
                        dayList.remove(day)
                        print(f"{LB}{day}{W} removed")
                    else:
                        dayList.append(day)
                        print(f"{LB}{day}{W} added")
                else:
                    print(f"{W}{day} does not exist")

        # Timing
        print("\n----------------------------------------\n")

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
                print(f"  {Y}{dayList[i]}{W}")

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
            print("\nDate population successful")
            break
        except Exception as e:
            print("\nAn error occured:", e)
            print("Please try again\n")
            input("Hit ENTER to continue... ")
            __import__('os').system('cls')

# New Student
def addNewStudent():
    db = sqlite3.connect("tuition.db")
    cur = db.cursor()
    
    name = input(f"Enter the name of the student: {Y}")
    print(W, end="")

    while True:
        try:
            standard = int(input(f"Enter class (11 or 12 only): {Y}"))
            print(W, end="")

            if standard in [11, 12]:
                break
            else:
                print(f"    {W}Out of range")
        except ValueError:
            print(f"    {W}Invalid Input")
        except EOFError:
            print(f"    {W}Invalid Input")
    standard = str(standard)

    while True:
        try:
            phone = input(f"Enter phone number: {Y}")
            print(W, end="")

            if phone.isnumeric() and len(phone) == 10:
                break
            else:
                print(f"{W}Invalid Phone Number")
        except ValueError:
            print(f"{W}Invalid Input\n")
        except EOFError:
            print(f"{W}Invalid Input\n")

    print("\n----------------------------------------\n")

    # Batch Selection
    classID = "CLS-11" if standard == 11 else "CLS-12"
    batchNameCombination = ask(f"SELECT Name, Batch_ID FROM Batch WHERE Class_ID = '{classID}'")
    batchIDList = ask(f"SELECT Batch_ID FROM Batch WHERE Class_ID = '{classID}'")[0]

    table = "  " + tabulate(batchNameCombination, headers=["Batch Name", "ID"], tablefmt="pretty").replace("\n", "\n  ")

    print(f"{BL}{B}Batch Selection{N}")
    print(f"  Batches in Class {standard}:")
    print(table)
    print()

    while True:
        batchID = input(f"  Select a batch from the above list (Enter the Batch ID): {Y}").strip().upper()
        print(W, end="")

        if batchID in batchIDList:
            break
        else:
            print(f"\tBatch with ID {Y}{batchID}{W} not available in Class 12")

    # Generating student ID
    studNum = str(len(ask(f"SELECT * FROM Student;")) + 1)
    studID = batchID + "-STU-0" + studNum if len(studNum) == 1 else batchID + "-STU-" + studNum

    print("\n----------------------------------------\n")

    def isDateValid(dateStr: str):
        dateComponent = dateStr.strip().split("-")

        monthLengthMap = {
            1: 31, 2: 28, 3: 31,
            4: 30, 5: 31, 6: 30,
            7: 31, 8: 31, 9: 30,
            10: 31, 11: 30, 12: 31
        }

        months = [
            "January", "February", "March", "April",
            "May", "June", "July", "August",
            "September", "October", "November", "December"
        ]

        if (
                len(dateComponent) != 3
                and len(dateStr) != 10
                and len(dateStr.replace("-", "")) == 8
                and not dateStr.replace("-", "").isnumeric()
                and dateStr[2] != "-"
                and dateStr[5] != "-"
            ):
            return f"{R}Invalid format: Date should be in {LY}DD-MM-YYYY{R} format{W}"
        else:
            i = 0
            while i in range(len(dateComponent)):
                dateComponent[i] = int(dateComponent[i])
                i += 1

            if dateComponent[2] not in range(2020, 2101):
                return f"{R}Invalid year component: Year should be an integer between 2020 and 2100 (Both included){W}"
            else:
                if dateComponent[1] not in range(1, 13):
                    return f"{R}Invalid month component: Month should be an integer from 1 to 12{W}"
                else:
                    if dateComponent[0] == 29 and dateComponent[1] == 2 and dateComponent[2] % 4 == 0:
                        return True
                    elif dateComponent[0] > monthLengthMap[dateComponent[1]] and dateComponent[1] == 2:
                        return f"{R}Invalid day component: {months[dateComponent[1] - 1]} {dateComponent[2]} has {monthLengthMap[dateComponent[1]]} days{W}"
                    elif dateComponent[0] > monthLengthMap[dateComponent[1]] and dateComponent[1] != 2:
                        return f"{R}Invalid day component: {months[dateComponent[1] - 1]} has {monthLengthMap[dateComponent[1]]} days{W}"
                    else:
                        return True

    def fixDateFormat(dateStr: str):
        dateComp = dateStr.split("-")
        return f"{dateComp[2]}-{dateComp[1]}-{dateComp[0]}"

    def getTodayDate():
        year = str(tuple(time.localtime())[0])
        month = str(tuple(time.localtime())[1])
        day = str(tuple(time.localtime())[2])

        if len(month) == 1:
            month = "0" + month

        if len(day) == 1:
            day = "0" + day

        return f"{year}-{month}-{day}"


    # Date of joining
    while True:
        joinDate = input(f"Enter the joinDate of joining ('TODAY' if joined today): {Y}").strip()
        print(W, end="")

        if joinDate.lower() == "today":
            joinDate = getTodayDate()
            break
        else:
            if isDateValid(joinDate) == True:
                joinDate = fixDateFormat(joinDate)
                break
            else:
                print(f"  {isDateValid(joinDate)}")

    try:
        cur.execute(f"INSERT INTO Student VALUES ('{studID}', '{batchID}', '{name}', '{phone}', '{joinDate}', 0)")
        db.commit()
        db.close()
        print("\nDate population successful")
    except Exception as e:
        print("\nAn error occured:", e)
        print("Please try again\n")
        input("Hit ENTER to continue... ")
        __import__('os').system('cls')
