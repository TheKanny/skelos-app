import cv2
import mediapipe as mp
import pandas as pd
import numpy as np
import subprocess
import os
from scipy.signal import savgol_filter
from utils import calculate_angle, get_vector, normalize_angles

class VideoProcessor:
    def __init__(self):
        self.mp_pose = mp.solutions.pose
        self.mp_drawing = mp.solutions.drawing_utils
        self.mp_drawing_styles = mp.solutions.drawing_styles
        self.pose = self.mp_pose.Pose(
            static_image_mode=False,
            model_complexity=1,
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5
        )

    def process_video(self, video_path, output_path):
        # Use /tmp for temporary files on Linux servers
        temp_output = os.path.join("/tmp", "temp_raw_processed.mp4")
        cap = cv2.VideoCapture(video_path)

        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        fps = int(cap.get(cv2.CAP_PROP_FPS))

        # Use mp4v for the temporary raw file
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        out = cv2.VideoWriter(temp_output, fourcc, fps, (width, height))

        data = []
        frame_idx = 0

        while cap.isOpened():
            success, frame = cap.read()
            if not success:
                break

            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = self.pose.process(frame_rgb)

            if results.pose_landmarks:
                landmarks = results.pose_landmarks.landmark

                frame_data = {
                    'frame': frame_idx,
                    'l_shoulder': [landmarks[11].x, landmarks[11].y, landmarks[11].z],
                    'r_shoulder': [landmarks[12].x, landmarks[12].y, landmarks[12].z],
                    'l_hip': [landmarks[23].x, landmarks[23].y, landmarks[23].z],
                    'r_hip': [landmarks[24].x, landmarks[24].y, landmarks[24].z],
                    'l_wrist': [landmarks[15].x, landmarks[15].y, landmarks[15].z],
                    'r_wrist': [landmarks[16].x, landmarks[16].y, landmarks[16].z],
                }
                data.append(frame_data)

                # Draw Skeletal HUD
                self.mp_drawing.draw_landmarks(
                    frame,
                    results.pose_landmarks,
                    self.mp_pose.POSE_CONNECTIONS,
                    self.mp_drawing_styles.get_default_pose_landmarks_style()
                )

                # Gold Biomechanical Lines
                l_sh = (int(landmarks[11].x * width), int(landmarks[11].y * height))
                r_sh = (int(landmarks[12].x * width), int(landmarks[12].y * height))
                cv2.line(frame, l_sh, r_sh, (0, 215, 255), 4)

                l_hip = (int(landmarks[23].x * width), int(landmarks[23].y * height))
                r_hip = (int(landmarks[24].x * width), int(landmarks[24].y * height))
                cv2.line(frame, l_hip, r_hip, (0, 215, 255), 4)

                mid_sh = ((l_sh[0]+r_sh[0])//2, (l_sh[1]+r_sh[1])//2)
                mid_hip = ((l_hip[0]+r_hip[0])//2, (l_hip[1]+r_hip[1])//2)
                cv2.line(frame, mid_sh, mid_hip, (0, 255, 0), 3)

            out.write(frame)
            frame_idx += 1

        cap.release()
        out.release()

        # --- FFmpeg Web-Optimization Step ---
        try:
            # Ensure output path is clean before starting
            if os.path.exists(output_path):
                os.remove(output_path)

            cmd = [
                'ffmpeg', '-y',
                '-i', temp_output,
                '-c:v', 'libx264',
                '-pix_fmt', 'yuv420p',
                '-preset', 'fast',
                '-movflags', 'faststart',
                output_path
            ]
            subprocess.run(cmd, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        except Exception as e:
            print(f"FFmpeg optimization failed: {e}. Using raw video instead.")
            if os.path.exists(temp_output):
                if os.path.exists(output_path):
                    os.remove(output_path)
                os.rename(temp_output, output_path)
        finally:
            # Always clean up temp raw file if it still exists
            if os.path.exists(temp_output):
                try:
                    os.remove(temp_output)
                except:
                    pass

        if not data:
            return pd.DataFrame(), output_path

        df = pd.DataFrame(data)
        smoothed_df = self._smooth_dataframe(df)

        return smoothed_df, output_path

    def _smooth_dataframe(self, df):
        smoothed_df = df.copy()
        for col in df.columns:
            if col == 'frame': continue
            coords = np.array(df[col].tolist())
            if len(coords) < 11: continue
            smoothed_coords = np.zeros_like(coords)
            for i in range(3):
                smoothed_coords[:, i] = savgol_filter(coords[:, i], 11, 3)
            smoothed_df[col] = [list(row) for row in smoothed_coords]
        return smoothed_df
