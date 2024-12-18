import numpy as np
import pandas as pd
import glob
import seaborn as sns
from matplotlib import pyplot as plt
pd.set_option('display.max_columns', 15)

sales_2022_csv_files = glob.glob('2022/*.csv')
sales_2023_csv_files = glob.glob('2023/*.csv')
sales_2024_csv_files = glob.glob('2024/*.csv')

sales_data_list = []

for file in sales_2022_csv_files:
    df = pd.read_csv(file, sep = '\t')
    sales_data_list.append(df)

for file in sales_2023_csv_files:
    df = pd.read_csv(file, sep = '\t')
    sales_data_list.append(df)

for file in sales_2024_csv_files:
    df = pd.read_csv(file, sep = '\t')
    sales_data_list.append(df)

sales_data = pd.concat(sales_data_list, ignore_index=True)
# print(sales_data.columns)

car_model = pd.read_csv('Car Model Lookup Table.csv', sep = '\t')
region = pd.read_csv('Region Lookup Table.csv', sep = '\t')
sales_rep = pd.read_csv('Sales Rep Lookup Table.csv', sep = '\t')

# print(car_model.columns)

sales_data = pd.merge(sales_data, car_model, on = 'Car Model ID', how = 'left')
sales_data = pd.merge(sales_data, region, on = 'Region ID', how = 'left')
sales_data = pd.merge(sales_data, sales_rep, on = 'Sales Rep ID', how = 'left')

sales_data.drop(sales_data.columns[[1,2,3,11]], axis = 1, inplace = True)

start_index = 1201
sales_data['Invoice ID'] = ['OLX-' + str(i) for i in range(start_index, start_index + len(sales_data))]

sales_data['Sale Date'] = pd.to_datetime(sales_data['Sale Date'], errors = 'coerce')

sales_data['Year'] = sales_data['Sale Date'].dt.year.astype(str)
sales_data['Quarter'] = 'Q' + sales_data['Sale Date'].dt.quarter.astype(str)
# Formatting the monthname (%B for Complete month name, %b for short name of the month using dt.strftime() method.
sales_data['Month'] = sales_data['Sale Date'].dt.strftime('%B')

month_abbreviations = {
    'January': 'Jan',
    'February': 'Feb',
    'March': 'Mar',
    'April': 'Apr',
    'May': 'May',
    'June': 'Jun',
    'July': 'Jul',
    'August': 'Aug',
    'September': 'Sep',
    'October': 'Oct',
    'November': 'Nov',
    'December': 'Dec'
}

sales_data['Month'] = sales_data['Month'].map(month_abbreviations)

sales_data['Sales'] = sales_data['Price'] * sales_data['Units Sold']

# Finding the Total Sales By Region
total_sales_by_region = sales_data.groupby('Region')['Sales'].sum().reset_index()
total_sales_by_region['Sales'] = pd.to_numeric(total_sales_by_region['Sales'])/1_000_000

# Finding the Total Sales By Car Model
total_sales_by_car_model = sales_data.groupby('Car Model')['Sales'].sum().reset_index()
total_sales_by_car_model['Sales'] = pd.to_numeric(total_sales_by_car_model['Sales'])/1_000_000

# Finding the Total Sales By Color
total_sales_by_color = sales_data.groupby('Color')['Sales'].sum().reset_index()
total_sales_by_color['Sales'] = pd.to_numeric(total_sales_by_color['Sales'])/1_000_000

# Finding the Total Revenue By Sales Rep Name
revenue_by_sales_rep = sales_data.groupby('Sales Rep Name')['Revenue'].sum().reset_index()
revenue_by_sales_rep['Revenue'] = pd.to_numeric(revenue_by_sales_rep['Revenue'])/1_000_000

# Finding the Average Sales By Car Model
avg_sales_by_car_model = sales_data.groupby('Car Model')['Sales'].mean().reset_index()
avg_sales_by_car_model['Sales'] = pd.to_numeric(avg_sales_by_car_model['Sales'])/1_000



plt.figure(figsize = (5,3))
bar_plot_1 = sns.barplot(data = total_sales_by_region, x = 'Region', y = 'Sales', color = '#ddb892')

for index, row in total_sales_by_region.iterrows():
    bar_plot_1.text(index, row.Sales - 0.5, f'{row.Sales:,.2f} M', color = 'black', ha = 'center', va = 'top')

plt.title('Total Sales By Region')
plt.show()


plt.figure(figsize = (15,4))
bar_plot_2 = sns.barplot(data = total_sales_by_car_model, x = 'Car Model', y = 'Sales', color= '#ddb892')

for index, row in total_sales_by_car_model.iterrows():
    bar_plot_2.text(index, row.Sales - 0.2, f'{row.Sales:.2f} M', color = 'black',ha = 'center', va = 'top')

plt.title('Total Sales by Car Model')
plt.show()

plt.figure(figsize = (10,4))
bar_plot_3 = sns.barplot(data = total_sales_by_color, x = 'Color', y = 'Sales', color = '#ddb892')

for index, row in total_sales_by_color.iterrows():
    bar_plot_3.text(index, row.Sales - 0.2, f'{row.Sales:.2f} M', color = 'black',ha = 'center', va = 'top')

plt.title('Total Sales by Color')
plt.show()