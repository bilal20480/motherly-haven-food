import streamlit as st
import google.generativeai as genai
from io import BytesIO
from fpdf import FPDF
import os
import base64

# ✅ Must be the first Streamlit command
st.set_page_config(page_title="Diet Planner", layout="wide")

# Load background image and convert to base64
def get_base64_image():
    for ext in ["webp", "jpg", "jpeg", "png"]:
        image_path = f"bg.{ext}"
        if os.path.exists(image_path):
            with open(image_path, "rb") as img_file:
                return base64.b64encode(img_file.read()).decode()
    return None

bg_img = get_base64_image()

# Inject custom background CSS
if bg_img:
    st.markdown(f"""
        <style>
        .stApp {{
            background: linear-gradient(rgba(255, 255, 255, 0.35), rgba(255, 255, 255, 0.85)),
                        url("data:image/png;base64,{bg_img}");
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
            background-attachment: fixed;
        }}
        .block-container {{
            background-color: rgba(255, 248, 243, 0.45);
            padding: 2rem 3rem;
            border-radius: 18px;
            margin-top: 2rem;
            box-shadow: 0 4px 12px rgba(0,0,0,0.1);
        }}
        h1, h2, h3, h4, h5, h6 {{
            color: #4B4B4B;
            font-family: 'Segoe UI', sans-serif;
        }}
        .export-buttons {{
            margin-top: 20px;
        }}
        </style>
    """, unsafe_allow_html=True)

# ✅ Configure Gemini API
genai.configure(api_key="AIzaSyC9jEg8Icw6kMPs0tdncQKUCGtdeI_xINo")  # Replace with your actual Gemini API key

# ✅ Initialize Gemini model
model = genai.GenerativeModel("gemini-2.0-flash")

st.title("🤱 Personalized Diet Planner for Women")

# ✅ Helper function to convert text to PDF
def create_pdf_from_text(text):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.set_font("Arial", size=12)
    for line in text.split('\n'):
        pdf.multi_cell(0, 10, line)
    pdf_bytes = pdf.output(dest='S').encode('latin1')
    return BytesIO(pdf_bytes)

# Phase selection
phase = st.sidebar.radio("Select your stage:", ["Pregnancy", "Postpartum"])

# -------------------- Pregnancy --------------------
if phase == "Pregnancy":
    st.sidebar.header("🤰 Pregnancy Information")
    allergies = st.sidebar.text_input("Food allergies (if any)")
    diet_type = st.sidebar.selectbox("Dietary preference", ["Vegetarian", "Non-vegetarian", "Eggetarian", "Vegan"])
    intolerances = st.sidebar.text_input("Food intolerances (gluten, dairy, etc.)")
    trimester = st.sidebar.selectbox("Current trimester", ["1", "2", "3"])
    weight_before = st.sidebar.text_input("Weight before pregnancy (kg)")
    current_weight = st.sidebar.text_input("Current weight (kg)")
    activity_level = st.sidebar.selectbox("Activity level", ["Sedentary", "Light", "Moderate", "Active"])
    water_intake = st.sidebar.slider("Water intake (glasses/day)", 0, 20, 8)
    goal = st.sidebar.text_input("Primary goal (e.g., healthy baby, energy boost, etc.)")

    if st.sidebar.button("Generate Diet Plan"):
        prompt = f"""
        Create a weekly pregnancy diet plan in a clean table format.
        Each day should have:
        - Breakfast
        - Lunch
        - Dinner
        - Optional Snack
        - Nutritional Benefit (per meal or overall)
        - Mother's Benefit (what it helps the woman with: e.g. energy, iron, digestion, etc.)

        Remove Morning and Evening Snacks. Use Indian-style meals and explain in short.

        Context:
        Allergies: {allergies}
        Diet type: {diet_type}
        Intolerances: {intolerances}
        Trimester: {trimester}
        Weight before: {weight_before}, Current weight: {current_weight}
        Activity level: {activity_level}
        Water intake: {water_intake} glasses/day
        Goal: {goal}

        Format the output in a clean table with 7 rows (Mon-Sun) and columns:
        Day, Breakfast, Lunch, Dinner, Optional Snack, Nutritional Benefit, Mother's Benefit
        """
        response = model.generate_content(prompt)
        st.subheader("📝 Your Pregnancy Diet Plan (Weekly)")
        st.markdown(response.text, unsafe_allow_html=True)

        pdf_data = create_pdf_from_text(response.text)
        st.download_button(label="📥 Download as PDF", data=pdf_data, file_name="pregnancy_diet_plan.pdf", mime="application/pdf")

# -------------------- Postpartum --------------------
elif phase == "Postpartum":
    st.sidebar.header("🤱 Postpartum Information")
    delivery_type = st.sidebar.selectbox("Delivery type", ["Normal", "C-Section", "Assisted"])
    breastfeeding = st.sidebar.selectbox("Breastfeeding status", ["Exclusive", "Partial", "Formula-fed"])
    milk_supply = st.sidebar.selectbox("Milk supply", ["Low", "Normal", "Over-supply"])
    diet_type = st.sidebar.selectbox("Dietary preference", ["Vegetarian", "Non-vegetarian", "Eggetarian", "Vegan"])
    digestion_issues = st.sidebar.text_input("Digestive issues (gas, bloating, etc.)")
    energy = st.sidebar.selectbox("Energy level", ["Low", "Normal", "High"])
    water = st.sidebar.slider("Water intake (glasses/day)", 0, 20, 8)
    goal = st.sidebar.text_input("Primary goal (e.g., healing, weight loss, boost milk, etc.)")

    if st.sidebar.button("Generate Diet Plan"):
        prompt = f"""
        Create a weekly postpartum diet plan in a structured table.
        Each day should have:
        - Breakfast
        - Lunch
        - Dinner
        - Optional Snack
        - Nutritional Benefit (overall)
        - Mother's Benefit (e.g. improves milk supply, healing, recovery, mood, energy, etc.)

        Do not include Morning/Evening snacks separately.
        Use Indian-style practical dishes, short wording.

        Context:
        Delivery type: {delivery_type}
        Breastfeeding: {breastfeeding}
        Milk supply: {milk_supply}
        Diet type: {diet_type}
        Digestive issues: {digestion_issues}
        Energy: {energy}
        Water intake: {water} glasses/day
        Goal: {goal}

        Table Columns: Day, Breakfast, Lunch, Dinner, Optional Snack, Nutritional Benefit, Mother's Benefit
        """
        response = model.generate_content(prompt)
        st.subheader("📝 Your Postpartum Diet Plan (Weekly)")
        st.markdown(response.text, unsafe_allow_html=True)

        pdf_data = create_pdf_from_text(response.text)
        st.download_button(label="📥 Download as PDF", data=pdf_data, file_name="postpartum_diet_plan.pdf", mime="application/pdf")
