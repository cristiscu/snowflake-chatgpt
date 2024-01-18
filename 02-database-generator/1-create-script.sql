-- Create a new database named OrderEntry
CREATE DATABASE IF NOT EXISTS OrderEntry;

-- Use the newly created database
USE DATABASE OrderEntry;

-- Create date dimension table
CREATE TABLE IF NOT EXISTS DimDate (
  DateKey INTEGER PRIMARY KEY,
  Date DATE NOT NULL,
  Year SMALLINT NOT NULL,
  Quarter TINYINT NOT NULL,
  Month TINYINT NOT NULL,
  DayOfMonth TINYINT NOT NULL,
  WeekOfYear TINYINT NOT NULL,
  DayOfWeek TINYINT NOT NULL,
  IsWeekend BOOLEAN NOT NULL
);

-- Create product dimension table
CREATE TABLE IF NOT EXISTS DimProduct (
  ProductKey INTEGER PRIMARY KEY,
  ProductName VARCHAR(255) NOT NULL,
  ProductCategory VARCHAR(50),
  Price DECIMAL(10,2) NOT NULL,
  Supplier VARCHAR(100)
);

-- Create customer dimension table
CREATE TABLE IF NOT EXISTS DimCustomer (
  CustomerKey INTEGER PRIMARY KEY,
  FirstName VARCHAR(50),
  LastName VARCHAR(50),
  Email VARCHAR(100),
  Phone VARCHAR(20),
  AddressLine1 VARCHAR(255),
  AddressLine2 VARCHAR(255),
  City VARCHAR(100),
  State VARCHAR(50),
  ZipCode VARCHAR(20),
  Country VARCHAR(50)
);

-- Create fact order table
CREATE TABLE IF NOT EXISTS FactOrder (
  OrderKey INTEGER PRIMARY KEY,
  DateKey INTEGER NOT NULL REFERENCES DimDate(DateKey),
  CustomerKey INTEGER NOT NULL REFERENCES DimCustomer(CustomerKey),
  ProductKey INTEGER NOT NULL REFERENCES DimProduct(ProductKey),
  Quantity INTEGER NOT NULL,
  TotalAmount DECIMAL(10,2) NOT NULL,
  OrderStatus VARCHAR(50),
  FOREIGN KEY (CustomerKey) REFERENCES DimCustomer (CustomerKey),
  FOREIGN KEY (ProductKey) REFERENCES DimProduct (ProductKey)
);
