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

model=load_model('albany price predictor','Production')

root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

# data={'id': 27886,
#  'listing_url': 'https://www.airbnb.com/rooms/27886',
#  'scrape_id': 20250911031321,
#  'last_scraped': '2025-09-11',
#  'source': 'city scrape',
#  'name': 'Romantic, stylish B&B houseboat in canal district',
#  'description': 'Stylish and romantic houseboat on fantastic historic location with breathtaking view.  Wheelhouse, deckhouse and captains room. Central, quiet. Great breakfast, 2 vanMoof design bikes and a Canadian Canoe are included. Just read the reviews on tripadvisor for instance!',
#  'neighborhood_overview': 'Central, quiet, safe, clean and beautiful.',
#  'picture_url': 'https://a0.muscache.com/pictures/02c2da9d-660e-451d-8a51-2f7a17469df7.jpg',
#  'host_id': 97647,
#  'host_url': 'https://www.airbnb.com/users/show/97647',
#  'host_name': 'Flip',
#  'host_since': 2023,
#  'host_location': 'Amsterdam, Netherlands',
#  'host_about': 'Marjan works in "eye" the dutch filmmuseum, and designs costumes for tv, film and theatre. Flip is an actor, mainly on stage, but also for film and tv. So for cultural advise, what to do, you are coming to the right place...\r\n\r\n',
#  'host_response_time': "within an hour",
#  'host_response_rate': 100,
#  'host_acceptance_rate': 97,
#  'host_is_superhost': 1,
#  'host_thumbnail_url': 'https://a0.muscache.com/im/users/97647/profile_pic/1273275077/original.jpg?aki_policy=profile_small',
#  'host_picture_url': 'https://a0.muscache.com/im/users/97647/profile_pic/1273275077/original.jpg?aki_policy=profile_x_medium',
#  'host_neighbourhood': 'Westelijke Eilanden',
#  'host_listings_count': 1.0,
#  'host_total_listings_count': 1.0,
#  'host_verifications': "['email', 'phone']",
#  'host_has_profile_pic': 1,
#  'host_identity_verified': 1,
#  'neighbourhood': 'Amsterdam, North Holland, Netherlands',
#  'neighbourhood_cleansed': 'Centrum-West',
#  'neighbourhood_group_cleansed': "Nan",
#  'latitude': 52.38761,
#  'longitude': 4.89188,
#  'property_type': 'Private room in houseboat',
#  'room_type': 'Private room',
#  'accommodates': 2,
#  'bathrooms': 1.5,
#  'bathrooms_text': 1.5,
#  'bedrooms': 1.0,
#  'beds': 1.0,
#  'amenities': 25,
#  'price': 132.00,
#  'minimum_nights': 3,
#  'maximum_nights': 356,
#  'minimum_minimum_nights': 3.0,
#  'maximum_minimum_nights': 3.0,
#  'minimum_maximum_nights': 30.0,
#  'maximum_maximum_nights': 30.0,
#  'minimum_nights_avg_ntm': 3.0,
#  'maximum_nights_avg_ntm': 30.0,
#  'calendar_updated': "None",
#  'has_availability': 1,
#  'availability_30': 2,
#  'availability_60': 5,
#  'availability_90': 16,
#  'availability_365': 17,
#  'calendar_last_scraped': '2025-09-11',
#  'number_of_reviews': 311,
#  'number_of_reviews_ltm': 33,
#  'number_of_reviews_l30d': 3,
#  'availability_eoy': 17,
#  'number_of_reviews_ly': 26,
#  'estimated_occupancy_l365d': 255,
#  'estimated_revenue_l365d': 33660.0,
#  'first_review': 2009,
#  'last_review': 2025,
#  'review_scores_rating': 4.92,
#  'review_scores_accuracy': 4.9,
#  'review_scores_cleanliness': 4.94,
#  'review_scores_checkin': 4.95,
#  'review_scores_communication': 4.93,
#  'review_scores_location': 4.9,
#  'review_scores_value': 4.78,
#  'license': '0363 974D 4986 7411 88D8',
#  'instant_bookable': 0,
#  'calculated_host_listings_count': 1,
#  'calculated_host_listings_count_entire_homes': 0,
#  'calculated_host_listings_count_private_rooms': 1,
#  'calculated_host_listings_count_shared_rooms': 0,
#  'reviews_per_month': 1.87}


def pre_process(data: dict):

    drop_list=["id","listing_url",'scrape_id','last_scraped','source','picture_url','host_id','price',
                 'host_url','host_thumbnail_url','host_picture_url','host_listings_count',
                 'neighbourhood_group_cleansed','calendar_updated','calendar_last_scraped','license',
                 'neighborhood_overview','host_about','host_neighbourhood','neighbourhood','estimated_occupancy_l365d','estimated_revenue_l365d','host_name','description']
    neighbourhood_cleansed = data['neighbourhood_cleansed']
    
    for key in drop_list:
        data.pop(key, None)

    #label encoding
    data['host_verifications']=host_verification_label_encoder[data['host_verifications']]

    label_encoder={'within an hour': 5, 'within a few hours': 4, 'within a day': 3, 'a few days or more': 2, 'not specified': 1}
    data['host_response_time']=label_encoder[data['host_response_time']]
    
    #target encoding
    data['neighbourhood_cleansed']=neighbourhood_cleansed_target_encoder[neighbourhood_cleansed]
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
    feature_names = [f"name_{feature}" for feature in name_tfidf_encoder.get_feature_names_out()]
    vector_df=pd.DataFrame(vector.toarray(), columns=feature_names) 
    data.pop('name')
    data.update(vector_df.iloc[0].to_dict())

    vector=host_location_tfidf_encoder.transform([data['host_location']])
    feature_names = [f"host_location_{feature}" for feature in host_location_tfidf_encoder.get_feature_names_out()]
    vector_df=pd.DataFrame(vector.toarray(), columns=feature_names) 
    data.pop('host_location')
    data.update(vector_df.iloc[0].to_dict())

    return data


def predict(request):

    data=request.model_dump()
    data=pre_process(data)
    data_df=pd.DataFrame([data])
    prediction=model.predict(data_df)
    
    return np.expm1(float(prediction[0]))
