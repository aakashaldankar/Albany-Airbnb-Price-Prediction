from pydantic import BaseModel, Field
from typing import Optional, Literal

class PredictionRequest(BaseModel):

    id: Optional[int]=None
    listing_url : Optional[str]=None #url
    scrape_id : Optional[int]=None
    last_scraped : Optional[str]=None
    source : Optional[str]=None
    name: str = Field(description="About the listing")
    description : Optional[str]
    neighborhood_overview : Optional[str]=None
    picture_url : Optional[str]=None #url
    host_id : Optional[int]=None
    host_url : Optional[str]=None #url
    host_name  : Optional[str]=None
    host_since  : int = Field(ge=2009, le=3000, description="Year since  the host")    
    host_location  : str 
    host_about : Optional[str]                             
    host_response_time : Literal['within an hour','within a few hours','within a day','a few days or more','not specified'] = Field(description=" Select one of these: within an hour,within a few hours,within a day,a few days or more,not specified")                         
    host_response_rate  : int = Field(ge=0, le=100)                         
    host_acceptance_rate  : int = Field(ge=0, le=100)                        
    host_is_superhost : Literal[1,0] = Field(description="If host is superhost then 1 else 0") #Enum(t,f)  
    host_thumbnail_url : Optional[str]=None #url
    host_picture_url : Optional[str]=None  #url
    host_neighbourhood : Optional[str]=None
    host_listings_count : Optional[float]=None                     
    host_total_listings_count : float = Field(description="Number of listings that host has")                  
    host_verifications  : Literal["['email', 'phone']","['email', 'phone', 'work_email']","['phone']","['phone', 'work_email']","['email']","['email', 'work_email']"] = Field(description=" Select one of these: ['email', 'phone'],['email', 'phone', 'work_email'],['phone'],['phone', 'work_email'],['email'],['email', 'work_email']")                        
    host_has_profile_pic : Literal[1,0] = Field(description="If host has profile pic then 1 else 0")                        
    host_identity_verified : Literal[1,0] = Field(description="If host identity is verified then 1 else 0")
    neighbourhood : Optional[str]=None                  
    neighbourhood_cleansed : str = Field(description="E.g Centrum-West, Centrum-Oost, Buitenveldert - Zuidas")
    neighbourhood_group_cleansed : Optional[float]=None               
    latitude : float = Field(ge=0, le=1000, description="Latitude of the listing")                                    
    longitude : float = Field(ge=0, le=1000, description="Longitude of the listing")                                
    property_type : Literal['Private room in houseboat', 'Private room in rental unit',
       'Private room in condo', 'Entire rental unit',
       'Entire guest suite', 'Entire condo', 'Entire townhouse',
       'Entire loft', 'Private room in home', 'Private room in boat',
       'Private room in bed and breakfast', 'Entire home',
       'Room in boutique hotel', 'Private room in loft',
       'Private room in guest suite', 'Private room in villa',
       'Entire guesthouse', 'Boat', 'Private room in townhouse',
       'Houseboat', 'Private room in farm stay',
       'Room in bed and breakfast', 'Private room in guesthouse',
       'Shared room in home', 'Private room in windmill',
       'Shared room in bed and breakfast', 'Private room in cottage',
       'Private room in nature lodge', 'Private room in hostel',
       'Private room in serviced apartment', 'Entire villa', 'Tiny home',
       'Private room in casa particular', 'Room in aparthotel', 'Barn',
       'Private room in bungalow', 'Private room in tiny home',
       'Entire cabin', 'Room in hotel', 'Entire serviced apartment',
       'Entire place', 'Entire cottage', 'Private room',
       'Private room in cabin', 'Private room in barn',
       'Room in serviced apartment', 'Private room in earthen home',
       'Entire vacation home', 'Shared room in houseboat',
       'Room in hostel', 'Shared room in hostel', 'Cave',
       'Shared room in hotel', 'Camper/RV', 'Yurt', 'Earthen home',
       'Casa particular', 'Private room in vacation home', 'Tower',
       'Private room in hut', 'Hut', 'Tent', 'Shepherd’s hut']                              
    room_type : Literal['Private room', 'Entire home/apt', 'Hotel room', 'Shared room']                                  
    accommodates : int = Field(description="No of accommodates")                                
    bathrooms : float = Field(description="Bathroom size")                                  
    bathrooms_text : float = Field(ge=0, le=13, description="The number of bathroms can be 1, 1.5, 2, 2.5...")                               
    bedrooms : float = Field(description="Size of bathroom. E.g 1.5, 1, 2.5...")                                    
    beds : float                                         
    amenities  : int = Field(ge=0, le=200, description="The number of amenities provided")                                 
    price : float = Field(ge=0, le=10000000000, description="price must be in dollars")                                       
    minimum_nights : int = Field(ge=0, le=100)                              
    maximum_nights : int = Field(ge=0, le=100)                                
    minimum_minimum_nights : float = Field(ge=0, le=10)                      
    maximum_minimum_nights : float = Field(ge=0, le=10)                     
    minimum_maximum_nights  : float = Field(ge=0, le=10)                 
    maximum_maximum_nights  : float = Field(ge=0, le=10)                     
    minimum_nights_avg_ntm  : float = Field(ge=0, le=10)                     
    maximum_nights_avg_ntm : float = Field(ge=0, le=10) 
    calendar_updated : Optional[float]=None                   
    has_availability  : Literal[1,0] = Field(description="If host has availability then 1 else 0")                          
    availability_30 : int = Field(ge=0, le=31)                               
    availability_60 : int = Field(ge=0, le=60)                            
    availability_90 : int = Field(ge=0, le=90)                             
    availability_365 : int = Field(ge=0, le=365)
    calendar_last_scraped : Optional[str]=None                        
    number_of_reviews : int = Field(ge=0)                          
    number_of_reviews_ltm : int = Field(ge=0)                       
    number_of_reviews_l30d : int = Field(ge=0)                       
    availability_eoy : int = Field(ge=0)                              
    number_of_reviews_ly : int = Field(ge=0) 
    estimated_occupancy_l365d : Optional[int]=None
    estimated_revenue_l365d : Optional[float]=None                      
    first_review : int = Field(ge=2009, le=3000, description="Year of first review")                                
    last_review : int = Field(ge=2010, le=3000, description="Year of last review")                                  
    review_scores_rating : float = Field(ge=0, le=5)                        
    review_scores_accuracy : float = Field(ge=0, le=5)                      
    review_scores_cleanliness : float = Field(ge=0, le=5)                  
    review_scores_checkin : float = Field(ge=0, le=5)                       
    review_scores_communication : float = Field(ge=0, le=5)                
    review_scores_location : float = Field(ge=0, le=5)                     
    review_scores_value : float = Field(ge=0, le=5) 
    license : Optional[str]=None                       
    instant_bookable : Literal[1,0] = Field(description="If instantly bookable then 1 else 0")                            
    calculated_host_listings_count : int = Field(ge=0, le=100)               
    calculated_host_listings_count_entire_homes : int = Field(ge=0, le=100)
    calculated_host_listings_count_private_rooms : int = Field(ge=0, le=100)
    calculated_host_listings_count_shared_rooms : int = Field(ge=0, le=100) 
    reviews_per_month : float = Field(ge=0, le=100)                         

class PredictionResult(BaseModel):
    result: float