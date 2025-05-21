"""
dashboard/sidebar.py

Sidebar content for Gaia DR3 dashboard: scientific explanations and project context.

"""

import streamlit as st

def sidebar_content():
    """
    Render the sidebar with scientific context, usage instructions, and references.
    """
    st.sidebar.title("About the Gaia DR3 Dashboard")
    st.sidebar.markdown(
        """
        Explore a scientific subset of the [Gaia DR3](https://gea.esac.esa.int/archive/) stellar catalog:

        - **Hertzsprung–Russell Diagram**: Plot stars by their color and brightness.
        - **Sky Map**: Visualize positions in the sky.
        - **Proper Motion**: Explore stellar velocities and clusters.

        ---
        ### How to Use
        - Use sidebar filters to select stars by distance (parallax), brightness, and color.
        - Toggle “Show Absolute Magnitude” for physical (distance-corrected) HR diagrams.
        - Try presets for solar neighborhood, open clusters, and high proper motion stars.

        ---
        ### What is Gaia?
        Gaia is a European Space Agency mission charting over a billion stars in our Galaxy with unprecedented precision. This dashboard lets you interactively explore real Gaia DR3 data.

        ---
        **Project by Christopher Crow**  
        [Project GitHub](https://github.com/christophercrow/gaia-dr3-dashboard)  
        [More on Gaia](https://www.cosmos.esa.int/web/gaia/science-performance)
        """
    )
