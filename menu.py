from datetime import datetime
from collections import OrderedDict
from clean import DataClean
from utils import Utils
from inventory import *
from check import Validate
import pdb


class Menu:

    def menu_loop(self):
        """Show the menu"""
        choice = None  # initialize the variable without giving it a value

        # Enable the user to quit at any point in the menu
        while choice != 'q':
            print("Enter 'q' to quit.")
            for key, value in self.menu.items():
                print(f'{key}) {value.__doc__}')
            choice = input('Action: ').lower().strip()

            # Select menu choice from the dictionary of
            # choices. Allows for a scalable menu
            if choice in self.menu:
                self.menu[choice](self)
            else:
                Utils().clear_screen()
                if choice != 'q':
                    print("Your selection is not available! \n"
                          "Please enter a choice from in the menu below")

    def add_prod(self):
        """Add a product"""
        Utils().clear_screen()

        # Initialize an empty list
        listp = []

        # Set question string and get user input for the product

        # Get product name
        product_name_str = 'Enter a product name to be entered in to the database: '
        product_name = Validate().prod_name_chk(product_name_str)

        # Get product price
        product_price_str = f'Enter the price of "{product_name}" in the format 9.56 for $9.56: >'
        product_price = Validate().price_chk(product_price_str)

        # Get product quantity
        product_quantity_str = f'Enter the quantity the quantity of "{product_name}"'
        product_quantity = Validate().quan_chk(product_quantity_str)

        # Get date product was updated
        date_updated_str = f'Enter the date "{product_name}" was updated MM/DD/YYYY'
        date_updated = Validate().date_chk(date_updated_str)

        # Append all the product values into a list
        listp.append(product_name)
        listp.append(product_price)
        listp.append(product_quantity)
        listp.append(date_updated)

        # Reuses the add dict and add products methods already built
        # to add products from the csv to the database
        # - note: The list is enclosed in another list to simulate
        # list of dictionaries even though just 1 dictionary
        add_products(DataClean().add_dict([listp]))

        # Improvement: Show product after adding

    def view_prods(self):
        """View previous products"""
        while True:
            # Get the product id from user that they would like to view
            Utils().clear_screen()
            product_id = input('''Please enter a product ID or q to go back to the menu: 
>  ''')
            if product_id == 'q':
                Utils().clear_screen()
                break

            # Query to get product from user input of product id
            products = Product \
                .select() \
                .order_by(Product.product_id) \
                .where(Product.product_id == product_id)
            # pdb.set_trace()

            # Checks to see if the query returned a product
            # If not an indexError will happen and send the logic below the except
            try:
                products[0]
            except IndexError:
                Utils().clear_screen()
                print(f"Unfortunately that ID = {product_id} is not in the database. \n"
                      "Please select an available id from the product list.\n")
                choice = input("Would you like to select another id ? [yN]")
                if choice.lower() == 'n':
                    # Go back to the main menu
                    Utils().clear_screen()
                    break
                # Go back to the top of the code view prods
                Utils().clear_screen()
                continue

            for product in products:
                # used the {:.2f}'.format to simulate currency to get the two decimal points
                # reference: https://stackoverflow.com/questions/21208376/converting-float-to-dollars-and-cents
                price = '${:.2f}'.format(product.product_price / 100)

                # Convert the date back to a string instead of datetime
                dateu = datetime.strftime(product.date_updated, '%m/%d/%Y')

                print(f'''
Product ID: {product.product_id}  
Product Name: {product.product_name}
Product Price: {price}
Product Quantity: {product.product_quantity}
Date Updated: {dateu}       
''')

            choice = input("Would you like to select another id ? [yN]")
            if choice.lower() == 'n':
                Utils().clear_screen()
                break

    def backup_prods(self):
        """Backup the entries to a backup csv file"""

        Utils().clear_screen()

        # Query the database for all the items by product id ascending
        products = Product \
            .select() \
            .order_by(Product.product_id.asc())

        # Set the fieldnames to be passed to the function
        fieldnames = ['product_name',
                      'product_price',
                      'product_quantity',
                      'date_updated']

        # Pass the fieldnames and the products from the
        # database to the write csv function
        Utils().writec_csv(fieldnames, products)

    menu = OrderedDict([
        ('a', add_prod),
        ('v', view_prods),
        ('b', backup_prods)
    ])
