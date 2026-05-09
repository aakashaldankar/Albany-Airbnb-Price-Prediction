from app.model_loader import load_model, load_encoders
import os
import pandas as pd
import numpy as np

encoders=load_encoders()

host_verification_label_encoder=encoders['host_verification_label_encoder']
neighbourhood_cleansed_target_encoder=encoders['neighbourhood_cleansed_target_encoder']
room_type_ohe=encoders['room_type_ohe']
property_type_target_encoder=encoders['property_type_target_encoder']
name_tfidf_encoder=encoders['name_tfidf_encoder']
host_location_tfidf_encoder=encoders['host_location_tfidf_encoder']

root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

test_data_path=os.path.join(root_dir, 'central_data', 'raw_data','train_data.csv')

# data_path='https://raw.githubusercontent.com/aakashaldankar/Albany-Airbnb-Listings-Data/refs/heads/main/listings.csv'

# df=pd.read_csv(data_path)

# print(df.info())

data={'id': 27886,
 'listing_url': 'https://www.airbnb.com/rooms/27886',
 'scrape_id': 20250911031321,
 'last_scraped': '2025-09-11',
 'source': 'city scrape',
 'name': 'Romantic, stylish B&B houseboat in canal district',
 'description': 'Stylish and romantic houseboat on fantastic historic location with breathtaking view.  Wheelhouse, deckhouse and captains room. Central, quiet. Great breakfast, 2 vanMoof design bikes and a Canadian Canoe are included. Just read the reviews on tripadvisor for instance!',
 'neighborhood_overview': 'Central, quiet, safe, clean and beautiful.',
 'picture_url': 'https://a0.muscache.com/pictures/02c2da9d-660e-451d-8a51-2f7a17469df7.jpg',
 'host_id': 97647,
 'host_url': 'https://www.airbnb.com/users/show/97647',
 'host_name': 'Flip',
 'host_since': '2010-03-23',
 'host_location': 'Amsterdam, Netherlands',
 'host_about': 'Marjan works in "eye" the dutch filmmuseum, and designs costumes for tv, film and theatre. Flip is an actor, mainly on stage, but also for film and tv. So for cultural advise, what to do, you are coming to the right place...\r\n\r\n',
 'host_response_time': 'within an hour',
 'host_response_rate': '100%',
 'host_acceptance_rate': '97%',
 'host_is_superhost': 't',
 'host_thumbnail_url': 'https://a0.muscache.com/im/users/97647/profile_pic/1273275077/original.jpg?aki_policy=profile_small',
 'host_picture_url': 'https://a0.muscache.com/im/users/97647/profile_pic/1273275077/original.jpg?aki_policy=profile_x_medium',
 'host_neighbourhood': 'Westelijke Eilanden',
 'host_listings_count': 1.0,
 'host_total_listings_count': 1.0,
 'host_verifications': "['email', 'phone']",
 'host_has_profile_pic': 't',
 'host_identity_verified': 't',
 'neighbourhood': 'Amsterdam, North Holland, Netherlands',
 'neighbourhood_cleansed': 'Centrum-West',
 'neighbourhood_group_cleansed': "Nan",
 'latitude': 52.38761,
 'longitude': 4.89188,
 'property_type': 'Private room in houseboat',
 'room_type': 'Private room',
 'accommodates': 2,
 'bathrooms': 1.5,
 'bathrooms_text': '1.5 baths',
 'bedrooms': 1.0,
 'beds': 1.0,
 'amenities': '["Canal view", "Coffee", "Private backyard \\u2013 Not fully fenced", "Bikes", "Portable fans", "Books and reading material", "Fast wifi \\u2013 245 Mbps", "Hangers", "Paid street parking off premises", "Shower gel", "Breakfast", "Wine glasses", "Dining table", "Private living room", "Hot water", "Bed linens", "TV with standard cable", "Heating - split type ductless system", "Long term stays allowed", "Central heating", "Self check-in", "Private patio or balcony", "City skyline view", "Shampoo", "Kayak", "Fire extinguisher", "Luggage dropoff allowed", "Outdoor dining area", "Hp neutral, eco friendly body soap", "Garden view", "Laundromat nearby", "Air conditioning", "Lake access", "Smart lock", "Dedicated workspace", "Boat slip", "Mini fridge", "Harbor view", "Hair dryer", "Private entrance", "Carbon monoxide alarm", "Coffee maker: Nespresso", "Safe", "Extra pillows and blankets", "Smoke alarm", "Refrigerator", "Essentials", "Outdoor furniture", "Waterfront", "Clothing storage: closet"]',
 'price': 132.00,
 'minimum_nights': 3,
 'maximum_nights': 356,
 'minimum_minimum_nights': 3.0,
 'maximum_minimum_nights': 3.0,
 'minimum_maximum_nights': 30.0,
 'maximum_maximum_nights': 30.0,
 'minimum_nights_avg_ntm': 3.0,
 'maximum_nights_avg_ntm': 30.0,
 'calendar_updated': "None",
 'has_availability': 't',
 'availability_30': 2,
 'availability_60': 5,
 'availability_90': 16,
 'availability_365': 17,
 'calendar_last_scraped': '2025-09-11',
 'number_of_reviews': 311,
 'number_of_reviews_ltm': 33,
 'number_of_reviews_l30d': 3,
 'availability_eoy': 17,
 'number_of_reviews_ly': 26,
 'estimated_occupancy_l365d': 255,
 'estimated_revenue_l365d': 33660.0,
 'first_review': '2012-01-09',
 'last_review': '2025-09-07',
 'review_scores_rating': 4.92,
 'review_scores_accuracy': 4.9,
 'review_scores_cleanliness': 4.94,
 'review_scores_checkin': 4.95,
 'review_scores_communication': 4.93,
 'review_scores_location': 4.9,
 'review_scores_value': 4.78,
 'license': '0363 974D 4986 7411 88D8',
 'instant_bookable': 'f',
 'calculated_host_listings_count': 1,
 'calculated_host_listings_count_entire_homes': 0,
 'calculated_host_listings_count_private_rooms': 1,
 'calculated_host_listings_count_shared_rooms': 0,
 'reviews_per_month': 1.87}


def pre_process(data: dict):

    # print(data['host_response_rate'])

    drop_list=["id","listing_url",'scrape_id','last_scraped','source','picture_url','host_id',
                 'host_url','host_thumbnail_url','host_picture_url','host_listings_count',
                 'neighbourhood_group_cleansed','calendar_updated','calendar_last_scraped','license',
                 'neighborhood_overview','host_about','host_neighbourhood','neighbourhood','estimated_occupancy_l365d','estimated_revenue_l365d','host_name','description']
    
    for key in drop_list:
        data.pop(key, None)

    data['price']=np.log1p(data['price'])

    #label encoding
    data['host_verifications']=host_verification_label_encoder[data['host_verifications']]
    
    #target encoding
    data['neighbourhood_cleansed']=neighbourhood_cleansed_target_encoder[data['host_verifications']]
    data['property_type']=property_type_target_encoder[data['property_type']]
 
    #one hot encoding
    data['room_type'] = data['room_type'] if data['room_type'] in {'Entire home/apt', 'Private room'} else 'Other'
    
    one_hot_data=pd.DataFrame({'room_type': [data['room_type']]})
    encoded_data=room_type_ohe.transform(one_hot_data)
    feature_names=room_type_ohe.get_feature_names_out(['room_type'])
    encoded_df=pd.DataFrame(encoded_data, columns=feature_names)
    data.pop('room_type')
    data.update(encoded_df.iloc[0].to_dict())

    #tfidf
    vector=name_tfidf_encoder.transform([data['name']])
    vector_df=pd.DataFrame(vector.toarray(), columns=name_tfidf_encoder.get_feature_names_out()) 
    data.pop('name')
    data.update(vector_df.iloc[0].to_dict())

    vector=name_tfidf_encoder.transform([data['host_location']])
    vector_df=pd.DataFrame(vector.toarray(), columns=host_location_tfidf_encoder.get_feature_names_out()) 
    data.pop('host_location')
    data.update(vector_df.iloc[0].to_dict())

    print(len(data))



    


    

    

    # print(data['host_response_rate'])


# pre_process(data)

pre_data={'host_since': '2010-03-23', 'host_response_time': 'within an hour', 'host_response_rate': '100%', 'host_acceptance_rate': '97%', 'host_is_superhost': 't', 'host_total_listings_count': 1.0, 'host_verifications': 0, 'host_has_profile_pic': 't', 'host_identity_verified': 't', 'neighbourhood_cleansed': np.float64(4.874017991224878), 'latitude': 52.38761, 'longitude': 4.89188, 'property_type': np.float64(5.1654585880588035), 'accommodates': 2, 'bathrooms': 1.5, 'bathrooms_text': '1.5 baths', 'bedrooms': 1.0, 'beds': 1.0, 'amenities': '["Canal view", "Coffee", "Private backyard \\u2013 Not fully fenced", "Bikes", "Portable fans", "Books and reading material", "Fast wifi \\u2013 245 Mbps", "Hangers", "Paid street parking off premises", "Shower gel", "Breakfast", "Wine glasses", "Dining table", "Private living room", "Hot water", "Bed linens", "TV with standard cable", "Heating - split type ductless system", "Long term stays allowed", "Central heating", "Self check-in", "Private patio or balcony", "City skyline view", "Shampoo", "Kayak", "Fire extinguisher", "Luggage dropoff allowed", "Outdoor dining area", "Hp neutral, eco friendly body soap", "Garden view", "Laundromat nearby", "Air conditioning", "Lake access", "Smart lock", "Dedicated workspace", "Boat slip", "Mini fridge", "Harbor view", "Hair dryer", "Private entrance", "Carbon monoxide alarm", "Coffee maker: Nespresso", "Safe", "Extra pillows and blankets", "Smoke alarm", "Refrigerator", "Essentials", "Outdoor furniture", "Waterfront", "Clothing storage: closet"]', 'price': np.float64(4.890349128221754), 'minimum_nights': 3, 'maximum_nights': 356, 'minimum_minimum_nights': 3.0, 'maximum_minimum_nights': 3.0, 'minimum_maximum_nights': 30.0, 'maximum_maximum_nights': 30.0, 'minimum_nights_avg_ntm': 3.0, 'maximum_nights_avg_ntm': 30.0, 'has_availability': 't', 'availability_30': 2, 'availability_60': 5, 'availability_90': 16, 'availability_365': 17, 'number_of_reviews': 311, 'number_of_reviews_ltm': 33, 'number_of_reviews_l30d': 3, 'availability_eoy': 17, 'number_of_reviews_ly': 26, 'first_review': '2012-01-09', 'last_review': '2025-09-07', 'review_scores_rating': 4.92, 'review_scores_accuracy': 4.9, 'review_scores_cleanliness': 4.94, 'review_scores_checkin': 4.95, 'review_scores_communication': 4.93, 'review_scores_location': 4.9, 'review_scores_value': 4.78, 'instant_bookable': 'f', 'calculated_host_listings_count': 1, 'calculated_host_listings_count_entire_homes': 0, 'calculated_host_listings_count_private_rooms': 1, 'calculated_host_listings_count_shared_rooms': 0, 'reviews_per_month': 1.87, 'room_type_Other': 0, 'room_type_Private room': 1, 'amsterdam': 0.0, 'apartment': 0.0, 'appartement': 0.0, 'canal': 1.0, 'center': 0.0, 'centre': 0.0, 'city': 0.0, 'cosy': 0.0, 'cozy': 0.0, 'family': 0.0, 'garden': 0.0, 'home': 0.0, 'house': 0.0, 'modern': 0.0, 'near': 0.0, 'private': 0.0, 'room': 0.0, 'spacious': 0.0, 'studio': 0.0, 'view': 0.0, 'amstelveen': 1.0, 'angeles': 0.0, 'belgium': 0.0, 'bergen': 0.0, 'brussels': 0.0, 'ca': 0.0, 'france': 0.0, 'germany': 0.0, 'groningen': 0.0, 'huizen': 0.0, 'kingdom': 0.0, 'london': 0.0, 'netherlands': 0.0, 'new': 0.0, 'ny': 0.0, 'paris': 0.0, 'united': 0.0, 'utrecht': 0.0, 'york': 0.0}
pre_data_columns=pre_data.keys()
# print(pre_data_columns)

columns_req=['host_since', 'host_response_time', 'host_response_rate',
       'host_acceptance_rate', 'host_is_superhost',
       'host_total_listings_count', 'host_verifications',
       'host_has_profile_pic', 'host_identity_verified',
       'neighbourhood_cleansed', 'latitude', 'longitude', 'property_type',
       'accommodates', 'bathrooms', 'bathrooms_text', 'bedrooms', 'beds',
       'amenities', 'price', 'minimum_nights', 'maximum_nights',
       'minimum_minimum_nights', 'maximum_minimum_nights',
       'minimum_maximum_nights', 'maximum_maximum_nights',
       'minimum_nights_avg_ntm', 'maximum_nights_avg_ntm', 'has_availability',
       'availability_30', 'availability_60', 'availability_90',
       'availability_365', 'number_of_reviews', 'number_of_reviews_ltm',
       'number_of_reviews_l30d', 'availability_eoy', 'number_of_reviews_ly',
       'first_review', 'last_review', 'review_scores_rating',
       'review_scores_accuracy', 'review_scores_cleanliness',
       'review_scores_checkin', 'review_scores_communication',
       'review_scores_location', 'review_scores_value', 'instant_bookable',
       'calculated_host_listings_count',
       'calculated_host_listings_count_entire_homes',
       'calculated_host_listings_count_private_rooms',
       'calculated_host_listings_count_shared_rooms', 'reviews_per_month',
       'room_type_Other', 'room_type_Private room', 'amsterdam', 'apartment',
       'appartement', 'canal', 'center', 'centre', 'city', 'cosy', 'cozy',
       'family', 'garden', 'home', 'house', 'modern', 'near', 'private',
       'room', 'spacious', 'studio', 'view', 'amstelveen', 'amsterdam.1',
       'angeles', 'belgium', 'bergen', 'brussels', 'ca', 'france', 'germany',
       'groningen', 'huizen', 'kingdom', 'london', 'netherlands', 'new', 'ny',
       'paris', 'united', 'utrecht', 'york']

for i in columns_req:

    if i in pre_data_columns:
        continue
    else:
        print(i)


