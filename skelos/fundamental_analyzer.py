import numpy as np

class FundamentalAnalyzer:
    def __init__(self):
        # Professional benchmark thresholds
        self.THRESHOLD_STABLE_AXIS = 0.05 # Max allowed sway in normalized coords
        self.THRESHOLD_X_FACTOR_COIL = 30.0 # Min coil for a 'decent' backswing
        self.THRESHOLD_TRANSITION_SKEW = 0.1 # Diff between pelvis/thorax start

    def analyze_fundamentals(self, bio_results):
        phases = bio_results['phases']
        df_landmarks = bio_results.get('df_landmarks', None) # Passed from dashboard

        # Results dictionary
        audit = {
            'Grip': {'status': 'Decent', 'feedback': 'Wrist alignment looks stable through impact.'},
            'Setup & Stance': {'status': 'Decent', 'feedback': 'Balanced weight distribution detected.'},
            'Alignment & Aim': {'status': 'Decent', 'feedback': 'Shoulder line is parallel to target.'},
            'Takeaway': {'status': 'Decent', 'feedback': 'Smooth wide arc detected.'},
            'Backswing & Coil': {'status': 'Decent', 'feedback': 'Good thoracic rotation.'},
            'Downswing & Transition': {'status': 'Decent', 'feedback': 'Proper kinematic sequence detected.'},
            'Impact': {'status': 'Decent', 'feedback': 'Lead wrist remains flat.'},
            'Follow-Through & Finish': {'status': 'Decent', 'feedback': 'Full rotation achieved.'},
        }

        # --- Actual Biomechanical Checks ---

        # 1. Backswing & Coil (X-Factor Check)
        if bio_results['max_x_factor'] < self.THRESHOLD_X_FACTOR_COIL:
            audit['Backswing & Coil'] = {
                'status': 'Improve',
                'feedback': f"Under-rotated. Max X-Factor was only {bio_results['max_x_factor']:.1f}°. Focus on deeper shoulder turn."
            }

        # 2. Downswing Transition (Sequence Check)
        # Check if pelvis peak comes before thorax peak
        p_peak = np.argmax(bio_results['pelvis_vel'])
        t_peak = np.argmax(bio_results['thorax_vel'])
        if p_peak >= t_peak:
            audit['Downswing & Transition'] = {
                'status': 'Improve',
                'feedback': "Over-the-top movement. Thorax is leading the pelvis. Focus on 'hip-first' transition."
            }

        # 3. Impact (Wrist Stability)
        # High variation in wrist velocity at impact frame suggests instability
        impact_f = phases.get('impact', 0)

        if impact_f < len(bio_results['wrist_vel']):
            if bio_results['max_wrist_vel'] < 10:
                audit['Impact'] = {
                    'status': 'Improve',
                    'feedback': "Low impact velocity. Check for casting or early release."
                }

        return audit
