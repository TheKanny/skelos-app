import numpy as np

class ScoringEngine:
    def __init__(self):
        # Professional Benchmarks (Simplified for MVP)
        self.BENCHMARKS = {
            'x_factor': {'optimal_min': 30.0, 'optimal_max': 45.0},
            'sequence': {'ideal_order': ['pelvis', 'thorax', 'wrist']},
            'velocity_ratio': {'ideal_wrist_to_pelvis': 2.5} # Wrist should be significantly faster
        }

    def calculate_grade(self, value, min_val, max_val):
        if min_val <= value <= max_val: return 'S', 100
        if (max_val < value <= max_val + 10) or (min_val - 10 <= value < min_val): return 'A', 85
        if (max_val < value <= max_val + 20) or (min_val - 20 <= value < min_val): return 'B', 70
        if (max_val < value <= max_val + 30) or (min_val - 30 <= value < min_val): return 'C', 50
        return 'D', 30

    def evaluate_swing(self, bio_results, fundamental_report):
        # 1. Efficiency Grade (X-Factor)
        x_grade, x_score = self.calculate_grade(
            bio_results['max_x_factor'],
            self.BENCHMARKS['x_factor']['optimal_min'],
            self.BENCHMARKS['x_factor']['optimal_max']
        )

        # 2. Sequence Grade (Kinematic Sequence)
        p_peak = np.argmax(bio_results['pelvis_vel'])
        t_peak = np.argmax(bio_results['thorax_vel'])
        w_peak = np.argmax(bio_results['wrist_vel'])

        if p_peak < t_peak < w_peak:
            seq_grade, seq_score = 'S', 100
        elif p_peak < w_peak and t_peak < w_peak:
            seq_grade, seq_score = 'B', 70
        else:
            seq_grade, seq_score = 'D', 40

        # 3. Power Grade (Wrist Peak)
        w_vel = bio_results['max_wrist_vel']
        if w_vel > 20: p_grade, p_score = 'S', 100
        elif w_vel > 15: p_grade, p_score = 'A', 85
        elif w_vel > 10: p_grade, p_score = 'B', 70
        else: p_grade, p_score = 'C', 50

        # 4. Fundamental Audit Score (The "Checklist" Score)
        # Calculate percentage of fundamentals marked as 'Decent'
        total_fundamentals = len(fundamental_report)
        decent_count = sum(1 for item in fundamental_report.values() if item['status'] == 'Decent')
        audit_score = (decent_count / total_fundamentals) * 100

        # --- HYBRID WEIGHTING ---
        # 60% Biomechanical Pillars, 40% Fundamental Audit
        bio_weighted = (x_score * 0.4) + (seq_score * 0.4) + (p_score * 0.2)
        overall_score = (bio_weighted * 0.6) + (audit_score * 0.4)

        if overall_score >= 90: final_grade = 'S'
        elif overall_score >= 80: final_grade = 'A'
        elif overall_score >= 70: final_grade = 'B'
        elif overall_score >= 60: final_grade = 'C'
        elif overall_score >= 50: final_grade = 'D'
        else: final_grade = 'F'

        return {
            'overall_grade': final_grade,
            'overall_score': round(overall_score, 1),
            'pillars': {
                'Efficiency': {'grade': x_grade, 'score': x_score, 'metric': f"{bio_results['max_x_factor']:.1f}°"},
                'Sequence': {'grade': seq_grade, 'score': seq_score, 'metric': 'Correct Order' if seq_grade == 'S' else 'Out of Sync'},
                'Power': {'grade': p_grade, 'score': p_score, 'metric': f"{bio_results['max_wrist_vel']:.1f} v"},
                'Fundamentals': {'grade': 'N/A', 'score': round(audit_score, 1), 'metric': f"{decent_count}/{total_fundamentals} Decent"}
            }
        }
