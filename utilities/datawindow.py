
import datetime

import numpy as np
import pandas as pd
import seaborn as sns
import tensorflow as tf
import matplotlib.pyplot as plt

from tensorflow.keras import Model, Sequential

from tensorflow.keras.optimizers import Adam
from tensorflow.keras.callbacks import EarlyStopping
from tensorflow.keras.losses import MeanSquaredError
from tensorflow.keras.metrics import MeanAbsoluteError

from tensorflow.keras.layers import Dense, Conv1D, LSTM, Lambda, Reshape, RNN, LSTMCell

class DataWindow():
    def __init__(self, input_width, label_width, shift, 
                 train_df, val_df, test_df, 
                 label_columns):
        
        self.train_df = train_df
        self.val_df = val_df
        self.test_df = test_df
        
        self.label_columns = label_columns
        if label_columns is not None:
            self.label_columns_indices = {name: i for i, name in enumerate(label_columns)}
        self.column_indices = {name: i for i, name in enumerate(train_df.columns)}
        
        self.input_width = input_width
        self.label_width = label_width
        self.shift = shift
        
        self.total_window_size = input_width + shift
        
        self.input_slice = slice(0, input_width)
        self.input_indices = np.arange(self.total_window_size)[self.input_slice]
        
        self.label_start = self.total_window_size - self.label_width
        self.labels_slice = slice(self.label_start, None)
        self.label_indices = np.arange(self.total_window_size)[self.labels_slice]
    
    def split_to_inputs_labels(self, features):
        inputs = features[:, self.input_slice, :]
        labels = features[:, self.labels_slice, :]
        if self.label_columns is not None:
            labels = tf.stack(
                [labels[:,:,self.column_indices[name]] for name in self.label_columns],
                axis=-1
            )
        inputs.set_shape([None, self.input_width, None])
        labels.set_shape([None, self.label_width, None])
        
        return inputs, labels
    
    def plot(self, model=None, plot_col='traffic_volume', max_subplots=3):
        inputs, labels = self.sample_batch
        
        plt.figure(figsize=(12, 8))
        plot_col_index = self.column_indices[plot_col]
        max_n = min(max_subplots, len(inputs))
        
        for n in range(max_n):
            plt.subplot(3, 1, n+1)
            plt.ylabel(f'{plot_col} [scaled]')
            plt.plot(self.input_indices, inputs[n, :, plot_col_index],
                     label='Inputs', marker='.', zorder=-10)

            if self.label_columns:
              label_col_index = self.label_columns_indices.get(plot_col, None)
            else:
              label_col_index = plot_col_index

            if label_col_index is None:
              continue

            plt.scatter(self.label_indices, labels[n, :, label_col_index],
                        edgecolors='k', marker='s', label='Labels', c='green', s=64)
            if model is not None:
              predictions = model(inputs)
              plt.scatter(self.label_indices, predictions[n, :, label_col_index],
                          marker='X', edgecolors='k', label='Predictions',
                          c='red', s=64)

            if n == 0:
              plt.legend()

        plt.xlabel('Time (h)')
        
    def make_dataset(self, data):
        data = np.array(data, dtype=np.float32)
        ds = tf.keras.preprocessing.timeseries_dataset_from_array(
            data=data,
            targets=None,
            sequence_length=self.total_window_size,
            sequence_stride=1,
            shuffle=True,
            batch_size=32
        )
        
        ds = ds.map(self.split_to_inputs_labels)
        return ds
    
    @property
    def train(self):
        return self.make_dataset(self.train_df)
    
    @property
    def val(self):
        return self.make_dataset(self.val_df)
    
    @property
    def test(self):
        return self.make_dataset(self.test_df)
    
    @property
    def sample_batch(self):
        result = getattr(self, '_sample_batch', None)
        if result is None:
            result = next(iter(self.train))
            self._sample_batch = result
        return result
    
class Baseline(Model):
    def __init__(self, label_index=None):
        super().__init__()
        self.label_index = label_index
        
    def call(self, inputs):
        if self.label_index is None:
            return inputs
        
        elif isinstance(self.label_index, list):
            tensors = []
            for index in self.label_index:
                result = inputs[:, :, index]
                result = result[:, :, tf.newaxis]
                tensors.append(result)
            return tf.concat(tensors, axis=-1)
        
        result = inputs[:, :, self.label_index]
        return result[:,:,tf.newaxis]
    

class AirQuality():

    def __init__(self, location):

        self.location = location
        self.raw_data = []
        self.model = None


    def pull_data(self, data_points):

        """Function queries data from openAQ api and returns dataframe

            Input: data_points
                int, contains max datapoints to return from API
            Returns: 
                None, updates internal data structure
        """

        # Defining url for location and requesting data
        converted = []
        
        # Defining dates
        today = str(datetime.date.today())
        year = today[:4]
        month = today[5:7]
        day = today[-2:]
        try:
            url = "https://api.openaq.org/v2/measurements?date_from=2024-05-30T00%3A00%3A00Z&date_to={}-{}-{}T20%3A45%3A00Z&limit={}&page=1&offset=0&sort=desc&parameter_id=2&radius=1000&location_id={}&order_by=datetime".format(year, month, day, data_points, self.location)
            headers = {"accept": "application/json"}
            response = requests.get(url, headers=headers)
            converted = response.json()['results']
        except:
            print("Invalid query")

        # Defining lists for data parsing
        values, date, location, parameter, latitude, longitude = [], [], [], [], [], []
        
        # Iterating through dict and appending values
        for entry in converted:
            values.append(entry['value'])
            date.append(entry['date']['utc'])
            location.append(entry['locationId'])
            parameter.append(entry['parameter'])
            latitude.append(entry['coordinates']['latitude'])
            longitude.append(entry['coordinates']['longitude'])

        df = pd.DataFrame.from_dict({"Date": date,
                                "Value": values,
                                "location": location,
                                "parameter": parameter,
                                'longitude': longitude,
                                "latitude": latitude})
        df['Date'] =  df['Date'].astype(str)
        
        # Converting datetime
        df['Data_Converted'] = df['Date'].str.slice(start = 0, stop = 10) + " " + df['Date'].str.slice(start = 11)
        df['Data_Converted'] = pd.to_datetime(df['Data_Converted'], format='mixed') 
        self.raw_data = df
