"""
dashboard/plots.py

========================================
Advanced Plotting Functions for Gaia DR3 Dashboard
========================================

This module provides specialized visualizations for Gaia DR3 stellar catalogs,
optimized for interactive exploration and scientific interpretation via Plotly.

Functions:
    - hr_diagram: Interactive Hertzsprung–Russell diagram with empirical main sequence overlay.
    - sky_map: Equatorial sky map using Mollweide projection, colored by G magnitude.
    - pm_plot: Proper motion scatter plot (pmRA vs pmDec), with optional high-PM highlighting.
    - histogram: High-quality histograms for any numerical column.

These visualizations are tailored for astrophysical data analysis, supporting
stellar population studies, kinematics, and survey completeness investigations.
"""

import plotly.express as px
import plotly.graph_objects as go
import numpy as np
import pandas as pd

def hr_diagram(
    df: pd.DataFrame,
    use_abs_mag: bool = True,
    color_by: str = "parallax"
) -> go.Figure:
    """
    Create an interactive Hertzsprung–Russell (HR) diagram with a real Gaia main sequence overlay.

    Parameters
    ----------
    df : pd.DataFrame
        Must contain 'bp_rp', magnitude column(s).
    use_abs_mag : bool
        If True, plot absolute G magnitude; else use apparent.
    highlight_main_sequence : bool
        Overlay empirical Gaia main sequence fit.
    color_by : str
        Data column for color scale (default: 'parallax').

    Returns
    -------
    plotly.graph_objects.Figure
    """
    y_col = "abs_mag_g" if use_abs_mag and "abs_mag_g" in df else "phot_g_mean_mag"
    if "bp_rp" not in df or y_col not in df:
        raise ValueError("DataFrame must contain 'bp_rp' and a magnitude column.")

    fig = px.scatter(
        df, x="bp_rp", y=y_col,
        color=color_by if color_by in df else None,
        color_continuous_scale="Viridis",
        hover_data=["source_id", "ra", "dec", "parallax", "phot_g_mean_mag", "bp_rp"],
        labels={
            "bp_rp": "BP−RP color (mag)",
            y_col: "Absolute G mag" if use_abs_mag else "Apparent G mag",
            color_by: color_by.replace("_", " ").title() if color_by in df else "",
        },
        title="Hertzsprung–Russell Diagram"
    )
    fig.update_yaxes(autorange="reversed", title_text=fig.layout.yaxis.title.text)
    fig.update_layout(
        legend_title="Color By",
        font=dict(size=14),
        margin=dict(l=60, r=30, t=50, b=50),
        height=600
    )


    return fig

def sky_map(df: pd.DataFrame) -> go.Figure:
    """
    Create an all-sky map (Mollweide projection) colored by Gaia G magnitude, 
    with country outlines for orientation.

    Parameters
    ----------
    df : pd.DataFrame
        Must have 'ra', 'dec', 'phot_g_mean_mag'.

    Returns
    -------
    plotly.graph_objects.Figure
    """
    required_cols = {"ra", "dec", "phot_g_mean_mag"}
    if not required_cols.issubset(df):
        raise ValueError(f"DataFrame must contain columns: {required_cols}")

    fig = px.scatter_geo(
        df,
        lon="ra",
        lat="dec",
        color="phot_g_mean_mag",
        color_continuous_scale="Viridis_r",  # Faint stars are yellow/white
        title="Sky Map (Mollweide Projection, Equatorial Coordinates)",
        labels={
            "ra": "Right Ascension (deg)",
            "dec": "Declination (deg)",
            "phot_g_mean_mag": "G mag"
        },
        projection="mollweide",
        hover_name="source_id",
        hover_data=["phot_g_mean_mag", "ra", "dec"]
    )
    fig.update_geos(
        showcoastlines=True,
        showland=True,
        showcountries=True,
        landcolor="rgba(220, 220, 220, 0.2)",  # Soft background for land
        showframe=False,
        fitbounds="locations",
        lonaxis_showgrid=True,
        lataxis_showgrid=True,
        resolution=110
    )
    fig.update_layout(
        height=300,
        font=dict(size=14),
        margin=dict(l=0, r=0, t=0, b=0)
    )
    return fig

def pm_plot(df: pd.DataFrame, highlight_high_pm: bool = False) -> go.Figure:
    """
    Create a proper motion scatter plot (pmRA vs pmDec), color-coded by total proper motion.

    Parameters
    ----------
    df : pd.DataFrame
        Must include "pmra" and "pmdec", and preferably "pm_total".
    highlight_high_pm : bool, optional
        Highlight stars with very high proper motion (pm_total > 100 mas/yr).

    Returns
    -------
    plotly.graph_objects.Figure
    """
    required_cols = {"pmra", "pmdec"}
    if not required_cols.issubset(df):
        raise ValueError("DataFrame must contain 'pmra' and 'pmdec'.")
    color_col = "pm_total" if "pm_total" in df else None

    fig = px.scatter(
        df,
        x="pmra", y="pmdec",
        color=color_col,
        color_continuous_scale="Plasma",
        labels={
            "pmra": "Proper Motion RA (mas/yr)",
            "pmdec": "Proper Motion Dec (mas/yr)",
            "pm_total": "Total Proper Motion (mas/yr)"
        },
        title="Proper Motion Vector Scatter"
    )
    fig.update_layout(
        font=dict(size=14),
        height=600,
        margin=dict(l=50, r=30, t=50, b=50),
        legend_title="Total PM"
    )

    if highlight_high_pm and color_col:
        high_pm = df[df["pm_total"] > 100]
        if not high_pm.empty:
            fig.add_trace(go.Scatter(
                x=high_pm["pmra"], y=high_pm["pmdec"],
                mode="markers",
                marker=dict(symbol="star", size=12, color="red"),
                name="High PM (>100 mas/yr)",
                showlegend=True
            ))

    return fig

def histogram(
    df: pd.DataFrame,
    column: str,
    xlabel: str,
    nbins: int = 30
) -> go.Figure:
    """
    Plot a histogram of any column in the dataframe.

    Parameters
    ----------
    df : pd.DataFrame
    column : str
        Name of the column to plot.
    xlabel : str
        Label for the x-axis.
    nbins : int, optional
        Number of histogram bins.

    Returns
    -------
    plotly.graph_objects.Figure
    """
    if column not in df or df.empty:
        return go.Figure()
    fig = px.histogram(
        df,
        x=column,
        nbins=nbins,
        labels={column: xlabel},
        color_discrete_sequence=["#6387A6"]
    )
    fig.update_layout(
        title=f"{xlabel} Distribution",
        bargap=0.1,
        font=dict(size=14),
        height=450,
        margin=dict(l=50, r=30, t=40, b=50)
    )
    return fig
