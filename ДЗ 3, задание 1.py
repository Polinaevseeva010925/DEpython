import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv('Electronic_sales_Sep2023-Sep2024.csv')
df['Purchase Date'] = pd.to_datetime(df['Purchase Date'])
preferred_payment = df.groupby('Customer ID')['Payment Method'].agg(lambda x: x.mode().iloc[0])
total_spent = df.groupby('Customer ID')['Total Price'].sum()
addon_spent = df.groupby('Customer ID')['Add-on Total'].sum()
customer_summary = pd.DataFrame({
    'Preferred Payment Method': preferred_payment,
    'Total Spent': total_spent,
    'Add-on Spent': addon_spent
})

print(customer_summary.head(10))