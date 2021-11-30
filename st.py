import numpy as np
import pandas as pd
import streamlit as st
import altair as alt
import global_happiness
import filtered_country
import about
import writeup
import dev_contact

PAGES = {
    "About the Project": about,
    "Global Happiness": global_happiness,
    "Specific Country Happiness": filtered_country,
    # "Machine Learning Results": test2,
    "Writeup": writeup,
    'Developer Contact': dev_contact
    }

cleaned_whr = pd.read_csv('cleaned_whr.csv')
st.sidebar.title('World Happiness Visualized')

selection = st.sidebar.selectbox("Go to", list(PAGES.keys()))
page = PAGES[selection]
page.run()