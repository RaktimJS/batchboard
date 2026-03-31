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

bold = "\033[1m"
itlc = "\033[3m"
undrln = "\033[4m"

RST = "\033[0m"




# Operation selection list
print(f"{Y}Batchboard v0.1{RST}")

print(f"├── {LY}{bold}1{RST}{W}. Students{RST}")
print(f"│   {LY}├── Enter {LY}{itlc}{bold}1.1{RST}{LB} {Y}→ {RST}Add new student")
print(f"│   {LY}├── Enter {LY}{itlc}{bold}1.2{RST}{LB} {Y}→ {RST}View student details")
print(f"│   {LY}└── Enter {LY}{itlc}{bold}1.3{RST}{LB} {Y}→ {RST}Remove student")

print(f"├── {LY}{bold}2{RST}{W}. Tests{RST}")
print(f"│   {LY}├── Enter {LY}{itlc}{bold}2.1{RST}{LB} {Y}→ {RST}Issue new test")
print(f"│   {LY}├── Enter {LY}{itlc}{bold}2.2{RST}{LB} {Y}→ {RST}Log test performance")
print(f"│   {LY}└── Enter {LY}{itlc}{bold}2.3{RST}{LB} {Y}→ {RST}View test details")

print(f"├── {LY}{bold}3{RST}{W}. Fees{RST}")
print(f"│   {LY}├── Enter {LY}{itlc}{bold}3.1{RST}{LB} {Y}→ {RST}Issue new fee")
print(f"│   {LY}├── Enter {LY}{itlc}{bold}3.2{RST}{LB} {Y}→ {RST}Update fee payment status")
print(f"│   {LY}└── Enter {LY}{itlc}{bold}3.3{RST}{LB} {Y}→ {RST}View fee details")

print(f"└── {LY}{bold}4{RST}{W}. Batches{RST}")
print(f"    {LY}├── Enter {LY}{itlc}{bold}4.1{RST}{LB} {Y}→ {RST}Add new batch")
print(f"    {LY}├── Enter {LY}{itlc}{bold}4.2{RST}{LB} {Y}→ {RST}Update batch timing")
print(f"    {LY}└── Enter {LY}{itlc}{bold}4.3{RST}{LB} {Y}→ {RST}Remove batch\n\n")
