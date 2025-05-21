"""
astro_etl/utils/transformations.py

Astrophysical transformation utilities for the Gaia DR3 ETL pipeline.
Includes conversions for distance, absolute magnitude, and proper motion.

Author: Your Name
Date: 2025-05-21
"""

import numpy as np
from typing import Union

def parallax_to_distance(parallax_mas: Union[float, np.ndarray]) -> Union[float, np.ndarray]:
    """
    Convert parallax (in milliarcseconds) to distance in parsecs.
    Negative or zero parallaxes return np.inf.

    Parameters
    ----------
    parallax_mas : float or np.ndarray
        Parallax in milliarcseconds (mas).

    Returns
    -------
    distance_pc : float or np.ndarray
        Distance in parsecs (pc).
    """
    parallax_arcsec = np.asarray(parallax_mas) / 1000.0
    # Avoid division by zero or negative values (invalid physical distances)
    with np.errstate(divide='ignore', invalid='ignore'):
        distance_pc = np.where(parallax_arcsec > 0, 1.0 / parallax_arcsec, np.inf)
    return distance_pc

def compute_abs_mag_g(phot_g_mean_mag: Union[float, np.ndarray], distance_pc: Union[float, np.ndarray]) -> Union[float, np.ndarray]:
    """
    Compute absolute G magnitude from apparent magnitude and distance.

    Parameters
    ----------
    phot_g_mean_mag : float or np.ndarray
        Apparent G-band magnitude.
    distance_pc : float or np.ndarray
        Distance in parsecs.

    Returns
    -------
    abs_mag : float or np.ndarray
        Absolute G-band magnitude.

    Notes
    -----
    Uses the distance modulus formula:
    M_G = m_G - 5 * (log10(distance_pc) - 1)
    """
    with np.errstate(divide='ignore', invalid='ignore'):
        abs_mag = phot_g_mean_mag - 5 * (np.log10(distance_pc) - 1)
    return abs_mag

def total_proper_motion(pmra: Union[float, np.ndarray], pmdec: Union[float, np.ndarray]) -> Union[float, np.ndarray]:
    """
    Compute total proper motion from pmra and pmdec (in mas/yr).

    Parameters
    ----------
    pmra : float or np.ndarray
        Proper motion in RA (mas/yr).
    pmdec : float or np.ndarray
        Proper motion in Dec (mas/yr).

    Returns
    -------
    pm_total : float or np.ndarray
        Total proper motion (mas/yr).
    """
    return np.sqrt(np.asarray(pmra)**2 + np.asarray(pmdec)**2)
