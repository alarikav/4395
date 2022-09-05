# Alarika Voora
# Assignment 1
# CS 4395

import sys
import re
import pickle

# person class
class Person:
  def __init__(self, last, first, mi, id, phone):
      # set class variables
    self.last, self.first, self.mi, self.id, self.phone = last, first, mi, id, phone

  def display(self):
      # display in the form:
          # id
          # Last MI First
          # phone
      print('\nEmployee id:\t', self.id, '\n\t\t\t\t', self.first, self.mi, self.last, '\n\t\t\t\t', self.phone)

# driver function
def main():
    # checking that an argument is provided, exiting code if it is not
    if len(sys.argv) <= 1:
        print("sys arg not defined, please run again and specify location of csv file with data")
        exit()

    people = processFile()  # parce file and create people using class Person

    pickle.dump(people, open('people.p', 'wb'))     # write binary to people.p pickle file

    read_pickle_people = pickle.load(open('people.p', 'rb'))    # read binary from people.p pickle file

    # print employees using display function to make sure people.p is unpickled correctly
    print('\nEmployee List:')
    for person in read_pickle_people.values():
        person.display()

def processFile():
    fp = open(sys.argv[1], 'r')     # open file
    fp.readline()      # skip header line
    line = fp.readline()
    people = {}     # create people dict
    while line:     # parce each line
        split = line.split(',')     # split line on comma

        # if no middle initial is provided, make X the middle initial
        if len(split[2]) == 0:
            split[2] = 'X'

        # if id is not in form alpha alpha #### ask for valid ID
        while re.search("^[a-zA-Z]{2}\d{4}$", split[3]) is None:
            print("ID" , split[3], "is invalid. \nID is two letters followed by fours digits")
            split[3] = input("Please enter a valid ID: ")

        # try to make phone number the correct form
        num = ""
        for c in split[4]:
            if c.isdigit():
                num = num + c
        split[4] = num[:3] + '-' + num[3:6] + '-' + num[6:]

        # if phone number is not in form ###-###-#### ask for valid number
        while re.search("^[1-9]\d{2}-\d{3}-\d{4}", split[4]) is None:
            print("Phone" , split[4], "is invalid. \nEnter phone number in form 123-456-7890")
            split[4] = input("Please enter a valid phone number: ")

        # add all valid fields to Person class and add to people dictionary
        people[split[3]] = (
            Person(split[0].capitalize(), split[1].capitalize(), split[2][0].upper(), split[3], split[4]))
        line = fp.readline()       # read next line in file

    fp.close()      # close file
    return people   # return dict of people of Person class

if __name__ == "__main__":
    main()
