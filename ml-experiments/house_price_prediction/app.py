import streamlit as st
import joblib
import numpy as np
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
model = joblib.load(BASE_DIR / "model.pkl")

st.title("House Price Prediction App")
st.divider()
st.write("This app uses ML for house price prediction based on a few house features.")
st.divider()

bedrooms = st.number_input("Number of Bedrooms", min_value=0, value=0, step=1)
bathrooms = st.number_input("Number of Bathrooms", min_value=0, value=0, step=1)
living_area = st.number_input("Living Area (in sqft)", min_value=0, value=2000, step=50)

condition = st.selectbox(
    "Condition of the House",
    options=[0, 1, 2, 3, 4, 5],
    index=3
)

schools_nearby = st.number_input("Number of Schools Nearby", min_value=0, value=0, step=1)

st.divider()

x = np.array([[bedrooms, bathrooms, living_area, condition, schools_nearby]])
predictbutton = st.button("Predict House Price")

if predictbutton:
    st.balloons()
    prediction = model.predict(x)[0]   # plocka ut första värdet
    st.success(f"The predicted house price is ${prediction:,.0f}")
else:
    st.info("Please provide the house features and click on Predict House Price button.")