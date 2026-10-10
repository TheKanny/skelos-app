import streamlit as st
import cv2
import pandas as pd
import plotly.graph_objects as go
import os
import base64
from video_processor import VideoProcessor
from biomechanics_engine import BiomechanicsEngine
from risk_analyzer import RiskAnalyzer
from scoring_engine import ScoringEngine
from fundamental_analyzer import FundamentalAnalyzer
from database_manager import DatabaseManager
from tips_library import TIPS_LIBRARY
from auth_manager import AuthManager

# --- Page Configuration ---
st.set_page_config(
    page_title="SKELOS | Pro Biomechanics",
    page_icon="🏌️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- ULTRA-PRO MAX DESIGN SYSTEM ---
st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;800&family=JetBrains+Mono:wght@400;700&display=swap');

        :root {
            --bg-deep: #05070A;
            --bg-surface: rgba(17, 25, 40, 0.7);
            --accent-gold: #FFD700;
            --accent-blue: #00E5FF;
            --accent-red: #FF3B30;
            --accent-orange: #FF9500;
            --text-main: #F5F5F7;
            --text-dim: #8E8E93;
            --border-color: rgba(255, 255, 255, 0.08);
            --glass-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.8);
        }

        .stApp {
            background-color: var(--bg-deep);
            color: var(--text-main);
            font-family: 'Inter', sans-serif;
        }

        /* Floating Glass Sidebar */
        [data-testid="stSidebar"] {
            background-color: rgba(10, 12, 18, 0.6);
            backdrop-filter: blur(20px);
            border-right: 1px solid var(--border-color);
        }

        /* Pro-Max Risk Cards */
        .risk-card {
            padding: 24px;
            border-radius: 20px;
            margin-bottom: 20px;
            border: 1px solid var(--border-color);
            background: linear-gradient(145deg, rgba(28, 35, 52, 0.8), rgba(17, 25, 40, 0.6));
            backdrop-filter: blur(15px);
            box-shadow: var(--glass-shadow);
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
            position: relative;
            overflow: hidden;
        }
        .risk-card.high { border-left: 8px solid var(--accent-red); }
        .risk-card.medium { border-left: 8px solid var(--accent-orange); }
        .risk-card:hover {
            transform: scale(1.02);
            background: rgba(30, 41, 65, 0.9);
            border-color: rgba(255, 215, 0, 0.4);
        }

        /* HUD Stat Tiles */
        .stat-tile {
            background: rgba(17, 25, 40, 0.5);
            padding: 24px;
            border-radius: 24px;
            text-align: center;
            border: 1px solid var(--border-color);
            box-shadow: inset 0 1px 1px rgba(255,255,255,0.1);
            transition: all 0.3s ease;
        }
        .stat-tile:hover {
            border-color: var(--accent-gold);
            background: rgba(25, 35, 55, 0.8);
        }
        .stat-value {
            font-family: 'JetBrains Mono', monospace;
            font-size: 2.8rem;
            font-weight: 800;
            color: var(--accent-gold);
            margin: 0;
            text-shadow: 0 0 15px rgba(255, 215, 0, 0.3);
        }
        .stat-label {
            font-size: 0.75rem;
            color: var(--text-dim);
            text-transform: uppercase;
            letter-spacing: 2px;
            margin: 0;
            font-weight: 600;
        }

        /* Pro-Max Buttons */
        .stButton>button {
            border-radius: 14px;
            padding: 14px 28px;
            font-weight: 700;
            background: linear-gradient(135deg, #FFD700 0%, #B8860B 100%);
            color: #000 !important;
            border: none;
            box-shadow: 0 4px 15px rgba(255, 215, 0, 0.2);
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        }
        .stButton>button:hover {
            box-shadow: 0 0 25px rgba(255, 215, 0, 0.5);
            transform: translateY(-2px);
            filter: brightness(1.1);
        }

        /* Input Refinement */
        .stTextInput > div > div > input {
            background-color: #0A0C10;
            color: white;
            border: 1px solid var(--border-color);
            border-radius: 14px;
            padding: 12px;
        }

        h1, h2, h3 {
            font-family: 'Inter', sans-serif;
            font-weight: 800 !important;
            letter-spacing: -1.5px;
        }

        /* Animations */
        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(20px); }
            to { opacity: 1; transform: translateY(0); }
        }
        .fade-in {
            animation: fadeIn 0.8s ease-out forwards;
        }
    </style>
""", unsafe_allow_html=True)

# --- Initialize Backend ---
db = DatabaseManager()
auth = AuthManager()

if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
if "user" not in st.session_state:
    st.session_state.user = None

# --- SHARED ANALYSIS LOGIC ---
def run_analysis(uploaded_file):
    video_path = os.path.join("/tmp", "temp_video.mp4")
    with open(video_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    processed_video_path = os.path.join("/tmp", "processed_swing.mp4")

    try:
        with st.spinner("⚡ Executing Kinematic Analysis..."):
            processor = VideoProcessor()
            engine = BiomechanicsEngine()
            analyzer = RiskAnalyzer()
            scorer = ScoringEngine()
            f_analyzer = FundamentalAnalyzer()

            df_landmarks, _ = processor.process_video(video_path, processed_video_path)
            bio_results = engine.analyze_swing(df_landmarks)
            risk_report = analyzer.analyze_risks(bio_results)
            fundamental_report = f_analyzer.analyze_fundamentals(bio_results)
            grade_report = scorer.evaluate_swing(bio_results, fundamental_report)

        return processed_video_path, bio_results, risk_report, grade_report, fundamental_report
    except Exception as e:
        st.error(f"Analysis partial failure: {e}")
        # Return a "safe" failure state so the UI can still render the video
        return processed_video_path, {}, [], {"overall_grade": "N/A", "overall_score": 0}, {}

    return processed_video_path, bio_results, risk_report, grade_report, fundamental_report

def render_results(video_path, bio_results, risk_report, grade_report, fundamental_report):
    # --- ELITE GRADE BADGE ---
    st.markdown(f"""
        <div style="text-align: center; margin-bottom: 2rem;">
            <p style="color: #8B949E; font-size: 1rem; margin-bottom: 0.5rem; text-transform: uppercase; letter-spacing: 2px;">Skelos Performance Grade</p>
            <h1 style="font-size: 6rem; color: #FFD700; margin: 0; line-height: 1; text-shadow: 0 0 20px rgba(255,215,0,0.5);">{grade_report['overall_grade']}</h1>
            <p style="color: #F5F5F7; font-size: 1.2rem; font-family: 'JetBrains Mono';">{grade_report['overall_score']}% Efficiency Score</p>
        </div>
    """, unsafe_allow_html=True)

    # --- ELITE STAT TILES ---
    st.markdown("<br>", unsafe_allow_html=True)
    t1, t2, t3, t4 = st.columns(4)
    with t1:
        st.markdown(f'<div class="stat-tile"><p class="stat-label">Max X-Factor</p><p class="stat-value">{bio_results["max_x_factor"]:.1f}°</p></div>', unsafe_allow_html=True)
    with t2:
        st.markdown(f'<div class="stat-tile"><p class="stat-label">Pelvis Peak</p><p class="stat-value">{bio_results["max_pelvis_vel"]:.1f}</p></div>', unsafe_allow_html=True)
    with t3:
        st.markdown(f'<div class="stat-tile"><p class="stat-label">Thorax Peak</p><p class="stat-value">{bio_results["max_thorax_vel"]:.1f}</p></div>', unsafe_allow_html=True)
    with t4:
        st.markdown(f'<div class="stat-tile"><p class="stat-label">Wrist Peak</p><p class="stat-value">{bio_results["max_wrist_vel"]:.1f}</p></div>', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    col1, col2 = st.columns([2, 1])

    with col1:
        st.subheader("Swing Visualization")
        try:
            with open(video_path, "rb") as v_file:
                video_bytes = v_file.read()

            # Embed video as Base64 for maximum browser compatibility
            video_base64 = base64.b64encode(video_bytes).decode()
            video_html = f"""
                <video width="100%" controls autoplay loop muted style="border-radius: 20px; border: 1px solid rgba(255,255,255,0.1);">
                    <source src="data:video/mp4;base64,{video_base64}" type="video/mp4">
                    Your browser does not support the video tag.
                </video>
            """
            st.markdown(video_html, unsafe_allow_html=True)
        except Exception as e:
            st.error(f"Could not load video: {e}")

        st.subheader("Kinematic Sequence")
        fig = go.Figure()
        fig.add_trace(go.Scatter(y=bio_results['x_factor'], name="X-Factor", line=dict(color='#FFD700', width=4)))
        fig.add_trace(go.Scatter(y=bio_results['pelvis_vel'], name="Pelvis", line=dict(color='#007AFF')))
        fig.add_trace(go.Scatter(y=bio_results['thorax_vel'], name="Thorax", line=dict(color='#50E3C2')))
        fig.add_trace(go.Scatter(y=bio_results['wrist_vel'], name="Wrist", line=dict(color='#FF3B30')))
        fig.update_layout(
            template="plotly_dark",
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            xaxis_title="Frame", yaxis_title="Value",
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
            margin=dict(l=20, r=20, t=20, b=20)
        )
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.subheader("Fundamental Audit")
        for fundamental, data in fundamental_report.items():
            color = "#00FF00" if data['status'] == 'Decent' else "#FFD700"
            status_label = "✅ Decent" if data['status'] == 'Decent' else "⚠️ Improve"
            st.markdown(f"""
                <div class="risk-card" style="border-left: 5px solid {color};">
                    <strong style="color: {color}; font-size: 1rem;">{fundamental}</strong><br>
                    <span style="color: #FFFFFF; font-size: 0.85rem; opacity: 0.9;">{status_label}: {data['feedback']}</span>
                </div>
                """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        st.subheader("Injury Risk Report")
        if not risk_report:
            st.success("✅ Biomechanicals are within safe range.")
        else:
            for risk in risk_report:
                color = "#FF3B30" if risk['level'] == 'High' else "#FF9500"
                level_class = "high" if risk['level'] == 'High' else "medium"
                st.markdown(f"""
                <div class="risk-card {level_class}">
                    <strong style="color: {color}; font-size: 1.1rem;">{risk['type'].capitalize()} - {risk['level']} Risk</strong><br>
                    <span style="color: #FFFFFF; font-size: 0.95rem; opacity: 0.9;">{risk['message']}</span>
                </div>
                """, unsafe_allow_html=True)

# --- AUTHENTICATION UI ---
def render_login_page():
    st.markdown("<br><br>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("<h1 style='text-align: center; font-size: 4rem; margin-bottom: 0;'>🏌️ SKELOS</h1>", unsafe_allow_html=True)
        st.markdown("<p style='text-align: center; color: #8B949E; font-size: 1.3rem; margin-bottom: 3rem;'>Elite Biomechanical Analysis & Injury Prevention</p>", unsafe_allow_html=True)

        # NEW: Try it out first!
        st.markdown('<div style="text-align: center; margin-bottom: 2rem;">', unsafe_allow_html=True)
        if st.button("✨ Try a Demo Swing (No Login)", use_container_width=True):
            st.session_state.demo_mode = True
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown("<p style='text-align: center; color: #FFD700; font-weight: 600; margin-bottom: 1rem;'>OR</p>", unsafe_allow_html=True)

        tab1, tab2 = st.tabs(["Sign In", "Join the Academy"])
        with tab1:
            email = st.text_input("Email", key="login_email")
            password = st.text_input("Password", type="password", key="login_pass")
            if st.button("Access Dashboard", use_container_width=True):
                result = auth.login(email, password)
                if result["success"]:
                    st.session_state.authenticated = True
                    st.session_state.user = result["user"]
                    st.rerun()
                else:
                    st.error(f"Authentication failed: {result['error']}")
        with tab2:
            new_email = st.text_input("Email", key="signup_email")
            new_password = st.text_input("Password", type="password", key="signup_pass")
            confirm_pass = st.text_input("Confirm Password", type="password", key="confirm_pass")
            if st.button("Create Pro Account", use_container_width=True):
                if new_password != confirm_pass:
                    st.error("Passwords do not match.")
                elif not new_email or not new_password:
                    st.error("Please fill in all fields.")
                else:
                    result = auth.sign_up(new_email, new_password)
                    if result["success"]:
                        st.success("Account created! Please sign in.")
                    else:
                        st.error(f"Error: {result['error']}")

# --- MAIN APPLICATION ---
def render_main_app():
    st.sidebar.markdown("<h2 style='color: white; margin-bottom: 0; letter-spacing: -1px;'>SKELOS</h2>", unsafe_allow_html=True)
    st.sidebar.markdown("<p style='color: #FFD700; font-size: 0.7rem; font-weight: 800; margin-top: 0; letter-spacing: 2px;'>ATHLETIC PROFICIENCY</p>", unsafe_allow_html=True)
    st.sidebar.markdown("<br>", unsafe_allow_html=True)

    page = st.sidebar.radio("Navigation", ["New Analysis", "Session History", "Grading Guide", "Skelos Academy"])

    st.sidebar.markdown("<br><br>", unsafe_allow_html=True)
    if st.sidebar.button("Sign Out", use_container_width=True):
        st.session_state.authenticated = False
        st.session_state.user = None
        st.session_state.demo_mode = False
        st.rerun()

    if page == "New Analysis":
        st.title("🎯 New Swing Analysis")
        st.markdown("<p style='color: #8B949E; margin-bottom: 2rem;'>Upload your swing video for an elite-level biomechanical breakdown.</p>", unsafe_allow_html=True)

        uploaded_file = st.file_uploader("Drag and drop swing video", type=["mp4", "mov", "avi"])

        if uploaded_file is not None:
            video_path, bio_results, risk_report, grade_report, fundamental_report = run_analysis(uploaded_file)
            render_results(video_path, bio_results, risk_report, grade_report, fundamental_report)

            if st.session_state.authenticated:
                st.markdown("---")
                st.subheader("Archive Analysis")
                player_name = st.text_input("Player Identity")
                if st.button("Save to Cloud", use_container_width=True):
                    if player_name:
                        session_id = db.save_session(player_name, uploaded_file.name, bio_results, risk_report)
                        st.success(f"Session archived successfully!")
                    else:
                        st.error("Please enter a player identity.")
            else:
                st.info("Log in to save this analysis to your history!")

    elif page == "Session History":
        if not st.session_state.authenticated:
            st.warning("Please sign in to view your session history.")
            return

        st.title("🕒 Session History")
        sessions = db.get_all_sessions()
        if not sessions:
            st.info("No saved sessions found. Start your first analysis!")
        else:
            session_options = {f"{s[0]} - {s[1]} ({s[2]})": s[0] for s in sessions}
            selected_session_label = st.selectbox("Select session:", list(session_options.keys()))
            if selected_session_label:
                session_id = session_options[selected_session_label]
                details = db.get_session_details(session_id)
                meta, metrics, risks = details['meta'], details['metrics'], details['risks']
                st.markdown(f"### Session: {meta[0]}")
                st.write(f"**Date:** {meta[1]} | **Video:** {meta[2]}")
                col1, col2 = st.columns([2, 1])
                with col1:
                    st.subheader("Metric Summary")
                    labels = ['Max X-Factor', 'Peak Pelvis Vel', 'Peak Thorax Vel', 'Peak Wrist Vel']
                    values = metrics[1:]
                    fig_summary = go.Figure([go.Bar(x=labels, y=values, marker_color='#007AFF')])
                    fig_summary.update_layout(template="plotly_dark", paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
                    st.plotly_chart(fig_summary, use_container_width=True)
                with col2:
                    st.subheader("Risk Archive")
                    if not risks:
                        st.success("✅ No risks recorded.")
                    else:
                        for risk in risks:
                            color = "#FF3B30" if risk[1] == 'High' else "#FF9500"
                            level_class = "high" if risk[1] == 'High' else "medium"
                            st.markdown(f"""
                            <div class="risk-card {level_class}">
                                <strong style="color: {color};">{risk[0]} - {risk[1]} Risk</strong><br>
                                <span style="font-size: 0.9rem;">{risk[2]}</span>
                            </div>
                            """, unsafe_allow_html=True)

    elif page == "Grading Guide":
        st.title("🏆 The Skelos Grading Standard")
        st.markdown("""
        <div style="background: rgba(255,215,0,0.1); padding: 20px; border-radius: 15px; border: 1px solid #FFD700; margin-bottom: 2rem;">
            <h3 style="color: #FFD700; margin-top: 0;">How Your Swing is Scored</h3>
            <p style="color: #F5F5F7; font-size: 1.1rem;">Skelos uses a <b>Hybrid Biomechanical Model</b>. Your grade is a weighted blend of raw physical output (60%) and technical correctness (40%).</p>
        </div>
        """, unsafe_allow_html=True)

        # Grade Definitions
        grades = [
            {"grade": "S", "label": "Elite", "color": "#FFD700", "desc": "Professional-grade physics and technique. Near-perfect kinematic sequence and optimal X-Factor."},
            {"grade": "A", "label": "Advanced", "color": "#00FF00", "desc": "Strong fundamentals. High efficiency with only minor gaps in peak power or sequence timing."},
            {"grade": "B", "label": "Competent", "color": "#00E5FF", "desc": "Solid base. Consistent mechanics but lacking the elite torsion and snap required for top-tier distance."},
            {"grade": "C", "label": "Developing", "color": "#FF9500", "desc": "Functional swing with noticeable technical flaws. Efficiency is limited by poor sequence or under-rotation."},
            {"grade": "D", "label": "Beginner", "color": "#FF3B30", "desc": "High risk of injury. Significant energy loss due to poor mechanics or extreme lumbar stress."},
            {"grade": "F", "label": "Critical", "color": "#8E8E93", "desc": "Immediate technical overhaul required. Swing is mechanically inefficient and potentially dangerous."}
        ]

        for g in grades:
            st.markdown(f"""
                <div class="risk-card" style="border-left: 8px solid {g['color']}; margin-bottom: 1rem;">
                    <div style="display: flex; align-items: center; gap: 20px;">
                        <span style="font-size: 3rem; font-weight: 800; color: {g['color']}; min-width: 60px;">{g['grade']}</span>
                        <div>
                            <strong style="font-size: 1.5rem; color: white;">{g['label']}</strong><br>
                            <span style="color: #8E8E93; font-size: 1rem;">{g['desc']}</span>
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        st.subheader("The Scoring Formula")
        st.markdown("""
        - **Biomechanical Pillars (60%):** Efficiency (X-Factor), Sequence (Timing), and Power (Wrist Snap).
        - **Fundamental Audit (40%):** A checklist of 8 key swing phases (Grip $\rightarrow$ Finish).
        """)
    elif page == "Skelos Academy":
        st.title("🎓 Skelos Academy")
        st.markdown("The definitive guide to golf biomechanics and injury prevention.")
        search_query = st.text_input("Search the knowledge base...", "").lower()
        for category, tip in TIPS_LIBRARY.items():
            if search_query in tip['title'].lower() or search_query in tip['description'].lower() or search_query in category:
                with st.expander(f"📖 {tip['title']} ({category.capitalize()})"):
                    st.markdown(f"**The Science:**\n{tip['description']}")
                    st.markdown(f"**The Action:**\n{tip['action']}")

    st.markdown("<br><br>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #8B949E; font-size: 0.8rem;'>SKELOS Analysis based on Biomechanical Poster Data. For educational purposes.</p>", unsafe_allow_html=True)

# --- Logic Router ---
if "demo_mode" not in st.session_state:
    st.session_state.demo_mode = False

if not st.session_state.authenticated and not st.session_state.demo_mode:
    render_login_page()
else:
    render_main_app()
