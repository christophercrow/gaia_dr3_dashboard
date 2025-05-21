# Gaia DR3 ETL & Interactive Dashboard

**A full-stack pipeline for querying, processing, and exploring Gaia DR3 data with scientific visualizations.**

![example_dashboard.png](example_dashboard.png)

---

## Project Overview

This project demonstrates an end-to-end, modular workflow for extracting astrophysical insight from the ESA Gaia DR3 catalog.  
It features:

- **Configurable ETL pipeline:** Download, clean, and load selected Gaia DR3 data into a PostgreSQL database using modern Python tools.
- **Interactive Streamlit dashboard:** Explore Hertzsprung–Russell diagrams, sky maps, and proper motion plots in real time.
- **Modular, testable codebase:** All components are unit-tested and can be extended for advanced research or teaching.
- **Reproducible deployment:** Docker, Makefile, and .env-driven configuration make setup fast on any platform.

## Scientific Motivation

The Gaia mission has transformed our understanding of the Milky Way by mapping the positions, distances, and motions of more than a billion stars.  
This project provides a *research-ready* starting point for:

- Exploring the solar neighborhood
- Identifying open clusters and stellar streams
- Studying high-proper-motion stars
- Teaching data-driven astrophysics with real data

## Directory Structure

```

gaia\_dr3\_dashboard/
│
├── astro\_etl/                # ETL pipeline (fetch, clean, transform, load)
│   ├── config.py
│   ├── data\_fetcher.py
│   ├── data\_cleaner.py
│   ├── load\_data.py
│   ├── database.py
│   ├── models.py
│   └── utils/
│       ├── transformations.py
│       └── logging\_util.py
├── dashboard/                # Streamlit app and plotting utilities
│   ├── app.py
│   ├── plots.py
│   ├── sidebar.py
│   └── data\_loader.py
├── scripts/                  # Database schema, partitioning, migration SQL
├── tests/                    # Unit and integration tests (pytest)
├── .github/workflows/ci.yml  # Continuous Integration
├── .env.example
├── config.yaml
├── requirements.txt
├── pyproject.toml
├── docker-compose.yml
├── Makefile
└── README.md

````

---

## 🛠️ Setup Instructions

### 1. **Clone and Install**

```bash
git clone https://github.com/yourusername/gaia-dr3-dashboard.git
cd gaia-dr3-dashboard
pip install -r requirements.txt
````

### 2. **Set Up PostgreSQL Database**

**Recommended:** Use Docker for portability.

```bash
docker-compose up -d db
```

Or install PostgreSQL locally.

**Create the schema:**

```bash
psql $DATABASE_URL -f scripts/schema.sql
```

### 3. **Configure Your Environment**

* Copy `.env.example` to `.env` and edit as needed.
* Edit `config.yaml` to set your sky region, limits, and filters.

### 4. **Run the ETL Pipeline**

```bash
make run_pipeline
```

This will:

* Query Gaia DR3 (using Astroquery and ADQL)
* Clean and transform the data
* Load it into the PostgreSQL database

### 5. **Launch the Dashboard**

```bash
make dashboard
```

Then open `http://localhost:8501` in your browser.

---

## Testing

Run all tests with:

```bash
make test
```

or

```bash
pytest tests/
```

---

## Example Scientific Use Cases

* **Solar Neighborhood:**
  Set `parallax_min: 20` (within 50pc), see the HR diagram for local stellar types.

* **Open Clusters:**
  Set `center_ra`, `center_dec`, and `radius` to match a cluster (e.g., Pleiades: RA=56.75, Dec=24.12, r=2°), study cluster sequence.

* **High Proper Motion Stars:**
  Filter by `pm_total > 50 mas/yr` to find runaway or nearby stars.

* **Color-Magnitude Selection:**
  Use the sidebar sliders to identify main sequence, white dwarfs, or giants.

---

## Documentation

### ETL Pipeline

* **astro\_etl/config.py:** Loads config from `.env` and `config.yaml` for all modules.
* **astro\_etl/data\_fetcher.py:** Fetches Gaia data with custom ADQL query.
* **astro\_etl/data\_cleaner.py:** Cleans, filters, and computes derived quantities (distance, abs mag, proper motion).
* **astro\_etl/load\_data.py:** Loads cleaned data into PostgreSQL with SQLAlchemy ORM.

### Dashboard

* **dashboard/app.py:** Main Streamlit entry point, ties together filters, plots, and sidebar.
* **dashboard/plots.py:** Plotly visualizations: HR diagram, sky map, proper motion.
* **dashboard/sidebar.py:** Scientific explanations and links for users.

### Database

* **scripts/schema.sql:** PostgreSQL schema for the `gaia_source` table.
* **scripts/partitions.sql:** (Optional) Partitioning for very large datasets.
* **scripts/migration\_example.sql:** Example migration for adding new science columns.

### Utilities

* **astro\_etl/utils/transformations.py:** Astrophysical helper functions for distance, magnitude, motion.
* **astro\_etl/utils/logging\_util.py:** Consistent logging configuration.

### Testing

* **tests/**: Unit and integration tests for every pipeline stage and dashboard plot.
* **.github/workflows/ci.yml:** Continuous Integration (pytest + lint on push).

---

## References & Attribution

* [Gaia DR3 Archive](https://gea.esac.esa.int/archive/)
* [Astroquery Documentation](https://astroquery.readthedocs.io/)
* [Streamlit Docs](https://docs.streamlit.io/)
* [ESA Gaia Mission Overview](https://www.cosmos.esa.int/web/gaia/science-performance)

**Cite Gaia as:**
Gaia Collaboration et al. 2022, A\&A, 666, A1.
See [https://gea.esac.esa.int/archive/documentation/GDR3/](https://gea.esac.esa.int/archive/documentation/GDR3/)

---

## Acknowledgments

* Built with open-source tools for research, teaching, and portfolio demonstration.
* Project maintained by Christopher Crow ([@yourgithub](https://github.com/christophercrow))

---

# FAQ

**Q: Can I extend this to other catalogs or science cases?**
A: Yes! The ETL and dashboard code are modular—swap out the ADQL query, add new features, or connect to additional astronomical tables.

**Q: How big a dataset can this handle?**
A: The structure is robust for tens to hundreds of thousands of stars (as a demo). For millions, use the partitioning scripts and consider optimizing dashboard queries.

**Q: How do I deploy this for a team/class?**
A: Use Docker for the database and Streamlit Cloud or similar for the dashboard UI.

---

# Contributing

Pull requests, issues, and feature requests are always welcome!
For major changes, please open an issue first to discuss what you’d like to change.

---

