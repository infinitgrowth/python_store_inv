import pdb
from datetime import datetime

from peewee import *

db = SqliteDatabase('inventory.db')


class Product(Model):
    product_id = AutoField(primary_key=True)
    # product_name = CharField(max_length=255)
    product_name = CharField(max_length=255, unique=True)
    product_price = IntegerField()
    product_quantity = IntegerField()
    date_updated = DateTimeField()

    class Meta:
        database = db  # This model uses the "inventory.db" database.


def add_products(list_dict):
    # pdb.set_trace()
    for product in list_dict:
        try:
            Product.create(product_name=product['product_name'],
                           product_price=product['product_price'],
                           product_quantity=product['product_quantity'],
                           date_updated=product['date_updated'])
        except IntegrityError:
            # Gets the product in product_record and enter it in product record
            product_record = Product.get(product_name=product['product_name'])

            # Sets dates to clear variables for code readability
            date_entered = product['date_updated']
            date_database = product_record.date_updated

            # Check to see if the entered date is more recent then the current
            # date in the database
            if date_entered > date_database:
                # Make the change to the database and save the new data
                product_record.product_price = product['product_price']
                product_record.product_quantity = product['product_quantity']
                product_record.date_updated = product['date_updated']
                product_record.save()

# if __name__ == '__main__':
#     db.connect()
#     db.create_tables([Product], safe=True)
#     add_products(inv_list)
