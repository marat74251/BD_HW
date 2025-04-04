# BD_HW
Концептуальная модель:
![alt text](https://github.com/marat74251/BD_HW/blob/head_bd/concept_model1.jpg?raw=true)
Логическая модель:
![alt text](https://github.com/marat74251/BD_HW/blob/head_bd/bd_logic_model.jpg?raw=true)
Используется 3 нормальная форма и 2 тип версионирования. 3 нормальная форма используется чтобы иметь однозначное трактование данных в таблицах(т.е. каждый атрибут в каждой табице зависит от первичного ключа этой таблицы и содержит информацию только о нём + все значения в таблице будут атомарны(1НФ) и первичный ключ в каждой таблице только 1(2НФ)) и упрощения понимания всей схемы. 2 тип версионирования используется т.к. нам необходимо хранить всю историю полностью и уметь к ней обращаться в любой момент.
Физическая модель: <br />
![ссылка на ворд файл](https://github.com/marat74251/BD_HW/blob/head_bd/Физ%20модель.docx?raw=true) <br />
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
