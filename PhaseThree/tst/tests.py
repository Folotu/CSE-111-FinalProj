import sqlite3
import unittest
from sqlite3 import Error

from mock_store import (add_product, closeConnection, openConnection,
                        update_product_stock, remove_product)

database = r"test.sqlite"

def assert_equals_product(actual, expected):
        assert(actual[0][0]==expected[0])
        assert(actual[0][1]==expected[1])
        assert(actual[0][2]==expected[2])
        assert(actual[0][3]==expected[3])
        assert(actual[0][4]==expected[4])
        assert(actual[0][5]==expected[5])
        assert(actual[0][6]==expected[6])
        assert(actual[0][7]==expected[7])
class TestMockStore(unittest.TestCase):
    def test_update_stock(self):
        id = 1
        newStock = 1599
        conn = openConnection(database)
        with conn:
            r = update_product_stock(conn, id, newStock)
            assert(r == newStock)
            newStock = 2
            r = update_product_stock(conn, id, newStock)
            assert(r == newStock)
        closeConnection(conn, database)
    
    def test_add_product(self):
        
        seller = 5
        name = f'''Kingdom Hearts III (Xbox One)'''
        price = 64.99
        image = "dummyimage.com"
        stock = 200
        type = "TRUE"
        discount = 0.20
        conn = openConnection(database)
        with conn:
            actual = add_product(conn, seller, name, price, image, type, stock, discount)
            expected = (actual[0][0], seller, name, price, image, type, stock, discount)
            assert_equals_product(actual, expected)
        closeConnection(conn, database)

    def test_remove_product(self):
        conn = openConnection(database)
        cur = conn.cursor()
        cur.execute(f'SELECT MAX(ProductID) FROM Product')
        id = cur.fetchall()
        with conn:
            r = remove_product(conn, id[0][0])
            assert(r)
            

if __name__ == '__main__':
    unittest.main()
