import numpy as np
import pandas as pd
import pickle
import streamlit as st

import sklearn
from sklearn.preprocessing import MinMaxScaler

# Read dependecies
df = pd.read_csv('cleaned_whr.csv')
df['year'] = df['year'].astype('int64')
features = ['year', 'Log GDP per capita',
       'Social support', 'Healthy life expectancy at birth',
       'Freedom to make life choices', 'Generosity',
       'Perceptions of corruption']
scaler = MinMaxScaler()
scaler.fit(df[features])

with open('rf.pkl', 'rb') as f:
    rf = pickle.load(f)

sample_id = np.random.randint(0, high=len(df))

# Intro
st.markdown('<h1><u>Happiness Score Prediction</u></h1>', unsafe_allow_html=True)
st.text("We used our trained Random Forest model to predict how happy a country is.")
st.text("Here we see how well it does.")



def get_pred_score(feat_vals):
    scaled_feat = scaler.transform(feat_vals.values.reshape(1, -1))[0]
    scaled_feat = scaled_feat.reshape(1, -1)
    return rf.predict(scaled_feat)[0]

country, year = df['Country name'].iloc[sample_id], df[features[0]].iloc[sample_id]
st.markdown(f'<h4>{country} in {year} </h4>', unsafe_allow_html=True)

feat_vals = df[features].iloc[sample_id]
feat_vals.name = ' '
score = df['Life Ladder'].iloc[sample_id]

pred_score = get_pred_score(feat_vals)

st.table(feat_vals[1:]) # [1:] to avoid year
st.write(f'Actual Happiness Score: {score}/10')
st.write(f'Predicted Happiness Score: {np.around(pred_score, decimals=3)}/10')

if st.button('Get new example'):
    sample_id = np.random.randint(0, high=len(df))

