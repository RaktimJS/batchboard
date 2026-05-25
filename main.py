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
print(f"{Y}Batchboard v0.1{n}")

print(f"├── {LY}{b}1{n}{W}. Students{n}")
print(f"│   {LY}├── Enter {LY}{i}{b}1.1{n}{LB} {Y}→ {n}Add new student")
print(f"│   {LY}├── Enter {LY}{i}{b}1.2{n}{LB} {Y}→ {n}View student details")
print(f"│   {LY}└── Enter {LY}{i}{b}1.3{n}{LB} {Y}→ {n}Remove student")

print(f"├── {LY}{b}2{n}{W}. Tests{n}")
print(f"│   {LY}├── Enter {LY}{i}{b}2.1{n}{LB} {Y}→ {n}Issue new test")
print(f"│   {LY}├── Enter {LY}{i}{b}2.2{n}{LB} {Y}→ {n}Log test performance")
print(f"│   {LY}└── Enter {LY}{i}{b}2.3{n}{LB} {Y}→ {n}View test details")

print(f"├── {LY}{b}3{n}{W}. Fees{n}")
print(f"│   {LY}├── Enter {LY}{i}{b}3.1{n}{LB} {Y}→ {n}Issue new fee")
print(f"│   {LY}├── Enter {LY}{i}{b}3.2{n}{LB} {Y}→ {n}Update fee payment status")
print(f"│   {LY}└── Enter {LY}{i}{b}3.3{n}{LB} {Y}→ {n}View fee details")

print(f"└── {LY}{b}4{n}{W}. Batches{n}")
print(f"    {LY}├── Enter {LY}{i}{b}4.1{n}{LB} {Y}→ {n}Add new batch")
print(f"    {LY}├── Enter {LY}{i}{b}4.2{n}{LB} {Y}→ {n}Update batch timing")
print(f"    {LY}└── Enter {LY}{i}{b}4.3{n}{LB} {Y}→ {n}Remove batch\n\n")



try:
        # Taking user's choice as input from the options in the above list
        while True:     # Iterate till the input is fully valid
                selector = input(f"Enter the choice from the above list: {Y}")  # Take an input in the form "a.b" where a, b are integers (expected)
                selector = selector.split(".")          # Converting the input string "a.b" to a list ["a", "b"] (expected)

                print(W, end="")

                # Input verification
                # Check number of components in the list formed
                if len(selector) == 2:
                        # Try to convert both elements in the list to an integer
                        try:
                                i = 0
                                while i < len(selector):
                                        selector[i] = int(selector[i])
                                        i += 1

                                # Check if both components of the input are in range
                                if selector[0] >= 1 and selector[0] <= 4:
                                        if selector[1] >= 1 and selector[1] <= 3:
                                                groupOp, featureOp = tuple(selector)
                                                print("\n")
                                                break
                                        else:
                                                print("Out of range sub index\n")
                                else:
                                        print("Out of range index\n")
                        except ValueError:
                                print("Invalid Input\n")
                        except Exception as e:
                                print(f"An unknown error occured, {e}\n")
                else:
                        print("Invalid input\n")
        



        # Creating blocks to be executed based on the index and sub index
        if groupOp == 1:
                print("Students")
                if featureOp == 1:
                        print("Add new student")
                elif featureOp == 2:
                        print("View student details")
                else:
                        print("Remove student")
        elif groupOp == 2:
                print("Tests")
                if featureOp == 1:
                        print("Issue new test")
                elif featureOp == 2:
                        print("Log test performance")
                else:
                        print("View test details")
        elif groupOp == 3:
                print("Fees")
                if featureOp == 1:
                        print("Issue new fee")
                elif featureOp == 2:
                        print("Update fee payment status")
                else:
                        print("View fee details")
        else:
                print("Batch")
                if featureOp == 1:
                        print("Add new batch")
                elif featureOp == 2:
                        print("Update batch timing")
                else:
                        print("Remove batch")
except Exception as e:
        print("An unknown error occured\n", e, sep="")
