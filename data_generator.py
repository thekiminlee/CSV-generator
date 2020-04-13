# Author: Ki Min Lee

import sys
import csv
import random

# Names of the attribute
ATTR_NAME = ['transaction_exp', 'payor_exp', 'payee_exp']
# List of numerial min,max, and incremental value for random data generation of each attribute.
# Number of ranges must match the number and order of attributes.
# store in tuple in the format: (min, max)
ATTR_RANGE = [(0.0, 5.0), (0.0, 5.0), (0.0, 5.0)]
# Decimal place for randomly generated float value. default at 1
DECIMAL = 1

data = []  # list of csv data for export
file_name = None
num_of_data = None


def generate():
    # Raise error is the number of attributes does not match
    if(len(ATTR_NAME) != len(ATTR_RANGE)):
        raise AttributeError("Attribute length does not match")

    # Generating <num_of_data> amount of data with given range for each attribute
    for i in range(0, num_of_data):
        generated_data = []
        for (minimum, maximum) in ATTR_RANGE:
            generated_data.append(
                round(random.uniform(minimum, maximum), DECIMAL))
        data.append(generated_data)


def export():
    with open(file_name, 'w') as csvfile:
        writer = csv.writer(csvfile, delimiter=",")
        writer.writerow(ATTR_NAME)
        for generated in data:
            writer.writerow(generated)


if __name__ == '__main__':
    file_name = sys.argv[1]
    num_of_data = int(sys.argv[2])

    generate()
    export()
