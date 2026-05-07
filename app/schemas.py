from pydantic import BaseModel
from typing import Optional, List, Literal

class PredictionRequest(BaseModel):

    id: int
    listing_url : str #url
    scrape_id : int
    last_scraped : str
    source : str
    name: str
    description : str
    neighborhood_overview : str
    picture_url : str #url
    host_id : int
    host_url : str #url
    host_name  : str
    host_since  : str     
    host_location  : str 
    host_about : str                             
    host_response_time : str                           
    host_response_rate  : str                          
    host_acceptance_rate  : str                         
    host_is_superhost : Literal['t','f'] #Enum(t,f)  
    host_thumbnail_url : str #url
    host_picture_url : str  #url
    host_neighbourhood : str  
    host_listings_count : float                      
    host_total_listings_count : float                   
    host_verifications  : List[str]                        
    host_has_profile_pic : Literal['t','f']                        
    host_identity_verified : Literal['t','f']
    neighbourhood : str                      
    neighbourhood_cleansed : str    
    neighbourhood_group_cleansed : float                   
    latitude : float                                     
    longitude : float                                    
    property_type : str                               
    room_type : str                                  
    accommodates : int                                
    bathrooms : float                                   
    bathrooms_text : str                               
    bedrooms : float                                     
    beds : float                                         
    amenities  : str                                   
    price : str                                        
    minimum_nights : int                                
    maximum_nights : int                                
    minimum_minimum_nights : float                       
    maximum_minimum_nights : float                      
    minimum_maximum_nights  : float                      
    maximum_maximum_nights  : float                      
    minimum_nights_avg_ntm  : float                      
    maximum_nights_avg_ntm : float  
    calendar_updated : float                     
    has_availability  : str                            
    availability_30 : int                               
    availability_60 : int                               
    availability_90 : int                              
    availability_365 : int  
    calendar_last_scraped : str                           
    number_of_reviews : int                           
    number_of_reviews_ltm : int                        
    number_of_reviews_l30d : int                        
    availability_eoy : int                             
    number_of_reviews_ly : int 
    estimated_occupancy_l365d : int
    estimated_revenue_l365d : float                       
    first_review : str                                
    last_review : str                                  
    review_scores_rating : float                         
    review_scores_accuracy : float                       
    review_scores_cleanliness : float                   
    review_scores_checkin : float                       
    review_scores_communication : float                 
    review_scores_location : float                      
    review_scores_value : float  
    license : str                       
    instant_bookable : str                            
    calculated_host_listings_count : int               
    calculated_host_listings_count_entire_homes : int 
    calculated_host_listings_count_private_rooms : int 
    calculated_host_listings_count_shared_rooms : int  
    reviews_per_month : float                            
