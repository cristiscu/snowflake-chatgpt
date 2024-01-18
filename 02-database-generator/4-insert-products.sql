INSERT INTO DimProduct (ProductKey, ProductName, ProductCategory, Price, Supplier)
SELECT
  SEQ4(),
  'Product ' || SEQ4(),
  DECODE(uniform(0, 1, RANDOM(1))*3::INT, 
          0, 'Electronics', 
          1, 'Home & Garden', 
          2, 'Sporting Goods'),
  ROUND((uniform(0, 1, RANDOM())*100)::DECIMAL(10,2), 2),
  DECODE(uniform(0, 1, RANDOM(1))*4::INT, 
          0, 'Acme Supplies', 
          1, 'Global Corp', 
          2, 'Quality Goods Inc.',
          3, 'Supply Nation')
FROM TABLE(GENERATOR(ROWCOUNT => 100));
