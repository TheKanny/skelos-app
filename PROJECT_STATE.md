# SKELOS: Comprehensive Project State Archive
Last Updated: 2026-10-08

## 1. Project Registry (File Map)
| Path | Purpose | Status |
|------|---------|--------|
| `Run_SKELOS.bat` | One-click launcher for the Streamlit app | ✅ Active |
| `requirements.txt` | Python dependency list | ✅ Current |
| `CLAUDE.md` | Guidance for AI agents working on this repo | ✅ Current |
| `todo.txt` | Master task list and progress tracker | ✅ Current |
| `Documentation/PROJECT_LOG.md` | Scientific foundation and development history | ✅ Current |
| `skelos/dashboard.py` | The main UI (Elite Pro-Max Design System) | ✅ Active |
| `skelos/video_processor.py` | MediaPipe AI landmark detection & smoothing | ✅ Active |
| `skelos/biomechanics_engine.py`| X-Factor and Kinematic Sequence math | ✅ Active |
| `skelos/risk_analyzer.py` | Injury prevention logic & thresholds | ✅ Active |
| `skelos/auth_manager.py` | Firebase Authentication integration | ✅ Active |
| `skelos/database_manager.py` | Supabase CRUD operations for sessions/metrics | ✅ Active |
| `skelos/config.py` | Secure config (reads from st.secrets) | ✅ Active |
| `skelos/cloud_config.py` | Supabase connection settings | ✅ Active |
| `skelos/tips_library.py` | Professional biomechanical advice database | ✅ Active |
| `skelos/utils.py` | General helper functions | ✅ Active |
| `.gitignore` | Prevents secrets/temp files from hitting GitHub | ✅ Current |

## 2. Technical Architecture
**The Pipeline:**
`User Upload (MP4/MOV)` $\rightarrow$ `VideoProcessor (MediaPipe)` $\rightarrow$ `BiomechanicsEngine (Rotation Math)` $\rightarrow$ `RiskAnalyzer (Threshold Checks)` $\rightarrow$ `DatabaseManager (Supabase)` $\rightarrow$ `Dashboard (Streamlit UI)`.

**Cloud Infrastructure:**
- **Auth/Storage:** Firebase (User accounts, secure video buckets).
- **Database:** Supabase (PostgreSQL) storing `sessions`, `metrics`, and `risks`.
- **Hosting:** Streamlit Cloud (linked to GitHub `main` branch).
- **Custom Domain:** Linked via CNAME to Streamlit Cloud.

## 3. Completed Milestones
- [x] **Core Engine:** AI pose estimation and biomechanical calculations implemented.
- [x] **Cloud Integration:** Full Firebase and Supabase wiring completed.
- [x] **Elite UI:** Pro-Max Design System (Glassmorphism, HUD Stat Tiles, Deep Onyx palette).
- [x] **Authentication:** Secure Sign-in/Sign-up flow with Firebase.
- [x] **Demo Mode:** "Try before you buy" analysis feature.
- [x] **GitHub Sync:** Project version-controlled and pushed to private repo.
- [x] **Secrets Migration:** Keys moved from hard-coded to `st.secrets` for cloud safety.

## 4. Current Work-in-Progress: The Clinical Pass
**Objective:** Validate the scientific accuracy of the risk reports.
**Current Status:**
- [x] Setup validation dataset (Perfect, Stiff, Erratic, High-Risk swings).
- [ ] Run "Blind" analysis on test videos.
- [ ] Compare results against the Biomechanical Research Poster.
- [ ] Calibrate thresholds in `risk_analyzer.py` based on findings.

## 5. Future Roadmap
- **Product Pass:** 
    - Side-by-side swing comparison tool.
    - Pro Gallery (Comparing user data to elite golfers).
    - Expanded corrective exercise library.
- **UX Refinement:** 
    - User profile dashboard for tracking improvement over time.
    - Mobile-optimized view for on-range use.
