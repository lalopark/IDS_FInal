import pandas as pd
import numpy as np
from sklearn import tree
from sklearn.model_selection import train_test_split


DATA = pd.read_csv("Data/cleaned_whr.csv")

def train_decision(df):
    clf = tree.DecisionTreeRegressor(random_state=0)
    # need to examine the data
    y = df["Life Ladder"].values
    X = df.drop(labels=["Life Ladder", "Country name"], axis=1)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.20, random_state=0)
    clf.fit(X_train, y_train)

    f_names = X.columns.values
    feature_importances = {(f_name, clf.feature_importances_[idx])for idx, f_name in enumerate(f_names)}
    return clf.score(X_test, y_test), feature_importances

if __name__ == "__main__":
    train_decision(DATA)