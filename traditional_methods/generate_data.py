import pandas as pd
import numpy as np
import random
import plotly.express as px

random.seed(10)

dates = pd.date_range(start='01-01-2000', end='01-01-2024', freq = 'QE')
product_line = 'XYZ'
starting_inventory = 1000
seasonal_magnitude = 200

# Simulating inventory data
inventory_over_time = [1000]
for i in range(len(dates)):

    quarterly_fluctuation = random.random() - 0.4
    inventory_over_time.append(inventory_over_time[i] + inventory_over_time[i] * quarterly_fluctuation *0.1)

# Creating dataframe
df = pd.DataFrame.from_dict({'product_line': [product_line] * len(dates),
                             'quarter': dates,
                             'inventory': inventory_over_time[1:]})

# Adding seasonal trend
cycles = 23 # how many sine cycles
resolution = len(dates) # how many datapoints to generate
length = np.pi * 2 * cycles
seasonal_series = np.sin(np.arange(0, length, length / resolution)) * seasonal_magnitude
df['inventory'] = df['inventory'] + seasonal_series

# Graphing data
fig = px.scatter(df, x = 'quarter', y = 'inventory')
fig.show()

# Writing data
df.to_csv('./traditional_methods/Data/quarterly_data.csv')