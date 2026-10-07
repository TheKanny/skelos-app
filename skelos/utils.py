import numpy as np

def calculate_angle(v1, v2):
    """Calculates the angle between two vectors in degrees."""
    unit_v1 = v1 / np.linalg.norm(v1)
    unit_v2 = v2 / np.linalg.norm(v2)
    dot_product = np.dot(unit_v1, unit_v2)
    # Clip for floating point errors
    angle = np.arccos(np.clip(dot_product, -1.0, 1.0))
    return np.degrees(angle)

def get_vector(p1, p2):
    """Returns the vector from p1 to p2."""
    return np.array(p2) - np.array(p1)

def normalize_angles(angles, baseline_index=0):
    """Sets the angle at baseline_index to 0 and offsets others."""
    baseline_val = angles[baseline_index]
    return angles - baseline_val
