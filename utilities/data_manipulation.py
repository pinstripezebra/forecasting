import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import plotly.graph_objects as go

def convert_to_supervised(data, n_in=1, n_out=1, dropnan=True):
 
    '''Converts a 1d time series dataset into a 2d supervised learning format'''

    df = pd.DataFrame(data)
    cols = list()
    # Training sequence (t-n, ... t-1)
    for i in range(n_in, 0, -1):
        cols.append(df.shift(i))
    
    # Forecast sequence (t, t+1, ... t+n)
    for i in range(0, n_out):
        cols.append(df.shift(-i))

    # Concatenating columns together
    agg = pd.concat(cols, axis=1)
 
    # drop rows with NaN values
    if dropnan:
        agg.dropna(inplace=True)
    return agg.values

def rename_dataframe_supervised(data_df, state_name = ""):

   '''Takes a dataframe with column names 1-x, relables them as t through t - x
   and returns. Used to illustrate how the timeseries to supervised conversion works'''

   # Renaming columns in dataframe
   max_col = max(data_df.columns.astype(int))
   for col in data_df.columns:
      if int(col) == max_col:
         data_df.rename(columns={col:"t"},inplace=True)
      else:
         data_df.rename(columns={col:"{state}t - {val}".format(state = state_name,val = max_col-col)},inplace=True)
   return data_df

def pivot_dataframe(input_df, identifier_col, value_col):

    '''Takes multilevel time-series dataframe with identifier_col specifying unique time series and returns
    wide dataframe with each level in time identifier_col as separate column'''

    unique_vals = input_df[identifier_col].drop_duplicates().to_list()
    independent_series = {}
    for val in unique_vals:
        independent_series[val] = input_df[input_df[identifier_col] == val][value_col].to_list()
    output_df = pd.DataFrame(independent_series)
    output_df['Date'] = input_df['Date'].drop_duplicates().to_list()

    return output_df


def plot_results(dataset, target_val, model_type):

    # Create traces
    fig = go.Figure()
    
    train_df = dataset[dataset['Prediction_Type'] == 'Train']
    test_df= dataset[dataset['Prediction_Type'] == 'Test']

    # Adding plot of original_df
    fig.add_trace(go.Scatter(x=dataset['Date'], y=dataset[target_val],
                        mode='lines',
                        name='Actual'))
    
    fig.add_trace(go.Scatter(x=train_df['Date'], y=train_df[target_val],
                        mode='lines+markers',
                        name='Train Prediction'))
    
    fig.add_trace(go.Scatter(x=test_df['Date'], y=test_df[target_val],
                        mode='markers', name='Test Prediction'))
    fig.update_layout(title = "Predicted vs. Actual, {model}".format(model = model_type))

    fig.show()