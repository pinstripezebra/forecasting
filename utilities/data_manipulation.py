import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots

def convert_to_supervised(data, window_size=1, forecast_size=1, dropnan=True):
 
    '''Converts a 1d time series dataset into a 2d supervised learning format'''

    df = pd.DataFrame(data)
    cols = list()
    # Training sequence: t-window_size, ..., t-1
    for i in range(window_size, 0, -1):
        cols.append(df.shift(i))
    
    # Forecast sequence: (t, t+1, ... t+forecast_size)
    for i in range(0, forecast_size):
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
    output_df = output_df.sort_values(by = 'Date', ascending=True).reset_index(drop=True)
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
    
    # Adding test and train predictions
    fig.add_trace(go.Scatter(x=train_df['Date'], y=train_df['Prediction'],
                        mode='markers',
                        name='Train Prediction'))
    
    fig.add_trace(go.Scatter(x=test_df['Date'], y=test_df['Prediction'],
                        mode='markers', name='Test Prediction'))
    fig.update_layout(title = "Predicted vs. Actual, {model}".format(model = model_type))

    fig.show()

def plot_comparison(train_pred, test_pred, train_y, test_y, dates):

    '''dates: list of dates to serve as x axis'''
    factor_levels = train_pred.shape[1]

    # making subplots
    fig = make_subplots(rows=factor_levels, cols=1)
    # iterating through factor levels
    for level in range(factor_levels):

        # defining dates for x axis
        train_dates = dates[:train_pred.shape[1]]
        test_dates = dates[-test_pred.shape[1]:]

        # train set
        fig.append_trace(go.Scatter(x=train_dates, y=train_y[:, level],
                            mode='lines',
                            name='Actual-Train'),
                            row=level, col=1)
        # test set
        fig.append_trace(go.Scatter(x=test_dates, y=test_y[:, level],
                            mode='lines',
                            name='Actual-Test'),
                            row=level, col=1)
        
        # train pred
        fig.append_trace(go.Scatter(x=train_dates, y=train_pred[:, level],
                            mode='Markers',
                            name='Pred-Train'),
                            row=level, col=1)
        # test pred
        fig.append_trace(go.Scatter(x=test_dates, y=test_pred[:, level],
                            mode='Markers',
                            name='Pred-Test'),
                            row=level, col=1)
        
    fig.update_layout(height=600, width=600, title_text="Test vs. Train, By Series")
    fig.show()