# Gaia DR3 ETL & Interactive Dashboard

**A full-stack pipeline for querying, processing, and exploring Gaia DR3 data with scientific visualizations.**

![Example Dashboard](example_dashboard.png)

---

## Project Overview

This project provides an **end-to-end, modular workflow** for extracting astrophysical insights from the ESA Gaia DR3 catalog.
It is built for **astronomers, data scientists, and students** who want to:

* Efficiently **fetch, clean, and manage** Gaia DR3 data.
* Store the data in a scalable **PostgreSQL** database.
* **Explore** and **visualize** the data interactively through a modern dashboard.

---

## Features

* **Configurable ETL pipeline:** Download, clean, and load selected Gaia DR3 data into PostgreSQL using Python.
* **Extensible data models:** Modular, well-documented scripts for further analysis or pipeline customization.
* **Interactive dashboard:** Built with Streamlit and Plotly for live data filtering, custom plots, and scientific exploration.
* **Dockerized deployment:** Run everything locally or in the cloud using Docker Compose.
* **Tested workflow:** Includes testing scripts for robust development.

---

## Folder Structure

```
.
├── astro_etl/            # ETL pipeline: fetch, clean, load Gaia DR3 data
├── dashboard/            # Streamlit dashboard app (main: app.py)
├── data/                 # (Optional) Local data storage
├── scripts/              # SQL and migration scripts for PostgreSQL
├── tests/                # Unit tests for ETL and dashboard modules
├── .env                  # Environment variables (DB credentials, etc.)
├── config.yaml           # Pipeline & dashboard config (sample included)
├── docker-compose.yml    # Orchestrate full stack with Docker
├── requirements.txt      # Python dependencies
├── pyproject.toml        # Project metadata
├── example_dashboard.png # Sample dashboard screenshot
└── README.md             # Project documentation
```

---

## Getting Started

### 1. **Clone the Repository**

```bash
git clone https://github.com/YOUR_USERNAME/gaia_dr3_dashboard.git
cd gaia_dr3_dashboard
```

### 2. **Set Up Environment**

* **Install Python 3.8+** and [pip](https://pip.pypa.io/en/stable/).

* *(Recommended)* Create a virtual environment:

  ```bash
  python -m venv venv
  source venv/bin/activate  # On Windows: venv\Scripts\activate
  ```

* **Install dependencies:**

  ```bash
  pip install -r requirements.txt
  ```

### 3. **Configure Database**

* Make sure you have a local or cloud **PostgreSQL** instance running.

* Copy `.env.example` to `.env` (or create `.env`) and set your database connection string:

  ```
  DATABASE_URL=postgresql://user:password@localhost:5432/gaia
  ```

* Run the migration scripts to set up the database schema:

  ```bash
  psql -U user -d gaia -f scripts/schema.sql
  ```

### 4. **Run the ETL Pipeline**

* **Configure your ETL pipeline** in `config.yaml`.
* Download, clean, and load data:

  ```bash
  python -m astro_etl.load_data
  ```

### 5. **Start the Dashboard**

```bash
cd dashboard
streamlit run app.py
```

* Access the dashboard in your browser at `http://localhost:8501`.

---

## Dockerized Workflow (Optional)

To launch the **database, ETL, and dashboard** all at once:

```bash
docker-compose up --build
```

* Modify `docker-compose.yml` as needed for your environment.

---

## Key Modules

* `astro_etl/`:

  * `data_fetcher.py`: Downloads Gaia DR3 data.
  * `data_cleaner.py`: Cleans and preprocesses raw data.
  * `database.py`: Handles database connections and queries.
  * `models.py`: Database models (SQLAlchemy).
  * `tiling_fetch.py`: Utilities for sky tiling queries.

* `dashboard/`:

  * `app.py`: Main Streamlit entry point.
  * `plots.py`: Generates interactive scientific plots (e.g., HR diagram, sky map).
  * `sidebar.py`: Sidebar with filters and info.
  * `data_loader.py`: Loads data from the database.

---

## Testing

To run unit tests:

```bash
pytest
```

---

## Example Usage

Explore features such as:

* Interactive Hertzsprung–Russell diagram
* Sky position maps
* Proper motion visualizations
* Custom histogram queries

---

## Requirements

* Python 3.8+
* PostgreSQL 12+
* See `requirements.txt` for Python dependencies:

  ```
  astroquery
  astropy
  sqlalchemy
  psycopg2-binary
  pandas
  numpy
  pyyaml
  streamlit
  plotly
  python-dotenv
  pytest
  ```

---

## Contributing

Pull requests are welcome!
Feel free to open issues for suggestions, bug reports, or new features.

---

## License

MIT License.

---

## Acknowledgments

* [ESA Gaia Mission](https://www.cosmos.esa.int/web/gaia)
* [Astroquery](https://astroquery.readthedocs.io/)
* [Astropy](https://www.astropy.org/)
* [Streamlit](https://streamlit.io/)

---

## Contact

For questions or collaboration, open an issue or contact \[github.com/christophercrow].

---

**Happy exploring the galaxy!** 🌌


