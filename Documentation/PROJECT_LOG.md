# SKELOS Project: Development Log & Documentation

## Project Overview
SKELOS is a golf swing analysis and injury prevention program. It uses AI pose estimation to translate video swings into biomechanical data, specifically focusing on the "X-Factor" and the Kinematic Sequence.

## Scientific Foundation
The program is based on research from the user's biomechanical poster (`poster.pdf`), implementing the following logic:
- **Kinematic Sequence:** Tracking energy transfer from Hips -> Shoulders -> Arms -> Club.
- **X-Factor:** Calculating the relative rotation between the pelvis and thorax.
- **Injury Prevention:** 
    - Flagging "Lumbar Compensation" when high X-Factor is paired with low hip internal rotation.
    - Monitoring lead shoulder impingement and lead wrist impact forces.

## Technical Architecture
- **Language:** Python 3.10+
- **Libraries:** MediaPipe (Pose Estimation), OpenCV (Video), Streamlit (UI), Plotly (Graphs).
- **Core Modules:**
    - `video_processor.py`: Handles AI landmark detection and signal smoothing.
    - `biomechanics_engine.py`: Calculates rotation angles and velocities.
    - `risk_analyzer.py`: Maps data to injury risks and corrective exercises.
    - `dashboard.py`: The interactive web interface.

## Setup Instructions
1. Install Python (ensure "Add to PATH" is checked).
2. Run `pip install -r requirements.txt`.
3. Launch via `Run_SKELOS.bat`.

## Future Roadmap
- [ ] Transition to Cloud Deployment (Streamlit Cloud) for web-based access.
- [ ] Refine risk thresholds based on professional golfer data.
- [ ] Expand corrective exercise library.
