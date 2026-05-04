import great_expectations as gx
import pandas as pd
import os
from src.logger import get_logger

root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
train_data_path = os.path.join(root_dir,'central_data','raw_data', 'train_data.csv')

script=os.path.basename(__file__)
logger=get_logger(script)

def validate(df: pd.DataFrame):
        
    try:

        gx_df=gx.from_pandas(df)

        # Expectations
        gx_df.expect_column_to_exist('price')
        gx_df.expect_column_values_to_be_of_type("name", "string")
        gx_df.expect_table_columns_to_match_ordered_list(["name","descriptions","host_name","host_since","host_location","host_response_time",
                                                        "host_response_rate","host_acceptance_rate","host_is_superhost","host_total_listings_count",
                                                        "host_verifications","host_has_profile_pic","host_identity_verified","neighbourhood_cleansed",
                                                        "latitude","longitude","property_type","room_type","accommodates","bathrooms","bathrooms_text",
                                                        "bedrooms","beds","amenities","price","minimum_nights","maximum_nights","minimum_minimum_nights",
                                                        "maximum_minimum_nights","minimum_maximum_nights","maximum_maximum_nights",
                                                        "minimum_nights_avg_ntm","maximum_nights_avg_ntm","has_availability","availability_30",
                                                        "availability_60","availability_90","availability_365","number_of_reviews","number_of_reviews_ltm",
                                                        "number_of_reviews_l30d","availability_eoy","number_of_reviews_ly","first_review","last_review",
                                                        "review_scores_rating","review_scores_accuracy","review_scores_cleanliness",
                                                        "review_scores_checkin","review_scores_communication","review_scores_location",
                                                        "review_scores_value","instant_bookable","calculated_host_listings_count",
                                                        "calculated_host_listings_count_entire_homes","calculated_host_listings_count_private_rooms",
                                                        "calculated_host_listings_count_shared_rooms","reviews_per_month"])
        
        # null value check
        gx_df.expect_column_values_to_not_be_null("price")
        gx_df.expect_column_values_to_be_null("description")

        # value range
        gx_df.expect_column_values_to_be_between("latitude", min_value=0, max_value=1000)

        results=gx_df.validate()

        print(results)

        if not results['success']:
            raise ValueError("Data Validation Failed")
        
        logger.info("data validation performed successfully")

    except Exception as e:
        logger.error("unexpected error occured, %s", e)
        raise


def main():

    df=pd.read_csv(train_data_path)

    validate(df)


if __name__=='__main__':
    main()




    
    

    



