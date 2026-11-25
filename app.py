
import streamlit as st
import pandas as pd
import numpy as np
import joblib
import pickle
from pathlib import Path
from html import escape
from datetime import time

# Page configuration
st.set_page_config(
    page_title="SkyFare | Plan Smarter, Fly Better",
    page_icon="✈️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Load saved files
folder = Path(__file__).parent

@st.cache_resource
def load_files():

    model = joblib.load(folder / "flight_model_c.pkl")

    with open(folder / "onehot_encoder.pkl", "rb") as file:
        OHE = pickle.load(file)

    with open(folder / "scaler.pkl", "rb") as file:
        scaler = pickle.load(file)

    return model, OHE, scaler

model, OHE, scaler = load_files()


# ==============================
# WEBSITE STYLING
# ==============================

st.html("""
<style>

.stApp {
    background: linear-gradient(
        135deg, #020617, #0F172A, #102A43
    );
    color: white;
}

[data-testid="stHeader"] {
    background: transparent;
}

.block-container {
    max-width: 1200px;
    padding-top: 2rem;
    padding-bottom: 2rem;
}

.hero {
    background:
        linear-gradient(
            90deg,
            rgba(2, 6, 23, 0.92),
            rgba(2, 6, 23, 0.30)
        ),
        url('https://images.unsplash.com/photo-1436491865332-7a61a109cc05?auto=format&fit=crop&w=1600&q=85');

    background-size: cover;
    background-position: center;
    padding: 60px 35px;
    border-radius: 25px;
    border: 1px solid #334155;
    margin-bottom: 25px;
    animation: fadeIn 0.8s ease-in-out;
}

.brand {
    color: #38BDF8;
    font-size: 28px;
    font-weight: 800;
    letter-spacing: 4px;
}

.namaste {
    color: #BAE6FD;
    font-size: 21px;
    margin-top: 25px;
}

.hero-title {
    font-size: clamp(30px, 5vw, 52px);
    font-weight: 800;
    color: white;
    line-height: 1.2;
    margin-top: 12px;
}

.hero-subtitle {
    font-size: 22px;
    color: #E2E8F0;
    margin-top: 18px;
}

.hero-description {
    color: #CBD5E1;
    font-size: 16px;
    margin-top: 10px;
}

.section-title {
    font-size: 28px;
    font-weight: 700;
    color: #E0F2FE;
    margin-bottom: 5px;
}

.section-description {
    color: #94A3B8;
    margin-bottom: 20px;
}

[data-testid="stWidgetLabel"] p {
    color: #E2E8F0;
    font-weight: 600;
    font-size: 15px;
}

div[data-baseweb="select"] > div {
    background-color: #172B45;
    border: 1px solid #334155;
    border-radius: 12px;
    color: white;
}

div[data-baseweb="input"] {
    background-color: #172B45;
    border-radius: 12px;
}

div[data-baseweb="input"] input {
    color: white;
}

div.stButton > button {
    background: linear-gradient(
        90deg, #0284C7, #2563EB
    );
    color: white;
    border: none;
    border-radius: 14px;
    min-height: 55px;
    font-size: 18px;
    font-weight: 700;
    transition: all 0.3s ease;
}

div.stButton > button:hover {
    background: linear-gradient(
        90deg, #0369A1, #1D4ED8
    );
    color: white;
    transform: translateY(-2px);
    box-shadow: 0 8px 25px rgba(56,189,248,0.25);
}

.fare-card {
    background: linear-gradient(
        135deg, #0F2942, #172554
    );
    border: 1px solid #38BDF8;
    border-radius: 25px;
    padding: 35px;
    text-align: center;
    margin-top: 25px;
    box-shadow: 0 10px 40px rgba(0,0,0,0.3);
    animation: fadeIn 0.7s ease-in-out;
}

.fare-label {
    color: #CBD5E1;
    font-size: 20px;
}

.fare-price {
    color: #7DD3FC;
    font-size: clamp(35px, 6vw, 65px);
    font-weight: 800;
    margin: 15px 0;
}

.route {
    color: white;
    font-size: 25px;
    font-weight: 600;
}

.flight-info {
    color: #CBD5E1;
    font-size: 16px;
    margin-top: 15px;
}

.fare-note {
    color: #94A3B8;
    font-size: 13px;
    margin-top: 25px;
}

.sky-footer {
    text-align: center;
    padding: 25px 10px;
    color: #94A3B8;
    font-size: 14px;
}

.developer {
    color: #38BDF8;
    font-size: 16px;
    font-weight: 600;
}

@keyframes fadeIn {
    from {
        opacity: 0;
        transform: translateY(15px);
    }
    to {
        opacity: 1;
        transform: translateY(0);
    }
}

@media (max-width: 600px) {
    .hero {
        padding: 35px 20px;
    }

    .fare-card {
        padding: 25px 15px;
    }
}

@media (prefers-reduced-motion: reduce) {
    .hero, .fare-card {
        animation: none;
    }
}

</style>
""")


# ==============================
# WELCOME BANNER
# ==============================

st.html("""
<div class="hero">

    <div class="brand">
        ✈ SKYFARE
    </div>

    <div class="namaste">
        🙏 Namaste! Welcome to SkyFare
    </div>

    <div class="hero-title">
        Your Next Journey<br>
        Starts Here.
    </div>

    <div class="hero-subtitle">
        Plan Smarter. Fly Better.
    </div>

    <div class="hero-description">
        Explore destinations. Estimate fares. Travel smarter.
    </div>

</div>
""")


# ==============================
# FLIGHT DETAILS
# ==============================

st.html("""
<div class="section-title">
    🛫 Find Your Estimated Fare
</div>

<div class="section-description">
    Enter your flight details and discover your
    estimated ticket price in seconds.
</div>
""")


# Get available categories
categories = dict(
    zip(OHE.feature_names_in_, OHE.categories_)
)

col1, col2, col3 = st.columns(3)


with col1:

    source = st.selectbox(
        "🛫 Departure City",
        categories["Source"]
    )

    destination = st.selectbox(
        "🛬 Arrival City",
        categories["Destination"]
    )

    airline = st.selectbox(
        "✈️ Select Airline",
        categories["Airline"]
    )


with col2:

    journey_date = st.date_input(
        "📅 Journey Date"
    )

    dep_time = st.time_input(
        "🕐 Departure Time",
        value=time(9, 30)
    )

    arrival_time = st.time_input(
        "🕐 Arrival Time",
        value=time(11, 30)
    )


with col3:

    stop_options = {
        "Non-stop": 0,
        "1 Stop": 1,
        "2 Stops": 2,
        "3 Stops": 3,
        "4 Stops": 4
    }

    selected_stop = st.selectbox(
        "📍 Total Stops",
        list(stop_options.keys())
    )

    stops = stop_options[selected_stop]

    duration_hours = st.number_input(
        "⏳ Duration Hours",
        min_value=0,
        max_value=50,
        value=2
    )

    duration_min = st.number_input(
        "⏱️ Duration Minutes",
        min_value=0,
        max_value=59,
        value=0
    )


st.write("")
st.divider()


# ==============================
# FLIGHT PRICE PREDICTION
# ==============================

if st.button(
    "✈️ Get Estimated Fare",
    type="primary",
    use_container_width=True
):

    if source == destination:

        st.warning(
            "Departure and arrival cities cannot be the same."
        )

    elif duration_hours == 0 and duration_min == 0:

        st.warning(
            "Please enter a valid flight duration."
        )

    else:

        try:

            with st.spinner("Estimating your flight fare..."):

                # Numerical input
                num_df = pd.DataFrame([{
                    "Total_Stops": stops,
                    "Date": journey_date.day,
                    "Month": journey_date.month,
                    "Year": journey_date.year,
                    "Dep_hours": dep_time.hour,
                    "Dep_min": dep_time.minute,
                    "Arrival_hours": arrival_time.hour,
                    "Arrival_min": arrival_time.minute,
                    "Duration_hours": duration_hours,
                    "Duration_min": duration_min
                }])

                # Categorical input
                cat_df = pd.DataFrame([{
                    "Airline": airline,
                    "Source": source,
                    "Destination": destination
                }])

                # Match original column order
                num_df = num_df[scaler.feature_names_in_]

                cat_df = cat_df[OHE.feature_names_in_]

                # Transform numerical and categorical data
                num_df_trans = scaler.transform(num_df)

                cat_df_trans = OHE.transform(cat_df)

                # Convert numerical output into DataFrame
                if not isinstance(
                    num_df_trans, pd.DataFrame
                ):

                    num_df_trans = pd.DataFrame(
                        num_df_trans,
                        columns=scaler.get_feature_names_out()
                    )

                # Convert categorical output into DataFrame
                if not isinstance(
                    cat_df_trans, pd.DataFrame
                ):

                    if hasattr(cat_df_trans, "toarray"):

                        cat_df_trans = cat_df_trans.toarray()

                    cat_df_trans = pd.DataFrame(
                        cat_df_trans,
                        columns=OHE.get_feature_names_out()
                    )

                # Combine transformed data
                input_data = pd.concat(
                    [num_df_trans, cat_df_trans],
                    axis=1
                )

                # Match original training feature order
                if hasattr(model, "feature_names_in_"):

                    input_data = input_data[
                        model.feature_names_in_
                    ]

                # Predict price
                prediction = model.predict(input_data)

                price = float(
                    np.asarray(prediction).ravel()[0]
                )


            # ==============================
            # DISPLAY ESTIMATED FARE
            # ==============================

            st.html(f"""
            <div class="fare-card">

                <div class="fare-label">
                    Your Estimated Ticket Price
                </div>

                <div class="fare-price">
                    ₹{price:,.2f}
                </div>

                <div class="route">
                    {escape(str(source))}
                    ✈
                    {escape(str(destination))}
                </div>

                <div class="flight-info">
                    {escape(str(airline))}
                    &nbsp; | &nbsp;
                    {selected_stop}
                    &nbsp; | &nbsp;
                    {duration_hours}h {duration_min}m
                </div>

                <div class="flight-info">
                    📅 {journey_date.strftime('%d %B %Y')}
                </div>

                <div class="flight-info">
                    Departure:
                    {dep_time.strftime('%I:%M %p')}
                    &nbsp; | &nbsp;
                    Arrival:
                    {arrival_time.strftime('%I:%M %p')}
                </div>

                <div class="fare-note">
                    Estimated fare only.
                    Actual ticket prices may vary.
                </div>

            </div>
            """)

        except Exception as e:

            st.error(
                "Unable to estimate your fare. "
                "Please check your flight details."
            )

            print("Prediction Error:", e)


# ==============================
# WEBSITE FOOTER
# ==============================

st.divider()

st.html("""
<div class="sky-footer">

    <h2 style="color:#38BDF8; letter-spacing:3px;">
        ✈ SKYFARE
    </h2>

    <p>
        Plan Smarter. Fly Better.
    </p>

    <p class="developer">
        Designed & Developed by Alapati Jayanth
    </p>

    <p>
        Thank you for visiting SkyFare.<br>
        Have a safe and happy journey! ✈️
    </p>

    <p style="font-size:12px;">
        © 2026 SkyFare. All Rights Reserved.
    </p>

</div>
""")
