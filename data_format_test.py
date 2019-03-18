# Author: Cameron Brown
# Date: 16/03/2019
# Purpose: Test the PetsDataExtractor and PetsDataFormatter classes.

CSV_FILENAME = "pets_raw.csv"
CSV_PATH = os.path.join(os.path.dirname(os.path.realpath(__file__)), CSV_FILENAME)

# Nothing fancy here, just runs the script.
csv_raw = open(CSV_PATH, "r")
data_extractor = PetsDataExtractor(csv_raw, True)
pets_raw = data_extractor.parse_all()
data_formatter = PetsDataFormatter(pets_raw, True)
(breeds, listings) = data_formatter.format_all()
csv_raw.close()