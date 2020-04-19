# Author: Ki Min Lee

import sys
import csv
import random

# List of attributes, stored in list format [name1, name2, ...]
ATTR_NAME = []
# List of ranges of attributes
# Number of ranges must match the number and order of attributes.
ATTR_RANGE = []
# Name of the output file
FILE = None
# Decimal place for randomly generated float value.
# Default at 1
DECIMAL = 1

sample_data = []  # list of csv data for export


def generate(numData, exporting=True):
    # Configuration check
    if(exporting and FILE == None):
        raise FileNotFoundError("File path not specified")
    elif(len(ATTR_NAME) == 0 or len(ATTR_RANGE) == 0):
        raise ValueError("ATTR_NAME or ATTR_RANGE Empty")
    elif(len(ATTR_RANGE) != len(ATTR_NAME)):
        raise ValueError(
            "Number of attributes does not match the number of ranges")
    elif(numData < 1):
        raise ValueError("Number of generating data must be greater than 0")

    data_generator = generator(numData)

    if not exporting:
        return construct_data(data_generator)

    export(data_generator)
    print("Export complete.")
    return 1


def generator(numData):
    # Creates a generator of sample data
    while(numData >= 0):
        data = []
        for attribute in ATTR_RANGE:
            if type(attribute) == list:
                data.append(attribute[random.randint(0, len(attribute)-1)])
            elif type(attribute) == tuple:
                minimum, maximum = attribute
                if(type(minimum) == float):
                    data.append(
                        round(random.uniform(minimum, maximum), DECIMAL))
                else:
                    data.append(random.randint(minimum, maximum))
        numData -= 1
        yield data


def construct_data(generator):
    sample_data = []
    sample_data.append(ATTR_NAME)
    for data in generator:
        sample_data.append(data)
    return sample_data


def export(data):
    with open(FILE, 'w') as csvfile:
        writer = csv.writer(csvfile, delimiter=",")
        writer.writerow(ATTR_NAME)
        for generated in data:
            writer.writerow(generated)


def data_print(start_index=0, end_index=len(sample_data)-1):
    pass
