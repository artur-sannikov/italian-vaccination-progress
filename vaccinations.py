import pandas as pd
import os
import logging

# Initialize formatters
file_formatter = logging.Formatter(
    "%(asctime)s~%(levelname)s~%(message)s~module:%(module)s~function:%(module)s"
)
console_formatter = logging.Formatterconsole_formatter = logging.Formatter(
    "%(asctime)s~%(levelname)s -- %(message)s"
)

# Set handlers
file_handler = logging.FileHandler("logfile.log")
file_handler.setLevel(logging.WARN)
file_handler.setFormatter(file_formatter)
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)
console_handler.setFormatter(console_formatter)

logger = logging.getLogger()
logger.addHandler(file_handler)
logger.addHandler(console_handler)
logger.setLevel(logging.DEBUG)

# Try authentication
try:
    from kaggle.api.kaggle_api_extended import KaggleApi
except:
    logging.exception("Authentication failed")
    exit()


vax_administration = pd.read_csv(
    "https://raw.githubusercontent.com/italia/covid19-opendata-vaccini/master/dati/somministrazioni-vaccini-latest.csv"
)

# Change current working directory to project's root directory
proj_dir = os.path.abspath(__file__)  # Absolute path to config.py
dir_name = os.path.dirname(proj_dir)  # Extract directory name of project's root
os.chdir(dir_name)

# Translate columns from English into Italian
renamed_cols = {
    "data": "administration_date",
    "forn": "supplier",
    "area": "region",
    "eta": "age_range",
    "m": "males",
    "f": "females",
    "d1": "first_dose",
    "d2": "second_dose",
    "dpi": "previous_infection",
    "db1": "additional_booster_dose",
    "dbi": "booster_immuno",
    "db2": "second_booster",
    "N1": "NUTS1_code",
    "N2": "NUTS2_code",
    "ISTAT": "ISTAT_regional_code",
    "reg": "region_name",
}
vax_administration = vax_administration.rename(renamed_cols, axis="columns")

# Replace Pfizer Pediatrico to Pfizer for children
vax_administration["supplier"].replace(
    "Pfizer Pediatrico", "Pfizer for children", inplace=True
)

# Save in csv
vax_administration.to_csv("./data/italian_vaccination.csv", index=False)

# Kaggle authentication
api = KaggleApi()
api.authenticate()

# Create a new version of the data set
logging.info("Uploading new data set version")
api.dataset_create_version(folder="./data", version_notes="Daily Update")
