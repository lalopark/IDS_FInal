import numpy as np
import pandas as pd
import streamlit as st
import altair as alt
import general_viz
import filtered_country
import about
import writeup
import dev_contact
import ml_page
import ml_sample_input

PAGES = {
    "About the Project": about,
    "General Visualization": general_viz,
    "Filtered Country Happiness": filtered_country,
    "Machine Learning": ml_page,
    "Machine Learning Survey": ml_sample_input,
    "Writeup": writeup,
    'Developer Contact': dev_contact
    }
st.set_page_config(layout="wide")
st.sidebar.title('World Happiness Visualized')

selection = st.sidebar.selectbox("Go to", list(PAGES.keys()))
page = PAGES[selection]
page.run()