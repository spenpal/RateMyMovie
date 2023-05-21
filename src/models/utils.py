import pickle
from itertools import cycle

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from category_encoders.cat_boost import CatBoostEncoder
from sklearn.ensemble import GradientBoostingClassifier, RandomForestClassifier
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_selection import SelectFromModel, SelectKBest, chi2
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    RocCurveDisplay,
    accuracy_score,
    auc,
    classification_report,
    confusion_matrix,
    mean_squared_error,
    r2_score,
    roc_curve,
)
from sklearn.model_selection import (
    GridSearchCV,
    KFold,
    RandomizedSearchCV,
    RepeatedStratifiedKFold,
    StratifiedKFold,
    cross_val_score,
    train_test_split,
)
from sklearn.multiclass import OneVsRestClassifier
from sklearn.naive_bayes import CategoricalNB, GaussianNB, MultinomialNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn.preprocessing import (
    LabelBinarizer,
    LabelEncoder,
    OneHotEncoder,
    StandardScaler,
    label_binarize,
)
from sklearn.tree import DecisionTreeClassifier


def rating_encoding(rating_col, bin_num=3):
    # Convert rating into a classification problem
    bin_edges = np.linspace(
        start=0, stop=10, num=bin_num + 1
    )  # Create evenly spaced bins between 0 and 10
    bin_labels = list(range(bin_num))

    # Create a new column 'rating_class' that contains the bin labels
    rating_col = pd.cut(rating_col, bins=bin_edges, labels=bin_labels)
    rating_col = pd.to_numeric(rating_col, downcast="integer")
    return rating_col


def count_encoding(df, rating_bin_num=3):
    pass


def catboost_encoding(*splits):
    X_train, X_test, y_train, y_test = splits

    cat_cols = X_train.select_dtypes(include=["category", "object"]).columns.tolist()

    cbe = CatBoostEncoder()
    train = X_train[cat_cols]
    cbe.fit(train, y_train)
    X_train[cat_cols] = cbe.transform(train)

    cbe = CatBoostEncoder()
    train = X_test[cat_cols]
    cbe.fit(train, y_test)
    X_test[cat_cols] = cbe.transform(train)

    return X_train, X_test
