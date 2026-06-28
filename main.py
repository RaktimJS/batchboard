# Entry point to the system

import os, sqlite3
import functions




# Database and Cursor
db = sqlite3.connect("tuition.db")
cur = db.cursor()

os.system("cls")

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



while True:
    # Operation selection list
    print(f"{BL}{B}BatchBoard v1{N}")
    print(f"  {Y}CREATE{N}")
    print(f"    ├── Enter {I}{B}1{N} {Y}→{N} Log New Session")
    print(f"    ├── Enter {I}{B}2{N}  {Y}→{N} Add new student")
    print(f"    ├── Enter {I}{B}3{N} {Y}→{N} Add new batch")
    print(f"    ├── Enter {I}{B}4{N}  {Y}→{N} Issue new test")
    print(f"    ├── Enter {I}{B}5{N}  {Y}→{N} Log test performance")
    print(f"    ├── Enter {I}{B}6{N}  {Y}→{N} Issue new fee")
    print(f"    ├── Enter {I}{B}7{N}  {Y}→{N} Log Payment")
    print(f"  {Y}READ{N}")
    print(f"    ├── Enter {I}{B}8{N}  {Y}→{N} View Batch Timetable")
    print(f"    ├── Enter {I}{B}9{N}  {Y}→{N} View Student Details")
    print(f"    ├── Enter {I}{B}10{N}  {Y}→{N} View Class-Wide Test Report")
    print(f"    ├── Enter {I}{B}11{N}  {Y}→{N} View Class-Wide Test Report per Batch")
    print(f"    ├── Enter {I}{B}12{N}  {Y}→{N} View Fee Defaulter Details")
    print(f"  {Y}UPDATE{R} (NOT AVAILABLE YET){W}")
    print(f"    ├── ..........")
    print(f"    ├── ..........")
    print(f"    ├── ..........")
    print(f"    ├── ..........")
    print(f"  {Y}DELETE{R} (NOT AVAILABLE YET){W}")
    print(f"    ├── ..........")
    print(f"    ├── ..........")
    print(f"    ├── ..........")
    print(f"    └── ..........\n")

    try:
        # Taking user's choice as input from the options in the above list
        while True:     # Iterate till the input is fully valid
            selector = input("Enter your choice from the above list: ")

            try:
                selector = int(selector)

                if selector >= 1 and selector <= 12:
                    os.system('cls')
                    break
                else:
                    if selector > 12:
                        print(f"  Options beyond {Y}12{W} are WIP")
                    else:
                        print("Out of range input\n")
            except ValueError:
                print("Invalid Input\n")
            except EOFError:
                print("Invalid Input\n")

        if selector == 1:
            functions.logSession()
        elif selector == 2:
            functions.addNewStudent()
        elif selector == 3:
            functions.addNewBatch()
        elif selector == 4:
            functions.issueNewTest()
        elif selector == 5:
            functions.logTestPerformance()
        elif selector == 6:
            functions.issueNewFee()
        elif selector == 7:
            functions.logPayments()
        elif selector == 8:
            functions.pivotBatchTime()
        elif selector == 9:
            functions.seeStudDetail()
        elif selector == 10:
            functions.classWideTestReport()
        elif selector == 11:
            functions.batchWiseTestReport()
        elif selector == 12:
            functions.defaulters()

        input(f"\n{B}Press ENTER to continue...{N}")
        os.system('cls')
    except Exception as e:
        print("An unknown error occured\n", e, sep="")
