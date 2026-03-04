"""
FastAPI service to serve house price predictions.
Loads trained preprocessing + model pipeline.
"""

from fastapi import FastAPI
from pydantic import BaseModel
import joblib
import pandas as pd
from fastapi.middleware.cors import CORSMiddleware



# -----------------------------
# LOAD PIPELINE
# -----------------------------
pipeline = joblib.load("model/model.pkl")

# Get the exact column names the model was trained on
trained_columns = pipeline.named_steps["preprocessor"].feature_names_in_


# -----------------------------
# FASTAPI INIT
# -----------------------------
app = FastAPI(title="House Price Prediction API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


# -----------------------------
# INPUT SCHEMA
# -----------------------------
class HouseInput(BaseModel):
    data: dict


# -----------------------------
# ROOT ENDPOINT
# -----------------------------
@app.get("/")
def home():
    return {"message": "House Price Prediction API is running"}


# -----------------------------
# PREDICTION ENDPOINT
# -----------------------------
@app.post("/predict")
def predict(input_data: HouseInput):

    # Convert input dict to DataFrame
    df = pd.DataFrame([input_data.data])

    # Add any missing columns with NaN (pipeline will handle them)
    for col in trained_columns:
        if col not in df.columns:
            df[col] = None

    # Ensure column order matches training
    df = df[trained_columns]

    # Generate prediction
    prediction = pipeline.predict(df)[0]

    return {"predicted_price": float(prediction)}