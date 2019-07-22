import sys
import csv
import logging
import os.path
from prettytable import PrettyTable

def ask_user(to_print):
    print(to_print)
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

def name_formatter(data, index, formatter, former):
    formatted = ""
    for form in former:
        if form in index.keys(): 
            formatted += data[index[form]] + " " 
        if form in formatter.keys():
            formatted += data[formatter[form]] + " " 
    return formatted

def check_format(data, index, formatter):
    inp = input("\nPlease specify the format for the names:\nE.g. name + roomno + company if the fields in csv file are name, name_roomno, name_company\n")
    former = inp.replace(" ", "").split("+")
    try:
        print("\n")
        print(name_formatter(data, index, formatter, former))
    except Exception as e:
        print("ERROR: " + str(e))
    if(not ask_user("Is this formatting fine?")):
        check_format(data, index, formatter)
    return former

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
        
        table = PrettyTable(data[0])
        try:
            table.add_row(data[1])
        except:
            print("The csv file doesn't seem to have any data")
        print(table, "\n")

        logging.info(data[0])
        
        attributes = {'FN': 'name',
                    'NICKNAME': 'nick',
                    'BDAY': 'birthday',
                    'ANNIVERSARY': 'anniversary',
                    'TEL;WORK;VOICE': 'phone',
                    'ADR;HOME': 'address',
                    'EMAIL': 'email'
                    }

        with open(filename.split(".")[0]+".vcf", "w+") as file:
            index = {}
            for i, column in enumerate(data[0]):
                    index[column] = i
            logging.info(index)
            
            # formatter attributes
            formatter = {}
            for key in data[0]:
                splitted_key = key.split("_")
                try:
                    if splitted_key[0] == "name" and splitted_key[1]:
                        formatter[splitted_key[1]] = data[0].index(key)
                except: 
                    pass
            former = check_format(data[1], index, formatter)

            #vcard writer
            for i, row in enumerate(data[1:]):
                file.write("BEGIN:VCARD\n")
                file.write("VERSION:4.0\n")
                for attribute in attributes.keys():
                    if attributes[attribute] in data[0]:
                        if attributes[attribute] == 'name' and formatter:
                            file.write("{}:{}\n".format(attribute, encode(name_formatter(data[i+1], index, formatter, former))))
                        else:
                            file.write("{}:{}\n".format(attribute, encode(data[i+1][index[attributes[attribute]]])))
                file.write("END:VCARD\n")
        
        if(ask_user(("Check the contacts imported with the {} file".format(filename.split(".")[0]+".vcf"))) == True):
            print("Thanks for using :)")
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
        