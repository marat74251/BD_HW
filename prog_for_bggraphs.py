import pandas as pd
import psycopg2
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import f_oneway
from scipy.stats import ttest_ind

conn = psycopg2.connect(
    dbname="postgres",
    user="postgres",
    password="utyz@2005",
    host="localhost",
    port="5432"
)

query = """
    SELECT 
        c.category_name,
        SUM(oi.order_item_quantity * p.product_price) AS revenue,
        COUNT(DISTINCT o.order_id) AS order_count
    FROM sales_management.order_items oi
    JOIN sales_management.orders o ON oi.order_id = o.order_id
    JOIN sales_management.products p ON oi.product_id = p.product_id
    JOIN sales_management.categories c ON p.category_id = c.category_id
    GROUP BY c.category_name
"""
df = pd.read_sql(query, conn)

plt.figure(figsize=(8, 8))
plt.pie(df['revenue'], labels=df['category_name'], autopct='%1.1f%%')
plt.title('Распределение выручки по категориям')
plt.show()

# test 1

plt.figure(figsize=(10, 6))
sns.scatterplot(data=df, x='order_count', y='revenue', hue='category_name', s=100)
plt.title("Зависимость выручки от количества заказов")
plt.xlabel("Количество заказов")
plt.ylabel("Общая выручка")
plt.legend(title="Категория")
plt.show()
correlation = df['order_count'].corr(df['revenue'])
print(f"Корреляция между заказами и выручкой: {correlation:.2f}")

# test 2

plt.figure(figsize=(10, 6))
sns.barplot(x='category_name', y='order_count', data=df)
plt.title('Количество заказов по категориям')
plt.xticks(rotation=45)
plt.show()

df['avg_check'] = df['revenue'] / df['order_count']

categories_avg_checks = []
for category in df['category_name']:
    avg_check_for_category = df.loc[df['category_name'] == category]['avg_check']
    categories_avg_checks.append(avg_check_for_category.values)

stat, p_val = f_oneway(*categories_avg_checks)
if p_val < 0.05:
    print("Есть значительные различия между средним чеком различных категорий.")
else:
    print("Различия между средним чеком незначительны.")

plt.figure(figsize=(10, 6))
sns.boxplot(data=df, x='category_name', y='avg_check')
plt.title("Средний чек по категориям")
plt.xticks(rotation=45)
plt.show()

# test 3

bins = [0, df['order_count'].quantile(0.33), df['order_count'].quantile(0.66), float('inf')]
labels = ['Низкая активность', 'Средняя активность', 'Высокая активность']
df['activity_level'] = pd.cut(df['order_count'], bins=bins, labels=labels)
grouped_data = df.groupby('activity_level').agg({'avg_check': 'mean'})
print(grouped_data)
low_activity_avg_check = df.query("activity_level == 'Низкая активность'")['avg_check']
high_activity_avg_check = df.query("activity_level == 'Высокая активность'")['avg_check']

t_stat, p_val = ttest_ind(low_activity_avg_check, high_activity_avg_check)
if p_val < 0.05:
    print("Клиенты с высоким уровнем активности имеют значительно больший средний чек.")
else:
    print("Нет существенной разницы в среднем чеке между клиентами разной активности.")
