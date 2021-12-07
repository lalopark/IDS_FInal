import streamlit as st
import pandas as pd
from PIL import Image

def run():
    st.title('Project Motivation')
    # image : michael jackson (include globe image) - heal the world
    image = Image.open('plots/image.jpeg')
    st.image(image, caption='https://www.mjvibe.com/people-around-the-world-turns-to-michael-jacksons-music-to-comfort-each-other/')

    st.write("This project stems from our curiosity with how the world's happiness has been changing over time. Specifically, \
         which qualitative and quantitative features contribute the most to a citizen's self-identified level of happiness.")


# blurb about the dataset (paragraph)
    st.write(
        "We used the World Happiness Report 2021 dataset (https://www.kaggle.com/ajaypalsinghlo/world-happiness-report-2021?select=world-happiness-report.csv), "
        "which surveyed the state of happiness in the world accross years and scores of other factors that will affect happiness in a country."
    )

# df.head (10 rows)
 # present df
    path = 'Data/cleaned_whr.csv'
    df = pd.read_csv(path)
    # df['Country name'] = df['Country name'].astype(str)
    # df['year'] = df['year'].astype(int)
    # df.iloc[:,2:] = df.iloc[:,2:].astype(float)

    st.subheader('What the Dataset Looks Like')
    st.write(df.head())

# data types
    st.subheader('The metadata of this dataset is')
    des = ['country name', 'year of collection', "happiness score or subjective well-being, which is measured by the national average response to the question of life evaluations. The English wording of the question is “Please imagine a ladder, with steps numbered from 0 at the bottom to 10 at the top. The top of the ladder represents the best possible life for you and the bottom of the ladder represents the worst possible life for you. On which step of the ladder would you say you personally feel you stand at this time?”",
    'a country\'s economic output per person and is calculated by dividing the GDP of a country by its population',
    'the national average of the binary responses (either 0 or 1) to the GWP question “If you were in trouble, do you have relatives or friends you can count on to help you whenever you need them, or not?” ',
    'healthy life expectancies at birth',
    'the national average of responses to the GWP question “Are you satisfied or dissatisfied with your freedom to choose what you do with your life?” ',
    'the residual of regressing national average of response to the GWP question “Have you donated money to a charity in the past month?” on GDP per capita',
    'the national average of the survey responses to two questions in the GWP: “Is corruption widespread throughout the government or not” and “Is corruption widespread within businesses or not?” ']
    names = list(df.columns)
    dttypes = ["str", "int", "float", "float", "float", "float","float", "float",'float']
    # print(df.describe())

    col_info = pd.DataFrame({'Name':names,
        'Data Types':dttypes,
        'Description': des
                             }).astype(str)
    st.table(col_info)

    st.subheader('Our Story')
    st.write("The main research question we were motivated to investigate was which factors contribute to a nation's happiness. Aside from more objective statistics such as log GDP per capita and healthy life expectancy at birth, the World Happiness Report surveys the citizens of their self-reported level of corruption, generosity, freedom to make life choices, and social support present in their country or culture. We examined these various demographic features’ correlation with each nation’s yearly happiness score (“life ladder” score in the report) and visualized the temporal trends for each country with a focus on those with a life ladder score of 0.6 and higher versus lower, to assess the self-perceived importance of feature in determining how happy a country is and whether there’s a temporal/casual relationship that can be potentially extrapolated.\n\nFrom our analysis, we observe that the level of correlation varies significantly across countries as shown in the correlation matrices. The strength of correlation varies based on the country’s reported happiness score, as the top 10 to 30 happiest countries showed a strong correlation between freedom and social support with happiness, while the bottom 10 to 30 happiest countries’ correlation map displayed higher values for GDP and corruption. We included an interactive scaling feature that allows the user to freely choose a country and plot the temporal trends across the past 15 years to assess on their own. We also employed several supervised machine learning practices to quantify the impact that each factor has on a country's happiness and included an another interactive feature where the user can input their own nation (or even an imagined nation)’s values to output our predicted happiness score. When observing the weights of the different models, we can see that the linear regression model places a higher importance on log GDP per capita and social support, while the decision tree prioritizes healthy life expectancy at 0.667. From both visualizations and modeling, we observe further the ambiguity of the correlations between the features and happiness as all of our models place different importances on the features, hence we invite all website visitors to freely explore, investigate, and reach out their own hypotheses to our emails as listed in the Developer Contact section.")
# explain what each column means:
