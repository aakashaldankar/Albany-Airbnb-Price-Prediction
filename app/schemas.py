from pydantic import BaseModel, Field
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
    host_since  : int = Field(ge=2009, le=3000, description="Year since  the host")    
    host_location  : str 
    host_about : Optional[str]                             
    host_response_time : Literal['within an hour','within a few hours','within a day','a few days or more','not specified']                          
    host_response_rate  : int = Field(ge=0, le=100)                         
    host_acceptance_rate  : int = Field(ge=0, le=100)                        
    host_is_superhost : Literal[1,0] = Field(description="If host is superhost then 1 else 0") #Enum(t,f)  
    host_thumbnail_url : Optional[str]=None #url
    host_picture_url : Optional[str]=None  #url
    host_neighbourhood : Optional[str]=None
    host_listings_count : Optional[float]=None                     
    host_total_listings_count : float                   
    host_verifications  : Literal["['email', 'phone']","['email', 'phone', 'work_email']","['phone']","['phone', 'work_email']","['email']","['email', 'work_email']"]                        
    host_has_profile_pic : Literal[1,0] = Field(description="If host has profile pic then 1 else 0")                        
    host_identity_verified : Literal[1,0] = Field(description="If host identity is verified then 1 else 0")
    neighbourhood : Optional[str]=None                  
    neighbourhood_cleansed : str    
    neighbourhood_group_cleansed : Optional[float]=None               
    latitude : float                                     
    longitude : float                                    
    property_type : str                               
    room_type : str                                  
    accommodates : int                                
    bathrooms : float                                   
    bathrooms_text : float = Field(ge=0, le=13, description="The number of bathroms can be 1, 1.5, 2, 2.5...")                               
    bedrooms : float                                     
    beds : float                                         
    amenities  : int = Field(ge=0, le=200, description="The number of amenities provided")                                 
    price : float = Field(ge=0, le=10000000000, description="price must be in dollars")                                       
    minimum_nights : int                                
    maximum_nights : int                                
    minimum_minimum_nights : float                       
    maximum_minimum_nights : float                      
    minimum_maximum_nights  : float                      
    maximum_maximum_nights  : float                      
    minimum_nights_avg_ntm  : float                      
    maximum_nights_avg_ntm : float  
    calendar_updated : Optional[float]=None                   
    has_availability  : Literal[1,0] = Field(description="If host has availability then 1 else 0")                          
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
    first_review : int = Field(ge=2009, le=3000, description="Year of first review")                                
    last_review : int = Field(ge=2010, le=3000, description="Year of last review")                                  
    review_scores_rating : float                         
    review_scores_accuracy : float                       
    review_scores_cleanliness : float                   
    review_scores_checkin : float                       
    review_scores_communication : float                 
    review_scores_location : float                      
    review_scores_value : float  
    license : Optional[str]=None                       
    instant_bookable : Literal[1,0] = Field(description="If instantly bookable then 1 else 0")                            
    calculated_host_listings_count : int               
    calculated_host_listings_count_entire_homes : int 
    calculated_host_listings_count_private_rooms : int 
    calculated_host_listings_count_shared_rooms : int  
    reviews_per_month : float                            

class PredictionResult(BaseModel):
    result: float