SELECT State, strftime('%Y', Order_Date) AS Year, SUM(Profit) AS TotalProfit
FROM superstore
WHERE strftime('%Y', Order_Date) = '2014'
GROUP BY State;

SELECT DISTINCT State
From Superstore;

SELECT States.State,
       IFNULL(SUM(ss.Profit), 0) AS TotalProfit
FROM (SELECT DISTINCT State
        FROM Superstore) AS States
LEFT JOIN superstore ss ON States.State = ss.State AND strftime('%Y', ss.Order_Date) = '2014'
GROUP BY States.State;


SELECT strftime('%m', Order_Date) AS Month, strftime('%Y', Order_Date) AS Year,
       Category, SUM(Profit) AS TotalProfit
FROM superstore
WHERE Category = 'Furniture'
GROUP BY strftime('%Y', Order_Date), strftime('%m', Order_Date);
