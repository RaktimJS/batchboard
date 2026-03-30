# Entry poin to the system

import os

os.system("cls")

# colors
R = "\033[38;2;255;0;0m"
Y = "\033[38;2;255;255;0m"
B = "\033[38;2;0;0;255m"
W = "\033[38;2;212;212;212m"
LB = "\033[38;2;135;206;235m"
LY = "\033[38;2;255;255;153m"




# Operation selection list
print(f"{Y}Batchboard v0.1{W}")

print(f"├── {LY}1. {W}Students{W}")
print(f"│   {LY}├── 1.1 {LB}Add new student{W}")
print(f"│   {LY}├── 1.2 {LB}View student details{W}")
print(f"│   {LY}└── 1.3 {LB}Remove student{W}")

print(f"├── {LY}2. {W}Tests{W}")
print(f"│   {LY}├── 2.1 {LB}Issue new test{W}")
print(f"│   {LY}├── 2.2 {LB}Log test performance{W}")
print(f"│   {LY}└── 2.3 {LB}View test details{W}")

print(f"├── {LY}3. {W}Fees{W}")
print(f"│   {LY}├── 3.1 {LB}Issue new fee{W}")
print(f"│   {LY}├── 3.2 {LB}Update fee payment status{W}")
print(f"│   {LY}└── 3.3 {LB}View fee details{W}")

print(f"└── {LY}4. {W}Batches{W}")
print(f"    {LY}├── 4.1 {LB}Add new batch{W}")
print(f"    {LY}├── 4.2 {LB}Update batch timing{W}")
print(f"    {LY}└── 4.3 {LB}Remove batch{W}")
