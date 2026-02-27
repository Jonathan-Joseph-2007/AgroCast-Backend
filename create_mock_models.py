import joblib
from sklearn.linear_model import LinearRegression
import numpy as np
import os

def create_mock_models():
    print("Creating mock models for testing pipeline...")

    # 1. Mock Environmental Model
    # Predicts AQI based on temp, humidity, precip
    env_model = LinearRegression()
    # Dummy data
    X_env = np.array([[30, 60, 0], [20, 40, 5], [35, 80, 0]])
    y_env = np.array([120, 50, 150]) # Mock AQI values
    env_model.fit(X_env, y_env)

    # 2. Mock Price Model
    # Predicts price gap based on forecasted AQI and live market price
    price_model = LinearRegression()
    # Dummy data 
    X_price = np.array([[100, 2000], [50, 2100], [150, 1900]])
    y_price = np.array([2100, 2150, 1800]) # Mock predicted prices
    price_model.fit(X_price, y_price)

    # Save models
    joblib.dump(env_model, "environmental_model.pkl")
    joblib.dump(price_model, "price_model.pkl")
    
    print("Successfully created environmental_model.pkl and price_model.pkl")

if __name__ == "__main__":
    create_mock_models()
