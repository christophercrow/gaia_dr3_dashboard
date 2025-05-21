"""
astro_etl/models.py

SQLAlchemy ORM model(s) for the Gaia DR3 database schema.

"""

from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, BigInteger, Float, Integer

Base = declarative_base()

class GaiaSource(Base):
    """
    SQLAlchemy model for a Gaia DR3 source.

    Attributes
    ----------
    source_id : int
        Gaia source identifier (unique, primary key).
    ra : float
        Right Ascension (ICRS, degrees).
    dec : float
        Declination (ICRS, degrees).
    parallax : float
        Parallax (mas).
    phot_g_mean_mag : float
        G-band mean magnitude.
    bp_rp : float
        BP - RP color index (mag).
    distance_pc : float
        Distance in parsecs (derived).
    abs_mag_g : float
        Absolute G-band magnitude (derived).
    pmra : float
        Proper motion in RA (mas/yr).
    pmdec : float
        Proper motion in Dec (mas/yr).
    pm_total : float
        Total proper motion (mas/yr).
    healpix : int, optional
        HEALPix index (for partitioning), optional.
    """
    __tablename__ = "gaia_source"

    source_id = Column(BigInteger, primary_key=True, index=True, doc="Gaia source_id")
    ra = Column(Float, nullable=False, doc="Right Ascension (deg, ICRS)")
    dec = Column(Float, nullable=False, doc="Declination (deg, ICRS)")
    parallax = Column(Float, nullable=True, doc="Parallax (mas)")
    phot_g_mean_mag = Column(Float, nullable=True, doc="G mean magnitude")
    bp_rp = Column(Float, nullable=True, doc="BP - RP color (mag)")
    distance_pc = Column(Float, nullable=True, doc="Distance (parsec, computed)")
    abs_mag_g = Column(Float, nullable=True, doc="Absolute G mag (computed)")
    pmra = Column(Float, nullable=True, doc="Proper motion in RA (mas/yr)")
    pmdec = Column(Float, nullable=True, doc="Proper motion in Dec (mas/yr)")
    pm_total = Column(Float, nullable=True, doc="Total proper motion (mas/yr)")
    healpix = Column(Integer, nullable=True, doc="HEALPix index for partitioning (optional)")
