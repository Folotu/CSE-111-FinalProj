import sqlite3
from sqlite3 import Error
        
def openConnection(_dbFile):
    conn = None
    try:
        conn = sqlite3.connect(_dbFile)
        print("successfully connected to database")
    except Error as e:
        print(e)
    return conn

def closeConnection(_conn, _dbFile):
    print("Close database: ", _dbFile)

    try:
        _conn.close()
        print("successfully closed")
    except Error as e:
        print(e)

def updateProductStock(_conn, productId, newStock):
    cur = _conn.cursor()
    cur.execute(
        f'''
        UPDATE Product
        SET Stock = {newStock}
        WHERE ProductID = {productId}
        '''
    )
    cur.execute(
        f'''
        SELECT Stock 
        FROM Product
        WHERE ProductID = {productId}
        '''
    )
    r = cur.fetchall()
    return r[0][0]

