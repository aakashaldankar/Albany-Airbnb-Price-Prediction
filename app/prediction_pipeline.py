from app.model_loader import load_encoders, load_best_model
import os
import pandas as pd
import numpy as np

root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
MODEL_NAME = os.getenv("MODEL_NAME", "albany-price-predictor")
MODEL_ALIAS = os.getenv("MODEL_ALIAS", "champion")

def get_encoders():
    encoders=load_encoders(MODEL_NAME, MODEL_ALIAS)
    return encoders

def get_model():
    model=load_best_model(MODEL_NAME, MODEL_ALIAS)
    return model

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
