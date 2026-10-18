import sqlite3
import pandas as pd

conn = sqlite3.connect('data.sqlite')

# pd.read_sql("""SELECT * FROM sqlite_master""", conn)
df_boston = pd.read_sql_query("""
    SELECT e.firstName, e.lastName
    FROM employees e
    JOIN offices o USING (officeCode)
    WHERE o.city = 'Boston';
    """, conn)

df_zero_emp = pd.read_sql("""
    SELECT o.*
    FROM offices o
    LEFT JOIN employees e USING (officeCode)
    WHERE e.employeeNumber IS NULL;
    """, conn)

df_employee = pd.read_sql("""
    SELECT e.firstName, e.lastName, o.city, o.state
    FROM employees e
    LEFT JOIN offices o USING (officeCode)
    ORDER BY e.firstName, e.lastName;
    """, conn)

df_contacts = pd.read_sql("""
    SELECT c.contactFirstName, c.contactLastName, c.phone, c.salesRepEmployeeNumber
    FROM customers c
    LEFT JOIN orders o USING (customerNumber)
    WHERE o.customerNumber IS NULL
    ORDER BY c.contactLastName ASC;
    """, conn)

df_payment = pd.read_sql("""
    SELECT c.contactFirstName, c.contactLastName, p.paymentDate, p.amount
    FROM customers c
    JOIN payments p USING (customerNumber)
    ORDER BY CAST(p.amount AS REAL) DESC;
    """, conn)

df_credit = pd.read_sql("""
    SELECT e.employeeNumber, e.firstName, e.lastName, COUNT(c.customerNumber) AS n_customers
    FROM employees e
    JOIN customers c ON c.salesRepEmployeeNumber = e.employeeNumber
    GROUP BY e.employeeNumber, e.firstName, e.lastName
    HAVING AVG(c.creditLimit) > 90000
    ORDER BY n_customers DESC;
    """, conn)

df_product_sold =pd.read_sql("""
    SELECT p.productName,
           COUNT(od.orderNumber) AS numorders,
           SUM(od.quantityOrdered) AS totalunits
    FROM products p
    JOIN orderdetails od USING (productCode)
    GROUP BY p.productCode, p.productName
    ORDER BY totalunits DESC;
""", conn)

df_total_customers = pd.read_sql("""
    SELECT p.productName, p.productCode,
           COUNT(DISTINCT o.customerNumber) AS numpurchasers
    FROM products p
    JOIN orderdetails od USING (productCode)
    JOIN orders o USING (orderNumber)
    GROUP BY p.productCode, p.productName
    ORDER BY numpurchasers DESC;
""", conn)

df_customers = pd.read_sql("""
    SELECT COUNT(c.customerNumber) AS n_customers,
           o.officeCode, o.city
    FROM customers c
    JOIN employees e ON c.salesRepEmployeeNumber = e.employeeNumber
    JOIN offices o USING (officeCode)
    GROUP BY o.officeCode, o.city;
""", conn)

df_under_20 = pd.read_sql("""
    SELECT DISTINCT e.employeeNumber, e.firstName, e.lastName,
           o.city, o.officeCode
    FROM employees e
    JOIN offices o USING (officeCode)
    JOIN customers c ON c.salesRepEmployeeNumber = e.employeeNumber
    JOIN orders ord USING (customerNumber)
    JOIN orderdetails od USING (orderNumber)
    WHERE od.productCode IN (
        SELECT od2.productCode
        FROM orderdetails od2
        JOIN orders o2 USING (orderNumber)
        GROUP BY od2.productCode
        HAVING COUNT(DISTINCT o2.customerNumber) < 20
    )
    ORDER BY e.lastName, e.firstName;
""", conn)

conn.close()