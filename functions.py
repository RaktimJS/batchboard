"""
Contains several functions that can be called whenever and wherever needed
"""

import sqlite3
from datetime import date, timedelta, datetime
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

        return tabulate(rows, headers=headers, tablefmt="pretty")
    except sqlite3.Error as e:
        print(f"Error: {e}")
        return None
    finally:
        conn.close()


# Functions for handling dates
def isDateValid(dateStr: str, indent = 0):
    try:
        datetime.strptime(dateStr, "%d-%m-%Y")
        return True
    except ValueError:
        return f"{R}{" "*indent}Invalid Date\n{" "*indent}Please check format: DD-MM-YYYY\n{" "*indent}Check for leap years and validate the number of days in each month{N}"

def fixDateFormat(dateStr: str):
    dateComp = dateStr.split("-")
    return f"{dateComp[2]}-{dateComp[1]}-{dateComp[0]}"


# Function to format ask() output
def toList(iterable:list):
    i = 0
    while i in range(len(iterable)):
        if len(iterable[i]) > 1:
            temp = []
            j = 0
            while j in range(len(iterable[i])):
                temp.append(iterable[i][j])
                j += 1
            iterable[i] = temp
            i += 1
        else:
            iterable[i] = iterable[i][0]
            i += 1

    return iterable




"""
    Core functions
"""


""" DATA CREATION FUNCTIONS """ 
# New Batch Creator
def addNewBatch():
    db = sqlite3.connect("tuition.db")
    cur = db.cursor()

    isSlotOccupied = False
    dayTimeList = []

    # Generate an ID for the batch
    cur.execute("SELECT * FROM Batch")
    batchNum = str(len(cur.fetchall()) + 1)

    if len(batchNum) == 1:
        batchNum = "0" + batchNum

    batchID = "BAT-" + batchNum
    print(f"Batch ID: {Y}{batchID}{N}")


    # Fetching Class ID
    while True:
        try:
            standard = input(f"Enter class (11 or 12 only): {Y}")
            standard = int(standard)
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
    classID = cur.fetchall()[0][0]

    # Batch Name
    batchName = input(f"Enter the batch name: {Y}").upper()
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
        cur.execute(f"INSERT INTO Batch (Batch_ID, Class_ID, Name) VALUES ('{batchID}', '{classID}', '{batchName}')")

        for i in dayTimeList:
            cur.execute(f"INSERT INTO Batch_Schedule (Batch_ID, Day, Time, Duration) VALUES ('{batchID}', '{i[0]}', '{i[1]}', '{i[2]}')")

        db.commit()
        db.close()
        print("\nDate population successful")
    except Exception as e:
        print("\nAn error occured:", e)
        print("Please try again\n")
        input("Hit ENTER to continue... ")
        __import__('os').system('cls')
        addNewBatch()


# New Student
def addNewStudent():
    db = sqlite3.connect("tuition.db")
    cur = db.cursor()
    
    name = input(f"Enter the name of the student: {Y}")
    print(W, end="")

    while True:
        try:
            standard = input(f"Enter class (11 or 12 only): {Y}")
            standard = int(standard)
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
    batchNameCombination = ask(f"SELECT Batch_Name, Batch_ID FROM Batch WHERE Class_ID = '{classID}'")
    batchIDList = toList(ask(f"SELECT Batch_ID FROM Batch WHERE Class_ID = '{classID}'"))

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
    studNum = str(len(ask(f"SELECT * FROM Student WHERE Batch_ID = '{batchID}';")) + 1)
    studID = batchID + "-STU-0" + studNum if len(studNum) == 1 else batchID + "-STU-" + studNum

    print("\n----------------------------------------\n")

    # Date of joining
    while True:
        joinDate = input(f"Enter the date of joining ('TODAY' if joined today): {Y}").strip()
        print(W, end="")

        if joinDate.lower() == "today":
            joinDate = str(date.today())
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
        addNewStudent()


# Log new session
def logSession():
    print(f"{B}{BL}Batch Selection{N}")

    grade11Batches = ask("SELECT Name, Batch_ID FROM Batch where Class_ID = 'CLS-11';")
    grade12Batches = ask("SELECT Name, Batch_ID FROM Batch where Class_ID = 'CLS-12';")

    if len(grade11Batches) != 0:
        print(f"{LY}  Batches in Class 11{N}")
        print("   ", tabulate(grade11Batches, headers=["Name", "Batch ID"], tablefmt="pretty").replace("\n", "\n    "))

        i = 0
        while i in range(len(grade11Batches)):
            grade11Batches[i] = grade11Batches[i][1]
            i += 1
    else:
        print(f"{LY}  Batches in Class 11{N}")
        print("    No Batches in Class 11")

    print()

    if len(grade12Batches) != 0:
        print(f"{LY}  Batches in Class 12{N}")
        print("   ", tabulate(grade12Batches, headers=["Name", "Batch ID"], tablefmt="pretty").replace("\n", "\n    "))

        i = 0
        while i in range(len(grade12Batches)):
            grade12Batches[i] = grade12Batches[i][1]
            i += 1
    else:
        print(f"{LY}  Batches in Class 12{N}")
        print("    No Batches in Class 12")

    print()

    while True:
        batchID = input(f"  Enter a batch ID from the above lists: {Y}").strip().upper()
        print(W, end="")

        if batchID in grade11Batches or batchID in grade12Batches:
            break
        else:
            print(f"    {R}Invalid Batch ID: No batch with ID {LY}{batchID}{R} was found{W}")

    print("\n----------------------------------------\n")

    print(f"{B}{BL}Date selection:")
    print(f"{R}  SESSIONS CAN BE LOGGED ONLY WITHIN 7 DAYS OF CONDUCTING IT{N}\n")

    print(f"  Enter {LY}TODAY{N} to select today's date")
    print(f"  Enter {LY}YESTERDAY{N} to select yesterday's date")
    print(f"  Enter any particular date within last 7 days in {LY}DD-MM-YYYY{N} format to select that date\n")
    
    while True:
        sessDate = input(f"    Enter your choice from the above list: {Y}").lower()
        print(W, end="")
        
        if sessDate == "today":
            sessDate = str(date.today())
            break
        elif sessDate == "yesterday":
            sessDate = str(date.today() - timedelta(days=1))
            break
        else:
            verifiedLogDate = isDateValid(sessDate)
            
            if verifiedLogDate == True:
                if datetime.strptime(sessDate, "%d-%m-%Y").date() >= date.today() - timedelta(days=7) and datetime.strptime(sessDate, "%d-%m-%Y").date() <= date.today():
                    break
                elif datetime.strftime(sessDate) >= date.today():
                    print(f"{R}Can't log future sessions{W}")
                else:
                    print(f"{R}Can't log a session after 7 days of conducting it{W}")
            else:
                print(verifiedLogDate)

    sessionNum = str(len(ask(f"SELECT * FROM Session WHERE Batch_ID = '{batchID}'")) + 1)

    if len(sessionNum) == 1:
        sessionNum = "0" + sessionNum

    sessionID = f"{batchID}-SES-{sessionNum}"

    db = sqlite3.connect("tuition.db")
    cur = db.cursor()

    try:
        cur.execute(f"INSERT INTO Session VALUES ('{sessionID}', '{batchID}', '{sessDate}')")
        db.commit()
        db.close()
        print("\nDate population successful")
    except Exception as e:
        print("\nAn error occured:", e)
        print("Please try again\n")
        input("Hit ENTER to continue... ")
        __import__('os').system('cls')
        logSession()


# Issue new Test
def issueNewTest():
    db = sqlite3.connect("tuition.db")
    cur = db.cursor()

    while True:
        try:
            standard = input(f"Enter class (11 or 12 only): {Y}")
            standard = int(standard)
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


    classID = ask(f"SELECT Class_ID FROM Class WHERE Class_Name = 'Class {standard}';")[0][0]
    testNum = str(len(ask(f"SELECT * FROM Test_Detail WHERE Class_ID = '{classID}';")) + 1)

    if len(testNum) == 1:
        testNum = "0" + testNum
    
    testID = f"{classID}-TST-{testNum}"

    testName = input(f"Enter the name of the test: {Y}").upper()
    print(W, end="")

    print("\n----------------------------------------\n")

    print(f"{BL}{B}Date Selection:{N}")
    print(f"  Enter {LY}TODAY{N} to select today's date")
    print(f"  Enter any particular date in {LY}DD-MM-YYYY{N} format to select that date\n")
    
    while True:
        testDate = input(f"    Enter your choice from the above list: {Y}").lower()
        print(W, end="")
        
        if testDate == "today":
            testDate = str(date.today())
            break
        else:
            verifiedTestDate = isDateValid(testDate)
            
            if verifiedTestDate == True:
                break
            else:
                print(verifiedTestDate)
    
    print("\n----------------------------------------\n")

    while True:
        try:
            fullMarks = input(f"Enter full marks for the test: {Y}")
            fullMarks = int(fullMarks)
            print(W, end="")
            
            if fullMarks <= 0:
                print(f"  {R}Full Marks cannot be less than or equal to zero{W}")
            else:
                break
        except ValueError:
            print(f"  {R}Invalid Input{W}")
        except EOFError:
            print(f"  {R}Invalid Input{W}")

    try:
        cur.execute(f"INSERT INTO Test_Detail VALUES ('{testID}', '{classID}', '{testName}', '{testDate}', '{fullMarks}')")
        db.commit()
        db.close()
        print("\nDate population successful")
    except Exception as e:
        print("\nAn error occured:", e)
        print("Please try again\n")
        input("Hit ENTER to continue... ")
        __import__('os').system('cls')
        issueNewTest()


# Log test performance
def logTestPerformance():
    # Test Selection
    print(f"{B}{BL}Unlogged Test Selection:{N}")
    testNameCombination = ask("SELECT Test_Name, Test_ID FROM Test_Detail td WHERE NOT EXISTS (SELECT 'any' FROM Test_Performance tp WHERE td.Test_ID = tp.Test_ID );")
    unloggedTests = toList(ask("SELECT Test_ID FROM Test_Detail td WHERE NOT EXISTS (SELECT 'any' FROM Test_Performance tp WHERE td.Test_ID = tp.Test_ID );"))

    table = "  " + tabulate(testNameCombination, headers=["Test Name", "ID"], tablefmt="pretty").replace("\n", "\n  ")
    print(table)
    print()

    while True:
        testID = input(f"  Select an unlogged test from the above list (Enter the Test ID): {Y}").strip().upper()
        print(W, end="")

        if testID in unloggedTests:
            break
        else:
            print(f"    {R}Test with ID {Y}{testID}{R} is either does not exit or has been logged already{W}")

    print("\n----------------------------------------\n")

    # Marks population
    idNameBatch = toList(ask(f"SELECT Stud_ID, Stud_Name, Batch_Name FROM Student NATURAL JOIN Batch NATURAL JOIN Test_Detail WHERE Test_ID = '{testID}';"))
    fullMarks = toList(ask(f"SELECT Full_Marks FROM test_Detail WHERE Test_ID = '{testID}'"))[0]

    testPerformanceValueList = []

    print(f"{BL}{B}Marks population:{N}")
    print(f"  ENTER {LY}ABS{N} TO MARK ABSENT\n")

    for i in idNameBatch:
        while True:
            try:
                markScored = input(f"  Student ID: {Y}{i[0]}{W} | Name: {Y}{i[1]}{W} | Batch: {Y}{i[0]}{W} | Marks Scored (Out of {fullMarks}): {Y}").strip().upper()
                print(W, end="")

                if markScored == "ABS":
                    testPerformanceValueList.append((testID, i[0], "ABSENT"))
                    break
                else:
                    markScored = int(markScored)

                    if markScored >= 0 and markScored <= fullMarks:
                        testPerformanceValueList.append(f"('{testID}', '{i[0]}', {markScored})")
                        break
                    else:
                        print(f"    Value must be in the range 0 to {fullMarks} (inclusive)")
            except ValueError:
                print(f"    {R}Invalid Input{W}")
            except EOFError:
                print(f"    {R}Invalid Input{W}")
        
    db = sqlite3.connect("tuition.db")
    cur = db.cursor()

    try:
        for i in testPerformanceValueList:
            cur.execute(f"INSERT INTO Test_Performance VALUES {i}")

        db.commit()
        db.close()
        print("\nDate population successful")
    except Exception as e:
        print("\nAn error occured:", e)
        print("Please try again\n")
        input("Hit ENTER to continue... ")
        __import__('os').system('cls')
        issueNewTest()


# Issue new fee
def issueNewFee():
    while True:
        try:
            standard = input(f"Enter class (11 or 12 only): {Y}")
            standard = int(standard)
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
    
    print("\n----------------------------------------\n")

    # Issue Date
    print(f"{BL}{B}Issue Date:{N}")
    
    feeIssueDate = str(date.today())
    today_date = str(date.today()).split("-")
    today_date = f"{today_date[-1]}-{today_date[-2]}-{today_date[-3]}"

    print(f"  Issue date: {Y}{today_date}{W}")
    
    while True:
        todayYN = input(f"  Proceed? (Y/N): {W}")
        
        if todayYN.upper() in ["Y", "N"]:
            break

    if todayYN.upper() == "Y":
        pass
    elif todayYN.upper() == "N":
        while True:
            feeIssueDate = input(f"\n  Enter issue date: {Y}").upper()
            print(W, end="")

            verifiedFeeIssueDate = isDateValid(feeIssueDate, 4)
            
            if verifiedFeeIssueDate == True:
                feeIssueDate = fixDateFormat(feeIssueDate)
                break
            else:
                print(verifiedFeeIssueDate)
    else:
        print(f"    {R}Invalid Input{W}")

    print("\n----------------------------------------\n")

    # Fee name
    print(f"{B}{BL}Fee Description{N}")
    print(f"  {Y}Options{N}")
    print(f"    Enter {Y}1{W} for {LY}Monthly Fee{W}")
    print(f"    Enter {Y}2{W} for {LY}Revision Class Fee{W}")
    print(f"    Enter {Y}3{W} for {LY}Additional Class Fee{W}")
    print(f"    Enter {Y}4{W} for {LY}Other... (Enter manually){W}\n")

    while True:
        try:
            feeNameChoice = input(f"    Choose from the above list: {Y}")
            print(W, end="")
            feeNameChoice = int(feeNameChoice)

            if feeNameChoice < 0 or feeNameChoice > 4:
                print(f"      {R}Out of range input{W}")
            else:
                if feeNameChoice == 1:
                    feeName = "Monthly Fee"
                elif feeNameChoice == 2:
                    feeName = "Revision Class Fee"
                elif feeNameChoice == 3:
                    feeName = "Additional Class Fee"
                else:
                    feeName = input(f"      Enter a short fee description: {Y}")
                    print(W, end="")
                
                break
        except ValueError:
            print(f"      {R}Invalid input{W}")
        except EOFError:
            print(f"      {R}Invalid input{W}")

    print("\n----------------------------------------\n")

    # Student Selection by batch
    classID = "CLS-11" if standard == 11 else "CLS-12"
    batchNameCombination = ask(f"SELECT Batch_Name, Batch_ID FROM Batch WHERE Class_ID = '{classID}'")
    batchIDList = toList(ask(f"SELECT Batch_ID FROM Batch WHERE Class_ID = '{classID}'"))

    table = "    " + tabulate(batchNameCombination, headers=["Batch Name", "ID"], tablefmt="pretty").replace("\n", "\n    ")

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
    feeNum = str(len(ask(f"SELECT DISTINCT Fee_ID FROM Fee NATURAL JOIN Fee_Assignment NATURAL JOIN Student WHERE Batch_ID = '{batchID}';")) + 1)
    feeID = batchID + "-FEE-0" + feeNum if len(feeNum) == 1 else batchID + "-FEE-" + feeNum

    print("\n----------------------------------------\n")

    # Assign fee to
    print(f"{BL}{B}Fee assignment options{N}")
    print()
    print(f"  Enter {Y}1{W} to assign fee to all students")
    print(f"  Enter {Y}2{W} to assign fee to all students except selected students")
    print(f"  Enter {Y}3{W} to assign fee to only selected students\n")

    while True:
        try:
            choice = input(f"  Choice: {Y}")
            print(W, end="")
            choice = int(choice)

            if choice < 0 or choice > 3:
                print(f"    {R}Out of range input{W}")
            else:
                break
        except ValueError:
            print(f"    {R}Invalid input{W}")
        except EOFError:
            print(f"    {R}Invalid input{W}")

    if choice == 1:
        studIDList = toList(ask(f"SELECT Stud_ID FROM Student WHERE Batch_ID = '{batchID}'"))
        try:
            db = sqlite3.connect("tuition.db")
            cur = db.cursor()
            cur.execute(f"INSERT INTO Fee VALUES ('{feeID}', '{feeIssueDate}', '{feeName}')")

            for i in studIDList:
                cur.execute(f"INSERT INTO Fee_Assignment VALUES ('{feeID}', '{i}')")

            db.commit()
            db.close()
            print()
            print("\nDate population successful")
        except Exception as e:
            print("\nAn error occured:", e)
            print("Please try again\n")
            input("Hit ENTER to continue... ")
            __import__('os').system('cls')
            issueNewTest()
    elif choice == 2:
        studIDNameCombination = ask(f"SELECT Stud_ID, Stud_Name FROM Student WHERE Batch_ID = '{batchID}'")
        studIDList = toList(ask(f"SELECT Stud_ID FROM Student WHERE Batch_ID = '{batchID}'"))

        try:
            print("   ", tabulate(studIDNameCombination, headers=["ID", "Name"], tablefmt="pretty").replace("\n", "\n    "))
            print()

            excludedIDList = []

            print(f"{Y}  Rules{LY}")
            print(f"    Enter an ID to put it into exclusion list")
            print(f"    Re-enter the ID to remove it from the exclusion list")
            print(f"    Enter {Y}END{LY} to quit entering IDs further{Y}\n")
            print(f"    NOTE: If exclusion list is empty, then the fee will be issued to all students{W}\n")

            while True:
                excludedID = input(f"  Enter ID to exclude (Enter {Y}'END'{W} to quit): {Y}").strip().upper()
                print(W, end="")

                if excludedID == "END":
                    break
                else:
                    if excludedID in studIDList and excludedID not in excludedIDList:
                        excludedIDList.append(excludedID)
                        print(f"    {LB}Student with ID {excludedID} exluded{W}")
                    elif excludedID in studIDList and excludedID in excludedIDList:
                        excludedIDList.remove(excludedID)
                        print(f"    {LB}Student with ID {excludedID} removed from exlusion list{W}")
                    else:
                        print(f"    {LB}Student with ID {excludedID} does not exist{W}")

            db = sqlite3.connect("tuition.db")
            cur = db.cursor()
            cur.execute(f"INSERT INTO Fee VALUES ('{feeID}', '{feeIssueDate}', '{feeName}')")

            for i in studIDList:
                if i not in excludedIDList:
                    cur.execute(f"INSERT INTO Fee_Assignment VALUES ('{feeID}', '{i}')")

            db.commit()
            db.close()
            print()
            print("\nDate population successful")
        except Exception as e:
            print("\nAn error occured:", e)
            print("Please try again\n")
            input("Hit ENTER to continue... ")
            __import__('os').system('cls')
            issueNewTest()
    else:
        studIDNameCombination = ask(f"SELECT Stud_ID, Stud_Name FROM Student WHERE Batch_ID = '{batchID}'")
        studIDList = toList(ask(f"SELECT Stud_ID FROM Student WHERE Batch_ID = '{batchID}'"))

        try:
            print("   ", tabulate(studIDNameCombination, headers=["ID", "Name"], tablefmt="pretty").replace("\n", "\n    "))
            print()

            selectedIDList = []

            print(f"{Y}  Rules{LY}")
            print(f"    Enter an ID to put it into selectionion list")
            print(f"    Re-enter the ID to remove it from the selectionion list")
            print(f"    Enter {Y}END{LY} to quit entering IDs further{Y}\n")
            print(f"    NOTE: Selection list cannot be empty{W}\n")

            while True:
                selectedID = input(f"  Enter ID to select (Enter {Y}'END'{W} to quit): {Y}").strip().upper()
                print(W, end="")

                if selectedID == "END":
                    if len(selectedIDList) >= 1:
                        break
                    else:
                        print(f"    {LB}Selection list cannot be empty. Please select at least one student")
                else:
                    if selectedID in studIDList and selectedID not in selectedIDList:
                        selectedIDList.append(selectedID)
                        print(f"    {LB}Student with ID {selectedID} selected{W}")
                    elif selectedID in studIDList and selectedID in selectedIDList:
                        selectedIDList.remove(selectedID)
                        print(f"    {LB}Student with ID {selectedID} removed from selection list{W}")
                    else:
                        print(f"    {LB}Student with ID {selectedID} does not exist{W}")

            db = sqlite3.connect("tuition.db")
            cur = db.cursor()
            cur.execute(f"INSERT INTO Fee VALUES ('{feeID}', '{feeIssueDate}', '{feeName}')")
            
            for i in selectedIDList:
                cur.execute(f"INSERT INTO Fee_Assignment VALUES ('{feeID}', '{i}')")

            db.commit()
            db.close()
            print("\nDate population successful")
        except Exception as e:
            print("\nAn error occured:", e)
            print("Please try again\n")
            input("Hit ENTER to continue... ")
            __import__('os').system('cls')
            issueNewTest()


__import__('os').system('cls')
print(drawTable("select * from student;"))
print(drawTable("select * from fee;"))
print(drawTable("select * from fee_assignment;"))

issueNewFee()

print(drawTable("select * from student;"))
print(drawTable("select * from fee;"))
print(drawTable("select * from fee_assignment;"))
