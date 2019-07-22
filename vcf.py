import sys
import csv
import logging
import os.path
from prettytable import PrettyTable

def ask_user(header):
    print("Is this the field containing the name?")
    table = PrettyTable(header)
    # table.add_row(['Alice', 24])
    # table.add_row(['Bob', 19])
    print(table)

    check = str(input("Reply in (Y/N): ")).lower().strip()
    try:
        if check[0] == 'y':
            return True
        elif check[0] == 'n':
            return False
        else:
            print('Invalid Input')
            return ask_user()
    except Exception as error:
        print("Please enter valid inputs")
        print(error)
        return ask_user()

def encode(text):
    #char to encode "\\" / "\," / "\n"(Backslashes, commas, and newlines must be encoded)
    encoded = text.replace('\\', '\\\\')
    encoded = encoded.replace(',', '\\,')
    return encoded
#print(encode("this is one value,this \is another"))

def name_formatter(data, index, formatter):
    formatted = data[index['FN']] + " " + data[formatter['roomno']] + " " + data[formatter['company']]
    return formatted

def vcfcreator(filename="sample.csv"):                      #main function
    if not os.path.isfile(filename):                        #checking if the file exists
        print("File doesn't exist. :(")
        return 0
    else:
        data = []
        print("File found. Processing...")
        with open(filename, 'r') as csvfile:                #loading the file               
            reader = csv.reader(csvfile, delimiter=',')
            for row in reader:
                data.append(row)

        logging.info(data[0])
        index = {}

        attributes = {'FN': 'name',
                    'NICKNAME': 'nick',
                    'BDAY': 'birthday',
                    'ANNIVERSARY': 'anniversary',
                    'TEL;WORK;VOICE': 'phone',
                    'ADR;HOME': 'address',
                    'EMAIL': 'email'
                    }

        with open(filename.split(".")[0]+".vcf", "w+") as file:
            for attribute in attributes.keys():
                if attributes[attribute] in data[0]:
                    index[attribute] = data[0].index(attributes[attribute])
            logging.info(index)
            print(index)
            
            #formatter attributes
            formatter = {}
            for key in data[0]:
                splitted_key = key.split("_")
                try:
                    if splitted_key[0] == "name" and splitted_key[1]:
                        formatter[splitted_key[1]] = data[0].index(key)
                except: 
                    pass
            print(formatter)

            #vcard writer
            for i, row in enumerate(data[1:]):
                file.write("BEGIN:VCARD\n")
                file.write("VERSION:4.0\n")
                for attribute in attributes.keys():
                    if attributes[attribute] in data[0]:
                        if attributes[attribute] == 'name':
                            file.write("{}:{}\n".format(attribute, name_formatter(data[i+1], index, formatter)))
                        else:
                            file.write("{}:{}\n".format(attribute, data[i+1][index[attribute]]))
                file.write("END:VCARD\n")
        
        if(ask_user(data[0]) == True):
            print("Write Successful. Thanks for using :)")
        else:
            print("Raise an issue with the details and the vcf file created")
            

if __name__ == "__main__":
    print("""
  _    ______________   ______                __            
 | |  / / ____/ ____/  / ____/_______  ____ _/ /_____  _____
 | | / / /   / /_     / /   / ___/ _ \/ __ `/ __/ __ \/ ___/
 | |/ / /___/ __/    / /___/ /  /  __/ /_/ / /_/ /_/ / /    
 |___/\____/_/       \____/_/   \___/\__,_/\__/\____/_/                                                             
    """)
    try:
        vcfcreator(sys.argv[1])
    except(IndexError):
        print("No file provided. Running the sample csv!")
        vcfcreator()
        