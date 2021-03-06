import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import pandas_datareader as data
from keras.models import load_model
import streamlit as st

start='2010-01-01'
end='2021-12-30'

st.title('TREND PREDICTION OF STOCKS')

user_input=st.text_input('ENTER THE TICKER','INFY')
df=data.DataReader(user_input,'yahoo',start,end)

#DATA DESCRIPTION
st.subheader('Data From 2010-2021')
st.write(df.describe())

#VISUALIZATIONS
st.subheader('CLOSING PRICE VS TIME')
figure=plt.figure(figsize=(12,6))
plt.plot(df.Close)
st.pyplot(fig)

st.subheader('CLOSING PRICE VS TIME with MAVG100')
mavg100=df.Close.rolling(100).mean()
figure=plt.figure(figsize=(12,6))
plt.plot(mavg100)
plt.plot(df.Close)
st.pyplot(fig)

st.subheader('CLOSING PRICE VS TIME with MAVG100 & MAVG200')
mavg100=df.Close.rolling(100).mean()       
mavg200=df.Close.rolling(200).mean()
figure=plt.figure(figsize=(12,6))
plt.plot(mavg100)          
plt.plot(mavg200)
plt.plot(df.Close)
st.pyplot(fig)

data_train=pd.DataFrame(df['Close'][0:int(len(df)*0.70)])
data_test=pd.DataFrame(df['Close'][int(len(df)*0.70):int(len(df))])
from sklearn.preprocessing import MinMaxScaler
scaler=MinMaxScaler(feature_range=(0,1))
data_train_array=scaler.fit_transform(data_train)

# CONVERT X_TRAIN & Y_TRAIN TO NUMPY ARRAYS
x_train=[]
y_train=[]
for i in range(100,data_train_array.shape[0]):
    x_train.append(data_train_array[i-100:i])
    y_train.append(data_train_array[i,0])
x_train,y_train=np.array(x_train),np.array(y_train)

#LOAD THE MODEL
model=load_model('lstm_model.h5')

prev_100_days=data_train.tail(100)
final_df=prev_100_days.append(data_test,ignore_index=True)
input_data=scaler.fit_transform(final_df)
x_test=[]
y_test=[]
for i in range(100,input_data.shape[0]):
    x_test.append(input_data[i-100:i])
    y_test.append(input_data[i,0])
    
x_test,y_test=np.array(x_test),np.array(y_test)
y_predicted=model.predict(x_test)

scaler=scaler.scale_
scale_factor=1/scaler[0]
y_predicted=y_predicted*scale_factor
y_test=y_test*scale_factor

#FINE GRAPH
st.subheader('ACTAUAL VS PREDICTED')
fig2=plt.figure(figsize=(12,6))
plt.plot(y_test,'b',label='original price')
plt.plot(y_predicted,'r',label='predicted price')
plt.xlabel('TIME')
plt.ylabel('PRICE')
plt.legend()
st.pyplot(fig2)


