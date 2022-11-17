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

def update_product_stock(_conn, productId, newStock):
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

'''
Adds new product to product table and returns the added product from the table
:param seller: id of the seller selling added product
:param product_name: name of the product
:param price: product's price
:param image: product's display image
:param type: product's type (either digital or not)
:param stock: available stock for new product
:param discount: discount for product (if available); Nullable attr.
'''
def add_product(_conn, seller, product_name, price, image, type, stock, discount):
    cur = _conn.cursor()
    cur.execute(
        f'''
        SELECT * FROM Product 
        WHERE SellerID = {seller} AND Name = (:name)
        ''', {'name': product_name}
    )
    res = cur.fetchall()
    # if a product with this name exists under the provided seller, prevent addition to
    # product table
    if len(res[0]) > 0:
        return "Cannot add existing item to listing!"
    cur.execute(
        '''
        SELECT MAX(ProductID) from Product
        '''
    )
    id = cur.fetchall()[0][0] + 1
    cur.execute(
        f'''
        INSERT INTO Product
        VALUES({id}, {seller}, (:name), {price}, (:image), (:type), {stock}, {discount})
        ''', {'name': product_name, 'image': image, 'type': type}
    )
    return cur.execute(f'SELECT * FROM Product WHERE ProductID = {id}').fetchall()

'''
Remove product from product table based on id. Returns true if successful
:param id: id of product to be removed
'''
# TODO: need to add code to return false if product with provided ID doesn't exist
# or if a failure occurs
def remove_product(_conn, id):
    cur = _conn.cursor()
    cur.execute(
        f'''
        DELETE FROM Product 
        WHERE ProductId = {id}
        '''
    )
    return True

'''
Sorts products by :param sort_by: and returns a list of product ids sorted accordingly
:param sort_by: String which determines what to sort products by
'''
#TODO: Add other sorting methods, such as sorting by seller
def product_sort_by(_conn, sort_by):
    cur = _conn.cursor()
    sorted_products = []
    if sort_by == "Most Popular":
        cur.execute(
            '''
            SELECT p.ProductID, COUNT(p.ProductID) FROM Order_item oi
            JOIN Product p on oi.ProductID = p.ProductID
            GROUP BY p.ProductID
            ORDER BY COUNT(p.ProductID) DESC
            '''
        )
        results = cur.fetchall()
        for p in results:
            sorted_products.append(p[0])
    return sorted_products

