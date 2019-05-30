import pdb
import datetime
from utils import Utils


class DataClean:
    def add_dict(self, inv_list):

        inv_list_dict = []
        for item in inv_list:
            # product_name,product_price,product_quantity,date_updated
            inv_dict = {
                'product_name': f'{item[0]}',
                'product_price': self.int_prodp(item[1]),
                'product_quantity': self.int_prodq(item[2]),
                'date_updated': self.date_prod(item[3]),
            }
            inv_list_dict.append(inv_dict)

        return inv_list_dict

    # Converts the product quantity from string to integer
    def int_prodq(self, prod_q):
        return int(prod_q)

    # Converts the product price to an integer,
    # while first removing the $ (get substring without first character)
    # and multiplying the float by a 100
    # then using the int function
    def int_prodp(self, prod_p):
        return int(float(prod_p)*100)

    # Converts the date string format of month day year to a date time object
    def date_prod(self, date_p):
        return datetime.datetime.strptime(date_p, '%m/%d/%Y')

