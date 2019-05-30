import os
import csv
import pdb
import re
from datetime import datetime


class Utils:

    # Clears the terminal to provide a cleaner ui
    def clear_screen(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    # Checks if the log csv is empty for the header writer in
    # the method update csv
    def csv_empty(self):
        with open('inventory.csv', 'r') as csvfile:
            csv_list = []
            for row in csv.reader(csvfile):
                csv_list.append(row)
            if len(csv_list) == 0:
                empty = 'yes'
            else:
                empty = 'no'
        return empty

    # Compiles the regex pattern to be used more efficiently when
    # called several times in the code
    def row_comp(self):
        row = re.compile('''
        ^(?P<product_name>[\w\s-]+,*[\w\s-]*),
        \$*(?P<product_price>\d+.\d{2}),
        (?P<product_quantity>\d+),
        (?P<date_updated>\d{1,2}\/\d{1,2}\/\d{4}),
        (?P<id>\d*)\n$
        ''', re.X | re.M)
        return row

    # retrieve the csv line into the class as an object
    def read_csv(self):
        line = self.row_comp()

        # Initiate empty list
        datalist = []

        with open('inventory.csv') as csvfile:
            logreader = csv.reader(csvfile)
            data = ""

            # Create index used in the update and delete functions
            # of the display_records method
            # - in addition append the data from the csv to the index
            for i, row in enumerate(logreader):
                row.append(f'{i}')
                data += (','.join(row)) + '\n'

            # pdb.set_trace()
            # Using the compiled regex stored in "line"
            for match in line.finditer(data):
                minilist = match.groupdict().values()
                datalist.append(list(minilist))

        # return the correctly matched list with an index
        return datalist

    # overwrites the csv file with the modified data which could
    # be deleted or modified tasks
    def writec_csv(self, fldnames, data):
        with open('inventory_backup.csv', 'w') as csvfile:
            fieldnames = fldnames

            # Set the csv DictWriter class to a variable
            taskwriter = csv.DictWriter(csvfile, fieldnames=fieldnames)

            # Write the header using the imported fieldnames
            taskwriter.writeheader()

            # Writes multiple rows using the dictionary format of {'key': 'value'}
            for product in data:

                # used the {:.2f}'.format to simulate currency to get the two decimal points
                # reference: https://stackoverflow.com/questions/21208376/converting-float-to-dollars-and-cents
                price = '${:.2f}'.format(product.product_price/100)

                # Convert the date back to a string instead of datetime
                dateu = datetime.strftime(product.date_updated, '%m/%d/%Y')

                # Use the write row method of the DictWriter object to write
                # the dictionary to rows in the csv
                taskwriter.writerow({
                    'product_name': f'{product.product_name}',
                    'product_price': price,
                    'product_quantity': f'{product.product_quantity}',
                    'date_updated': dateu
                })
