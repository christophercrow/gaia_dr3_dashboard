"""
dashboard/data_loader.py

Utility for loading Gaia DR3 data from the database for dashboard visualization.

Author: Your Name
Date: 2025-05-21
"""

import pandas as pd
from sqlalchemy import create_engine
from typing import Optional


def load_dashboard_data(
    db_url: str, 
    table: str = "gaia_source", 
    limit: Optional[int] = 50000
) -> pd.DataFrame:
    engine = create_engine(db_url)
    query = f"SELECT * FROM {table}"
    if limit is not None:
        query += f" LIMIT {limit}"
    df = pd.read_sql(query, engine)
    print("Loaded dashboard data shape:", df.shape)
    print(df.head())
    return df


# def load_dashboard_data(
#     db_url: str, 
#     table: str = "gaia_source", 
#     limit: Optional[int] = 50000
# ) -> pd.DataFrame:
#     """
#     Load Gaia DR3 data from a database table for visualization.

#     Parameters
#     ----------
#     db_url : str
#         SQLAlchemy database URL.
#     table : str, optional
#         Table name to query from (default: 'gaia_source').
#     limit : int or None, optional
#         Max number of rows to load (default: 50,000). Set to None for all.

#     Returns
#     -------
#     pd.DataFrame
#         Resulting DataFrame for plotting and analysis.
#     """
#     engine = create_engine(db_url)
#     query = f"SELECT * FROM {table}"
#     if limit is not None:
#         query += f" LIMIT {limit}"
#     df = pd.read_sql(query, engine)
#     return df
