# Entry poin to the system

import os

os.system("cls")

# formatting options
R = "\033[38;2;255;0;0m"
Y = "\033[38;2;255;255;0m"
B = "\033[38;2;0;0;255m"
W = "\033[38;2;212;212;212m"
LB = "\033[38;2;135;206;235m"
LY = "\033[38;2;255;255;153m"

b = "\033[1m"
i = "\033[3m"
u = "\033[4m"

n = "\033[0m"




# Operation selection list
print(f"{Y}TuitionDesk v0.1{n}")
print(f"    {LY}├── Enter {i}{b}1{n}  {Y}→{n} Add new student")
print(f"    {LY}├── Enter {i}{b}2{n}  {Y}→{n} View student details")
print(f"    {LY}├── Enter {i}{b}3{n}  {Y}→{n} Remove student")
print(f"    {LY}├── Enter {i}{b}4{n}  {Y}→{n} Issue new test")
print(f"    {LY}├── Enter {i}{b}5{n}  {Y}→{n} Log test performance")
print(f"    {LY}├── Enter {i}{b}6{n}  {Y}→{n} View test details")
print(f"    {LY}├── Enter {i}{b}7{n}  {Y}→{n} Issue new fee")
print(f"    {LY}├── Enter {i}{b}8{n}  {Y}→{n} Update fee payment status")
print(f"    {LY}├── Enter {i}{b}9{n}  {Y}→{n} View fee details")
print(f"    {LY}├── Enter {i}{b}10{n} {Y}→{n} Add new batch")
print(f"    {LY}├── Enter {i}{b}11{n} {Y}→{n} Update batch timing")
print(f"    {LY}├── Enter {i}{b}12{n} {Y}→{n} Remove batch")
print(f"    {LY}└── Enter {i}{b}13{n} {Y}→{n} Log New Session\n")

try:
        # Taking user's choice as input from the options in the above list
        while True:     # Iterate till the input is fully valid
                selector = input("Enter your choice from the above list: ")

                try:
                        selector = int(selector)

                        if selector >= 1 and selector <= 13:
                                break
                        else:
                                print("Out of range input\n")
                except ValueError:
                        print("Invalid Input\n")
                except EOFError:
                        print("Invalid Input\n")

                if selector == 1:
                        print("Option 1")
                elif selector == 2:
                        print("Option 2")
                elif selector == 3:
                        print("Option 3")
                elif selector == 4:
                        print("Option 4")
                elif selector == 5:
                        print("Option 5")
                elif selector == 6:
                        print("Option 6")
                elif selector == 7:
                        print("Option 7")
                elif selector == 8:
                        print("Option 8")
                elif selector == 9:
                        print("Option 9")
                elif selector == 10:
                        print("Option 10")
                elif selector == 11:
                        print("Option 11")
                elif selector == 12:
                        print("Option 12")
                elif selector == 13:
                        print("Option 13")
                elif selector < 1:
                        print("Option 1")
                else:
                        print("Option 13")
except Exception as e:
        print("An unknown error occured\n", e, sep="")
