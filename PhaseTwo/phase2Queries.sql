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
    SellerID  INTEGER      PRIMARY KEY,
    Email     VARCHAR (50),
    Password  VARCHAR (50),
    ProductID INTEGER
);

CREATE TABLE IF NOT EXISTS Product (
    ProductID INTEGER       PRIMARY KEY,
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


SELECT * FROM Product;

SELECT Customer.CustomerID
FROM Orders, Customer
WHERE Customer.CustomerID = Orders.CustomerID
AND Orders.Price > 100;

SELECT Seller.Email
FROM Seller, Checkout
WHERE Seller.SellerID == Checkout.SellerID;

