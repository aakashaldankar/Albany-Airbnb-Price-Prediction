from pydantic import BaseModel
from typing import Optional, List, Literal

class PredictionRequest(BaseModel):

    id: Optional[int]=None
    listing_url : Optional[str]=None #url
    scrape_id : Optional[int]=None
    last_scraped : Optional[str]=None
    source : Optional[str]=None
    name: str
    description : Optional[str]
    neighborhood_overview : Optional[str]=None
    picture_url : Optional[str]=None #url
    host_id : Optional[int]=None
    host_url : Optional[str]=None #url
    host_name  : Optional[str]=None
    host_since  : str     
    host_location  : str 
    host_about : Optional[str]                             
    host_response_time : str                           
    host_response_rate  : str                          
    host_acceptance_rate  : str                         
    host_is_superhost : Literal['t','f'] #Enum(t,f)  
    host_thumbnail_url : Optional[str]=None #url
    host_picture_url : Optional[str]=None  #url
    host_neighbourhood : Optional[str]=None
    host_listings_count : Optional[float]=None                     
    host_total_listings_count : float                   
    host_verifications  : List[str]                        
    host_has_profile_pic : Literal['t','f']                        
    host_identity_verified : Literal['t','f']
    neighbourhood : Optional[str]=None                  
    neighbourhood_cleansed : str    
    neighbourhood_group_cleansed : Optional[float]=None               
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
    calendar_updated : Optional[float]=None                   
    has_availability  : str                            
    availability_30 : int                               
    availability_60 : int                               
    availability_90 : int                              
    availability_365 : int  
    calendar_last_scraped : Optional[str]=None                        
    number_of_reviews : int                           
    number_of_reviews_ltm : int                        
    number_of_reviews_l30d : int                        
    availability_eoy : int                             
    number_of_reviews_ly : int 
    estimated_occupancy_l365d : Optional[int]=None
    estimated_revenue_l365d : Optional[float]=None                      
    first_review : str                                
    last_review : str                                  
    review_scores_rating : float                         
    review_scores_accuracy : float                       
    review_scores_cleanliness : float                   
    review_scores_checkin : float                       
    review_scores_communication : float                 
    review_scores_location : float                      
    review_scores_value : float  
    license : Optional[str]=None                       
    instant_bookable : str                            
    calculated_host_listings_count : int               
    calculated_host_listings_count_entire_homes : int 
    calculated_host_listings_count_private_rooms : int 
    calculated_host_listings_count_shared_rooms : int  
    reviews_per_month : float                            

class PredictionResult(BaseModel):
    result: float