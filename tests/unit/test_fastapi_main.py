from app.fastapi_main import app, get_predictor
from fastapi.testclient import TestClient

client=TestClient(app)

def test_health():

    response=client.get('/health')
    assert response.status_code==200
    assert response.json()=={"status":"ok"}

def test_predict_price(monkeypatch):

    def mock_predict(request):
        return 3.201
    
    payload={
    "id": 27886,
    "listing_url": "https://www.airbnb.com/rooms/27886",
    "scrape_id": 20250911031321,
    "last_scraped": "2025-09-11",
    "source": "city scrape",
    "name": "Romantic, stylish B&B houseboat in canal district",
    "description": "Stylish houseboat on a central, quiet canal.",
    "neighborhood_overview": "Central, quiet, safe, clean and beautiful.",
    "picture_url": "https://a0.muscache.com/pictures/sample.jpg",
    "host_id": 97647,
    "host_url": "https://www.airbnb.com/users/show/97647",
    "host_name": "Demo Host",
    "host_since": 2023,
    "host_location": "Amsterdam, Netherlands",
    "host_about": "Experienced local host.",
    "host_response_time": "within an hour",
    "host_response_rate": 100,
    "host_acceptance_rate": 97,
    "host_is_superhost": 1,
    "host_thumbnail_url": "https://a0.muscache.com/sample-profile-small.jpg",
    "host_picture_url": "https://a0.muscache.com/sample-profile.jpg",
    "host_neighbourhood": "Centrum-West",
    "host_listings_count": 1.0,
    "host_total_listings_count": 1.0,
    "host_verifications": "['email', 'phone']",
    "host_has_profile_pic": 1,
    "host_identity_verified": 1,
    "neighbourhood": "Amsterdam, North Holland, Netherlands",
    "neighbourhood_cleansed": "Centrum-West",
    "neighbourhood_group_cleansed": None,
    "latitude": 52.38761,
    "longitude": 4.89188,
    "property_type": "Private room in houseboat",
    "room_type": "Private room",
    "accommodates": 2,
    "bathrooms": 1.5,
    "bathrooms_text": 1.5,
    "bedrooms": 1.0,
    "beds": 1.0,
    "amenities": 25,
    "price": 132.0,
    "minimum_nights": 3,
    "maximum_nights": 30,
    "minimum_minimum_nights": 3.0,
    "maximum_minimum_nights": 3.0,
    "minimum_maximum_nights": 10.0,
    "maximum_maximum_nights": 10.0,
    "minimum_nights_avg_ntm": 3.0,
    "maximum_nights_avg_ntm": 10.0,
    "calendar_updated": None,
    "has_availability": 1,
    "availability_30": 2,
    "availability_60": 5,
    "availability_90": 16,
    "availability_365": 17,
    "calendar_last_scraped": "2025-09-11",
    "number_of_reviews": 311,
    "number_of_reviews_ltm": 33,
    "number_of_reviews_l30d": 3,
    "availability_eoy": 17,
    "number_of_reviews_ly": 26,
    "estimated_occupancy_l365d": 255,
    "estimated_revenue_l365d": 33660.0,
    "first_review": 2009,
    "last_review": 2025,
    "review_scores_rating": 4.92,
    "review_scores_accuracy": 4.9,
    "review_scores_cleanliness": 4.94,
    "review_scores_checkin": 4.95,
    "review_scores_communication": 4.93,
    "review_scores_location": 4.9,
    "review_scores_value": 4.78,
    "license": "0363 974D 4986 7411 88D8",
    "instant_bookable": 0,
    "calculated_host_listings_count": 1,
    "calculated_host_listings_count_entire_homes": 0,
    "calculated_host_listings_count_private_rooms": 1,
    "calculated_host_listings_count_shared_rooms": 0,
    "reviews_per_month": 1.87,}

    app.dependency_overrides[get_predictor] = lambda: mock_predict

    response=client.post("/predict", json=payload)

    assert response.status_code==200
    assert response.json()=={"result": 3.201}

    app.dependency_overrides.clear()

def test_predict_price_invalid_payload():
      
    def mock_predict(request):
        return 3.201
      
    app.dependency_overrides[get_predictor] = lambda: mock_predict
    response=client.post("/predict", json={})
    assert response.status_code==422

    app.dependency_overrides.clear()
