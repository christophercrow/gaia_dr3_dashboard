# Makefile

.PHONY: run_pipeline dashboard test tile_fetch tile_pipeline

run_pipeline:
	python -m astro_etl.data_fetcher
	python -m astro_etl.data_cleaner
	python -m astro_etl.load_data

dashboard:
	PYTHONPATH=$(pwd) streamlit run dashboard/app.py

test:
	pytest --maxfail=1 --disable-warnings

tile_fetch:
	python -m astro_etl.tiling_fetch

tile_pipeline:
	python -m astro_etl.tiling_fetch
	python -m astro_etl.data_cleaner data/tiling_gaia.csv
	python -m astro_etl.load_data data/cleaned_tiling_gaia.csv
