"""
tests/test_dashboard.py

Unit tests for dashboard/data_loader and dashboard/plots.
"""

import pandas as pd
import plotly.graph_objects as go
from dashboard.plots import hr_diagram, sky_map, pm_plot

def example_df():
    # Minimal Gaia-like DataFrame
    return pd.DataFrame({
        "source_id": [1, 2, 3],
        "ra": [10.0, 20.0, 30.0],
        "dec": [-10.0, 0.0, 15.0],
        "parallax": [10.0, 12.0, 8.0],
        "phot_g_mean_mag": [11.1, 12.2, 13.3],
        "bp_rp": [0.7, 1.1, 1.8],
        "distance_pc": [100, 83.3, 125],
        "abs_mag_g": [6.1, 7.3, 7.5],
        "pmra": [2.0, 3.0, 4.0],
        "pmdec": [1.0, 2.0, 3.0],
        "pm_total": [2.2, 3.6, 5.0]
    })

def test_hr_diagram_returns_figure():
    df = example_df()
    fig = hr_diagram(df, use_abs_mag=True)
    assert isinstance(fig, go.Figure)
    # Should have x, y axes
    assert fig.data[0].x is not None
    assert fig.data[0].y is not None

def test_sky_map_returns_figure():
    df = example_df()
    fig = sky_map(df)
    assert isinstance(fig, go.Figure)
    assert fig.layout.title.text.startswith("Sky Map")

def test_pm_plot_returns_figure():
    df = example_df()
    fig = pm_plot(df)
    assert isinstance(fig, go.Figure)
    assert "Proper Motion" in fig.layout.title.text
