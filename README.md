# BD_HW
Концептуальная модель:
![alt text](https://github.com/marat74251/BD_HW/blob/head_bd/concept_model1.jpg?raw=true)
Логическая модель:
![alt text](https://github.com/marat74251/BD_HW/blob/head_bd/bd_logic_model.jpg?raw=true)
Используется 3 нормальная форма и 2 тип версионирования. 3 нормальная форма используется чтобы иметь однозначное трактование данных в таблицах(т.е. каждый атрибут в каждой табице зависит от первичного ключа этой таблицы и содержит информацию только о нём + все значения в таблице будут атомарны(1НФ) и первичный ключ в каждой таблице только 1(2НФ)) и упрощения понимания всей схемы. 2 тип версионирования используется т.к. нам необходимо хранить всю историю полностью и уметь к ней обращаться в любой момент.
Физическая модель: [ссылка на ворд файл](https://github.com/marat74251/BD_HW/blob/head_bd/Физ%20модель.docx) <br />
Скриншоты ворда, если невозможно открыть: <br />
![](https://github.com/marat74251/BD_HW/blob/head_bd/фт1.jpg?raw=true)
![](https://github.com/marat74251/BD_HW/blob/head_bd/фт2.jpg?raw=true)
![](https://github.com/marat74251/BD_HW/blob/head_bd/фт3.jpg?raw=true) <br />
DDL-скрипты: <br />
``` SQL
CREATE SCHEMA sales_management;
SET search_path TO sales_management;
CREATE TABLE Statuses (
    status_id INT PRIMARY KEY,
    status_name VARCHAR(50) NOT NULL,
    description VARCHAR(50) NOT NULL
);

CREATE TABLE Customers (
    customer_id INT PRIMARY KEY,
    customer_name VARCHAR(100) NOT NULL,
    customer_phone VARCHAR(20) NOT NULL,
    customer_email VARCHAR(100),
    customer_address TEXT NOT NULL,
    registration_date TIMESTAMP,
    last_modified TIMESTAMP
);

-- Создание таблицы категорий
CREATE TABLE Categories (
    category_id INT PRIMARY KEY,
    category_name VARCHAR(100) NOT NULL,
    description TEXT,
    valid_from TIMESTAMP NOT NULL,
    valid_to TIMESTAMP
);

CREATE TABLE Supplier_companies (
    supplier_id INT PRIMARY KEY,
    supplier_name VARCHAR(100) NOT NULL,
    supplier_phone VARCHAR(20) NOT NULL,
    supplier_email VARCHAR(100) NOT NULL,
    supplier_address TEXT NOT NULL
);

CREATE TABLE Contact_person (
    contact_person_id INT PRIMARY KEY,
    supplier_id INT NOT NULL,
    contact_name VARCHAR(100) NOT NULL,
    contact_phone VARCHAR(20) NOT NULL,
    contact_email VARCHAR(100) NOT NULL,
    valid_from DATE NOT NULL,
    valid_to DATE NOT NULL,
    FOREIGN KEY (supplier_id) REFERENCES Supplier_companies(supplier_id)
);

CREATE TABLE Employees (
    employee_id INT PRIMARY KEY,
    employee_name VARCHAR(100) NOT NULL,
    employee_position VARCHAR(50) NOT NULL,
    employee_phone VARCHAR(20) NOT NULL,
    employee_email VARCHAR(100) NOT NULL,
    hire_date DATE NOT NULL,
    valid_from TIMESTAMP NOT NULL,
    valid_to TIMESTAMP
);

-- Создание таблицы продуктов
CREATE TABLE Products (
    product_id INT PRIMARY KEY,
    product_name VARCHAR(100) NOT NULL,
    category_id INT NOT NULL,
    supplier_id INT NOT NULL,
    product_price INT NOT NULL,
    stock_quantity INT NOT NULL,
    description TEXT,
    valid_from TIMESTAMP NOT NULL,
    valid_to TIMESTAMP NOT NULL,
    FOREIGN KEY (category_id) REFERENCES Categories(category_id),
    FOREIGN KEY (supplier_id) REFERENCES Supplier_companies(supplier_id)
);

CREATE TABLE Orders (
    order_id INT PRIMARY KEY,
    customer_id INT NOT NULL,
    order_date TIMESTAMP NOT NULL,
    status_id INT NOT NULL,
    notes TEXT,
    FOREIGN KEY (customer_id) REFERENCES Customers(customer_id),
    FOREIGN KEY (status_id) REFERENCES Statuses(status_id)
);

CREATE TABLE Order_items (
    order_item_id INT PRIMARY KEY,
    order_id INT NOT NULL,
    product_id INT NOT NULL,
    order_item_quantity INT NOT NULL,
    FOREIGN KEY (order_id) REFERENCES Orders(order_id),
    FOREIGN KEY (product_id) REFERENCES Products(product_id)
);

CREATE TABLE Deliveries (
    delivery_id INT PRIMARY KEY,
    order_id INT NOT NULL,
    employee_id INT NOT NULL,
    planned_delivery_date TIMESTAMP NOT NULL,
    actual_delivery_date TIMESTAMP,
    status_id INT NOT NULL,
    notes TEXT,
    FOREIGN KEY (order_id) REFERENCES Orders(order_id),
    FOREIGN KEY (employee_id) REFERENCES Employees(employee_id),
    FOREIGN KEY (status_id) REFERENCES Statuses(status_id)
);
```
Ссылка на файл с DDL-скриптами: <br />
[DDL](https://github.com/marat74251/BD_HW/blob/head_bd/DDL-script.sql) <br />
Так как файл с DML-скриптами слишком большой то на него будет только ссылка, чтобы не захламлять место: <br />
[DML](https://github.com/marat74251/BD_HW/blob/head_bd/DML-script.sql) <br />
Перед выполнением скриптов прописать:
``` SQL
SET search_path TO sales_management;
```
В дальнейшем все скрипты будут указваться с учётом того что эта команда была прописана. <br />
<br />
№1: скрипт для получения информации о доставленных заказах <br />
``` SQL
SELECT o.order_id, c.customer_name, s.status_name, o.order_date
FROM Orders o
JOIN Customers c ON o.customer_id = c.customer_id
JOIN Statuses s ON o.status_id = s.status_id
WHERE s.status_name = 'Доставлен';
```
№2: получение категорий товаров с наибольшей выручкой <br />
``` SQL
SELECT cat.category_name, SUM(p.product_price * oi.order_item_quantity) AS total_sum
FROM Order_items oi
JOIN Products p ON oi.product_id = p.product_id
JOIN Categories cat ON p.category_id = cat.category_id
GROUP BY cat.category_name
ORDER BY total_sum DESC;
```
№3: получение самых активных клиентов, сделавших более 3 заказов (таких нет (для проверки можно поменять 3 на 2, такие есть (3 поставил т.к. 2 выглядит не солидно))) <br />
``` SQL
SELECT c.customer_id, c.customer_name, COUNT(o.order_id) AS order_count
FROM Customers c
JOIN Orders o ON c.customer_id = o.customer_id
GROUP BY c.customer_id, c.customer_name
HAVING COUNT(o.order_id) > 3
ORDER BY order_count DESC;
```
№4: получение топ-5 самых дорогих товаров на складе <br />
``` SQL
SELECT product_name, product_price, stock_quantity
FROM Products
WHERE stock_quantity > 0
ORDER BY product_price DESC
LIMIT 5;
```
№5: нахождение товаров, которые ни разу не были заказаны (таких нет) <br />
``` SQL
SELECT p.product_id, p.product_name
FROM Products p
WHERE NOT EXISTS (
    SELECT *
    FROM Order_items oi
    WHERE oi.product_id = p.product_id
);
```
№6: ранжирование клиентов по общей сумме, потраченной на заказы <br />
``` SQL
SELECT 
    c.customer_id,
    c.customer_name,
    SUM(p.product_price * oi.order_item_quantity) AS total_spent,
    RANK() OVER (ORDER BY SUM(p.product_price * oi.order_item_quantity) DESC) AS customer_rank
FROM Customers c
JOIN Orders o ON c.customer_id = o.customer_id
JOIN Order_items oi ON o.order_id = oi.order_id
JOIN Products p ON oi.product_id = p.product_id
GROUP BY c.customer_id, c.customer_name
ORDER BY total_spent DESC;
```
№7: вычисление средней стоимости заказа для каждого клиента <br />
``` SQL
SELECT 
    c.customer_id,
    c.customer_name,
    (SELECT AVG(p.product_price * oi.order_item_quantity)
     FROM Orders o
     JOIN Order_items oi ON o.order_id = oi.order_id
     JOIN Products p ON oi.product_id = p.product_id
     WHERE o.customer_id = c.customer_id) AS avg_order_value
FROM Customers c
ORDER BY avg_order_value DESC NULLS LAST;
```
№8: анализ гипотетической иерархии сотрудников (по дате наёма) <br />
``` SQL
SELECT e1.employee_id, e1.employee_name, e1.hire_date,
       e2.employee_id AS manager_id,
       e2.employee_name AS manager_name,
       e2.hire_date AS manager_hire_date
FROM Employees e1
JOIN Employees e2 ON e1.employee_id > e2.employee_id
WHERE e1.hire_date > e2.hire_date;
```
№9: сравнение каждого заказа со средним чеком по всем заказам <br />
``` SQL
SELECT 
    o.order_id,
    c.customer_name,
    SUM(p.product_price * oi.order_item_quantity) AS order_total,
    AVG(SUM(p.product_price * oi.order_item_quantity)) OVER () AS avg_order_value,
    ABS(SUM(p.product_price * oi.order_item_quantity) - AVG(SUM(p.product_price * oi.order_item_quantity)) OVER ()) AS diff_from_avg
FROM Orders o
JOIN Customers c ON o.customer_id = c.customer_id
JOIN Order_items oi ON o.order_id = oi.order_id
JOIN Products p ON oi.product_id = p.product_id
GROUP BY o.order_id, c.customer_name
ORDER BY diff_from_avg DESC;
```
№10: нахождение товаров с ценой выше средней по их категории <br />
``` SQL
SELECT p.product_id, p.product_name, p.product_price, cat.category_id, cat.category_name
FROM Products p
JOIN Categories cat ON p.category_id = cat.category_id
WHERE p.product_price > ANY (
    SELECT AVG(product_price)
    FROM Products
    WHERE category_id = p.category_id
);
```
