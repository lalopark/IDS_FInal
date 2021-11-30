import numpy as np
import streamlit as st
import pandas as pd
import pydeck as pdk
from pydeck.types import String
import seaborn as sns
# import plotly.figure_factory as ff
import matplotlib.pyplot as plt

path = 'cleaned_whr.csv'
df = pd.read_csv(path)
st.set_page_config(layout="wide")

# present df
st.header('Table schema')
st.write(df.head())

# top 10 bottom 10
df = df.sort_values(by=["Life Ladder"], ascending=False)
topk = botk = 10
top = df.iloc[:topk]
bot = df.iloc[-botk:]
st.header('Top %d happiest countries'%topk)
st.bar_chart(data=top['Life Ladder'], width=0, height=0, use_container_width=True)
st.header('Top %d least happiest countries'%botk)
st.bar_chart(data=bot['Life Ladder'], width=0, height=0, use_container_width=True)


# score over year
year_filtered_df = df[df['year'] != 2005]
avg_happiness = year_filtered_df.groupby(['year'])['Life Ladder'].mean()
st.header('Average Happiness over time without 2005 data')
st.line_chart(data=avg_happiness, width=0, height=0, use_container_width=True)


# sns.set()
# f, axs = plt.subplots(1, 2, figsize=(15, 8))
# sns.barplot(ax=axs[0], x=bot['Life Ladder'], y=bot['Country name'], color='red')
# sns.barplot(ax=axs[1], x=top['Life Ladder'], y=top['Country name'], color='blue')
# axs[0].set_xlabel('Life Ladder')
# axs[1].set_xlabel('Life Ladder')
# axs[0].set_ylabel('Countries')
# axs[1].set_ylabel('Countries')
# axs[0].set_title("Top 10 Least Happiest Countries")
# axs[1].set_title("Top 10 Happiest Countries")
# # f.tight_layout()
# st.pyplot(f)
#


