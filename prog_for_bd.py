import psycopg2
from faker import Faker # для генерации случайных, но подходящих данных
import random

conn = psycopg2.connect(
    dbname="postgres",
    user="postgres",
    password="utyz@2005",
    host="localhost",
    port="5432"
)
cursor = conn.cursor()

fake = Faker()

cursor.execute("SELECT MAX(customer_id) FROM sales_management.customers")
max_id = cursor.fetchone()[0] or 0 

new_id = max_id + 1
for i in range(1):
    cursor.execute(
        "INSERT INTO sales_management.customers "
        "(customer_id, customer_name, customer_phone, customer_email, customer_address, registration_date, last_modified) "
        "VALUES (%s, %s, %s, %s, %s, %s, %s) "
        "RETURNING customer_id",
        (str(new_id + i), fake.name(), fake.phone_number(), fake.email(), fake.address(), fake.date_time_this_decade(), fake.date_time_this_decade())
    )

cursor.execute("SELECT customer_id FROM sales_management.customers")
customer_ids = [row[0] for row in cursor.fetchall()]

cursor.execute("SELECT product_id, product_price FROM sales_management.products")
products = cursor.fetchall()

cursor.execute("SELECT MAX(order_id) FROM sales_management.orders")
max_id = cursor.fetchone()[0] or 0 

new_id = max_id + 1

for j in range(1):
    customer_id = random.choice(customer_ids)
    order_date = fake.date_between(start_date='-1y', end_date='today')
    
    cursor.execute(
        "INSERT INTO sales_management.orders (order_id, customer_id, order_date, status_id, notes) "
        "VALUES (%s, %s, %s, %s, %s) RETURNING order_id",
        (str(new_id + j), customer_id, order_date, random.randint(1, 7), fake.sentence())
    )
    
    order_id = cursor.fetchone()[0]
    
    cursor.execute("SELECT MAX(order_item_id) FROM sales_management.order_items")
    max_i_id = cursor.fetchone()[0] or 0 

    new_i_id = max_i_id + 1

    for k in range(random.randint(1, 5)):
        product_id, price = random.choice(products)
        quantity = random.randint(1, 3)
        
        cursor.execute(

            "INSERT INTO sales_management.order_items (order_item_id, order_id, product_id, order_item_quantity) "
            "VALUES (%s, %s, %s, %s)",
            (str(new_i_id + k), order_id, product_id, quantity)
        )

conn.commit()
cursor.close()
conn.close()