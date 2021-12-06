import numpy as np
import pandas as pd
import pickle
import streamlit as st
from sklearn.preprocessing import MinMaxScaler


def run():
    # Read dependecies
    df = pd.read_csv('./Data/cleaned_whr.csv')
    df['year'] = df['year'].astype('int64')
    features = ['year', 'Log GDP per capita',
           'Social support', 'Healthy life expectancy at birth',
           'Freedom to make life choices', 'Generosity',
           'Perceptions of corruption']
    scaler = MinMaxScaler()
    scaler.fit(df[features])

    with open('Models/rf.pkl', 'rb') as f:
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


    with st.form(key="test"):
        year = st.select_slider(label="year", options=np.array(np.arange(2005, 2022)))
        gdp = st.slider(label="Log GDP Per Capita", min_value=6.0, max_value=12.0, value=6.0, step=0.1)
        social_support = st.slider(label="Social Support", min_value=0.0, max_value=1.0, value=0.0, step=0.01)
        life_expect = st.slider(label="Life Expectancy", min_value=30.0, max_value=100.0, value=30.0, step=0.5)
        freedom = st.slider(label="Freedom to Make life Choice", min_value=0.0, max_value=1.0, value=0.0, step=0.01)
        generosity = st.slider(label="Genorosity", min_value=-0.4, max_value=1.0, value=-0.4, step=0.01)
        corruption = st.slider(label="Perception of Corruption", min_value=0.0, max_value=1.0, value=0.0, step=0.01)

        X = np.array([year, gdp, social_support, life_expect, freedom, generosity, corruption]).reshape(1, -1)
        X = scaler.transform(X)
        y_hat = round(rf.predict(X)[0], 3)

        submit_form = st.form_submit_button(label='Try Our model!')
        if submit_form:
            y_hat = str(y_hat)
            st.success("Random Forest Predicted {0} for Life Happiness".format(y_hat))


if __name__ == "__main__":
    run()
















