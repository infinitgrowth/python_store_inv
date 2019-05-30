from utils import Utils
from clean import DataClean

from inventory import *  # Import everything from the inventory file
from menu import Menu


def main():
    Utils().clear_screen()

    # Read the csv inventory file
    inventory_list = Utils().read_csv()

    # Clean the data in the dictionary
    inv_list_dict = DataClean().add_dict(inventory_list)

    # Database
    # Using the import statement I imported everything so it can be used in this file
    # ===============================================================================

    # Connect to the inventory database
    db.connect()

    # Create the table Products in the inventory database
    db.create_tables([Product], safe=True)

    # Add to the products table using the cleaned inventory list of dictionaries of each product
    add_products(inv_list_dict)

    # Bring up the user menu
    Menu().menu_loop()

    # Close connection to the inventory database
    # db.close()


if __name__ == "__main__":
    main()
