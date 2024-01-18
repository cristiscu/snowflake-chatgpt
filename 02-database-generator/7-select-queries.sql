SELECT 
  ProductCategory,
  COUNT(*) AS NumberOfProducts
FROM DimProduct
GROUP BY ProductCategory;

SELECT 
  Supplier,
  AVG(Price) AS AveragePrice
FROM DimProduct
GROUP BY Supplier;

SELECT 
  ProductCategory,
  MIN(Price) AS MinPrice,
  MAX(Price) AS MaxPrice,
  AVG(Price) AS AvgPrice
FROM DimProduct
GROUP BY ProductCategory;
