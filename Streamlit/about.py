import streamlit as st
import pandas as pd
from PIL import Image

def run():
    st.title('Project Motivation')
    # image : michael jackson (include globe image) - heal the world
    image = Image.open('plots/image.jpeg')
    st.image(image, caption='https://www.mjvibe.com/people-around-the-world-turns-to-michael-jacksons-music-to-comfort-each-other/')

    st.write("This project stems from our curiosity with how the world's happiness has been changing over time. Specifically, \
        we want to see how happiness has changed over time and which qualitative and quantitative features contribute the most to a citizen's self-identified level of happiness.")


# blurb about the dataset (paragraph)
    st.write(
        "We used the World Happiness Report 2021 dataset, "
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
    des = ['country name', 'year of collection', "happiness score or subjective well-being, which is measured by the national average response to the question of life evaluations. The English wording of the question is “Please imagine a ladder, with steps numbered from 0 at the bottom to 10 at the top. The top of the ladder represents the best possible life for you and the bottom of the ladder represents the worst possible life for you. On which step of the ladder would you say you personally feel you stand at this time?",
    'a country\'s economic output per person and is calculated by dividing the GDP of a country by its population.',
    'the national average of the binary responses (either 0 or 1) to the GWP question “If you were in trouble, do you have relatives or friends you can count on to help you whenever you need them, or not?” ',
    'healthy life expectancies at birth',
    'the national average of responses to the GWP question “Are you satisfied or dissatisfied with your freedom to choose what you do with your life?” ',
    'the residual of regressing national average of response to the GWP question “Have you donated money to a charity in the past month?” on GDP per capita.',
    'the national average of the survey responses to two questions in the GWP: “Is corruption widespread throughout the government or not” and “Is corruption widespread within businesses or not?” ']
    names = list(df.columns)
    dttypes = ["str", "int", "float", "float", "float", "float","float", "float",'float']
    # print(df.describe())

    col_info = pd.DataFrame({'Name':names,
        'Data Types':dttypes,
        'Description': des
                             }).astype(str)
    st.table(col_info)






# explain what each column means:
