import pytest
from app import schemas, models


def test_get_all_auctions(client):
    response = client.get("/")
    assert response.status_code == 200

def test_db_connection(test_item_category):
    print(test_item_category)