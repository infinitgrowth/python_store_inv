import pdb
import re
from datetime import datetime
from utils import Utils


class Validate:
    def prod_name_chk(self, inp_string):
        """Checks to ensure it's a valid product title"""
        while True:
            prod_name = input(f'''{inp_string}
> ''')
            if len(prod_name) == 0:
                Utils().clear_screen()
                print('Please enter a title that represents your task')
                continue
            elif len(prod_name) >= 255:
                print('Product name is too long, please shorten the name')
            break

        return prod_name

    def price_chk(self, inp_string):
        while True:
            try:
                prod_price = input(f'''{inp_string}
> ''')
                float(prod_price)
            except ValueError:
                print("Please be sure to enter a valid number")
                continue
            try:
                if float(prod_price)*100 % 1 != 0:
                    raise ValueError
            except ValueError:
                print("Please only add two decimal places to the number after the point")
                continue
            try:
                price = re.search(r"\d+[\d,]*\.\d{2}", prod_price)
                price_regx = price.group()
                price_rep = re.sub(",", "", price_regx)
            except AttributeError:
                print("Please be sure to enter the format specified")
                continue

            if len(price_rep) < 1:
                Utils().clear_screen()
                print("Please enter a value")
                continue

            break

        return price_rep

    def quan_chk(self, inp_string):
        while True:
            try:
                prod_quan = input(f'''{inp_string}
> ''')
                int(prod_quan)
            except ValueError:
                print("Please enter an integer value.")
                continue
            if len(prod_quan) < 1:
                Utils().clear_screen()
                print("Please enter a value")
                continue

            break

        return prod_quan

    def date_chk(self, inp_string):
        """Checks to see if the date is a valid date"""

        while True:
            try:
                date = input(f'''{inp_string}
> ''')
                result = datetime.strptime(date, '%m/%d/%Y')
                break
            except ValueError:
                Utils().clear_screen()
                print("Please enter a correct date with the format suggested")

        return datetime.strftime(result, '%m/%d/%Y')
