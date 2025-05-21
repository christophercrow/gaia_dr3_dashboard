"""
tests/test_utils.py

Tests for astro_etl.utils.transformations.
"""

import numpy as np
from astro_etl.utils.transformations import parallax_to_distance, compute_abs_mag_g, total_proper_motion

def test_parallax_to_distance_behavior():
    assert parallax_to_distance(10) == 100.0
    assert parallax_to_distance(0) == np.inf
    assert parallax_to_distance(-5) == np.inf

def test_compute_abs_mag_g_math():
    mag = compute_abs_mag_g(15.0, 100.0)
    # At 100 pc, abs mag = m - 5(log10(100) - 1) = m - 5(2-1) = m-5
    assert abs(mag - 10.0) < 1e-6

def test_total_proper_motion_vector():
    pm = total_proper_motion(3.0, 4.0)
    assert abs(pm - 5.0) < 1e-6
