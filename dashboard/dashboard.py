import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

# Load the data
df = pd.read_csv('data/day.csv')

# Denormalize the temperature values
df['temp_actual'] = (df['temp'] * (39 - (-8)) + (-8)).astype(int)

# Convert the 'dteday' column to datetime
df['dteday'] = pd.to_datetime(df['dteday'])
df['year_month'] = df['dteday'].dt.to_period('M')

# Streamlit app
st.title('Bike Sharing Data Dashboard')

# Sidebar filters
st.sidebar.header('Filters')
temp_range = st.sidebar.slider('Temperature Range (°C)', min_value=int(df['temp_actual'].min()), max_value=int(df['temp_actual'].max()), value=(int(df['temp_actual'].min()), int(df['temp_actual'].max())))
start_date, end_date = st.sidebar.date_input('Date Range', value=[df['dteday'].min(), df['dteday'].max()])

# Filter data based on selections
df_filtered_by_temp = df[(df['temp_actual'] >= temp_range[0]) & (df['temp_actual'] <= temp_range[1])]

# Bar chart by temperature
st.subheader('Count of Total Rental Bikes Based on Temperature')
plt.figure(figsize=(12, 6))
sns.barplot(x='temp_actual', y='cnt', data=df_filtered_by_temp, errorbar=None)
plt.xlabel('Temperature (°C)')
plt.ylabel('Count of Total Rental Bikes')
plt.title('Count of Total Rental Bikes Based on Temperature')
st.pyplot(plt)

# Group by year and month for filtered data
df_filtered_by_date = df[(df['dteday'] >= pd.to_datetime(start_date)) & (df['dteday'] <= pd.to_datetime(end_date))].groupby('year_month')['cnt'].sum().reset_index()

# Bar chart by month and year
st.subheader('Count of Total Rental Bikes by Month and Year')
plt.figure(figsize=(12, 6))
plt.bar(df_filtered_by_date['year_month'].astype(str), df_filtered_by_date['cnt'])
plt.xlabel('Year-Month')
plt.ylabel('Count of Total Rental Bikes')
plt.title('Count of Total Rental Bikes by Month and Year')
plt.xticks(rotation=45)
st.pyplot(plt)
