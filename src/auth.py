"""Authentication module: exact replica of the clean, modern student performance dashboard design with premium professional coloring."""

import streamlit as st
import json
import os
import hashlib

USERS_FILE = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "users.json")


def load_users():
    if not os.path.exists(USERS_FILE):
        return {}
    with open(USERS_FILE, "r") as f:
        return json.load(f)


def save_users(users):
    os.makedirs(os.path.dirname(USERS_FILE), exist_ok=True)
    with open(USERS_FILE, "w") as f:
        json.dump(users, f, indent=2)


def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()


def auth_page():
    # ── Inject custom CSS for premium professional coloring and single-line title ──
    st.markdown(
        """
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=Inter:wght@400;500;600;700&display=swap');

        /* Hide Streamlit default chrome & sidebar on login page */
        [data-testid="stSidebar"], [data-testid="stSidebarNav"] {
            display: none !important;
        }
        #MainMenu, footer, header {
            visibility: hidden !important;
        }
        [data-testid="collapsedControl"] {
            display: none !important;
        }

        /* Full page background - sleek modern soft tech gradient */
        html, body, [class*="css"], .stApp, [data-testid="stAppViewContainer"] {
            font-family: 'Plus Jakarta Sans', 'Inter', -apple-system, sans-serif !important;
            background: radial-gradient(circle at 12% 10%, rgba(20, 84, 206, 0.07) 0%, transparent 45%),
                        radial-gradient(circle at 88% 85%, rgba(99, 102, 241, 0.05) 0%, transparent 45%),
                        linear-gradient(180deg, #F0F4FA 0%, #F8FAFD 50%, #FFFFFF 100%) !important;
            color: #0F172A !important;
        }

        /* Container width & padding */
        .block-container {
            max-width: 760px !important;
            padding-top: 1.5rem !important;
            padding-bottom: 3.5rem !important;
            margin: 0 auto !important;
        }

        /* ── Rich Vibrant Hero Banner ─────────────────────────── */
        .auth-banner {
            background: radial-gradient(circle at 82% 18%, rgba(255, 255, 255, 0.22) 0%, transparent 42%),
                        linear-gradient(135deg, #0A3592 0%, #1656CC 48%, #2B75F6 100%);
            border: 1px solid rgba(255, 255, 255, 0.24);
            border-radius: 22px;
            padding: 38px 24px 34px 24px;
            text-align: center;
            color: #FFFFFF !important;
            box-shadow: 0 20px 40px -10px rgba(22, 86, 204, 0.35), 0 8px 16px -4px rgba(0, 0, 0, 0.08);
            margin-bottom: 26px;
            position: relative;
            overflow: hidden;
        }
        .auth-banner::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            height: 1px;
            background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.6), transparent);
        }
        .auth-banner-icon {
            font-size: 2.7rem;
            margin-bottom: 8px;
            display: inline-block;
            filter: drop-shadow(0 6px 14px rgba(0, 0, 0, 0.25));
        }
        .auth-banner-title {
            color: #FFFFFF !important;
            font-size: clamp(1.2rem, 3.4vw, 1.95rem) !important;
            font-weight: 800 !important;
            margin: 0 0 10px 0 !important;
            line-height: 1.25 !important;
            letter-spacing: -0.35px !important;
            white-space: nowrap !important;
            text-shadow: 0 2px 10px rgba(0, 0, 0, 0.2);
        }
        .auth-banner-subtitle {
            color: rgba(255, 255, 255, 0.94) !important;
            font-size: 0.94rem !important;
            font-weight: 400 !important;
            margin: 0 auto 20px auto !important;
            max-width: 90% !important;
            line-height: 1.45 !important;
            letter-spacing: 0.1px !important;
        }
        .auth-banner-pills {
            display: inline-flex !important;
            align-items: center !important;
            justify-content: center !important;
            gap: 12px !important;
            background: rgba(8, 28, 88, 0.48) !important;
            border: 1px solid rgba(255, 255, 255, 0.26) !important;
            border-radius: 9999px !important;
            padding: 7px 22px !important;
            font-size: 0.8rem !important;
            color: #FFFFFF !important;
            font-weight: 600 !important;
            backdrop-filter: blur(10px) !important;
            box-shadow: inset 0 1px 1px rgba(255, 255, 255, 0.2), 0 4px 12px rgba(0, 0, 0, 0.12);
        }
        .auth-banner-pills span.dot {
            opacity: 0.55;
            font-size: 0.75rem;
        }

        /* ── Tabs Styling ─────────────────────────────────────── */
        .stTabs [data-baseweb="tab-list"] {
            gap: 12px !important;
            background: transparent !important;
            border-bottom: 1px solid #E2E8F0 !important;
            padding-bottom: 8px !important;
            margin-bottom: 22px !important;
            justify-content: flex-start !important;
        }
        .stTabs [data-baseweb="tab"] {
            border-radius: 8px !important;
            padding: 8px 20px !important;
            background-color: transparent !important;
            color: #64748B !important;
            font-weight: 600 !important;
            font-size: 0.9rem !important;
            border: none !important;
            transition: all 0.25s ease !important;
        }
        .stTabs [data-baseweb="tab"]:hover {
            color: #1656CC !important;
            background-color: rgba(22, 86, 204, 0.05) !important;
        }
        .stTabs [data-baseweb="tab"][aria-selected="true"] {
            background: linear-gradient(135deg, #1656CC 0%, #2570EA 100%) !important;
            color: #FFFFFF !important;
            font-weight: 600 !important;
            box-shadow: 0 4px 14px rgba(22, 86, 204, 0.28) !important;
        }
        .stTabs [data-baseweb="tab-highlight"],
        .stTabs [data-baseweb="tab-border"] {
            display: none !important;
        }

        /* ── Headings ─────────────────────────────────────────── */
        .auth-form-title {
            color: #0F172A !important;
            font-size: 1.55rem !important;
            font-weight: 800 !important;
            margin: 0 0 5px 0 !important;
            letter-spacing: -0.4px !important;
        }
        .auth-form-subtitle {
            color: #64748B !important;
            font-size: 0.9rem !important;
            margin: 0 0 18px 0 !important;
            font-weight: 400 !important;
        }

        /* ── Card & Form Styling ──────────────────────────────── */
        [data-testid="stForm"] {
            background: #FFFFFF !important;
            border: 1px solid rgba(226, 232, 240, 0.95) !important;
            border-radius: 18px !important;
            padding: 28px !important;
            box-shadow: 0 16px 40px -8px rgba(15, 23, 42, 0.07), 0 4px 12px rgba(15, 23, 42, 0.03) !important;
        }

        /* ── Inputs ───────────────────────────────────────────── */
        [data-testid="stForm"] label,
        [data-testid="stForm"] [data-testid="stWidgetLabel"] p {
            color: #334155 !important;
            font-size: 0.88rem !important;
            font-weight: 600 !important;
            margin-bottom: 6px !important;
        }
        [data-testid="stForm"] input {
            background-color: #F8FAFC !important;
            border: 1px solid #E2E8F0 !important;
            border-radius: 10px !important;
            color: #0F172A !important;
            padding: 11px 15px !important;
            font-size: 0.92rem !important;
            transition: all 0.2s ease !important;
        }
        [data-testid="stForm"] input::placeholder {
            color: #94A3B8 !important;
        }
        [data-testid="stForm"] input:focus {
            background-color: #FFFFFF !important;
            border-color: #2570EA !important;
            box-shadow: 0 0 0 3px rgba(37, 112, 234, 0.16) !important;
            outline: none !important;
        }

        /* ── Action Button ────────────────────────────────────── */
        [data-testid="stForm"] button[kind="primary"],
        [data-testid="stForm"] button {
            background: linear-gradient(135deg, #1656CC 0%, #2570EA 100%) !important;
            color: #FFFFFF !important;
            border: none !important;
            border-radius: 10px !important;
            padding: 12px 20px !important;
            font-size: 0.96rem !important;
            font-weight: 600 !important;
            width: 100% !important;
            margin-top: 16px !important;
            box-shadow: 0 4px 15px rgba(22, 86, 204, 0.32) !important;
            transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1) !important;
        }
        [data-testid="stForm"] button:hover {
            background: linear-gradient(135deg, #1247AA 0%, #1E60D5 100%) !important;
            box-shadow: 0 6px 20px rgba(22, 86, 204, 0.44) !important;
            transform: translateY(-1px) !important;
        }
        [data-testid="stForm"] button:active {
            transform: translateY(0) !important;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    # ── 1. Top Blue Hero Banner (Content preserved, enhanced coloring) ───────
    st.markdown(
        """
        <div class="auth-banner">
            <div class="auth-banner-icon">🎓</div>
            <h1 class="auth-banner-title">Student Performance Analysis System</h1>
            <p class="auth-banner-subtitle">
                Analyse student performance, generate predictions and identify academic attention indicators.
            </p>
            <div class="auth-banner-pills">
                <span>📊 Data Analytics</span>
                <span class="dot">•</span>
                <span>🧠 AI Prediction</span>
                <span class="dot">•</span>
                <span>🎯 Student Insights</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # ── 2. Tabs: Sign In | Sign Up ────────────────────────────────────────
    tab1, tab2 = st.tabs(["🔐 Sign In", "📝 Sign Up"])
    users = load_users()

    with tab1:
        st.markdown('<div class="auth-form-title">Welcome Back</div>', unsafe_allow_html=True)
        st.markdown(
            '<div class="auth-form-subtitle">Sign in to access your student performance dashboard.</div>',
            unsafe_allow_html=True,
        )

        with st.form("login_form"):
            email = st.text_input("Email", placeholder="Enter your email")
            password = st.text_input("Password", type="password", placeholder="Enter your password")
            submit = st.form_submit_button("🔐 Sign In", use_container_width=True)

            if submit:
                email_clean = email.strip()
                if not email_clean or not password:
                    st.error("Please enter both email and password.")
                elif email_clean in users and users[email_clean] == hash_password(password):
                    st.session_state["logged_in"] = True
                    st.session_state["username"] = email_clean
                    st.rerun()
                else:
                    st.error("Invalid email or password.")

    with tab2:
        st.markdown('<div class="auth-form-title">Create Account</div>', unsafe_allow_html=True)
        st.markdown(
            '<div class="auth-form-subtitle">Sign up to access your student performance dashboard.</div>',
            unsafe_allow_html=True,
        )

        with st.form("signup_form"):
            new_email = st.text_input("Email", placeholder="Enter your email")
            new_pass = st.text_input("Password", type="password", placeholder="Enter your password")
            confirm_pass = st.text_input("Confirm Password", type="password", placeholder="Confirm your password")
            submit_up = st.form_submit_button("📝 Sign Up", use_container_width=True)

            if submit_up:
                email_clean = new_email.strip()
                if not email_clean or not new_pass:
                    st.error("Please fill in all fields.")
                elif email_clean in users:
                    st.error("An account with this email already exists.")
                elif new_pass != confirm_pass:
                    st.error("Passwords do not match.")
                elif len(new_pass) < 4:
                    st.error("Password must be at least 4 characters.")
                else:
                    users[email_clean] = hash_password(new_pass)
                    save_users(users)
                    st.success("Account created successfully! You can now Sign In.")


def logout():
    st.session_state["logged_in"] = False
    st.session_state["username"] = None
    st.rerun()
