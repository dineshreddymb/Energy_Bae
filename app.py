
import base64
import os
import requests
import streamlit as st
from dotenv import load_dotenv
from PIL import Image

# ==========================================
# LOAD ENV VARIABLES
# ==========================================

load_dotenv()

N8N_WEBHOOK_URL = os.getenv("N8N_WEBHOOK_URL")
API_KEY = os.getenv("API_KEY", "")
GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")

# ==========================================
# PAGE CONFIG
# ==========================================

st.set_page_config(
    page_title="Energybae Solar Calculator",
    page_icon="☀️",
    layout="wide",
)

# ==========================================
# CUSTOM CSS
# ==========================================

st.markdown(
    """
    <style>

    .main-header {
        font-size: 2.8rem;
        color: #FF6B35;
        font-weight: bold;
    }

    .sub-header {
        font-size: 1.2rem;
        color: #2E7D32;
    }

    .stButton>button {
        background-color: #FF6B35;
        color: white;
        font-weight: bold;
        border-radius: 10px;
        padding: 0.6rem 2rem;
        border: none;
    }

    .metric-box {
        background-color: #F8F9FA;
        padding: 1rem;
        border-radius: 12px;
        border: 1px solid #E0E0E0;
    }

    </style>
    """,
    unsafe_allow_html=True,
)

# ==========================================
# HELPER FUNCTIONS
# ==========================================

def format_currency(value):

    if value in [None, ""]:
        return "N/A"

    value = str(value)

    if value.startswith("₹"):
        return value

    return f"₹{value}"


def format_kw(value):

    if value in [None, ""]:
        return "N/A"

    value = str(value)

    if "kw" in value.lower():
        return value

    return f"{value} kW"


def format_value(value):

    if value in [None, ""]:
        return "N/A"

    return str(value)

# ==========================================
# HEADER
# ==========================================

col1, col2 = st.columns([1, 5])

with col1:
    st.markdown("# ☀️")

with col2:

    st.markdown(
        '<p class="main-header">Energybae Solar Calculator</p>',
        unsafe_allow_html=True,
    )

    st.markdown(
        '<p class="sub-header">Upload your electricity bill and get AI-powered solar recommendations instantly</p>',
        unsafe_allow_html=True,
    )

st.divider()

# ==========================================
# SIDEBAR
# ==========================================

with st.sidebar:

    st.header("⚙️ Configuration")

    if N8N_WEBHOOK_URL:
        st.success("✅ n8n Webhook Connected")
    else:
        st.error("❌ Missing N8N_WEBHOOK_URL")

    if GROQ_API_KEY:
        st.success("✅ GROQ API Loaded")
    else:
        st.warning("⚠️ GROQ API Missing")

# ==========================================
# FILE UPLOAD SECTION
# ==========================================

st.subheader("📄 Upload Electricity Bill")

uploaded_file = st.file_uploader(
    "Choose PDF or Image",
    type=["pdf", "png", "jpg", "jpeg"],
)

# ==========================================
# IMAGE PREVIEW
# ==========================================

if uploaded_file:

    st.success(f"✅ Uploaded: {uploaded_file.name}")

    if uploaded_file.type.startswith("image"):

        image = Image.open(uploaded_file)

        st.image(
            image,
            caption="Uploaded Electricity Bill",
            use_container_width=True,
        )

# ==========================================
# PROCESS BUTTON
# ==========================================

if uploaded_file and st.button("🚀 Calculate Solar Recommendation"):

    with st.spinner("Processing your bill using AI..."):

        try:

            # ==========================================
            # SEND FILE TO N8N
            # ==========================================

            response = requests.post(

                N8N_WEBHOOK_URL,

                files={
                    "file": (
                        uploaded_file.name,
                        uploaded_file.getvalue(),
                        uploaded_file.type,
                    )
                },

                data={
                    "filename": uploaded_file.name,
                    "file_type": uploaded_file.type,
                    "groq_api_key": GROQ_API_KEY,
                },

                headers={
                    "Authorization": f"Bearer {API_KEY}"
                } if API_KEY else {},

                timeout=180,
            )

            # ==========================================
            # CHECK RESPONSE STATUS
            # ==========================================

            if response.status_code != 200:

                st.error(f"❌ HTTP Error {response.status_code}")

                st.text(response.text)

                st.stop()

            # ==========================================
            # CONVERT RESPONSE TO JSON
            # ==========================================

            try:

                result = response.json()

            except Exception:

                st.error("❌ Invalid JSON response from n8n")

                st.text(response.text)

                st.stop()

            # ==========================================
            # DEBUG RESPONSE
            # ==========================================

            with st.expander("🛠 Raw API Response"):

                st.json(result)

            # ==========================================
            # CHECK STATUS
            # ==========================================

            if result.get("status") != "success":

                st.error(
                    result.get(
                        "message",
                        "Bill processing failed"
                    )
                )

                st.stop()

            # ==========================================
            # EXTRACT DATA
            # ==========================================

            data = result.get("data", {})

            # ==========================================
            # DISPLAY RESULTS
            # ==========================================

            st.divider()

            st.subheader("📊 Solar Recommendation Results")

            col1, col2, col3 = st.columns(3)

            # ==========================================
            # COLUMN 1
            # ==========================================

            with col1:

                st.metric(
                    "⚡ Monthly Units",
                    format_value(
                        data.get("units_consumed")
                    )
                )

                st.metric(
                    "💰 Monthly Bill",
                    format_currency(
                        data.get("total_amount")
                    )
                )

                st.metric(
                    "📅 Billing Month",
                    format_value(
                        data.get("billing_month")
                    )
                )

            # ==========================================
            # COLUMN 2
            # ==========================================

            with col2:

                st.metric(
                    "🏠 Sanctioned Load",
                    format_value(
                        data.get("sanctioned_load")
                    )
                )

                st.metric(
                    "📋 Tariff Category",
                    format_value(
                        data.get("tariff_category")
                    )
                )

                st.metric(
                    "⚡ Unit Cost",
                    format_currency(
                        data.get("unit_cost")
                    )
                )

            # ==========================================
            # COLUMN 3
            # ==========================================

            with col3:

                st.metric(
                    "☀️ Recommended Solar",
                    format_kw(
                        data.get(
                            "required_solar_capacity_kw"
                        )
                    )
                )

                st.metric(
                    "🔋 Number of Panels",
                    format_value(
                        data.get(
                            "recommended_number_of_panels"
                        )
                    )
                )

                st.metric(
                    "📈 Predicted Next Bill",
                    format_currency(
                        data.get(
                            "predicted_next_month_bill"
                        )
                    )
                )

            # ==========================================
            # ADDITIONAL ANALYSIS
            # ==========================================

            st.divider()

            st.subheader("🧠 AI Bill Analysis")

            analysis_col1, analysis_col2 = st.columns(2)

            with analysis_col1:

                st.info(
                    f"""
                    **Consumption Level:**  
                    {format_value(data.get("consumption_level"))}
                    """
                )

                st.info(
                    f"""
                    **Solar Recommendation:**  
                    {format_value(data.get("solar_recommendation"))}
                    """
                )

            with analysis_col2:

                st.info(
                    f"""
                    **Bill Analysis:**  
                    {format_value(data.get("bill_analysis"))}
                    """
                )

                st.info(
                    f"""
                    **Daily Average Units:**  
                    {format_value(data.get("daily_average_units"))}
                    """
                )

            # ==========================================
            # CUSTOMER DETAILS
            # ==========================================

            st.divider()

            st.subheader("👤 Customer Details")

            customer_col1, customer_col2 = st.columns(2)

            with customer_col1:

                st.text_input(
                    "Customer Name",
                    value=format_value(
                        data.get("customer_name")
                    ),
                    disabled=True,
                )

            with customer_col2:

                st.text_input(
                    "Consumer Number",
                    value=format_value(
                        data.get("consumer_number")
                    ),
                    disabled=True,
                )

            # ==========================================
            # FULL JSON VIEW
            # ==========================================

            with st.expander("🔍 Full Extracted Data"):

                st.json(data)

            # ==========================================
            # EXCEL DOWNLOAD
            # ==========================================

            excel_base64 = result.get("excel_base64")

            if excel_base64:

                try:

                    excel_data = base64.b64decode(
                        excel_base64
                    )

                    st.download_button(

                        label="📥 Download Excel Report",

                        data=excel_data,

                        file_name="solar_report.xlsx",

                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                    )

                except Exception as e:

                    st.error(
                        f"Excel Decode Error: {str(e)}"
                    )

        # ==========================================
        # ERROR HANDLING
        # ==========================================

        except requests.Timeout:

            st.error(
                "❌ Request timed out. n8n workflow may still be processing."
            )

        except requests.ConnectionError:

            st.error(
                "❌ Could not connect to n8n webhook."
            )

        except Exception as e:

            st.error(
                f"❌ Unexpected Error: {str(e)}"
            )
