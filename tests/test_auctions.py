import pytest
from app import schemas, models


def test_get_all_auctions(client):
    response = client.get("/auctions")
    assert response.status_code == 200

def test_get_existing_auction(client, test_auction):
    response = client.get(f"/auctions/{test_auction['auction_id']}")
    auction = schemas.GeneralAuctionResponse(**response.json())
    
    assert response.status_code == 200
    assert auction.auction_id == test_auction['auction_id']
    assert auction.item_name == test_auction['item_name']
    assert auction.item_description == test_auction['item_description']
    assert auction.current_bid == test_auction['current_bid']
    assert auction.reserve_price == test_auction['reserve_price']
    assert auction.itemcategory.category_id == test_auction['itemcategory']['category_id']
    assert auction.reservestatus.status_id == test_auction['reservestatus']['status_id']
    assert auction.auctionstatus.status_id == test_auction['auctionstatus']['status_id']
    assert auction.user.user_id == test_auction['user']['user_id']

def test_get_nonexistent_auction(client):
    response = client.get("/auctions/12")
    assert response.status_code == 404

def test_create_auction(client,test_user,test_item_categories,test_auction_statuses, test_reserve_statuses):
    dummy_auction = {
        'item_name':"Sony WF-1000XM4 TWS Earbuds - Black",
        'item_description':'8 hours long battery with Noise Canceling',
        'item_category': test_item_categories[0].category_id,
        'reserve_status':test_reserve_statuses[0].status_id,
        'reserve_price':39000,
        'seller':test_user['user_id']
    }
    response = client.post("/auctions/new", json=dummy_auction)
    auction = schemas.GeneralAuctionResponse(**response.json())

    assert response.status_code == 201

    assert auction.item_name == dummy_auction['item_name']
    assert auction.item_description == dummy_auction['item_description']
    assert auction.current_bid == 0
    assert auction.reserve_price == dummy_auction['reserve_price']
    assert auction.itemcategory.category_id == dummy_auction['item_category']
    assert auction.reservestatus.status_id == dummy_auction['reserve_status']
    assert auction.auctionstatus.status_id == test_auction_statuses[0].status_id
    assert auction.user.user_id == dummy_auction['seller']

