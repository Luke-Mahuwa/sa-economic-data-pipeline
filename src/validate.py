import datetime

import pandera.errors
from pandera.pandas import Check, Column, DataFrameSchema

EXPECTED_COUNTRY_CODE = "ZAF"
MIN_YEAR = 1960


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


def _gdp_schema():
    current_year = datetime.date.today().year

    return DataFrameSchema(
        {
            "country": Column(str, nullable=False),
            "country_code": Column(str, Check.eq(EXPECTED_COUNTRY_CODE)),
            "indicator": Column(str, nullable=False),
            "indicator_code": Column(str, nullable=False),
            "year": Column(int, Check.in_range(MIN_YEAR, current_year), nullable=False),
            "value": Column(float, Check.ge(0), nullable=False),
        },
        unique=["year"],
        strict=False,
    )


def validate_gdp_dataframe(df):
    if df.empty:
        raise DataValidationError("Transformed DataFrame has no rows.")

    try:
        _gdp_schema().validate(df, lazy=True)
    except pandera.errors.SchemaErrors as exc:
        raise DataValidationError(str(exc.failure_cases)) from exc

    return df
