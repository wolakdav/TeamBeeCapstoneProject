import pytest
from src.tables import Service_Periods

@pytest.fixture
def service_periods_fixture():
    return Service_Periods("sw23", "fake")

def test_creation_sql(service_periods_fixture):
    expected = "".join(["""
            CREATE TABLE IF NOT EXISTS """, "hive", ".", "service_periods", """
            (
                service_key BIGSERIAL PRIMARY KEY,
                month SMALLINT NOT NULL CHECK ( (month <= 12) AND (month >= 1) ),
                year SMALLINT NOT NULL CHECK (year > 1700),
                ternary SMALLINT NOT NULL CHECK ( (ternary <= 3) AND (ternary >= 1) ),
                UNIQUE (month, year, ternary)
            );"""])
    assert expected == service_periods_fixture._creation_sql
