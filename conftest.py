import pandas as pd
import pytest
from app.schemas import PredictionRequest

@pytest.fixture
def sample_dataframe():

    return pd.DataFrame({
        'id': [2788,28871,29051,44391,48373],
        'listing_url': ['https://www.airbnb.com/rooms/27886','https://www.airbnb.com/rooms/28871','https://www.airbnb.com/rooms/29051','https://www.airbnb.com/rooms/44391','https://www.airbnb.com/rooms/48373'],
        'scrape_id': [20250911031321,20250911031321,20250911031321,20250911031321,20250911031321],
        'last_scraped': ['2025-09-11','2025-09-11','2025-09-11','2025-09-11','2025-09-11'] ,
        'source': ['city scrape','city scrape','city scrape','previous scrape','previous scrape'],
        'name': ['Romantic, stylish B&B houseboat in canal district','Comfortable double room','Comfortable single / double room','Quiet 2-bedroom Amsterdam city centre apartment','Cozy family home in Amsterdam South'],
        'description': ['Stylish and romantic houseboat on fantastic historic location with breathtaking view.  Wheelhouse, deckhouse and captains room. Central, quiet. Great breakfast, 2 vanMoof design bikes and a Canadian Canoe are included. Just read the reviews on tripadvisor for instance!',
                       'Basic bedroom in the center of Amsterdam.',
                       'This room can also be rented as a single or a small double<br /><br />Also a cat lives here',
                       'Guests greatly appreciate the unique location of the apartment. It is located in a very quiet part of the city centre whilst only 1,5km away from central station. A bus takes you there directly in just five minutes. Restaurants, bars, musea, the Amsterdam Zoo and the popular citypark Marineterrein are just around the corner. The apartment itself is very well isolated so you can sleep in silence. The large private terrace provides you, directly from the kitchen, a nice outdoor space! Have a look!',
                       'Charming modern apartment in the quiet and green Southern part of Amsterdam, surrounded by trees and parks. Ideal for family stay as there are also playgrounds for children in the neighbourhood. <br />Minimum stay 7 days.<br />City center is about 15 minutes away by public transport or bicycle where you can find amazing and the best Amsterdam restaurants and famous museums.'],
        'neighborhood_overview': ['Central, quiet, safe, clean and beautiful.',
                                 'Flower market , Leidseplein , Rembrantsplein',
                                 'the street is quite lively especially on weekends when the weather is good',
                                 'The appartment is located in the city centre. Famous Amsterdam places such as the Amsterdam Zoo and the Maritime Museam are in 5 minutes walking distance. The supermarket is literally the next door!',
                                 'Apartment is located between Amsterdamse Bos and Amstel Park. in the very green and quiet area. Shopping-mall Gelderlandplein is 10 minutes walk.'],
        'picture_url': ['https://a0.muscache.com/pictures/02c2da9d-660e-451d-8a51-2f7a17469df7.jpg',
                       'https://a0.muscache.com/pictures/160889/362340f7_original.jpg',
                       'https://a0.muscache.com/pictures/162009/bd6be2f8_original.jpg',
                       'https://a0.muscache.com/pictures/97741545/39000c13_original.jpg',
                       'https://a0.muscache.com/pictures/miso/Hosting-48373/original/ee2d14f7-27cb-46e9-b623-15e1080725e5.jpeg'],
        'host_id': [97647,124245,124245,194779,220434],
        'host_url': ['https://www.airbnb.com/users/show/97647',
                    'https://www.airbnb.com/users/show/124245',
                    'https://www.airbnb.com/users/show/124245',
                    'https://www.airbnb.com/users/show/194779',
                    'https://www.airbnb.com/users/show/220434'],
        'host_name': ['Flip','Edwin','Edwin','Jan','Vesna & Misha'],
        'host_since': ['2010-03-23','2010-05-13','2010-05-13','2010-08-08','2010-09-01'],
        'host_location': ['Amsterdam, Netherlands','Amsterdam, Netherlands','Amsterdam, Netherlands','Amsterdam, Netherlands','Amsterdam, Netherlands'],
        'host_about': ['Marjan works in "eye" the dutch filmmuseum, and designs costumes for tv, film and theatre. Flip is an actor, mainly on stage, but also for film and tv. So for cultural advise, what to do, you are coming to the right place...\r\n\r\n','Hi','Hi','Love to travel while hosting and to host while travelling!',None],
        'host_response_time': ['within an hour','within an hour','within an hour',None,None],
        'host_response_rate': ['100%','100%','100%',None,None],
        'host_acceptance_rate': ['97%','99%','99%',None,None],
        'host_is_superhost': ['t','t','t','f','f'],
        'host_thumbnail_url':['https://a0.muscache.com/im/users/97647/profile_pic/1273275077/original.jpg?aki_policy=profile_small',
                              'https://a0.muscache.com/im/pictures/user/9986bbdb-632f-42b5-a866-8e3307184977.jpg?aki_policy=profile_small',
                              'https://a0.muscache.com/im/pictures/user/9986bbdb-632f-42b5-a866-8e3307184977.jpg?aki_policy=profile_small',
                              'https://a0.muscache.com/im/users/194779/profile_pic/1436464796/original.jpg?aki_policy=profile_small',
                              'https://a0.muscache.com/im/pictures/user/User-220434/original/6559512c-20fa-45ac-b45c-0e0eb9773c5f.jpeg?aki_policy=profile_small'],
        'host_picture_url': ['https://a0.muscache.com/im/users/97647/profile_pic/1273275077/original.jpg?aki_policy=profile_x_medium',
                              'https://a0.muscache.com/im/pictures/user/9986bbdb-632f-42b5-a866-8e3307184977.jpg?aki_policy=profile_x_medium',
                              'https://a0.muscache.com/im/pictures/user/9986bbdb-632f-42b5-a866-8e3307184977.jpg?aki_policy=profile_x_medium',
                              'https://a0.muscache.com/im/users/194779/profile_pic/1436464796/original.jpg?aki_policy=profile_x_medium',
                              'https://a0.muscache.com/im/pictures/user/User-220434/original/6559512c-20fa-45ac-b45c-0e0eb9773c5f.jpeg?aki_policy=profile_x_medium'],
        'host_neighbourhood': ['Westelijke Eilanden','Amsterdam Centrum','Amsterdam Centrum','Oostelijke Eilanden en Kadijken','Amsterdam Centrum'],
        'host_listings_count': [1.0, 2.0, 2.0, 1.0, 1.0],
        'host_total_listings_count': [1.0, 2.0, 2.0, 1.0, 1.0],
        'host_verifications': ["['email', 'phone']",
                                "['email', 'phone']",
                                "['email', 'phone']",
                                "['email', 'phone']",
                                "['email', 'phone']"],
        'host_has_profile_pic': ['t', 't', 't', 't', 't'],
        'host_identity_verified': ['t', 't', 't', 't', 't'],
        'neighbourhood': ['Amsterdam, North Holland, Netherlands','Amsterdam, North Holland, Netherlands','Amsterdam, North Holland, Netherlands',
                          'Amsterdam, Noord-Holland, Netherlands','Amsterdam, Noord-Holland, Netherlands'],
        'neighbourhood_cleansed': ['Centrum-West','Centrum-West','Centrum-Oost',
                                    'Centrum-Oost','Buitenveldert - Zuidas'],
        'neighbourhood_group_cleansed':[None, None, None, None, None],
          'latitude': [52.38761,52.36775,52.36584,52.37168,52.32780775677816],
        'longitude': [4.89188,4.89092,4.89111,4.91471,4.87680005722526],
        'property_type': ['Private room in houseboat','Private room in rental unit','Private room in condo',
                          'Entire rental unit','Entire rental unit'],
        'room_type': ['Private room','Private room','Private room',
                      'Entire home/apt','Entire home/apt'],
        'accommodates': [2, 2, 2, 4, 4],
          'bathrooms': [1.5, 1.0, 1.0, None, None],
        'bathrooms_text': ['1.5 baths','1 shared bath','1 shared bath',
                          '1.5 baths','1.5 baths'],
        'bedrooms':[1.0, 1.0, 1.0, 2.0, 2.0],
        'beds':[1.0, 1.0, 1.0, None, None],
        'amenities':['["Canal view", "Coffee", "Private backyard \\u2013 Not fully fenced", "Bikes", "Portable fans", "Books and reading material", "Fast wifi \\u2013 245 Mbps", "Hangers", "Paid street parking off premises", "Shower gel", "Breakfast", "Wine glasses", "Dining table", "Private living room", "Hot water", "Bed linens", "TV with standard cable", "Heating - split type ductless system", "Long term stays allowed", "Central heating", "Self check-in", "Private patio or balcony", "City skyline view", "Shampoo", "Kayak", "Fire extinguisher", "Luggage dropoff allowed", "Outdoor dining area", "Hp neutral, eco friendly body soap", "Garden view", "Laundromat nearby", "Air conditioning", "Lake access", "Smart lock", "Dedicated workspace", "Boat slip", "Mini fridge", "Harbor view", "Hair dryer", "Private entrance", "Carbon monoxide alarm", "Coffee maker: Nespresso", "Safe", "Extra pillows and blankets", "Smoke alarm", "Refrigerator", "Essentials", "Outdoor furniture", "Waterfront", "Clothing storage: closet"]',
                         '["Heating", "Lock on bedroom door", "Hair dryer", "Private entrance", "Carbon monoxide alarm", "Cleaning products", "Smoke alarm", "Refrigerator", "Wifi", "Hot water", "Bed linens", "Hangers", "Essentials", "Host greets you", "Iron", "Shampoo", "Coffee maker", "Fire extinguisher"]',
                         '["Heating", "Lock on bedroom door", "Hair dryer", "Private entrance", "Carbon monoxide alarm", "Smoke alarm", "Refrigerator", "Wifi", "Hot water", "Bed linens", "Hangers", "Essentials", "Host greets you", "Iron", "Shampoo", "Coffee maker", "Shower gel", "Fire extinguisher"]',
                         '["Wifi", "Hangers", "Shower gel", "Washer", "Hot water", "Bed linens", "TV with standard cable", "Iron", "Cooking basics", "Shampoo", "Dishes and silverware", "Coffee maker", "Luggage dropoff allowed", "Microwave", "Air conditioning", "Stove", "Paid parking on premises", "Host greets you", "Oven", "Paid parking off premises", "Heating", "Hair dryer", "Private entrance", "Carbon monoxide alarm", "Dishwasher", "Smoke alarm", "Extra pillows and blankets", "Refrigerator", "Kitchen", "Essentials", "Patio or balcony"]',
                         '["Courtyard view", "Free dryer \\u2013 In unit", "Books and reading material", "Wifi", "Hangers", "Hot water kettle", "Piano", "Wine glasses", "Cleaning products", "Dining table", "TV", "Hot water", "Bed linens", "Long term stays allowed", "Outdoor playground", "Central heating", "Iron", "Room-darkening shades", "Cooking basics", "Dishes and silverware", "Coffee maker", "Laundromat nearby", "Trash compactor", "Stove", "Drying rack for clothing", "Dedicated workspace", "Oven", "Bathtub", "Hair dryer", "Carbon monoxide alarm", "Dishwasher", "Smoke alarm", "Extra pillows and blankets", "Refrigerator", "Kitchen", "Essentials", "Free washer \\u2013 In unit", "Clothing storage: closet"]'],
        'price': ['$132.00', '$89.00', '$61.00', None, None],
        'minimum_nights': [3, 2, 2, 3, 3],
        'maximum_nights':[356, 730, 730, 730, 1125],
        'minimum_minimum_nights': [3.0, 1.0, 1.0, 3.0, 3.0],
        'maximum_minimum_nights': [3.0, 2.0, 2.0, 3.0, 3.0],
        'minimum_maximum_nights': [30.0, 730.0, 730.0, 730.0, 1125.0],
        'maximum_maximum_nights': [30.0, 730.0, 730.0, 730.0, 1125.0],
        'minimum_nights_avg_ntm': [3.0, 2.0, 2.0, 3.0, 3.0],
        'maximum_nights_avg_ntm': [30.0, 730.0, 730.0, 730.0, 1125.0],
        'calendar_updated': [None, None, None, None, None],
        'has_availability': ['t', 't', 't', 't', 't'],
        'availability_30': [2, 0, 0, 0, 0],
        'availability_60': [5, 2, 1, 0, 0],
        'availability_90': [16, 10, 13, 0, 0],
        'availability_365': [17, 126, 95, 0, 0],
        'calendar_last_scraped': ['2025-09-11','2025-09-11','2025-09-11',
                                   '2025-09-11','2025-09-11'],
        'number_of_reviews': [311, 732, 849, 42, 5],
        'number_of_reviews_ltm': [33, 93, 86, 0, 0],
        'number_of_reviews_l30d': [3, 9, 8, 0, 0],
        'availability_eoy': [17, 15, 13, 0, 0],
        'number_of_reviews_ly': [26, 96, 88, 0, 3],
        'estimated_occupancy_l365d': [255, 255, 255, 0, 0],
        'estimated_revenue_l365d': [33660.0,22695.0,15555.0,None,None],
        'first_review': ['2012-01-09','2010-08-22','2011-03-16','2010-09-16','2023-07-21'],
        'last_review': ['2025-09-07','2025-09-07','2025-09-08','2022-08-20','2024-04-28'],
        'review_scores_rating': [4.92, 4.87, 4.81, 4.71, 5.0],
        'review_scores_accuracy': [4.9, 4.9, 4.88, 4.68, 5.0],
        'review_scores_cleanliness': [4.94, 4.86, 4.83, 4.49, 5.0],
        'review_scores_checkin': [4.95, 4.94, 4.93, 4.95, 5.0],
        'review_scores_communication': [4.93, 4.94, 4.92, 4.9, 5.0],
        'review_scores_location': [4.9, 4.93, 4.87, 4.68, 4.6],
        'review_scores_value': [4.78, 4.83, 4.79, 4.5, 5.0],
        'license': ['0363 974D 4986 7411 88D8','0363 607B EA74 0BD8 2F6F','0363 607B EA74 0BD8 2F6F',
                     '0363 E76E F06A C1DD 172C','0363 4A2B A6AD 0196 F684'],
        'instant_bookable': ['f', 'f', 'f', 'f', 'f'],
        'calculated_host_listings_count': [1, 2, 2, 1, 1],
        'calculated_host_listings_count_entire_homes': [0, 0, 0, 1, 1],
        'calculated_host_listings_count_private_rooms': [1,2,2,0,0],
        'calculated_host_listings_count_shared_rooms': [0, 0, 0, 0, 0],
        'reviews_per_month': [1.87, 3.99, 4.81, 0.23, 0.19]
    })

@pytest.fixture
def sample_feature_df():

    return pd.DataFrame({

        "host_response_rate": ["90%"],
        "host_acceptance_rate": ["80%"],
        "host_is_superhost": ["t"],
        "host_has_profile_pic": ["t"],
        "host_identity_verified": ["f"],
        "price": ["$100.00"],
        "has_availability": ["t"],
        "first_review": ["2020-01-01"],
        "last_review": ["2024-01-01"],
        "host_since": ["2015-01-01"],
        "instant_bookable": ["f"],
        "host_response_time": ["within an hour"],
        "bathrooms_text": ["1.5 baths"],
        "amenities": ["['Wifi', 'TV']"]
    })

@pytest.fixture
def sample_train_data():

    train_data=pd.DataFrame({
        "feature1": [1,2,3,4,5],
        "feature2":[23,56,87,12,11],
        "price":[234,5432,765,455,985]
    })

    test_data=pd.DataFrame({
        "feature1":[4,6,1,5,9],
        "feature2":[2,9,0,3,1],
        "price":[345,678,100,390,999]
    })

    return train_data, test_data

@pytest.fixture
def prediction_request():

    request = PredictionRequest(

        name="Beautiful apartment in Amsterdam",

        description="A cozy apartment near the city center",

        host_since=2018,

        host_location="Amsterdam, Netherlands",

        host_response_time="within an hour",

        host_response_rate=95,

        host_acceptance_rate=90,

        host_about= 'Marjan works in "eye" the dutch filmmuseum, and designs costumes for tv, film and theatre. Flip is an actor, mainly on stage, but also for film and tv. So for cultural advise, what to do, you are coming to the right place...\r\n\r\n',

        host_is_superhost=1,

        host_total_listings_count=3,

        host_verifications="['email', 'phone']",

        host_has_profile_pic=1,

        host_identity_verified=1,

        neighbourhood_cleansed="Centrum-West",

        latitude=52.3676,

        longitude=4.9041,

        property_type="Entire rental unit",

        room_type="Entire home/apt",

        accommodates=4,

        bathrooms=1.0,

        bathrooms_text=1.0,

        bedrooms=2.0,

        beds=2.0,

        amenities=25,

        price=150.0,

        minimum_nights=2,

        maximum_nights=30,

        minimum_minimum_nights=1.0,

        maximum_minimum_nights=3.0,

        minimum_maximum_nights=3.0,

        maximum_maximum_nights=6.0,

        minimum_nights_avg_ntm=2.0,

        maximum_nights_avg_ntm=5.0,

        has_availability=1,

        availability_30=20,

        availability_60=40,

        availability_90=70,

        availability_365=250,

        number_of_reviews=120,

        number_of_reviews_ltm=25,

        number_of_reviews_l30d=5,

        availability_eoy=150,

        number_of_reviews_ly=30,

        first_review=2019,

        last_review=2025,

        review_scores_rating=4.8,

        review_scores_accuracy=4.9,

        review_scores_cleanliness=4.7,

        review_scores_checkin=4.9,

        review_scores_communication=5.0,

        review_scores_location=4.8,

        review_scores_value=4.6,

        instant_bookable=1,

        calculated_host_listings_count=3,

        calculated_host_listings_count_entire_homes=2,

        calculated_host_listings_count_private_rooms=1,

        calculated_host_listings_count_shared_rooms=0,

        reviews_per_month=2.5
    )

    return request
