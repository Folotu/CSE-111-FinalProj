CREATE TABLE IF NOT EXISTS Orders (
    OrderID      INTEGER      PRIMARY KEY,
    Receipt_Date VARCHAR (50),
    Order_Date   VARCHAR (50),
    Price        REAL,
    CustomerID   INTEGER
);

CREATE TABLE IF NOT EXISTS Order_item (
    OrderItemID INTEGER PRIMARY KEY,
    OrderID     INTEGER,
    ProductID   INTEGER,
    Oder_qty    INTEGER
);

CREATE TABLE IF NOT EXISTS Customer (
    CustomerID INTEGER      NOT NULL,
    email      VARCHAR (50) DEFAULT NULL,
    password   VARCHAR (50) DEFAULT NULL,
    ship_addr  VARCHAR (50) DEFAULT NULL,
    bill_addr  VARCHAR (50) DEFAULT NULL,
    PRIMARY KEY (
        CustomerID
    )
);

CREATE TABLE IF NOT EXISTS Checkout (
    CheckoutID INTEGER PRIMARY KEY,
    CustomerID INTEGER,
    CartID     INTEGER,
    SellerID   INTEGER
);

CREATE TABLE IF NOT EXISTS Cart (
    CartID     INTEGER PRIMARY KEY,
    CustomerID INTEGER,
    OrderID    INTEGER,
    Cart_total REAL
);

CREATE TABLE IF NOT EXISTS Seller (
    SellerID  INTEGER,
    Email     VARCHAR (50),
    Password  VARCHAR (50),
    ProductID INTEGER
);

CREATE TABLE IF NOT EXISTS Product (
    ProductID INTEGER,
    SellerID  INTEGER,
    Name      VARCHAR (200),
    Price     REAL,
    Image     VARCHAR (100),
    Type      VARCHAR (50),
    Stock     INTEGER
);


.mode "csv"
.separator ","


.import ./CSE-111-InciteDataset/InciteDataset-CartTable.csv Cart
.import ./CSE-111-InciteDataset/InciteDataset-CheckoutTable.csv Checkout
.import ./CSE-111-InciteDataset/InciteDataset-CustomerTable.csv Customer
.import ./CSE-111-InciteDataset/InciteDataset-OrderItemTable.csv Order_item
.import ./CSE-111-InciteDataset/InciteDataset-OrdersTable.csv Orders
.import ./CSE-111-InciteDataset/InciteDataset-ProductTable.csv Product
.import ./CSE-111-InciteDataset/InciteDataset-SellerTable.csv Seller

-- 1. Selecting all products
SELECT * FROM Product;

-- 2. Find the customers who have orders over 100 in price
SELECT Customer.CustomerID
FROM Orders, Customer
WHERE Customer.CustomerID = Orders.CustomerID
AND Orders.Price > 100;

-- 3.
SELECT Seller.Email
FROM Seller, Checkout
WHERE Seller.SellerID == Checkout.SellerID;

-- 4. Get the carts that have items in them
SELECT c2.CartID 
FROM Cart c2 JOIN Customer c1
ON c1.CustomerID = c2.CustomerID
WHERE Cart_total > 0;

-- 5. Create a new cart
INSERT INTO CART
VALUES(3, 1, 3, 20);

-- 6. Update cart 3's total
UPDATE CART 
SET Cart_total = 25.47
WHERE CartID = 3;

-- 7. How many carts is product 1 in
SELECT COUNT(*) FROM Cart c1
JOIN Customer c2 
ON c1.CustomerID = c2.CustomerID
JOIN Orders o 
ON c1.OrderID = o.OrderID
JOIN Order_item oi 
ON o.OrderID = oi.OrderID
JOIN Product p 
ON oi.ProductID = p.ProductID
WHERE p.ProductID = 1;

-- 8. How many orders have customer 1 made
SELECT COUNT(*) as num_orders 
FROM Cart c1
JOIN Customer c2 
ON c1.CustomerID = c2.CustomerID
JOIN Orders o 
ON c1.OrderID = o.OrderID
WHERE c2.CustomerID = 1;

-- 9. How many times has customer 2 ordered product 1
SELECT COUNT(*) as times_ordered
FROM Cart c1
JOIN Customer c2 
ON c1.CustomerID = c2.CustomerID
JOIN Orders o 
ON c1.OrderID = o.OrderID
JOIN Order_item oi 
ON o.OrderID = oi.OrderID
JOIN Product p 
ON oi.ProductID = p.ProductID
WHERE p.ProductID = 1 AND c2.CustomerID = 2;


-- 10. Get the seller(s) who sell the product: Wine - Ej Gallo Sonoma
SELECT s.SellerID as seller_id 
FROM Seller s 
JOIN Product p on s.ProductID = p.ProductID
WHERE p.Name = "Wine - Ej Gallo Sonoma";

-- 11. Add discount column to a product and add value of 10%
ALTER TABLE Product 
ADD Discount REAL;
UPDATE Product 
SET Discount = 0.10
WHERE ProductID = 1;

-- 12. Check if a discount exists for all products, and if a product does have one,
-- output that it does or output that the discount is unavailable. 
-- Display the results as DisocuntPrice 
SELECT *,
CASE WHEN Discount IS NOT NULL 
THEN "Discount(s) available for this item"
ELSE "No discount available for this item"
END AS DiscountPrice
FROM Product;

-- 13. Get the sellers who have sold more than 1 product to customers
SELECT * FROM
(SELECT s.SellerID FROM Product p 
JOIN Seller s
ON p.ProductID = s.ProductID
JOIN Order_item o1
ON o1.ProductID = p.ProductID
JOIN Orders o2
ON o1.OrderID = o2.OrderID
JOIN Customer c 
ON c.CustomerID = o2.CustomerID
WHERE (s.SellerID) > 1);

-- 14. 
UPDATE Cart
SET Cart_total = subq1.Price
FROM (SELECT Orders.Price, Orders.OrderID
      FROM Orders) AS subq1
WHERE Cart.OrderID = subq1.OrderID

--15. How many products does each seller sell 

SELECT SellerID, COUNT(ProductID)
FROM Seller
GROUP BY SellerID

-- 16. Sellers that sell the same product

SELECT Product.SellerID, Product.Name
FROM Product, (SELECT ProductID
				FROM Product
				GROUP BY ProductID
				HAVING COUNT(ProductID) > 1) AS sbq1
WHERE Product.ProductID = sbq1.ProductID;

--17. Out of the sellers that sell the same product, 
--    select the ones that have the greater stock 

SELECT Product.SellerID, Product.Name, MAX(Product.Stock)
FROM Product, (SELECT ProductID
				FROM Product
				GROUP BY ProductID
				HAVING COUNT(ProductID) > 1) AS sbq1
WHERE Product.ProductID = sbq1.ProductID
GROUP BY Product.Name;

--18. What is the cheapest and most expensive product 

SELECT MIN(Price) AS Price, Name
FROM Product

UNION ALL

SELECT MAX(Price), Name
FROM Product

--19. Which products are digital 

SELECT Name
FROM Product
WHERE Type = 'TRUE';


--20 which products are NOT digital 

SELECT Name
FROM Product
WHERE Type = 'FALSE';

--21 For each item that is ordered display seller information and customer information and product purchased 
SELECT Seller.SellerID AS TheSeller, Seller.Email AS SellersEmail, Customer.CustomerID, Customer.email AS CustomerEmail, Product.Name AS ProductsName, Order_item.OrderItemID, Product.ProductID, Orders.OrderID
FROM Seller, Product, Customer, Orders, Order_item
WHERE Seller.SellerID = Product.SellerID
AND Orders.OrderID = Order_item.OrderID
AND Orders.CustomerID = Customer.CustomerID
AND Product.ProductID = Order_item.ProductID
GROUP BY Order_item.OrderItemID

--2. Out of the items ordered, display how many total items were ordered from each seller who has had items purchased
SELECT SellerId, SUM(Oder_qty) FROM
(SELECT * FROM Seller, Product, Customer, Orders, Order_item
WHERE Seller.SellerID = Product.SellerID
AND Orders.OrderID = Order_item.OrderID
AND Orders.CustomerID = Customer.CustomerID
AND Product.ProductID = Order_item.ProductID
AND Seller.SellerID IN (Select Seller.SellerID FROM Seller)
GROUP BY Order_item.OrderItemID)
GROUP BY SellerID


