import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv('Electronic_sales_Sep2023-Sep2024.csv')
df['Purchase Date'] = pd.to_datetime(df['Purchase Date'])
income_by_shipping = df.groupby('Shipping Type')['Total Price'].sum()
income_by_product = df.groupby('Product Type')['Total Price'].sum()

df['Month'] = df['Purchase Date'].dt.to_period('M')
income_addon_monthly = df.groupby('Month')['Add-on Total'].sum()

df['Quarter'] = df['Purchase Date'].dt.to_period('Q')
income_addon_quarterly = df.groupby('Quarter')['Add-on Total'].sum()

fig, axs = plt.subplots(2, 2, figsize=(14, 10))

income_by_shipping.plot(kind='bar', ax=axs[0, 0], title='Доход по методу доставки')
income_by_product.plot(kind='bar', ax=axs[0, 1], title='Доход по типу продукта')
income_addon_monthly.plot(kind='line', ax=axs[1, 0], title='Доход по доп. услугам за месяц')
income_addon_quarterly.plot(kind='line', ax=axs[1, 1], title='Доход по доп. услугам за квартал')

plt.tight_layout()
plt.show()