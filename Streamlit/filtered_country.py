import numpy as np
import pandas as pd
import streamlit as st
import altair as alt
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt
from plotly.subplots import make_subplots
import plotly.graph_objects as go

def run():
    st.title("Visualization at a Global Scale")

    cleaned_whr = pd.read_csv('Data/cleaned_whr.csv')

    happy_list = ['Finland', 'Denmark','Switzerland','Iceland','Netherlands','Norway','Sweden','Luxembourg','New Zealand','Austria']
    unhappy_list = ['Burundi','Yemen','Tanzania','Haiti','Malawi','Lesotho','Botswana','Rwanda','Zimbabwe','Afghanistan']

    happy = cleaned_whr.loc[cleaned_whr['Country name'].isin(happy_list)]
    unhappy = cleaned_whr.loc[cleaned_whr['Country name'].isin(unhappy_list)]

    features = ['Freedom to make life choices', 'Generosity', 'Perceptions of corruption', 'Life Ladder', 'Social Support', 'Healthy life expectancy at birth']
    countries = cleaned_whr['Country name'].unique()
    country = st.selectbox("Select a country to analyze", countries)
    feature = st.selectbox("Select a feature to analyze", features)


    """ 
    df_melt = happy.melt(id_vars='Country name', value_vars=feature)
    happy_fig = px.box(df_melt, x="Country name", y='value', title=f'Top 10 Unhappiest Countries: Level of self-reported {feature.lower()} by country')
    st.plotly_chart(happy_fig)

    df_melt = unhappy.melt(id_vars='Country name', value_vars=feature)
    unhappy_fig = px.box(df_melt, x="Country name", y='value', title=f'Top 10 Unhappiest Countries: Level of self-reported {feature.lower()} by country')
    st.plotly_chart(unhappy_fig)
    """ 

    # 1st plot 
    df = cleaned_whr[cleaned_whr['Country name']==country]

    # Create figure with secondary y-axis
    fig = make_subplots(specs=[[{"secondary_y": True}]])

    # Add traces
    fig.add_trace(
        go.Scatter(x=df['year'], y=df[str(feature)], name="Feature"),
        secondary_y=False,
    )

    fig.add_trace(
        go.Scatter(x=df['year'], y=df['Life Ladder'], name="Life Ladder"),
        secondary_y=True,
    )
    
    # Add figure title
    fig.update_layout(
        title_text=f"{country}'s {feature.lower()} and life ladder score over the years") 

    # Set x-axis title
    fig.update_xaxes(title_text="Year")

    # Set y-axes titles
    fig.update_yaxes(title_text="<b>Feature</b>", secondary_y=False)
    fig.update_yaxes(title_text="<b>Life Ladder</b>", secondary_y=True)

    st.plotly_chart(fig)  


    # 2nd plot  
    """ 
    import plotly.express as px
    
    dot = df[df['year'] == 2021]['Life Ladder'] 
    st.write(dot)

    fig2 = px.box(cleaned_whr[cleaned_whr['year']==2021], y="Life Ladder")
    fig2.add_trace(go.Box(y = [df[df['year'] == 2021]['Life Ladder']], 
    name=f"{country}",
    # jitter=0.3,
    #pointpos=-1.8,
    boxpoints='all', # represent all points
    # marker_color='rgb(255,0,0)',
    # line_color='rgb(255,0,255)',

    line=dict(color='rgb(255,0,0)')
))

    st.plotly_chart(fig2) 
    










    # 3rd plot

    st.write('For this analysis, we defined "happy countries" as countries with the life ladder score equal to or greater than 6.')
    happy = cleaned_whr.loc[cleaned_whr['Life Ladder']>= 6]
    unhappy = cleaned_whr.loc[cleaned_whr['Life Ladder']< 6]
    happy = happy.rename(columns={feature:f'Happy Countries'})
    unhappy = unhappy.rename(columns={feature:f'Unhappy Countries'})
    concat = pd.concat([happy, unhappy])
    concat = concat[[f'Happy Countries', f'Unhappy Countries']]
    concat = concat.melt(
            var_name="Category", 
            value_name=feature)

    box = px.box(concat, x="Category", y=feature, title=f"{feature} Distribution")
    st.plotly_chart(box)

     

    st.markdown("#### **Select Year:**")

    min_year = cleaned_whr['year'].min()
    max_year = cleaned_whr['year'].max()
    year = st.slider("Year", min_year, max_year, value=max_year)

    year_filtered = cleaned_whr[cleaned_whr["year"] == year]

    features = ['Log GDP per capita', 'Social support', 'Healthy life expectancy at birth', 'Freedom to make life choices', 'Generosity', 'Perceptions of corruption']
    x_feature = st.selectbox("Select a feature for the x axis", features, index=0)
    y_feature = st.selectbox("Select a feature for the y axis", features, index=1)

    fig = alt.Chart(year_filtered).mark_circle(size=60).encode(
        x=x_feature,
        y=y_feature,
        color='Life Ladder',
        tooltip=['Country name', 'Life Ladder'] + features
        ).interactive()

    st.altair_chart(fig, use_container_width=True)


#     st.write(x_feature, y_feature)

#     countries = cleaned_whr.groupby('Country name')['Country name'].count().index

#     st.markdown("#### **Select Country:**")
#     selected_country = []
#     selected_country.append(st.selectbox("Select a country to analyze", countries))
#     country_filtered = cleaned_whr[cleaned_whr["Country name"].isin(selected_country)]

#     min_year = country_filtered['year'].min()
#     max_year = country_filtered['year'].max()
#     year = st.slider("Year", min_year, max_year, value=min_year)

#     st.markdown("#### **Select Year:**")
#     year_filtered = country_filtered[country_filtered["year"] == year]

#     st.write(year_filtered)
""" 