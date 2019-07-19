import csv
import os.path

def ask_user():
    print(f"-- Is this the field containing the name?")
    print(f"-- and this the field containing the room number?")
    print(f"-- and this the field containing the phone number?")
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

def name_formatter(name):
    return name

def vcfcreator(filename):                                   #main function
    if not os.path.isfile(filename):                        #checking if the file exists
        print("File doesn't exist. :(")
        return 0
    else:
        data = []
        print("File found. :)\nProcessing...")
        with open(filename, 'r') as csvfile:             #loading the file               
            reader = csv.reader(csvfile, delimiter=',')
            for row in reader:
                data.append(row)

        print(data[0])
        index = {}

        attributes = {'FN': 'name',
                    'NICKNAME': 'nick',
                    'BDAY': 'birthday',
                    'ANNIVERSARY': 'anniversary',
                    'TEL': 'phone',
                    'ADR': 'address',
                    'EMAIL': 'email'
                    }

        with open("contacts.vcf", "w+") as file:
            file.write("BEGIN:VCARD\n")
            file.write("VERSION:4.0\n")

            for row in data[1:]:
                for attribute in attributes.keys():
                    if attributes[attribute] in data[0]:
                        index[attribute] = data[0].index(attributes[attribute])
            print(index)

            for i, row in enumerate(data[1:]):
                for attribute in attributes.keys():
                    if attributes[attribute] in data[0]:
                        file.write("{}:{}\n".format(attribute, data[i+1][index[attribute]]))

            file.write("END:VCARD\n")
        
        if(ask_user() == True):
            print("Write Successful. Thanks for using :)")
        else:
            print("Raise an issue with the details and the vcf file created")
            

	
vcfcreator("sample.csv")