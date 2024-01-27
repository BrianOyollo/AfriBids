from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient
import pytest
import os
from dotenv import load_dotenv
from app.database import Base, get_db
from app.main import app
from app import models, utils


load_dotenv()
POSTGRES_USERNAME=os.getenv('POSTGRES_USERNAME')
POSTGRES_PASSWORD=os.getenv('POSTGRES_PASSWORD')
DATABASE_NAME=os.getenv('TEST_DATABASE_NAME')
POSTGRES_PORT=os.getenv('POSTGRES_PORT')
POSTGRES_HOST=os.getenv('POSTGRES_HOST')


SQLALCHEMY_DATABASE_URL = f"postgresql://{POSTGRES_USERNAME}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{DATABASE_NAME}"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
TestSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture
def TestSession():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    db = TestSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture
def client(TestSession):
    def override_get_db():
        try:
            yield TestSession
        finally:
            TestSession.close()

    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)



@pytest.fixture
def test_user(client):
    dummy_user = {
        "email":"testuser@gmail.com",
        "display_name":"testuser_123",
        "password": "TestPassword123"
    }

    response = client.post("/users/new", json=dummy_user)
    test_user = response.json()
    test_user['password'] = dummy_user['password']
    return test_user


@pytest.fixture
def test_item_categories(TestSession):
    dummy_categories = [
        {'category_name':'Electronics'},
        {'category_name':"Autoparts and supplies"},
        {'category_name':'Tvs and Audio'}
    ]
    for category in dummy_categories:
        obj = models.ItemCategory(**category)
        TestSession.add(obj)

    TestSession.commit()
    categories = TestSession.query(models.ItemCategory).all()
    return categories

@pytest.fixture
def test_reserve_statuses(TestSession):
    dummy_statuses = [
        {
            'status':'Reserve',
            'status_description':'The auction listing has a reserve price set by the seller. Bidders must meet or exceed this predetermined minimum bid for the item to be sold. If the reserve price is not met by the end of the auction, the item remains unsold'
        },
        {
            'status':'No Reserve',
            'status_description':'The auction listing has no reserve price set by the seller. The highest bid, regardless of its value, at the end of the auction period secures the successful purchase of the item. This approach allows the item to be sold to the highest bidder, irrespective of a minimum bid requirement'
        }
    ]

    for status in dummy_statuses:
        obj = models.ReserveStatus(**status)
        TestSession.add(obj)

    TestSession.commit()
    statuses = TestSession.query(models.ReserveStatus).all()
    return statuses

@pytest.fixture
def test_auction_statuses(TestSession):
    dummy_statuses = [

        {
            'status':'Ongoing',
            'status_description':'The auction is currently in progress. Bidders can place bids, and the item is available for purchase until the specified end time.'
        },
        {
            'status':'Sold',
            'status_description':'The auction has concluded successfully, and the item has been sold to the highest bidder. The winning bidder has met or exceeded the reserve price, if applicable.'
        },
        {
            'status':'Cancelled',
            'status_description':'The auction has been canceled before its scheduled end time. This status may be applied in exceptional circumstances, such as the withdrawal of the item or unforeseen issues.'
        },
        {
            'status':'Reserve Price Not Met',
            'status_description':'The auction has concluded, but the reserve price, a minimum acceptable bid set by the seller, has not been met. As a result, the item remains unsold, and the transaction is not completed.'
        }
    ]
    for status in dummy_statuses:
        obj = models.AuctionStatus(**status)
        TestSession.add(obj)

    TestSession.commit()
    statuses = TestSession.query(models.AuctionStatus).all()
    return statuses

@pytest.fixture
def test_auction(client, test_user,test_item_categories,test_auction_statuses, test_reserve_statuses):
    dummy_auction = {
        'item_name':"Sony WF-1000XM4 TWS Earbuds - Black",
        'item_description':'8 hours long battery with Noise Canceling',
        'item_category': test_item_categories[0].category_id,
        'reserve_status':test_reserve_statuses[0].status_id,
        'reserve_price':39000,
        'seller':test_user['user_id']
    }
    images = utils.generate_random_image()
    files = {
        'images':('dummy_image', images, 'image/jpeg')
    }
    response = client.post("/auctions/new", files=files, data=dummy_auction)
    created_auction = response.json()
    return created_auction