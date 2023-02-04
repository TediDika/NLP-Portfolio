# Homework 1
# Tedi Dika

import sys
import pathlib
import re
import pickle


class Person:
    # Default constructor initializes variables related to an Employee
    def __init__(self, last, first, mi, id, phone):
        self.last = last
        self.first = first
        self.mi = mi
        self.id = id
        self.phone = phone

    # Prints out Employee information
    def display(self):
        print("Employee id: " + self.id)
        print("\t" + self.first + " " + self.mi + " " + self.last)
        print("\t" + self.phone + '\n')


# Text processing
def process_lines(text):
    dictP = {}
    for line in text:
        fields = line.split(",")
        last = fields[0].capitalize()
        first = fields[1].capitalize()
        if not fields[2]:
            middle = 'X'
        else:
            middle = fields[2].upper()

        # r denotes a raw string and keeps newlines and tab spaces, This is useful when dealing with regex
        matchID = re.match(r'^[A-Z]{2}[0-9]{4}$', fields[3])
        if not matchID:
            print("ID invalid: " + fields[3])
            print("ID is two letters followed by 4 digits")
            id = input("Please enter a valid id: ")
        else:
            id = fields[3]

        matchPhone = re.match(r'^[0-9]{3} - [0-9]{3} - [0-9]{4}$', fields[4])
        if not matchPhone:
            print("Phone " + fields[4] + " is invalid")
            print("Enter phone number in form 123-456-7890")
            number = input("Enter phone number: ")
        else:
            number = fields[4]

        if id in dictP.keys():
            print("Error: Duplicate id's found for this id: " + id)
            quit()
        dictP[id] = Person(last, first, middle, id, number)

    return dictP


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Please enter a filename as a system arg')
        quit()

    # pathlib makes it so the code is Mac/Windows compatible because path symbols are different depending on OS
    # read() reads in entire file, splitlines() is a String method that splits a string into a list based on new lines
    rel_path = sys.argv[1]
    with open(pathlib.Path.cwd().joinpath(rel_path), 'r') as f:
        text_in = f.read().splitlines()

    employees = process_lines(text_in[1:]) #ignores heading line

    #pickling in this program is pointless but its just for experience
    # pickle the employees
    pickle.dump(employees, open('employees.pickle', 'wb'))

    # read the pickle back in
    employees_in = pickle.load(open('employees.pickle', 'rb'))

    # output employees
    print('\n\nEmployee list:\n')

    for emp_id in employees_in.keys():
        employees_in[emp_id].display()

