import os
import sys
import unittest

import pandas as pd

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from validate import DataValidationError, validate_gdp_dataframe, validate_raw_response


def make_df(**overrides):
    base = {
        "country": ["South Africa"],
        "country_code": ["ZAF"],
        "indicator": ["GDP (current US$)"],
        "indicator_code": ["NY.GDP.MKTP.CD"],
        "year": [2020],
        "value": [1000.0],
    }
    base.update(overrides)
    return pd.DataFrame(base)


class TestValidateRawResponse(unittest.TestCase):
    def test_accepts_well_formed_response(self):
        data = [{"page": 1}, [{"date": "2020"}]]
        self.assertEqual(validate_raw_response(data), data)

    def test_rejects_wrong_shape(self):
        with self.assertRaises(DataValidationError):
            validate_raw_response({"not": "a list"})

    def test_rejects_null_records(self):
        with self.assertRaises(DataValidationError):
            validate_raw_response([{"message": "invalid country"}, None])

    def test_rejects_empty_records(self):
        with self.assertRaises(DataValidationError):
            validate_raw_response([{"page": 1}, []])


class TestValidateGdpDataframe(unittest.TestCase):
    def test_accepts_valid_dataframe(self):
        df = make_df()
        self.assertTrue(validate_gdp_dataframe(df) is df)

    def test_rejects_empty_dataframe(self):
        with self.assertRaises(DataValidationError):
            validate_gdp_dataframe(make_df().iloc[0:0])

    def test_rejects_missing_column(self):
        df = make_df().drop(columns=["value"])
        with self.assertRaises(DataValidationError):
            validate_gdp_dataframe(df)

    def test_rejects_negative_value(self):
        df = make_df(value=[-5.0])
        with self.assertRaises(DataValidationError):
            validate_gdp_dataframe(df)

    def test_rejects_year_out_of_range(self):
        df = make_df(year=[1900])
        with self.assertRaises(DataValidationError):
            validate_gdp_dataframe(df)

    def test_rejects_duplicate_years(self):
        df = pd.concat([make_df(), make_df()], ignore_index=True)
        with self.assertRaises(DataValidationError):
            validate_gdp_dataframe(df)

    def test_rejects_unexpected_country_code(self):
        df = make_df(country_code=["USA"])
        with self.assertRaises(DataValidationError):
            validate_gdp_dataframe(df)


if __name__ == "__main__":
    unittest.main()
