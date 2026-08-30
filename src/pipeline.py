from extract import extract_gdp_data
from transform import transform_gdp_data
from load import load_data

print("Extracting data...")
data = extract_gdp_data()

print("Transforming data...")
df = transform_gdp_data(data)

print("Loading data...")
load_data(df)

print("Pipeline completed succefully,")