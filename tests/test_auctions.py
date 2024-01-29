import pytest
from app import schemas, models, utils
from datetime import datetime
import pytz



def test_get_all_auctions(client):
    response = client.get("/auctions")
    assert response.status_code == 200

def test_get_existing_auction(client, test_auction):
    response = client.get(f"/auctions/{test_auction['auction_id']}")
    auction = schemas.FullAuctionProfile(**response.json())
    # print(auction)
    
    assert response.status_code == 200
    assert auction.auction_id == test_auction['auction_id']
    assert auction.item_name == test_auction['item_name']
    assert auction.item_description == test_auction['item_description']
    assert auction.current_bid == test_auction['current_bid']
    assert auction.itemcategory.category_id == test_auction['itemcategory']['category_id']
    assert auction.reservestatus.status_id == test_auction['reservestatus']['status_id']
    assert auction.auctionstatus.status_id == test_auction['auctionstatus']['status_id']

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
    dummy_image = utils.generate_random_image()
    files = {
        'images':('dummy_image', dummy_image, 'image/jpeg')
    }
    response = client.post("/auctions/new", files=files, data=dummy_auction)

    assert response.status_code == 201
    auction_item = response.json()

    assert auction_item['item_name'] == dummy_auction['item_name']
    assert auction_item['item_description'] == dummy_auction['item_description']
    assert auction_item['current_bid'] == 0
    assert auction_item['itemcategory']['category_id'] == dummy_auction['item_category']
    assert auction_item['reservestatus']['status_id'] == dummy_auction['reserve_status']
    assert auction_item['auctionstatus']['status_id'] == test_auction_statuses[0].status_id

def test_cancel_auction(client,test_auction,):
    response = client.put(f"/auctions/{test_auction['auction_id']}/cancel", json={'reason':'i changed my mind'})
    assert response.status_code == 200
    assert response.json()[0]['auction_status'] == 3 

def test_cancel_non_existent_auction(client):
    response = client.put(f"/auctions/1/cancel", json={'reason':'i changed my mind'})
    assert response.status_code == 404

def test_bid_on_non_existent_auction(client):
    response = client.post("/auctions/1232/bid", json={'amount':1500})
    assert response.status_code == 404

def test_successful_bid(client, test_auction, test_user2, TestSession):
    auction_id = test_auction['auction_id']
    response = client.post(f"/auctions/{auction_id}/bid", json={'amount':40000}) # reserve price of test_auction is 39k

    assert response.status_code == 201

    bid = TestSession.query(models.Bid).filter(models.Bid.auction_id == test_auction['auction_id']).first()
    assert bid.auction_id == test_auction['auction_id']
    assert bid.bidder_id == test_user2['user_id']
    assert bid.bidder.username == test_user2['username']
    assert bid.created_at < datetime.strptime(test_auction['end_time'], "%Y-%m-%dT%H:%M:%S.%f%z" )
    assert bid.amount == 40000
    assert (bid.amount - test_auction['reserve_price']) >= 50

