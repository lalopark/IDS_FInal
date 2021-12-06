import numpy as np
import streamlit as st
import pandas as pd
import pydeck as pdk
from pydeck.types import String
import seaborn as sns
# import plotly.figure_factory as ff
import matplotlib.pyplot as plt
import plotly.io as pio
pio.templates.default = "plotly_white" 
import plotly.express as px
import plotly.graph_objects as go
from plotly import figure_factory as ff
import pycountry


def run():
    path = 'cleaned_whr.csv'
    df = pd.read_csv(path)
    # st.set_page_config(layout="wide")

    # present df
    st.subheader('What the Dataset Looks Like')

    st.write(df.head())

    # top 10 bottom 10
    df_2021 = df[df['year']==2021]
    df_2021 = df_2021.sort_values(by=["Life Ladder"], ascending=False)
    topk = botk = 10
    top = df_2021.iloc[:topk]
    bot = df_2021.iloc[-botk:]

    top_desc = top.sort_values(by=['Life Ladder'], ascending=True)
    fig = px.bar(top_desc, y="Country name", x="Life Ladder", orientation='h',color="Life Ladder",color_continuous_scale='RdPu')
    st.subheader('Top 10 Happiest Countries in 2021')
    st.plotly_chart(fig) 

    bot_asc = bot.sort_values(by=['Life Ladder'], ascending=False)
    fig2 = px.bar(bot_asc, y="Country name", x="Life Ladder", orientation='h',color="Life Ladder",color_continuous_scale='PuBu')
    st.subheader('Top 10 Unhappiest Countries in 2021')
    st.plotly_chart(fig2) 

    # score over year
    year_filtered_df = df[df['year'] != 2005]
    avg_happiness = pd.DataFrame(year_filtered_df.groupby(['year'])['Life Ladder'].mean()).reset_index()

    fig3 = px.line(avg_happiness, x="year", y="Life Ladder")
    st.subheader('Average Happiness over time since 2006')
    st.plotly_chart(fig3) 

    # histogram
    fig8 = px.histogram(df_2021, x= 'Life Ladder', nbins = 50)
    fig8.update_layout(bargap=0.2)
    st.subheader('Happiness Score Distribution for 2021')
    st.plotly_chart(fig8) 

    # country map 
    countries = {}
    for country in pycountry.countries:
        countries[country.name] = country.alpha_3

    codes = [countries.get(country, 'Unknown code') for country in df_2021['Country name']]

    df_2021['codes'] = codes

    fig7 = px.choropleth(df_2021, locations="codes",
                        color="Life Ladder", # lifeExp is a column of gapminder
                        hover_name="Country name", # column to add to hover information
                        color_continuous_scale=px.colors.sequential.RdBu_r)
    fig7.update_layout(
        autosize=False,
        margin = dict(
        l=0,
        r=0,
        b=0,
        t=0,
        pad=4,
        autoexpand=True
        ),
        width=1500,
        #     height=400,
    )
    st.subheader('Happiness Score (Life Ladder) in 2021')
    st.plotly_chart(fig7, use_container_width=True) 




    # correlation amongst features: all 
    df_corr = df.drop('year',1).corr().round(2)
    fig4 = ff.create_annotated_heatmap(z=df_corr.to_numpy(), 
                                    x=df_corr.columns.tolist(),
                                    y=df_corr.columns.tolist(),
                                    colorscale=px.colors.sequential.Agsunset,
                                    hoverinfo="none", #Shows hoverinfo for null values
                                    showscale=True, ygap=1, xgap=1
                                    )
    st.subheader('Correlation Matrix Amongst Features')
    st.plotly_chart(fig4) 

    # correlation amongst features: happy 
    top_corr = top.drop('year',1).corr().round(2)
    fig5 = ff.create_annotated_heatmap(z=top_corr.to_numpy(), 
                                    x=top_corr.columns.tolist(),
                                    y=top_corr.columns.tolist(),
                                    colorscale=px.colors.sequential.RdPu,
                                    hoverinfo="none", #Shows hoverinfo for null values
                                    showscale=True, ygap=1, xgap=1
                                    )
    st.subheader('Happiest Countries: Correlation Matrix Amongst Features')
    st.plotly_chart(fig5) 

    # correlation amongst features: unhappy 
    bot_corr = bot.drop('year',1).corr().round(2)
    fig6 = ff.create_annotated_heatmap(z=bot_corr.to_numpy(), 
                                    x=bot_corr.columns.tolist(),
                                    y=bot_corr.columns.tolist(),
                                    colorscale=px.colors.sequential.PuBu,
                                    hoverinfo="none", #Shows hoverinfo for null values
                                    showscale=True, ygap=1, xgap=1
                                    )
    st.subheader('Unhappiest Countries: Correlation Matrix Amongst Features')
    st.plotly_chart(fig6) 

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



    #st.header('Top %d happiest countries'%topk)
    #st.bar_chart(data=top['Life Ladder'], width=0, height=0, use_container_width=True)
    #st.header('Top %d least happiest countries'%botk)
    #st.bar_chart(data=bot['Life Ladder'], width=0, height=0, use_container_width=True)
