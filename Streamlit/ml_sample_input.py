import numpy as np
import pandas as pd
import pickle
import streamlit as st
from sklearn.preprocessing import MinMaxScaler
from sklearn import tree
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt

def run():
    with open("Models/tree.pkl", "rb") as f:
        clf_tree = pickle.load(f)

    with open("Models/linreg.pkl", "rb") as f:
        linreg = pickle.load(f)

    st.title("Predicting Happiness with Machine Learning")

    # Read dependecies
    df = pd.read_csv('./Data/cleaned_whr.csv')
    df['year'] = df['year'].astype('int64')
    features = ['year', 'Log GDP per capita',
                'Social support', 'Healthy life expectancy at birth',
                'Freedom to make life choices', 'Generosity',
                'Perceptions of corruption']
    scaler = MinMaxScaler()
    scaler.fit(df[features])

    with open('Models/rf.pkl', 'rb') as f:
        rf = pickle.load(f)

    sample_id = np.random.randint(0, high=len(df))

    # Intro
    st.header('Happiness Score Prediction')
    st.write("We trained three interpretable models on our dataset: Linear Regression, "
             "Decision Tree, and Random Forest. Each of these models are inherently interpretable."
             " Thus, we are able to determine the importance of each feature on our prediction for happiness"
             "for each of the three models")
    st.write("Of all the models we trained, the Random Forest model had the highest R squared value (0.86) and we will now "
             "demonstrate its performance on example data from our training set")

    # pull up the button here
    # add caption: on what you can do with the button
    # all three models and compare

    def get_pred_score(feat_vals):
        scaled_feat = scaler.transform(feat_vals.values.reshape(1, -1))[0]
        scaled_feat = scaled_feat.reshape(1, -1)
        return rf.predict(scaled_feat)[0]

    if st.button('Get new example'):
        sample_id = np.random.randint(0, high=len(df))
    country, year = df['Country name'].iloc[sample_id], df[features[0]].iloc[sample_id]
    st.markdown(f'<h4>{country} in {year} </h4>', unsafe_allow_html=True)

    feat_vals = df[features].iloc[sample_id]
    feat_vals.name = ' '
    score = df['Life Ladder'].iloc[sample_id]

    pred_score = get_pred_score(feat_vals)

    st.table(feat_vals[1:])  # [1:] to avoid year
    st.write(f'Actual Happiness Score: {score}/10')
    st.write(f'Predicted Happiness Score: {np.around(pred_score, decimals=3)}/10')

    st.header("Try it yourself!")

    with st.form(key="test"):
        year = st.select_slider(label="year", options=np.array(np.arange(2005, 2022)))
        gdp = st.slider(label="Log GDP Per Capita", min_value=6.0, max_value=12.0, value=6.0, step=0.1)
        social_support = st.slider(label="Social Support", min_value=0.0, max_value=1.0, value=0.0, step=0.01)
        life_expect = st.slider(label="Life Expectancy", min_value=30.0, max_value=100.0, value=30.0, step=0.5)
        freedom = st.slider(label="Freedom to Make life Choice", min_value=0.0, max_value=1.0, value=0.0, step=0.01)
        generosity = st.slider(label="Genorosity", min_value=-0.4, max_value=1.0, value=-0.4, step=0.01)
        corruption = st.slider(label="Perception of Corruption", min_value=0.0, max_value=1.0, value=0.0, step=0.01)

        X = np.array([year, gdp, social_support, life_expect, freedom, generosity, corruption]).reshape(1, -1)
        X = scaler.transform(X)
        y_hat_rf = str(round(rf.predict(X)[0], 3))
        y_hat_dt = str(round(clf_tree.predict(X)[0], 3))
        y_hat_lr = str(round(linreg.predict(X)[0][0], 3))
        submit_form = st.form_submit_button(label='Try Our model!')
        if submit_form:
            st.success("Random Forest predicted {0}".format(y_hat_rf))
            st.success("Linear Regression predicted {0}".format(y_hat_lr))
            st.success("Decision Tree predicted {0}".format(y_hat_dt))





    dict_1 = {'Freedom to make life choices': 0.03926471494672855,
              'Generosity': .043878197820076,
              'Healthy life expectancy at birth': 0.667677972695485,
              'Log GDP per capita': 0.12226628421571906,
              'Perceptions of corruption': 0.03171853554898575,
              'Social support': 0.07874270842129999,
              'year': 0.01645158635170472}

    with open("Models/feature_importances.pkl", "rb") as f:
        dict_2 = pickle.load(f)

    with open("Models/feature_weights.pkl", "rb") as f:
        dict_3 = pickle.load(f)

    linear_df = pd.DataFrame([dict_2], index=["Linear Regression"]).transpose()
    decision_tree_df = pd.DataFrame([dict_1], index=["Decision Tree"]).transpose()
    random_forest_df = pd.DataFrame([dict_3], index=["Random Forest"]).transpose()

    st.caption("For Linear Regression, we treat the learned coefficients as rough estimates of the feature importance."
               " Also note that features were normalized before training which influence the coefficients that are learned. The R squared"
               " score was 0.7799. The graph on the right demonstrates the relationship between the actual outputs "
               "and the predictions from the model")

    col1, col2 = st.columns(2)
    col1.write(linear_df)
    col2.image("plots/linreg_performance.png")

    st.caption(
        "We also trained a decision tree on the same data with an R squared value of 0.74945. The importance of a feature is "
        "computed as the (normalized) total reduction of the criterion brought by that feature")

    col3, col4 = st.columns(2)
    col3.write(decision_tree_df)
    col4.image("plots/dt_pic.png", width=300)


    st.caption(
        "Finally, our most powerful model was a Random Forest which has its feature importance values calculated in the same"
        " way as a decision tree, but over all trees in the forest")

    col5, col6 = st.columns(2)
    col5.write(random_forest_df)
    col6.image("plots/rf_performance.png")




if __name__ == "__main__":
    run()
