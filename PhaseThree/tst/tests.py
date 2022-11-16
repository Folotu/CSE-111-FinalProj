import sqlite3
from sqlite3 import Error
from MockStore import updateProductStock, openConnection, closeConnection
import unittest

class TestMockStore(unittest.TestCase):
    def test_update_stock(self):
        database = r"test.sqlite"
        id = 1
        newStock = 1599
        conn = openConnection(database)
        with conn:
            r = updateProductStock(conn, 1, newStock)
            assert(r == newStock)
            newStock = 2
            r = updateProductStock(conn, 1, newStock)
            assert(r == newStock)
        closeConnection(conn, database)

if __name__ == '__main__':
    unittest.main()