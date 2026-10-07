import streamlit as st
import cv2
import pandas as pd
import plotly.graph_objects as go
from skelos.video_processor import VideoProcessor
from skelos.biomechanics_engine import BiomechanicsEngine
from skelos.risk_analyzer import RiskAnalyzer
from skelos.database_manager import DatabaseManager
from skelos.tips_library import TIPS_LIBRARY

st.set_page_config(page_title="SKELOS - Golf Biomechanics", layout="wide")

# Initialize Database
db = DatabaseManager()

st.title("🏌️ SKELOS: Golf Swing Analysis & Injury Prevention")
st.markdown("---")

# --- Sidebar Navigation ---
st.sidebar.title("Menu")
page = st.sidebar.radio("Go to:", ["New Analysis", "Session History", "Skelos Academy"])

if page == "New Analysis":
    st.subheader("New Swing Analysis")
    uploaded_file = st.file_uploader("Upload Golf Swing Video", type=["mp4", "mov", "avi"])

    if uploaded_file is not None:
        # Save uploaded file to disk temporarily
        video_path = "temp_video.mp4"
        with open(video_path, "wb") as f:
            f.write(uploaded_file.getbuffer())

        with st.spinner("Analyzing swing biomechanics..."):
            processor = VideoProcessor()
            engine = BiomechanicsEngine()
            analyzer = RiskAnalyzer()

            # 1. Process Video
            df_landmarks = processor.process_video(video_path)

            # 2. Compute Biomechanics
            bio_results = engine.analyze_swing(df_landmarks)

            # 3. Analyze Risks
            risk_report = analyzer.analyze_risks(bio_results)

        # --- Results Display ---
        col1, col2 = st.columns([2, 1])

        with col1:
            st.subheader("Swing Visualization")
            st.video(video_path)

            st.subheader("Kinematic Sequence & X-Factor")
            fig = go.Figure()
            fig.add_trace(go.Scatter(y=bio_results['x_factor'], name="X-Factor", line=dict(color='gold', width=4)))
            fig.add_trace(go.Scatter(y=bio_results['pelvis_vel'], name="Pelvis Velocity", line=dict(color='blue')))
            fig.add_trace(go.Scatter(y=bio_results['thorax_vel'], name="Thorax Velocity", line=dict(color='green')))
            fig.add_trace(go.Scatter(y=bio_results['wrist_vel'], name="Arm/Club Velocity", line=dict(color='red')))
            fig.update_layout(xaxis_title="Frame", yaxis_title="Value", legend_title="Metrics")
            st.plotly_chart(fig, use_container_width=True)

        with col2:
            st.subheader("Injury Prevention Report")
            if not risk_report:
                st.success("✅ No significant biomechanical risks detected!")
            else:
                for risk in risk_report:
                    color = "red" if risk['level'] == 'High' else "orange"
                    st.markdown(f"""
                    <div style="border-left: 5px solid {color}; padding: 10px; margin-bottom: 10px; background-color: #f0f2f6;">
                        <strong>{risk['type'].capitalize()} - {risk['level']} Risk</strong><br>
                        {risk['message']}<br>
                    </div>
                    """, unsafe_allow_html=True)

        # --- Dynamic Improvement Checklist ---
        if risk_report:
            st.markdown("---")
            st.subheader("🛠️ Your Improvement Checklist")
            st.info("Complete these targeted exercises to reduce your injury risk.")

            for risk in risk_report:
                with st.expander(f"Correcting {risk['type'].capitalize()} Issues"):
                    for step in risk['improvement_steps']:
                        st.checkbox(step, key=f"check_{risk['type']}_{step}")

        # --- Smart Recommendations ---
        if risk_report:
            st.markdown("---")
            st.subheader("💡 Recommended Pro Tips")
            recommended_tips = [TIPS_LIBRARY[r['type']] for r in risk_report if r['type'] in TIPS_LIBRARY]

            for tip in recommended_tips:
                st.markdown(f"**{tip['title']}**")
                st.write(tip['description'])
                st.info(f"**Action:** {tip['action']}")

        # --- Save Session ---
        st.markdown("---")
        st.subheader("Save Analysis to History")
        player_name = st.text_input("Enter Player Name")
        if st.button("Save Session"):
            if player_name:
                session_id = db.save_session(player_name, uploaded_file.name, bio_results, risk_report)
                st.success(f"Session saved successfully! (ID: {session_id})")
            else:
                st.error("Please enter a player name before saving.")

elif page == "Session History":
    st.subheader("Past Analysis History")
    sessions = db.get_all_sessions()

    if not sessions:
        st.info("No saved sessions found. Start by analyzing a new swing!")
    else:
        session_options = {f"{s[0]} - {s[1]} ({s[2]})": s[0] for s in sessions}
        selected_session_label = st.selectbox("Select a session to view:", list(session_options.keys()))

        if selected_session_label:
            session_id = session_options[selected_session_label]
            details = db.get_session_details(session_id)
            meta, metrics, risks = details['meta'], details['metrics'], details['risks']

            st.markdown(f"### Session Details: {meta[0]}")
            st.write(f"**Date:** {meta[1]} | **Video:** {meta[2]}")

            col1, col2 = st.columns([2, 1])
            with col1:
                st.subheader("Summary Metrics")
                labels = ['Max X-Factor', 'Peak Pelvis Vel', 'Peak Thorax Vel', 'Peak Wrist Vel']
                values = metrics[1:]
                fig_summary = go.Figure([go.Bar(x=labels, y=values, marker_color='teal')])
                fig_summary.update_layout(yaxis_title="Value")
                st.plotly_chart(fig_summary, use_container_width=True)

            with col2:
                st.subheader("Historical Risk Report")
                if not risks:
                    st.success("✅ No risks were recorded for this session.")
                else:
                    for risk in risks:
                        color = "red" if risk[1] == 'High' else "orange"
                        st.markdown(f"""
                        <div style="border-left: 5px solid {color}; padding: 10px; margin-bottom: 10px; background-color: #f0f2f6;">
                            <strong>{risk[0]} - {risk[1]} Risk</strong><br>
                            {risk[2]}<br>
                        </div>
                        """, unsafe_allow_html=True)

elif page == "Skelos Academy":
    st.subheader("🎓 Skelos Academy: Biomechanical Knowledge Base")
    st.markdown("Learn the science behind your swing and how to improve your body's mechanics.")

    search_query = st.text_input("Search tips by keyword...", "").lower()

    for category, tip in TIPS_LIBRARY.items():
        if search_query in tip['title'].lower() or search_query in tip['description'].lower() or search_query in category:
            with st.expander(f"📖 {tip['title']} ({category.capitalize()})"):
                st.markdown(f"**The Science:**\n{tip['description']}")
                st.markdown(f"**The Action:**\n{tip['action']}")

st.markdown("---")
st.caption("SKELOS Analysis based on Biomechanical Poster Data. For educational purposes.")
