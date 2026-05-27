from app.model_loader import load_model, load_encoders
import os
import pandas as pd
import numpy as np

root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

def get_encoders():
    encoders=load_encoders()
    return encoders

def get_model():
    model=load_model('albany price predictor','champion')
    return model

# request = PredictionRequest(

#     name="Beautiful apartment in Amsterdam",

#     description="A cozy apartment near the city center",

#     host_since=2018,

#     host_location="Amsterdam, Netherlands",

#     host_response_time="within an hour",

#     host_response_rate=95,

#     host_acceptance_rate=90,

#     host_about= 'Marjan works in "eye" the dutch filmmuseum, and designs costumes for tv, film and theatre. Flip is an actor, mainly on stage, but also for film and tv. So for cultural advise, what to do, you are coming to the right place...\r\n\r\n',

#     host_is_superhost=1,

#     host_total_listings_count=3,

#     host_verifications="['email', 'phone']",

#     host_has_profile_pic=1,

#     host_identity_verified=1,

#     neighbourhood_cleansed="Centrum-West",

#     latitude=52.3676,

#     longitude=4.9041,

#     property_type="Entire rental unit",

#     room_type="Entire home/apt",

#     accommodates=4,

#     bathrooms=1.0,

#     bathrooms_text=1.0,

#     bedrooms=2.0,

#     beds=2.0,

#     amenities=25,

#     price=150.0,

#     minimum_nights=2,

#     maximum_nights=30,

#     minimum_minimum_nights=1.0,

#     maximum_minimum_nights=3.0,

#     minimum_maximum_nights=3.0,

#     maximum_maximum_nights=6.0,

#     minimum_nights_avg_ntm=2.0,

#     maximum_nights_avg_ntm=5.0,

#     has_availability=1,

#     availability_30=20,

#     availability_60=40,

#     availability_90=70,

#     availability_365=250,

#     number_of_reviews=120,

#     number_of_reviews_ltm=25,

#     number_of_reviews_l30d=5,

#     availability_eoy=150,

#     number_of_reviews_ly=30,

#     first_review=2019,

#     last_review=2025,

#     review_scores_rating=4.8,

#     review_scores_accuracy=4.9,

#     review_scores_cleanliness=4.7,

#     review_scores_checkin=4.9,

#     review_scores_communication=5.0,

#     review_scores_location=4.8,

#     review_scores_value=4.6,

#     instant_bookable=1,

#     calculated_host_listings_count=3,

#     calculated_host_listings_count_entire_homes=2,

#     calculated_host_listings_count_private_rooms=1,

#     calculated_host_listings_count_shared_rooms=0,

#     reviews_per_month=2.5
# )


def pre_process(data: dict, encoders: dict=None):

    drop_list=["id","listing_url",'scrape_id','last_scraped','source','picture_url','host_id','price',
                 'host_url','host_thumbnail_url','host_picture_url','host_listings_count',
                 'neighbourhood_group_cleansed','calendar_updated','calendar_last_scraped','license',
                 'neighborhood_overview','host_about','host_neighbourhood','neighbourhood','estimated_occupancy_l365d','estimated_revenue_l365d','host_name','description']
    
    for key in drop_list:
        data.pop(key, None)

    if encoders is None:
        encoders = get_encoders()

    host_verification_label_encoder=encoders['host_verification_label_encoder']
    neighbourhood_cleansed_target_encoder=encoders['neighbourhood_cleansed_target_encoder']
    room_type_ohe=encoders['room_type_ohe']
    property_type_target_encoder=encoders['property_type_target_encoder']
    name_tfidf_encoder=encoders['name_tfidf_encoder']
    host_location_tfidf_encoder=encoders['host_location_tfidf_encoder']

    #label encoding
    data['host_verifications']=host_verification_label_encoder[data['host_verifications']]

    label_encoder={'within an hour': 5, 'within a few hours': 4, 'within a day': 3, 'a few days or more': 2, 'not specified': 1}
    data['host_response_time']=label_encoder[data['host_response_time']]
    
    #target encoding
    data['neighbourhood_cleansed']=neighbourhood_cleansed_target_encoder[data['neighbourhood_cleansed']]
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


def prediction(request, model=None, encoders=None):

    if model is None:
        model = get_model()
    
    if encoders is None:
        encoders = get_encoders()

    data=request.model_dump()
    data=pre_process(data, encoders)
    data_df=pd.DataFrame([data])

    prediction=model.predict(data_df)
    
    return np.expm1(float(prediction[0]))

# def main():
#     result=predict(request)
#     print(result)


# if __name__=='__main__':

#     main()
