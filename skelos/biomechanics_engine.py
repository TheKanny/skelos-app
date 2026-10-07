import numpy as np
import pandas as pd
from skelos.utils import calculate_angle, get_vector, normalize_angles

class BiomechanicsEngine:
    def __init__(self):
        # Target line is assumed to be X-axis for simplicity in 2D projection
        self.target_vector = np.array([1, 0, 0])

    def analyze_swing(self, df):
        # 1. Extract vectors for each frame
        pelvis_angles = []
        thorax_angles = []
        wrist_positions = []

        for _, row in df.iterrows():
            # Pelvis Vector (L Hip to R Hip)
            p_vec = get_vector(row['l_hip'], row['r_hip'])
            pelvis_angles.append(calculate_angle(p_vec, self.target_vector))

            # Thorax Vector (L Shoulder to R Shoulder)
            t_vec = get_vector(row['l_shoulder'], row['r_shoulder'])
            thorax_angles.append(calculate_angle(t_vec, self.target_vector))

            # Lead wrist for kinematics (assuming right-handed)
            wrist_positions.append(row['l_wrist'])

        # Normalize angles relative to address (frame 0)
        pelvis_angles = normalize_angles(np.array(pelvis_angles))
        thorax_angles = normalize_angles(np.array(thorax_angles))

        # 2. Calculate X-Factor
        x_factors = np.abs(thorax_angles - pelvis_angles)

        # 3. Kinematic Sequence (Angular Velocity)
        # Simplified: calculating change in angle per frame as proxy for velocity
        pelvis_vel = np.gradient(pelvis_angles)
        thorax_vel = np.gradient(thorax_angles)
        # Wrist velocity as a proxy for arm/club speed
        wrist_coords = np.array(wrist_positions)
        wrist_vel = np.linalg.norm(np.gradient(wrist_coords, axis=0), axis=1)

        return {
            'pelvis_angle': pelvis_angles,
            'thorax_angle': thorax_angles,
            'x_factor': x_factors,
            'pelvis_vel': pelvis_vel,
            'thorax_vel': thorax_vel,
            'wrist_vel': wrist_vel
        }
