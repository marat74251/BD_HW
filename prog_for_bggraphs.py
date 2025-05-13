import pandas as pd
import psycopg2
import matplotlib.pyplot as plt
import seaborn as sns

conn = psycopg2.connect(
    dbname="...",
    user="...",
    password="...",
    host="localhost"
)

query = """
    SELECT 
        c.category_name,
        SUM(oi.order_item_quantity * p.product_price) AS revenue,
        COUNT(DISTINCT o.order_id) AS order_count
    FROM order_items oi
    JOIN orders o ON oi.order_id = o.order_id
    JOIN products p ON oi.product_id = p.product_id
    JOIN categories c ON p.category_id = c.category_id
    GROUP BY c.category_name
"""
df = pd.read_sql(query, conn)

plt.figure(figsize=(8, 8))
plt.pie(df['revenue'], labels=df['category_name'], autopct='%1.1f%%')
plt.title('Распределение выручки по категориям')
plt.show()

plt.figure(figsize=(10, 6))
sns.barplot(x='category_name', y='order_count', data=df)
plt.title('Количество заказов по категориям')
plt.xticks(rotation=45)
plt.show()

plt.figure(figsize=(8, 6))
sns.scatterplot(x='order_count', y='revenue', hue='category_name', data=df, s=100)
plt.title('Зависимость выручки от количества заказов')
plt.xlabel('Количество заказов')
plt.ylabel('Выручка')
plt.show()