import json

import pytest
from approvaltests import verify
from approval_utilities.utils import get_adjacent_file

from statement import statement


def test_example_statement():
    with open(get_adjacent_file("invoice.json")) as f:
        invoice = json.loads(f.read())
    with open(get_adjacent_file("plays.json")) as f:
        plays = json.loads(f.read())
    verify(statement(invoice, plays))


def test_statement_with_new_play_types():
    with open(get_adjacent_file("invoice_new_plays.json")) as f:
        invoice = json.loads(f.read())
    with open(get_adjacent_file("new_plays.json")) as f:
        plays = json.loads(f.read())
    with pytest.raises(ValueError) as exception_info:
        statement(invoice, plays)
    assert "unknown type" in str(exception_info.value)

def test_tragedy_at_30_attendees():
    plays = {"hamlet": {"name": "Hamlet", "type": "tragedy"}}
    invoice = {"customer": "Test Customer","performances": [{"playID": "hamlet", "audience": 30}],}

    result = statement(invoice, plays)

    assert "Hamlet: $400.00 (30 seats)" in result
    assert "Amount owed is $400.00" in result
    assert "You earned 0 credits" in result


def test_comedy_at_20_attendees():
    plays = {"as-like": {"name": "As You Like It", "type": "comedy"}}
    invoice = {"customer": "Test Customer","performances": [{"playID": "as-like", "audience": 20}],}

    result = statement(invoice, plays)

    assert "As You Like It: $360.00 (20 seats)" in result
    assert "Amount owed is $360.00" in result
    assert "You earned 4 credits" in result

def test_historical_at_20_attendees():
    plays = {
        "henry-v": {"name": "Henry V", "type": "historical"}
    }
    invoice = {
        "customer": "Test Customer",
        "performances": [
            {"playID": "henry-v", "audience": 20}
        ],
    }

    result = statement(invoice, plays)

    assert "Henry V: $500.00 (20 seats)" in result
    assert "Amount owed is $500.00" in result
    assert "You earned 4 credits" in result


def test_historical_at_21_attendees():
    plays = {
        "henry-v": {"name": "Henry V", "type": "historical"}
    }
    invoice = {
        "customer": "Test Customer",
        "performances": [
            {"playID": "henry-v", "audience": 21}
        ],
    }

    result = statement(invoice, plays)

    assert "Henry V: $515.00 (21 seats)" in result
    assert "Amount owed is $515.00" in result
    assert "You earned 4 credits" in result


def test_historical_at_35_attendees():
    plays = {
        "henry-v": {"name": "Henry V", "type": "historical"}
    }
    invoice = {
        "customer": "Test Customer",
        "performances": [
            {"playID": "henry-v", "audience": 35}
        ],
    }

    result = statement(invoice, plays)

    assert "Henry V: $725.00 (35 seats)" in result
    assert "Amount owed is $725.00" in result
    assert "You earned 7 credits" in result