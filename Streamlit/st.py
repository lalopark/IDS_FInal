pip install --upgrade pip
import numpy as np
import pandas as pd
import streamlit as st
import altair as alt
import general_viz
import filtered_country
import about
# import writeup
import dev_contact
# import ml_page
import ml_sample_input

st.set_page_config(layout="wide")

PAGES = {
    "About the Project": about,
    "Visualization at a Global Scale": general_viz,
    "Visualization on a Country Level": filtered_country,
    # "Machine Learning": ml_page,
    "Predicting Happiness using ML": ml_sample_input,
    # "Writeup": writeup,
    'Developer Contact': dev_contact
    }

st.sidebar.title('World Happiness Visualized')

selection = st.sidebar.selectbox("Go to", list(PAGES.keys()))
page = PAGES[selection]
page.run()
