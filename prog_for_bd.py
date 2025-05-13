import pandas as pd
import psycopg2
from faker import Faker # для генерации случайных, но подходящих данных
import random
from datetime import datetime, timedelta

conn = psycopg2.connect(
    dbname="...",
    user="...",
    password="...",
    host="localhost"
)
cursor = conn.cursor()

fake = Faker()

for _ in range(50):
    cursor.execute(
        "INSERT INTO customers (customer_name, customer_phone, customer_email, customer_address) "
        "VALUES (%s, %s, %s, %s)",
        (fake.name(), fake.phone_number(), fake.email(), fake.address())
    )

cursor.execute("SELECT customer_id FROM customers")
customer_ids = [row[0] for row in cursor.fetchall()]

cursor.execute("SELECT product_id, product_price FROM products")
products = cursor.fetchall()

for _ in range(200):
    customer_id = random.choice(customer_ids)
    order_date = fake.date_between(start_date='-1y', end_date='today')
    
    cursor.execute(
        "INSERT INTO orders (customer_id, order_date, status_id) "
        "VALUES (%s, %s, %s) RETURNING order_id",
        (customer_id, order_date, random.randint(1, 7))
    )
    
    order_id = cursor.fetchone()[0]
    
    for _ in range(random.randint(1, 5)):
        product_id, price = random.choice(products)
        quantity = random.randint(1, 3)
        
        cursor.execute(
            "INSERT INTO order_items (order_id, product_id, order_item_quantity) "
            "VALUES (%s, %s, %s)",
            (order_id, product_id, quantity)
        )

conn.commit()
cursor.close()
conn.close()