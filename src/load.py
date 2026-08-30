import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()

def get_connection():
    return psycopg2.connect(
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT"),
        database=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD")
    )

def load_data(df):
    connection = get_connection()
    cursor = connection.cursor()

    try:
        country_name = df.iloc[0]["country"]
        country_code = df.iloc[0]["country_code"]

        indicator_name = df.iloc[0]["indicator"]
        indicator_code = df.iloc[0]["indicator_code"]

        cursor.execute(
            """
            INSERT INTO countries(country_code, country_name)
            VALUES (%s, %s)
                on conflict (country_code)
                DO UPDATE SET country_name = EXCLUDED.country_name
                RETURNING country_id
            """,
            (country_code, country_name)

        )

        country_id = cursor.fetchone()[0]

        cursor.execute(
             """
            INSERT INTO indicators(indicator_code, indicator_name)
            VALUES (%s, %s)
                on conflict (indicator_code)
                DO UPDATE SET indicator_name = EXCLUDED.indicator_name
                RETURNING indicator_id
            """,
            (indicator_code, indicator_name)
        )

        indicator_id = cursor.fetchone()[0]

        for _, row in df.iterrows():
            cursor.execute(
                """
                INSERT INTO economic_observations
                (country_id, indicator_id, year, value)
                VALUES (%s, %s, %s, %s)
                ON CONFLICT (country_id, indicator_id, year)
                DO UPDATE SET value = EXCLUDED.value;
                """,
                (
                    country_id,
                    indicator_id,
                    int(row["year"]),
                    float(row["value"])
                )
            )
        connection.commit()
        print(f'Loaded {len(df)} observations into PostgreSQL.')
    
    except Exception:
        connection.rollback()
        raise

    finally:
        cursor.close()
        connection.close()