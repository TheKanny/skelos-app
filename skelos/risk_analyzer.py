import numpy as np
# No imports from skelos.utils needed here, but keeping it clean

class RiskAnalyzer:
    def __init__(self):
        # Thresholds based on biomechanical poster data
        self.HIP_MOBILITY_THRESHOLD = 20.0  # Degrees of internal rotation
        self.X_FACTOR_MAX_SAFE = 45.0       # Degrees of torsion

    def analyze_risks(self, bio_data):
        """
        Analyzes biomechanical data for injury risks.
        Returns a list of risk dictionaries including improvement steps.
        """
        risks = []

        # 1. Lumbar Spine Risk
        max_x = np.max(bio_data['x_factor'])
        max_pelvis = np.max(np.abs(bio_data['pelvis_angle']))

        if max_x > 50.0 and max_pelvis < self.HIP_MOBILITY_THRESHOLD:
            risks.append({
                'type': 'lumbar',
                'level': 'High',
                'message': 'Critical risk of lumbar compensation. Limited hip rotation is forcing the lower back to over-rotate dangerously.',
                'improvement_steps': [
                    "Immediate focus on pelvic tilts to mobilize the lower spine",
                    "Execute 90/90 hip switches (3 sets of 10)",
                    "Engage core stability via Dead-bugs before swinging",
                    "Focus on hip-first transition in the downswing"
                ]
            })
        elif max_x > 45.0:
            risks.append({
                'type': 'lumbar',
                'level': 'High',
                'message': 'High X-Factor detected. This level of torsion puts significant stress on the lumbar discs.',
                'improvement_steps': [
                    "Plank rotations for core stability",
                    "Gentle thoracic spine rotations",
                    "Ensure lead hip is fully cleared during follow-through"
                ]
            })
        elif max_x > self.X_FACTOR_MAX_SAFE:
            risks.append({
                'type': 'lumbar',
                'level': 'Moderate',
                'message': 'Elevated X-Factor detected. Ensure core stability to manage torso torque.',
                'improvement_steps': [
                    "Plank rotations for core stability",
                    "Gentle thoracic spine rotations",
                    "Ensure lead hip is fully cleared during follow-through"
                ]
            })

        # 2. Lead Arm/Wrist Risk
        wrist_vel = bio_data['wrist_vel']
        if np.max(wrist_vel) > 0.5: # Normalized threshold
            risks.append({
                'type': 'wrist',
                'level': 'Moderate',
                'message': 'High impact forces detected. Risk of lead wrist hyperextension.',
                'improvement_steps': [
                    "Wrist curls for forearm strength",
                    "Eccentric wrist extensions",
                    "Focus on a 'flat' lead wrist at impact",
                    "Check grip pressure to avoid excessive tension"
                ]
            })

        # 3. Shoulder Risk
        if max_x > 60: # Extreme torsion usually stresses shoulders
            risks.append({
                'type': 'shoulder',
                'level': 'Moderate',
                'message': 'Extreme torsion may lead to shoulder impingement.',
                'improvement_steps': [
                    "Scapular retractions (Squeeze blades together)",
                    "Internal/External rotation with bands",
                    "Thoracic mobility foam rolling"
                ]
            })

        return risks
