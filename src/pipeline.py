from extract import extract_gdp_data
from transform import transform_gdp_data

data = extract_gdp_data()
df = transform_gdp_data(data)

print(df.head)
print(df.tail)