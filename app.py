import os
import streamlit as st
from src.auth import auth_page, logout
from src.utils import apply_custom_css
from src.data_loader import load_default_data, load_uploaded_data, validate_dataframe
from src.preprocessing import preprocess_data

# ──────────────────────────── PAGE CONFIG ────────────────────────────────
st.set_page_config(
    page_title="Student Performance Analysis System",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded",
)
# Initialize session state for auth
if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False
if "username" not in st.session_state:
    st.session_state["username"] = None

# If not logged in, show auth page and stop
if not st.session_state["logged_in"]:
    auth_page()
    st.stop()

# Apply dashboard theme only after successful login
apply_custom_css()

# ──────────────────────────── SIDEBAR & DATA SETUP ───────────────────────
with st.sidebar:
    st.markdown(
        f"""
        <div style="text-align:center; padding-bottom: 1rem; border-bottom: 1px solid rgba(255,255,255,0.1);">
            <h2 style='color:#14B8C4;margin-bottom:0'>🎓 Analytics</h2>
            <p style='margin-top: 5px; color: #A0AEC0;'>Welcome, <b>{st.session_state['username']}</b>!</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    
    if st.button("🚪 Logout", use_container_width=True):
        logout()
        
    st.markdown("---")

    # Data upload
    st.markdown("### 📁 Data Source")
    uploaded = st.file_uploader("Upload your CSV / XLSX", type=["csv", "xlsx"])

    sample_file_path = os.path.join(os.path.dirname(__file__), "data", "sample_student_records.csv")
    if os.path.exists(sample_file_path):
        with open(sample_file_path, "rb") as sf:
            st.download_button(
                label="📥 Download Sample CSV Template",
                data=sf.read(),
                file_name="sample_student_records.csv",
                mime="text/csv",
                use_container_width=True,
                help="Click to download a ready-made sample CSV file for testing upload",
            )

    if uploaded is not None:
        try:
            udf = load_uploaded_data(uploaded)
            valid, missing = validate_dataframe(udf)
            if valid:
                st.session_state["data"] = udf
                st.session_state["processed_data"] = preprocess_data(udf)
                st.success("✅ Custom data loaded!")
            else:
                st.error(f"❌ Missing columns: {', '.join(missing)}")
        except Exception as exc:
            st.error(f"Upload error: {exc}")

    # Fallback to default data
    if "data" not in st.session_state:
        with st.spinner("Loading default dataset…"):
            st.session_state["data"] = load_default_data()
            st.session_state["processed_data"] = preprocess_data(st.session_state["data"])
        st.info("ℹ️ Using built-in sample dataset")

    st.markdown("---")

    # System Status / Footer
    st.markdown("### 🖥️ System Status")
    st.markdown(
        """
        <div style="font-size: 0.85rem; color: #A0AEC0; padding: 10px; background: rgba(255,255,255,0.03); border-radius: 8px; border: 1px solid rgba(255,255,255,0.05);">
            <div style="display: flex; justify-content: space-between; margin-bottom: 5px;">
                <span>Database Connection:</span>
                <span style="color: #00D2A0; font-weight: 600;">● Secure</span>
            </div>
            <div style="display: flex; justify-content: space-between; margin-bottom: 5px;">
                <span>ML Models:</span>
                <span style="color: #00D2A0; font-weight: 600;">● Active</span>
            </div>
            <div style="display: flex; justify-content: space-between; margin-top: 10px; border-top: 1px solid rgba(255,255,255,0.1); padding-top: 8px;">
                <span>Version:</span>
                <span style="color: #14B8C4; font-weight: 600;">v2.5 Enterprise</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

# ──────────────────────────── NAVIGATION ROUTER ──────────────────────────
pages = {
    "Getting Started": [
        st.Page("views/0_Home.py", title="Home", icon="🏠"),
    ],
    "Dashboards": [
        st.Page("views/1_Overview.py", title="Overview", icon="📊"),
        st.Page("views/2_EDA.py", title="Exploratory Analysis", icon="🔍"),
        st.Page("views/3_Student_Analysis.py", title="Student Analysis", icon="👨‍🎓"),
        st.Page("views/4_Subject_Analysis.py", title="Subject Analysis", icon="📚"),
    ],
    "Machine Learning": [
        st.Page("views/5_Prediction.py", title="Prediction", icon="🎯"),
        st.Page("views/6_Model_Comparison.py", title="Model Comparison", icon="🤖"),
    ],
    "Exports": [
        st.Page("views/7_Reports.py", title="Reports & Downloads", icon="📋"),
    ]
}

pg = st.navigation(pages)
pg.run()
