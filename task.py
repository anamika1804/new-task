# -*- coding: utf-8 -*-
"""Untitled8.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1Nv5c1DDJ0OjfhgF-a66km14Ww8fQ7YaC
"""

!pip install scikit-optimize

pip show scikit-learn

import numpy as np
import pandas as pd

import seaborn as sns
from matplotlib import pyplot as plt
from matplotlib import style

# Preprocessing
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, OneHotEncoder

# Metrics
from sklearn.metrics import log_loss
from sklearn.model_selection import cross_val_score

import skopt
from skopt.space  import Real, Categorical, Integer
import math

train_df=pd.read_excel('Omnify-Analyst-Intership-Task.xlsx')

train_df.info()

train_df.head(8)

train_df.columns.values

#setting all null values to true
train_df.info(verbose=True, null_counts=True)

#count no of observations
train_df['Week'].value_counts()

#count no of observations
train_df['Cost ($)'].value_counts()

#count no of observations
train_df['Payment ($)'].value_counts()

train_df.isnull().sum()

# Transform the Date into a python datetime object.
train_df["Week"] = pd.to_datetime(train_df["Week"], format="%Y-%m-%d")

train_df.head(3)

# Day
train_df["Day"] = train_df["Week"].map(lambda x: x.day)

train_df["Month"] = train_df["Week"].map(lambda x: x.month)

train_df["Year"] = train_df["Week"].map(lambda x: x.year)

train_df.head(3)

#count of observation monthly

train_df['Month'].value_counts()

weekly_data = train_df[numeric_columns].resample('W').sum()

# Add the 'Week' column
weekly_data['Week'] = weekly_data.index.isocalendar().week

# Create a monthly report
monthly_data = train_df[numeric_columns].resample('M').sum()

# Add the 'Month' column
monthly_data['Month'] = monthly_data.index.to_series().dt.month

train_df['Payment ($)'] = train_df['Payment ($)'].replace('[\$,]', '', regex=True).astype(float)

train_df['Returns %'] = train_df['Payment ($)'] / train_df['Cost ($)'] * 100

train_df['Payments'] = pd.to_numeric(train_df['Payment ($)'])
train_df['Cost'] = pd.to_numeric(train_df['Cost ($)'])

weekly_report = train_df[['Cost ($)', 'Returns %', 'Impressions', 'Clicks', 'Prospects', 'Payment ($)']]

numeric_columns = train_df.select_dtypes(include=[float, int]).columns

channel_data = train_df.groupby('Ad group')[numeric_columns].sum()

# Calculate returns % for each channel
channel_data['Returns %'] = channel_data['Payments'] / channel_data['Cost'] * 100

# Identify the most profitable channel
most_profitable_channel = channel_data['Returns %'].idxmax()

# Group data by category/keyword and calculate total payments and costs
category_data = train_df.groupby('Search Keyword')[numeric_columns].sum()

# Calculate returns % for each category/keyword
category_data['Returns %'] = category_data['Payments'] / category_data['Cost'] * 100

# Identify the most profitable category/keyword
most_profitable_category = category_data['Returns %'].idxmax()

import matplotlib.pyplot as plt

# Plotting time series data
plt.figure(figsize=(10, 6))
plt.plot(train_df.index, train_df['Cost ($)'], label='Cost($)')
plt.plot(train_df.index, train_df['Returns %'], label='Returns %')
plt.plot(train_df.index, train_df['Impressions'], label='Impressions')
# Add other metrics here
plt.xlabel('Date')
plt.ylabel('Metrics')
plt.legend()
plt.title('Time Series Metrics')
plt.show()

# Group data by geography and calculate total payments and costs
geography_data = train_df.groupby('Country')[numeric_columns].sum()

# Calculate returns % for each geography
geography_data['Returns %'] = geography_data['Payments'] / geography_data['Cost'] * 100

# Plotting returns % for each geography
geography_data['Returns %'].plot(kind='bar')
plt.xlabel('Country')
plt.ylabel('Returns %')
plt.title('Returns % by Country')
plt.show()

