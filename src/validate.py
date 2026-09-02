import datetime

EXPECTED_COUNTRY_CODE = "ZAF"
MIN_YEAR = 1960
REQUIRED_COLUMNS = {"country", "country_code", "indicator", "indicator_code", "year", "value"}


class DataValidationError(Exception):
    pass


def validate_raw_response(data):
    if not isinstance(data, list) or len(data) != 2:
        raise DataValidationError("Unexpected World Bank API response shape.")

    metadata, records = data

    if records is None:
        raise DataValidationError(f"World Bank API returned no records: {metadata}")

    if not isinstance(records, list) or len(records) == 0:
        raise DataValidationError("World Bank API returned an empty records list.")

    return data


def validate_gdp_dataframe(df):
    if df.empty:
        raise DataValidationError("Transformed DataFrame has no rows.")

    missing_columns = REQUIRED_COLUMNS - set(df.columns)
    if missing_columns:
        raise DataValidationError(f"Missing expected columns: {sorted(missing_columns)}")

    if df["value"].isna().any():
        raise DataValidationError("Found null GDP values after transformation.")

    if (df["value"] < 0).any():
        raise DataValidationError("Found negative GDP values.")

    current_year = datetime.date.today().year
    invalid_years = df[(df["year"] < MIN_YEAR) | (df["year"] > current_year)]
    if not invalid_years.empty:
        raise DataValidationError(
            f"Found years outside the expected range [{MIN_YEAR}, {current_year}]: "
            f"{invalid_years['year'].tolist()}"
        )

    if df["year"].duplicated().any():
        raise DataValidationError("Found duplicate years in the dataset.")

    unexpected_codes = set(df["country_code"].unique()) - {EXPECTED_COUNTRY_CODE}
    if unexpected_codes:
        raise DataValidationError(f"Unexpected country codes found: {unexpected_codes}")

    return df
