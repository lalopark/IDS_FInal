import streamlit as st
import pandas as pd

def run():
    st.title('Project Motivation')
    st.write("This project stems from our curiosity with how the world's happiness is changing over time. Specifically, \
        we want to analyze further what factors affect a country's happiness and ")

# blurb about the dataset (paragraph)

# df.head (10 rows)
 # present df
    path = 'Data/cleaned_whr.csv'
    df = pd.read_csv(path)
    st.subheader('What the Dataset Looks Like')
    st.write(df.head())

# data types 

# image : michael jackson (include globe image) - heal the world 

# explain what each column means: 
