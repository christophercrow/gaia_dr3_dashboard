import streamlit as st
import os
import numpy as np

from dashboard.data_loader import load_dashboard_data
from dashboard.plots import hr_diagram, sky_map, pm_plot, histogram
from dashboard.sidebar import sidebar_content

st.set_page_config(page_title="Gaia DR3 Interactive Dashboard", layout="wide", page_icon=":milky_way:")

# --- SIDEBAR (About, Filters, Download) ---
sidebar_content()

db_url = os.getenv("DATABASE_URL", "postgresql://user:password@localhost:5432/gaia")

@st.cache_data(show_spinner="Loading Gaia DR3 data…")
def get_data():
    return load_dashboard_data(db_url)

with st.spinner("Loading data…"):
    df = get_data()

# ---- Data sanity: always show what loaded
st.sidebar.info(f"Loaded {len(df):,} stars from database.")
st.sidebar.write(df.head(2))
st.sidebar.markdown("**Quick Stats:**")
st.sidebar.write(df.describe())

# ---- Compute required columns if missing ----
if "pm_total" not in df or df["pm_total"].isnull().all():
    if "pmra" in df and "pmdec" in df:
        df["pm_total"] = np.sqrt(df["pmra"].astype(float).fillna(0)**2 + df["pmdec"].astype(float).fillna(0)**2)
    else:
        df["pm_total"] = np.nan

if "abs_mag_g" not in df or df["abs_mag_g"].isnull().all():
    if "parallax" in df and "phot_g_mean_mag" in df:
        parallax_safe = df["parallax"].replace([0, np.nan], 0.01)
        df["abs_mag_g"] = df["phot_g_mean_mag"] - 5 * np.log10(1000 / parallax_safe) + 5
    else:
        df["abs_mag_g"] = np.nan
        

# Helper to check if a column is fully valid numeric (not all NaN)
def valid_numeric_col(col):
    return (col in df) and (df[col].dtype in [float, int, np.float64, np.int64]) and (df[col].notnull().any())

# --- Smart slider min/max: return fallback if column is not valid
def col_range(col, pad=(0, 0)):
    if valid_numeric_col(col):
        vals = df[col].dropna()
        vmin, vmax = float(vals.min()), float(vals.max())
        vmin -= pad[0]
        vmax += pad[1]
        if vmin == vmax:
            vmax += 1.0
        return round(vmin, 2), round(vmax, 2)
    else:
        st.sidebar.warning(f"Column '{col}' is missing or all NaN, using default slider.")
        return 0.0, 1.0# --- Presets & Filters ---
st.sidebar.header("Filters")
preset = st.sidebar.selectbox(
    "Quick Presets",
    [
        "Manual", 
        "Solar Neighborhood (<50pc)", 
        "Bright Stars (G < 8)", 
        "High Proper Motion (>50)", 
        "Main Sequence", 
        "Nearby Red Dwarfs"
    ],
    index=0
)

if preset == "Manual":
    parallax_min_val, parallax_max_val = col_range("parallax", pad=(0.01, 1))
    gmag_min_val, gmag_max_val = col_range("phot_g_mean_mag", pad=(0.0, 0.5))
    bprp_min_val, bprp_max_val = col_range("bp_rp", pad=(0.05, 0.2))
    pm_total_min_val, pm_total_max_val = col_range("pm_total", pad=(0, 5))

    parallax_min, parallax_max = st.sidebar.slider(
        "Parallax (mas)",
        parallax_min_val, parallax_max_val,
        (parallax_min_val, parallax_max_val),
        step=0.01
    )
    gmag_min, gmag_max = st.sidebar.slider(
        "G magnitude",
        gmag_min_val, gmag_max_val,
        (gmag_min_val, gmag_max_val),
        step=0.01
    )
    bprp_min, bprp_max = st.sidebar.slider(
        "BP−RP color",
        bprp_min_val, bprp_max_val,
        (bprp_min_val, bprp_max_val),
        step=0.01
    )
    pm_total_min, pm_total_max = st.sidebar.slider(
        "Total Proper Motion (mas/yr)",
        pm_total_min_val, pm_total_max_val,
        (pm_total_min_val, pm_total_max_val),
        step=0.1
    )
else:
    # SCIENTIFIC PRESETS (only *set* the filter values, don't filter here)
    if preset == "Solar Neighborhood (<50pc)":
        parallax_min, parallax_max = 20, 50
        gmag_min, gmag_max = 0.0, 15.0
        bprp_min, bprp_max = 0.0, 3.0
        pm_total_min, pm_total_max = 0.0, 100.0
    elif preset == "Bright Stars (G < 8)":
        parallax_min, parallax_max = 0.1, 50.0
        gmag_min, gmag_max = 0.0, 8.0
        bprp_min, bprp_max = 0.0, 3.0
        pm_total_min, pm_total_max = 0.0, 100.0
    elif preset == "High Proper Motion (>50)":
        parallax_min, parallax_max = 0.1, 50.0
        gmag_min, gmag_max = 0.0, 15.0
        bprp_min, bprp_max = 0.0, 3.0
        pm_total_min, pm_total_max = 50.0, 500.0
    elif preset == "Main Sequence":
        parallax_min, parallax_max = 0.1, 50.0
        gmag_min, gmag_max = 3.0, 8.0
        bprp_min, bprp_max = 0.5, 2.0
        pm_total_min, pm_total_max = 0.0, 100.0
    elif preset == "Nearby Red Dwarfs":
        parallax_min, parallax_max = 20.0, 50.0
        gmag_min, gmag_max = 8.0, 15.0
        bprp_min, bprp_max = 1.3, 3.0
        pm_total_min, pm_total_max = 0.0, 100.0

# --- Data Filtering with robust column presence ---
mask = np.ones(len(df), dtype=bool)
filter_info = []
if valid_numeric_col("parallax"):
    mask &= df["parallax"].between(parallax_min, parallax_max)
else:
    filter_info.append("Parallax not available, filter skipped.")
if valid_numeric_col("phot_g_mean_mag"):
    mask &= df["phot_g_mean_mag"].between(gmag_min, gmag_max)
else:
    filter_info.append("G magnitude not available, filter skipped.")
if valid_numeric_col("bp_rp"):
    mask &= df["bp_rp"].between(bprp_min, bprp_max)
else:
    filter_info.append("BP−RP color not available, filter skipped.")
if valid_numeric_col("pm_total"):
    mask &= df["pm_total"].between(pm_total_min, pm_total_max)
else:
    filter_info.append("Proper motion not available, filter skipped.")

df_filt = df[mask].copy()
for msg in filter_info:
    st.sidebar.warning(msg)

if df_filt.empty:
    st.warning("No stars match the current filters. Try broadening your selection or resetting filters.")
    st.stop()
    
# --- Always handle empty data gracefully ---
if df_filt.empty:
    st.warning("No stars match the current filters. Try broadening your selection or resetting filters.")
    st.stop()

st.sidebar.markdown("---")
st.sidebar.download_button(
    label="Download Filtered Data as CSV",
    data=df_filt.to_csv(index=False),
    file_name="filtered_gaia.csv",
    mime="text/csv"
)

# --- Main Layout ---
st.title("Gaia DR3 Interactive Dashboard")
with st.expander("About this Dashboard & Science Context", expanded=True):
    st.write(
        """
        **Explore real stellar populations from the [ESA Gaia DR3](https://gea.esac.esa.int/archive/).**
        - HR diagram: Color/brightness, stellar types, main sequence
        - Sky map: True positions, clusters, moving groups
        - Proper motion: Stellar kinematics, high-velocity stars

        This tool is designed for both public engagement and serious research use.  
        [Project GitHub](https://github.com/christophercrow/gaia-dr3-dashboard)
        """
    )

# --- Statistics summary ---
st.markdown(
    f"<span style='font-size:1.1em'><b>{len(df_filt):,} stars</b> selected | "
    f"Mean distance: <b>{round(df_filt['parallax'].apply(lambda x: 1000/x if x > 0 else np.nan).mean() or 0, 1)} pc</b> | "
    f"Brightest G: <b>{df_filt['phot_g_mean_mag'].min():.2f}</b> | "
    f"Median BP–RP: <b>{df_filt['bp_rp'].median():.2f}</b></span>",
    unsafe_allow_html=True,
)
st.plotly_chart(
    sky_map(df_filt),
    use_container_width=True,
)
col1, col2 = st.columns([1.5, 1.5])
with col1:
    st.plotly_chart(
        hr_diagram(df_filt, use_abs_mag=True),
        use_container_width=True,
    )
    st.plotly_chart(
        pm_plot(df_filt, highlight_high_pm=True),
        use_container_width=True,
    )
with col2:
    st.markdown("#### Histograms")
    st.plotly_chart(histogram(df_filt, "phot_g_mean_mag", "G Magnitude"), use_container_width=True)
    st.plotly_chart(histogram(df_filt, "bp_rp", "BP–RP Color"), use_container_width=True)
    st.plotly_chart(histogram(df_filt, "parallax", "Parallax (mas)"), use_container_width=True)

with st.expander("Show Data Table", expanded=False):
    st.dataframe(df_filt, use_container_width=True)

st.markdown("---")
st.markdown(
    "Powered by [Streamlit](https://streamlit.io/) and [Plotly](https://plotly.com/python/). "
    "Data: ESA Gaia DR3."
)
