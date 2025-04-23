import streamlit as st
import numpy as np

st.set_page_config(page_title="Smart Ideal Weight Calculator", layout="centered")
st.title("⚖️ Smart Ideal Weight Calculator")
st.markdown("""
This tool estimates your **ideal weight range** using advanced health metrics — far beyond BMI.
""")

# --- User Inputs ---
col1, col2 = st.columns(2)

with col1:
    gender = st.selectbox("Gender", ["Male", "Female"])
    age = st.number_input("Age", min_value=10, max_value=100, value=25)
    height = st.number_input("Height (cm)", min_value=100, max_value=250, value=170)
    weight = st.number_input("Current Weight (kg)", min_value=30.0, max_value=200.0, value=70.0)

with col2:
    waist = st.number_input("Waist Circumference (cm)", min_value=40.0, max_value=200.0, value=80.0)
    hip = st.number_input("Hip Circumference (cm)", min_value=40.0, max_value=200.0, value=95.0)
    activity_level = st.selectbox("Activity Level", ["Sedentary", "Light", "Moderate", "Active"])
    body_type = st.selectbox("Body Type (optional)", ["Ectomorph", "Mesomorph", "Endomorph"])


# --- Calculation ---
def calculate_ideal_weight(age, gender, height, weight, waist, hip, activity_level):
    h_m = height / 100
    bmi_min = 18.5
    bmi_max = 24.9

    # Age factor
    if age > 50:
        bmi_min += 1.0
        bmi_max += 1.0

    # Gender factor
    gender_factor = 0.9 if gender.lower() == 'female' else 1.0

    # WHR
    whr = waist / hip
    if gender.lower() == "male" and whr > 0.9:
        bmi_max -= 1
    elif gender.lower() == "female" and whr > 0.85:
        bmi_max -= 1

    # Activity factor
    activity_factors = {
        "sedentary": -1.0,
        "light": 0.0,
        "moderate": 1.0,
        "active": 2.0
    }
    bmi_max += activity_factors.get(activity_level.lower(), 0)

    ideal_min = round(bmi_min * h_m**2 * gender_factor, 1)
    ideal_max = round(bmi_max * h_m**2 * gender_factor, 1)
    return ideal_min, ideal_max, whr

# --- Output ---
if st.button("Calculate Ideal Weight"):
    ideal_min, ideal_max, whr = calculate_ideal_weight(
        age, gender, height, weight, waist, hip, activity_level
    )

    st.success(f"✅ Your estimated ideal weight range is: **{ideal_min} kg – {ideal_max} kg**")

    st.markdown("---")
    st.markdown(f"**Waist-to-Hip Ratio (WHR):** `{whr:.2f}`")
    if (gender == "Male" and whr > 0.9) or (gender == "Female" and whr > 0.85):
        st.warning("Your WHR indicates central fat concentration. Consider fat loss strategies.")
    else:
        st.info("Your WHR is within a healthy range.")

    delta = weight - ((ideal_min + ideal_max) / 2)
    if delta > 3:
        st.markdown(f"You are approximately `{delta:.1f} kg` above the midpoint. 💡 Try light cardio and calorie control.")
    elif delta < -3:
        st.markdown(f"You are approximately `{abs(delta):.1f} kg` below the midpoint. 💡 Consider healthy weight gain.")
    else:
        st.markdown("✅ You're near your ideal weight! Keep up the good work.")
