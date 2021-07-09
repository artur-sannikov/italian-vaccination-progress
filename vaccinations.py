import pandas as pd
import os
from kaggle.api.kaggle_api_extended import KaggleApi

vax_administration = pd.read_csv(
    "https://raw.githubusercontent.com/italia/covid19-opendata-vaccini/master/dati/somministrazioni-vaccini-latest.csv"
)

# Change current working directory to project's root directory
proj_dir = os.path.abspath(__file__)  # Absolute path to config.py
dir_name = os.path.dirname(proj_dir)  # Extract directory name of project's root
os.chdir(dir_name)

# Translate columns from English into Italian
renamed_cols = {
    "data_somministrazione": "administration_date",
    "fornitore": "supplier",
    "area": "region",
    "fascia_anagrafica": "age_range",
    "sesso_maschile": "males",
    "sesso_femminile": "females",
    "categoria_operatori_sanitari_sociosanitari": "healthcare_workers",
    "categoria_personale_non_sanitario": "non_healthcare_workers",
    "categoria_ospiti_rs+a": "care_home_patients",
    "categoria_60_69": "category_60_69",
    "categoria_70_79": "category_70_79",
    "categoria_soggetti_fragili": "vulnerable_subjects",
    "categoria_over80": "over_80",
    "categoria_forze_armate": "armed_forces",
    "categoria_personale_scolastico": "school_staff",
    "categoria_altro": "others",
    "prima_dose": "first_dose",
    "seconda_dose": "second_dose",
    "codice_NUTS1": "NUTS1_code",
    "codice_NUTS2": "NUTS2_code",
    "codice_regione_ISTAT": "ISTAT_regional_code",
    "nome_area": "region_name",
}
vax_administration = vax_administration.rename(renamed_cols, axis="columns")

vax_administration.to_csv("./data/italian_vaccination.csv", index=False)

# Kaggle authentication
api = KaggleApi()
api.authenticate()

# Create a new version of the data set
api.dataset_create_version(folder="./data", version_notes="Daily Update")
