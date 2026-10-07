# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Development Commands
- **Run Application:** `Run_SKELOS.bat` or `python -m streamlit run skelos/dashboard.py`
- **Install Dependencies:** `pip install -r requirements.txt`

## Architecture Overview
SKELOS is a full-stack golf biomechanics analysis application. The data flow is:
`Video Upload` $\rightarrow$ `AI Pose Estimation` $\rightarrow$ `Biomechanical Calculation` $\rightarrow$ `Risk Analysis` $\rightarrow$ `Cloud Storage/UI`.

### Core Components
- **`skelos/video_processor.py`**: Uses MediaPipe for AI landmark detection and signal smoothing.
- **`skelos/biomechanics_engine.py`**: Calculates the "X-Factor" (pelvis vs. thorax rotation) and the Kinematic Sequence.
- **`skelos/risk_analyzer.py`**: Maps biomechanical data to injury risk flags (e.g., Lumbar Compensation) and provides corrective exercises.
- **`skelos/dashboard.py`**: Streamlit-based UI implementing the user flow and data visualization.

### Infrastructure & Cloud
- **Authentication & Storage**: Handled by `skelos/auth_manager.py` via **Firebase** (Auth and Storage).
- **Relational Data**: Handled by `skelos/database_manager.py` via **Supabase**. 
    - Tables: `sessions` (metadata), `metrics` (biomechanical values), `risks` (injury flags).
- **Configuration**: Shared settings in `skelos/config.py` and `skelos/cloud_config.py`.

### Knowledge Base
- **`skelos/tips_library.py`**: A mapping of biomechanical failures to professional pro-tips and actions.
- **`Documentation/PROJECT_LOG.md`**: Contains the scientific foundation and research logic used for the engine.
