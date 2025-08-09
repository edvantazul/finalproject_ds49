import streamlit as st
import pickle
import numpy as np

# ===== Load Model =====
with open("LightGBM_Regression_Model.pkl", "rb") as file:
    model = pickle.load(file)

st.set_page_config(page_title="Prediksi Tarif Uber", layout="wide")
st.title("🚖 Prediksi Tarif Uber Menggunakan LightGBM")
st.write("Masukkan detail perjalanan untuk memprediksi tarif.")

# ===== Form Input =====
st.subheader("📍 Lokasi")
col1, col2 = st.columns(2)
with col1:
    pickup_longitude = st.number_input("Pickup Longitude", value=-73.985428)
    dropoff_longitude = st.number_input("Dropoff Longitude", value=-73.985428)
with col2:
    pickup_latitude = st.number_input("Pickup Latitude", value=40.748817)
    dropoff_latitude = st.number_input("Dropoff Latitude", value=40.748817)

st.subheader("🧍 Informasi Penumpang & Waktu")
col3, col4, col5, col6 = st.columns(4)
with col3:
    passenger_count = st.number_input("Jumlah Penumpang", min_value=1, max_value=6, value=1)
with col4:
    year = st.number_input("Tahun", min_value=2009, max_value=2025, value=2015)
with col5:
    month = st.number_input("Bulan", min_value=1, max_value=12, value=6)
with col6:
    day = st.number_input("Tanggal", min_value=1, max_value=31, value=15)

hour = st.number_input("Jam Pickup (0-23)", min_value=0, max_value=23, value=14)
distance = st.number_input("Jarak (km)", min_value=0.0, value=5.0, step=0.1)

st.subheader("🌤 Musim")
pickup_season_spring = st.selectbox("Spring?", ["Tidak", "Ya"])
pickup_season_summer = st.selectbox("Summer?", ["Tidak", "Ya"])
pickup_season_winter = st.selectbox("Winter?", ["Tidak", "Ya"])

st.subheader("🕒 Periode Waktu")
pickup_period_evening = st.selectbox("Evening?", ["Tidak", "Ya"])
pickup_period_morning = st.selectbox("Morning?", ["Tidak", "Ya"])
pickup_period_night = st.selectbox("Night?", ["Tidak", "Ya"])

# ===== Konversi ke format model =====
input_data = np.array([[
    pickup_longitude,
    pickup_latitude,
    dropoff_longitude,
    dropoff_latitude,
    passenger_count,
    year,
    month,
    day,
    hour,
    distance,
    1 if pickup_season_spring == "Ya" else 0,
    1 if pickup_season_summer == "Ya" else 0,
    1 if pickup_season_winter == "Ya" else 0,
    1 if pickup_period_evening == "Ya" else 0,
    1 if pickup_period_morning == "Ya" else 0,
    1 if pickup_period_night == "Ya" else 0
]])

# ===== Prediksi =====
if st.button("Prediksi Tarif"):
    prediction = model.predict(input_data)[0]
    st.success(f"💰 Prediksi Tarif: ${prediction:,.2f}")
