"""
Train a Linear Regression model using Ames Housing dataset.
Includes preprocessing pipeline for deployment compatibility.
"""

import pandas as pd
import joblib

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, r2_score
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder
from sklearn.pipeline import Pipeline


# -----------------------------
# LOAD DATA
# -----------------------------
df = pd.read_csv("data/AmesHousing.csv")


# -----------------------------
# DROP HIGH MISSING COLUMNS
# -----------------------------
missing_percent = df.isnull().mean() * 100
cols_to_drop = missing_percent[missing_percent > 80].index
df.drop(columns=cols_to_drop, inplace=True)


# -----------------------------
# SPLIT FEATURES & TARGET
# -----------------------------
X = df.drop("SalePrice", axis=1)
y = df["SalePrice"]


# -----------------------------
# IDENTIFY COLUMN TYPES
# -----------------------------
num_cols = X.select_dtypes(include=["int64", "float64"]).columns
cat_cols = X.select_dtypes(include=["str"]).columns



# -----------------------------
# TRAIN TEST SPLIT
# -----------------------------
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)


# -----------------------------
# PREPROCESSOR
# -----------------------------
from sklearn.impute import SimpleImputer
from sklearn.pipeline import make_pipeline

num_transformer = make_pipeline(
    SimpleImputer(strategy="median")
)

cat_transformer = make_pipeline(
    SimpleImputer(strategy="constant", fill_value="Missing"),
    OneHotEncoder(handle_unknown="ignore")
)

preprocessor = ColumnTransformer(
    transformers=[
        ("num", num_transformer, num_cols),
        ("cat", cat_transformer, cat_cols),
    ]
)


# -----------------------------
# PIPELINE
# -----------------------------
pipeline = Pipeline(
    steps=[
        ("preprocessor", preprocessor),
        ("model", LinearRegression())
    ]
)


# -----------------------------
# TRAIN MODEL
# -----------------------------
pipeline.fit(X_train, y_train)


# -----------------------------
# EVALUATE MODEL
# -----------------------------
preds = pipeline.predict(X_test)

mae = mean_absolute_error(y_test, preds)
r2 = r2_score(y_test, preds)

print("MAE:", mae)
print("R2:", r2)


# -----------------------------
# SAVE PIPELINE
# -----------------------------
joblib.dump(pipeline, "model/model.pkl")
print("Pipeline saved successfully.")