import pandas as pd
import sqlite3

# 1. Create/connect to SQLite DB file
conn = sqlite3.connect("ecommerce_data.db")  # Output file: ecommerce_data.db

# 2. Load each Excel file (replace filenames with yours)
df1 = pd.read_excel("Product-Level Ad Sales and Metrics (mapped).xlsx")
df2 = pd.read_excel("Product-Level Eligibility Table (mapped).xlsx")
df3 = pd.read_excel("Product-Level Total Sales and Metrics (mapped).xlsx")

# 3. Save them as tables in the SQLite DB
df1.to_sql("Ad_Sales_and_Metrics", conn, if_exists="replace", index=False)
df2.to_sql("Eligibility", conn, if_exists="replace", index=False)
df3.to_sql("Total_Sales_and_Metrics", conn, if_exists="replace", index=False)

cursor = conn.cursor()

rows = cursor.execute("SELECT * FROM table1 LIMIT 5;")

for data in rows:
    print(data)


# 4. Done!
conn.close()
print("Database created with 3 tables!")
