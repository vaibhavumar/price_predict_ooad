from keras.models import load_model
import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from django.conf import settings
from django.contrib import messages

def predict_price(date):
	csv_filepath = settings.MEDIA_ROOT + '/BHEL_Feb_2015_19.csv'
	model_filepath = settings.MEDIA_ROOT + '/OOAD_LSTM_model.h5'

	dataset = pd.read_csv(csv_filepath)
	dataset['Date'] = pd.to_datetime(dataset.Date, format='%d-%b-%Y')
	dataset.index = dataset['Date']
	data = dataset.sort_index(ascending=True, axis=0)
	new_dataset = pd.DataFrame(index=range(0,len(dataset)),columns=['Date','Close'])
	for ind in range(0,len(data)):
		new_dataset['Date'][ind] = data['Date'][ind]
		new_dataset['Close'][ind] = data['Close Price'][ind]
	new_dataset.index = new_dataset.Date
	new_dataset.drop('Date', axis=1, inplace=True)
	dataset_values = new_dataset.values
	scaler = MinMaxScaler(feature_range=(0,1))
	scaled_data = scaler.fit_transform(dataset_values)

	if date in data.index:
		index_date = data.index.get_loc(date)
		if index_date >= 20:
			inputs = new_dataset.iloc[index_date:index_date - 20:-1].values
			inputs = inputs.reshape(-1,1)
			inputs = scaler.transform(inputs)
			X_test = []
			for i in range(0, inputs.shape[0]):
			  X_test.append(inputs[i])
			X_test = np.array(X_test)
			X_test = np.reshape(X_test, (1, X_test.shape[0], X_test.shape[1]))
			lstm_model = load_model(model_filepath)
			closing_price = lstm_model.predict(X_test)
			closing_price = scaler.inverse_transform(closing_price)
			predictedprice = closing_price[0][0]
			actualprice = new_dataset.loc[date]['Close']
			return predictedprice, actualprice
		else:
			return (-1, 'Input Date Greater than 2015-03-01')
	else:
		return (-1, 'Holiday')
