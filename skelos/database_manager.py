import pandas as pd
from supabase import create_client, Client
from cloud_config import SUPABASE_CONFIG

class DatabaseManager:
    def __init__(self):
        self.url: str = SUPABASE_CONFIG["url"]
        self.key: str = SUPABASE_CONFIG["api_key"]
        self.supabase: Client = create_client(self.url, self.key)
        self._init_db()

    def _init_db(self):
        """
        Initializes the cloud tables.
        Note: In Supabase, tables are usually created via the Dashboard SQL Editor.
        This method ensures the connection is working.
        """
        try:
            # We test the connection by attempting to fetch from a known table
            # The tables should be created in the Supabase SQL Editor
            self.supabase.table("sessions").select("*").limit(1).execute()
        except Exception:
            # If tables don't exist yet, we don't crash, but the user will be warned
            pass

    def save_session(self, user_id, player_name, video_filename, bio_results, risk_report):
        """Saves the analysis results to the Supabase cloud."""
        try:
            # 1. Insert into 'sessions' table
            session_data = {
                "user_id": user_id,
                "player_name": player_name,
                "video_filename": video_filename
            }
            session_response = self.supabase.table("sessions").insert(session_data).execute()
            session_id = session_response.data[0]['id']

            # 2. Insert into 'metrics' table
            metrics_data = {
                "session_id": session_id,
                "max_x_factor": float(np.max(bio_results['x_factor'])),
                "peak_pelvis_vel": float(np.max(np.abs(bio_results['pelvis_vel']))),
                "peak_thorax_vel": float(np.max(np.abs(bio_results['thorax_vel']))),
                "peak_wrist_vel": float(np.max(bio_results['wrist_vel']))
            }
            self.supabase.table("metrics").insert(metrics_data).execute()

            # 3. Insert into 'risks' table
            risks_data = []
            for risk in risk_report:
                risks_data.append({
                    "session_id": session_id,
                    "risk_type": risk['type'],
                    "risk_level": risk['level'],
                    "message": risk['message'],
                    "exercise": risk.get('improvement_steps', risk.get('exercise', ''))
                })
            self.supabase.table("risks").insert(risks_data).execute()

            return session_id
        except Exception as e:
            print(f"Error saving to Supabase: {e}")
            return None

    def get_all_sessions(self, user_id):
        """Retrieves all sessions for a specific logged-in user."""
        try:
            response = self.supabase.table("sessions").select("*").eq("user_id", user_id).order("created_at", desc=True).execute()
            return response.data
        except Exception as e:
            print(f"Error fetching sessions: {e}")
            return []

    def get_session_details(self, session_id):
        """Retrieves full details for a specific session."""
        try:
            meta = self.supabase.table("sessions").select("*").eq("id", session_id).single().execute().data
            metrics = self.supabase.table("metrics").select("*").eq("session_id", session_id).single().execute().data
            risks = self.supabase.table("risks").select("*").eq("session_id", session_id).execute().data

            return {
                'meta': (meta['player_name'], meta['created_at'], meta['video_filename']),
                'metrics': list(metrics.values()) if metrics else [],
                'risks': risks
            }
        except Exception as e:
            print(f"Error fetching details: {e}")
            return None

import numpy as np
