import streamlit as st
import pandas as pd
import pickle


def run():
    st.title("Predicting Happiness with Machine Learning")

    st.subheader("We trained three interpretable models on our dataset, a Linear Regressor, "
                 "a Decision Tree, and a Random Forest. Since these models are interpetable,"
                 "we are able to see what the most important features are for Happiness")

    # sentence edit
    # make font size consistent 
    # draw plots for each

    

    dict_1 = {'Freedom to make life choices': 0.03926471494672855,
     'Generosity': .043878197820076,
     'Healthy life expectancy at birth': 0.667677972695485,
     'Log GDP per capita' : 0.12226628421571906,
     'Perceptions of corruption' : 0.03171853554898575,
     'Social support' : 0.07874270842129999,
     'year' : 0.01645158635170472}


    with open("Models/feature_importances.pkl", "rb") as f:
        dict_2 = pickle.load(f)

    with open("Models/feature_weights.pkl", "rb") as f:
        dict_3 = pickle.load(f)

    linear_df = pd.DataFrame([dict_2], index=["Linear Regression"]).transpose()
    decision_tree_df = pd.DataFrame([dict_1], index=["Decision Tree"]).transpose()
    random_forest_df = pd.DataFrame([dict_3], index=["Random Forest"]).transpose()

    st.caption("For Linear Regression, we treat the learned coefficients as rough estimates of the feature importance."
               " Also note that features were normalized before training which influence the coefficients that are learned. The R squared"
               " score was 0.7799")
    st.write(linear_df)


    st.caption("We also trained a decision tree on the same data with an R squared value of 0.74945. The importance of a feature is "
               "computed as the (normalized) total reduction of the criterion brought by that feature")

    st.write(decision_tree_df)

    st.caption(
        "Finally, our most powerful model was a Random Forest which has its feature importance values calculated in the same"
        " way as a decision tree, but over all trees in the forest")

    st.write(random_forest_df)

if __name__ == "__main__":
    run()
