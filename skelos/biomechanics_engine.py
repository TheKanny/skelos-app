import numpy as np
import pandas as pd
from skelos.utils import calculate_angle, get_vector, normalize_angles

class BiomechanicsEngine:
    def __init__(self):
        self.target_vector = np.array([1, 0, 0])

    def _detect_phases(self, pelvis_angles, thorax_angles, wrist_vel):
        """
        Divide the swing into 8 fundamental phases based on kinematic markers.
        """
        total_frames = len(pelvis_angles)
        # 1. Top of swing is where X-Factor is max
        x_factors = np.abs(thorax_angles - pelvis_angles)
        top_frame = np.argmax(x_factors)

        # 2. Impact is where wrist velocity peaks
        impact_frame = np.argmax(wrist_vel)

        # 3. Takeaway is roughly the first 20% of the way to the top
        takeaway_frame = int(top_frame * 0.2)

        # 4. Setup is the first few frames (stability check)
        setup_end = int(total_frames * 0.05)

        # 5. Finish is the end of the video
        finish_frame = total_frames - 1

        return {
            'setup': (0, setup_end),
            'takeaway': (setup_end, takeaway_frame),
            'backswing': (takeaway_frame, top_frame),
            'downswing': (top_frame, impact_frame),
            'impact_range': (max(0, impact_frame - 2), min(total_frames, impact_frame + 2)),
            'follow_through': (impact_frame, finish_frame),
            'top': top_frame,
            'impact': impact_frame
        }

    def analyze_swing(self, df):
        pelvis_angles = []
        thorax_angles = []
        wrist_positions = []

        for _, row in df.iterrows():
            p_vec = get_vector(row['l_hip'], row['r_hip'])
            pelvis_angles.append(calculate_angle(p_vec, self.target_vector))

            t_vec = get_vector(row['l_shoulder'], row['r_shoulder'])
            thorax_angles.append(calculate_angle(t_vec, self.target_vector))

            wrist_positions.append(row['l_wrist'])

        pelvis_angles = normalize_angles(np.array(pelvis_angles))
        thorax_angles = normalize_angles(np.array(thorax_angles))
        x_factors = np.abs(thorax_angles - pelvis_angles)

        pelvis_vel = np.gradient(pelvis_angles)
        thorax_vel = np.gradient(thorax_angles)
        wrist_coords = np.array(wrist_positions)
        wrist_vel = np.linalg.norm(np.gradient(wrist_coords, axis=0), axis=1)

        # Detect the phases of the swing
        phases = self._detect_phases(pelvis_angles, thorax_angles, wrist_vel)

        return {
            'pelvis_angle': pelvis_angles,
            'thorax_angle': thorax_angles,
            'x_factor': x_factors,
            'max_x_factor': np.max(x_factors) if len(x_factors) > 0 else 0.0,
            'pelvis_vel': pelvis_vel,
            'max_pelvis_vel': np.max(pelvis_vel) if len(pelvis_vel) > 0 else 0.0,
            'thorax_vel': thorax_vel,
            'max_thorax_vel': np.max(thorax_vel) if len(thorax_vel) > 0 else 0.0,
            'wrist_vel': wrist_vel,
            'max_wrist_vel': np.max(wrist_vel) if len(wrist_vel) > 0 else 0.0,
            'phases': phases,
            'df_landmarks': df
        }
