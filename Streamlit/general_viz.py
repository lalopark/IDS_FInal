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
import altair as alt
import pycountry


def run():

    st.header('Visualization at a Global Scale')
    # CHANGE THIS TITLE 

    # make axis > SEE IF IT LOOKS GOOD. 

    # add a aparaph or two after each plot

    path = 'Data/cleaned_whr.csv'
    df = pd.read_csv(path)
    # st.set_page_config(layout="wide")

    # st.markdown("#### **Select Year:**")

    min_year = df['year'].min()
    max_year = df['year'].max()
    year = st.slider("Select a year to investigate (hover over each dot to see which country it is)! ", min_year, max_year, value=max_year)

    year_filtered = df[df["year"] == year]

    features = ['Log GDP per capita', 'Social support', 'Healthy life expectancy at birth', 'Freedom to make life choices', 'Generosity', 'Perceptions of corruption']
    x_feature = st.selectbox("Select a feature to plot on the x axis", features, index=0)
    y_feature = st.selectbox("Select a feature to plot on the y axis", features, index=1)

    fig = alt.Chart(year_filtered).mark_circle(size=60).encode(
        x=x_feature,
        y=y_feature,
        color='Life Ladder',
        tooltip=['Country name', 'Life Ladder'] + features
        ).interactive()

    st.altair_chart(fig, use_container_width=True)

    # top 10 bottom 10
    df_2021 = df[df['year']==year]
    df_2021 = df_2021.sort_values(by=["Life Ladder"], ascending=False)
    topk = botk = 10
    top = df_2021.iloc[:topk]
    bot = df_2021.iloc[-botk:]

    top_desc = top.sort_values(by=['Life Ladder'], ascending=True)
    fig = px.bar(top_desc, y="Country name", x="Life Ladder", orientation='h',color="Life Ladder",color_continuous_scale='RdPu')
    st.subheader(f'Top 10 Happiest Countries in {year}')
    st.plotly_chart(fig, use_container_width=True) 

    bot_asc = bot.sort_values(by=['Life Ladder'], ascending=False)
    fig2 = px.bar(bot_asc, y="Country name", x="Life Ladder", orientation='h',color="Life Ladder",color_continuous_scale='PuBu')
    st.subheader(f'Top 10 Unhappiest Countries in {year}')
    st.plotly_chart(fig2, use_container_width=True)

    st.write("In the following two graphs, we look at the top 10 happiest and unhappiest countries. We can see roughly that many of the happiest countries are located in Europe, while many of the unhappy countries are developing.")

    # score over year
    # BEN: create a year slider (2005 - 2021) 
     
    # include 2005 

    year_filtered_df = df[df['year'] != 2005]
    avg_happiness = pd.DataFrame(year_filtered_df.groupby(['year'])['Life Ladder'].mean()).reset_index()

    fig3 = px.line(avg_happiness, x="year", y="Life Ladder")
    st.subheader('Average Life Ladder Score over time since 2006')
    st.plotly_chart(fig3, use_container_width=True)
    
    st.write("If we look at all the countries as a whole, we can track how overall global happiness has changed over time. We observe that the global population happiness increases from 2005-2010, after which it levels fairly off. Moreover, there is a spike in happiness score in 2020, which is interesting because it was at the time of the pandemic. After the spike, the happiness begins to normalize back again.")


    # histogram
    st.subheader("Select a year to see the histogram distribution for:")

    min_year = df['year'].min()
    max_year = df['year'].max()
    year_hist = st.slider("Year", min_year, max_year, value=max_year, key="hist")

    year_filtered = df[df["year"] == year_hist]

    fig8 = px.histogram(year_filtered, x= 'Life Ladder', nbins = 50)
    fig8.update_layout(bargap=0.2)
    st.subheader(f'Life Ladder Score Distribution for {year_hist}')
    st.plotly_chart(fig8, use_container_width=True) 

    st.write("We can also look at the distribution of happiness across all countries over time. Roughly speaking, as time goes on, the distribution converges closer to a Gaussian distribution, with the mean gradually moving to the right.")

    # country map 
    st.subheader("Select a year to visualize the map of:")

    min_year = df['year'].min()
    max_year = df['year'].max()
    year_map = st.slider("Year", min_year, max_year, value=max_year, key="map")

    year_filtered = df[df["year"] == year_map]

    countries = {}
    for country in pycountry.countries:
        countries[country.name] = country.alpha_3

    # codes = [countries.get(country, 'Unknown code') for country in df_2021['Country name']]
    codes = [countries.get(country, 'Unknown code') for country in year_filtered['Country name']]

    year_filtered['codes'] = codes
    # df_2021['codes'] = codes

    fig7 = px.choropleth(year_filtered, locations="codes",
                        color="Life Ladder", # lifeExp is a column of gapminder
                        hover_name="Country name", # column to add to hover information
                        color_continuous_scale="Sunset")
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
    st.subheader(f'Life Ladder Score in {year_map}')
    st.plotly_chart(fig7, use_container_width=True) 

    st.write("Next, we can look at the happiness scores overlaid on a world map. An interesting thing to note here is that we begin collecting more and more data on more countries over time, as other countries participate in the survey. We can see again that the countries reporting lower values of happiness are located predominantly in Africa and in the Middle East while counties reporting higher values of happiness are located mostly in Europe, especially Scandinavia")

    # correlation amongst features: all 
    # make color schemes consistent (light vs dark)

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

    st.write("As you will see later on in the presentation, we will build ML models to predict happiness using the features below. Before using our data, we first examine the individual correlations between each of the features and Life Ladder (Happiness) as well as the correlations between the features. We can see that Life Ladder is surprisingly not very correlated with generosity, while the Log-GDP is quite correlated with Life Ladder. Additionally, as expected, as Log GDP increases, many other factors increase as well. Finally, it was surprising to note that freedom to make life choices is not very correlated with Life Happiness.")

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

    st.write("We can perform the same analysis for just the top 10 happiest countries and see that there are some interesting differences. Specifically, the Log-GDP then has a -0.2 Pearson correlation, supporting the claim that increases in money may increase happiness for countries but only up to a certain point.")

    # social support, freedom
    
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

    st.write("Looking only at the unhappiest countries, we see another interesting relationship: social support is positively correlated with perceptions of corruption. Additionally, Log-GDP remains fairly uncorrelated with Life Ladder in the unhappy country case.")
