import gradio as gr

from app.prediction_pipeline import predict
from app.schemas import PredictionRequest

PROPERTY_TYPES = [
    "Private room in houseboat",
    "Private room in rental unit",
    "Private room in condo",
    "Entire rental unit",
    "Entire guest suite",
    "Entire condo",
    "Entire townhouse",
    "Entire loft",
    "Private room in home",
    "Private room in boat",
    "Private room in bed and breakfast",
    "Entire home",
    "Room in boutique hotel",
    "Private room in loft",
    "Private room in guest suite",
    "Private room in villa",
    "Entire guesthouse",
    "Boat",
    "Private room in townhouse",
    "Houseboat",
    "Private room in farm stay",
    "Room in bed and breakfast",
    "Private room in guesthouse",
    "Shared room in home",
    "Private room in windmill",
    "Shared room in bed and breakfast",
    "Private room in cottage",
    "Private room in nature lodge",
    "Private room in hostel",
    "Private room in serviced apartment",
    "Entire villa",
    "Tiny home",
    "Private room in casa particular",
    "Room in aparthotel",
    "Barn",
    "Private room in bungalow",
    "Private room in tiny home",
    "Entire cabin",
    "Room in hotel",
    "Entire serviced apartment",
    "Entire place",
    "Entire cottage",
    "Private room",
    "Private room in cabin",
    "Private room in barn",
    "Room in serviced apartment",
    "Private room in earthen home",
    "Entire vacation home",
    "Shared room in houseboat",
    "Room in hostel",
    "Shared room in hostel",
    "Cave",
    "Shared room in hotel",
    "Camper/RV",
    "Yurt",
    "Earthen home",
    "Casa particular",
    "Private room in vacation home",
    "Tower",
    "Private room in hut",
    "Hut",
    "Tent",
    "Shepherd’s hut",
]

NEIGHBOURHOODS = [
    "Centrum-West",
    "Centrum-Oost",
    "De Pijp - Rivierenbuurt",
    "Westerpark",
    "Oud-Oost",
    "Oud-West",
    "Bos en Lommer",
    "Buitenveldert - Zuidas",
    "De Baarsjes - Oud-West",
    "Watergraafsmeer",
    "Noord-West",
    "Noord-Oost",
]

HOST_RESPONSE_TIMES = [
    "within an hour",
    "within a few hours",
    "within a day",
    "a few days or more",
    "not specified",
]

HOST_VERIFICATIONS = [
    "['email', 'phone']",
    "['email', 'phone', 'work_email']",
    "['phone']",
    "['phone', 'work_email']",
    "['email']",
    "['email', 'work_email']",
]

DEFAULT_PAYLOAD = {
    "id": 27886,
    "listing_url": "https://www.airbnb.com/rooms/27886",
    "scrape_id": 20250911031321,
    "last_scraped": "2025-09-11",
    "source": "city scrape",
    "name": "Romantic, stylish B&B houseboat in canal district",
    "description": "Stylish houseboat on a central, quiet canal.",
    "neighborhood_overview": "Central, quiet, safe, clean and beautiful.",
    "picture_url": "https://a0.muscache.com/pictures/sample.jpg",
    "host_id": 97647,
    "host_url": "https://www.airbnb.com/users/show/97647",
    "host_name": "Demo Host",
    "host_since": 2023,
    "host_location": "Amsterdam, Netherlands",
    "host_about": "Experienced local host.",
    "host_response_time": "within an hour",
    "host_response_rate": 100,
    "host_acceptance_rate": 97,
    "host_is_superhost": 1,
    "host_thumbnail_url": "https://a0.muscache.com/sample-profile-small.jpg",
    "host_picture_url": "https://a0.muscache.com/sample-profile.jpg",
    "host_neighbourhood": "Centrum-West",
    "host_listings_count": 1.0,
    "host_total_listings_count": 1.0,
    "host_verifications": "['email', 'phone']",
    "host_has_profile_pic": 1,
    "host_identity_verified": 1,
    "neighbourhood": "Amsterdam, North Holland, Netherlands",
    "neighbourhood_cleansed": "Centrum-West",
    "neighbourhood_group_cleansed": None,
    "latitude": 52.38761,
    "longitude": 4.89188,
    "property_type": "Private room in houseboat",
    "room_type": "Private room",
    "accommodates": 2,
    "bathrooms": 1.5,
    "bathrooms_text": 1.5,
    "bedrooms": 1.0,
    "beds": 1.0,
    "amenities": 25,
    "price": 132.0,
    "minimum_nights": 3,
    "maximum_nights": 30,
    "minimum_minimum_nights": 3.0,
    "maximum_minimum_nights": 3.0,
    "minimum_maximum_nights": 10.0,
    "maximum_maximum_nights": 10.0,
    "minimum_nights_avg_ntm": 3.0,
    "maximum_nights_avg_ntm": 10.0,
    "calendar_updated": None,
    "has_availability": 1,
    "availability_30": 2,
    "availability_60": 5,
    "availability_90": 16,
    "availability_365": 17,
    "calendar_last_scraped": "2025-09-11",
    "number_of_reviews": 311,
    "number_of_reviews_ltm": 33,
    "number_of_reviews_l30d": 3,
    "availability_eoy": 17,
    "number_of_reviews_ly": 26,
    "estimated_occupancy_l365d": 255,
    "estimated_revenue_l365d": 33660.0,
    "first_review": 2009,
    "last_review": 2025,
    "review_scores_rating": 4.92,
    "review_scores_accuracy": 4.9,
    "review_scores_cleanliness": 4.94,
    "review_scores_checkin": 4.95,
    "review_scores_communication": 4.93,
    "review_scores_location": 4.9,
    "review_scores_value": 4.78,
    "license": "0363 974D 4986 7411 88D8",
    "instant_bookable": 0,
    "calculated_host_listings_count": 1,
    "calculated_host_listings_count_entire_homes": 0,
    "calculated_host_listings_count_private_rooms": 1,
    "calculated_host_listings_count_shared_rooms": 0,
    "reviews_per_month": 1.87,
}

PRESETS = {
    "Canal private room": {},
    "Central entire apartment": {
        "name": "Bright entire apartment near museums and canals",
        "property_type": "Entire rental unit",
        "room_type": "Entire home/apt",
        "accommodates": 4,
        "bathrooms": 1.0,
        "bathrooms_text": 1.0,
        "bedrooms": 2.0,
        "beds": 2.0,
        "amenities": 42,
        "neighbourhood_cleansed": "Centrum-Oost",
        "minimum_nights": 2,
        "maximum_nights": 30,
        "availability_30": 8,
        "availability_60": 18,
        "availability_90": 31,
        "availability_365": 140,
        "review_scores_rating": 4.78,
        "reviews_per_month": 2.3,
    },
    "Budget shared room": {
        "name": "Simple shared room with transit access",
        "property_type": "Shared room in hostel",
        "room_type": "Shared room",
        "accommodates": 1,
        "bathrooms": 1.0,
        "bathrooms_text": 1.0,
        "bedrooms": 1.0,
        "beds": 1.0,
        "amenities": 14,
        "neighbourhood_cleansed": "Noord-West",
        "host_is_superhost": 0,
        "host_identity_verified": 1,
        "minimum_nights": 1,
        "maximum_nights": 14,
        "availability_30": 20,
        "availability_60": 42,
        "availability_90": 70,
        "availability_365": 240,
        "review_scores_rating": 4.35,
        "reviews_per_month": 0.8,
    },
}

CSS = """
.gradio-container {
    max-width: 1280px !important;
}
.app-header {
    border: 1px solid #d8e2dc;
    border-radius: 8px;
    padding: 20px 22px;
    background: linear-gradient(135deg, #f6fff8 0%, #edf6f9 100%);
}
.app-header h1 {
    margin: 0 0 8px;
    font-size: 2rem;
    line-height: 1.15;
    color: #102a43;
    font-weight: 700;
}
.app-header p {
    margin: 0;
    color: #334155;
    font-size: 1rem;
}
.result-panel {
    border: 1px solid #d0d5dd;
    border-radius: 8px;
    padding: 22px;
    background: #ffffff;
}
.price-card {
    border-radius: 8px;
    padding: 36px 28px;
    background: linear-gradient(135deg, #102a43 0%, #243b53 100%);
    color: #ffffff;
    box-shadow: 0 10px 28px rgba(16, 42, 67, 0.22);
    min-height: 190px;
    display: flex;
    flex-direction: column;
    justify-content: center;
    text-align: center;
}

.price-card .label {
    color: #d9e2ec;
    font-size: 1rem;
    font-weight: 650;
    margin-bottom: 12px;
    letter-spacing: 0;
    text-transform: uppercase;
}

.price-card .value {
    font-size: clamp(3.75rem, 7vw, 5.5rem);
    font-weight: 800;
    line-height: 1;
    color: #ffffff;
}
.status-ok {
    color: #027a48;
    font-weight: 650;
}
.status-error {
    color: #b42318;
    font-weight: 650;
}
"""


def merged_payload(**updates):
    payload = DEFAULT_PAYLOAD.copy()
    payload.update({key: value for key, value in updates.items() if value is not None})
    return payload


def predict_price(
    name,
    property_type,
    room_type,
    accommodates,
    bedrooms,
    beds,
    bathrooms,
    amenities,
    neighbourhood_cleansed,
    latitude,
    longitude,
    host_since,
    host_location,
    host_response_time,
    host_response_rate,
    host_acceptance_rate,
    host_is_superhost,
    host_total_listings_count,
    host_verifications,
    host_has_profile_pic,
    host_identity_verified,
    minimum_nights,
    maximum_nights,
    availability_30,
    availability_60,
    availability_90,
    availability_365,
    number_of_reviews,
    number_of_reviews_ltm,
    number_of_reviews_l30d,
    first_review,
    last_review,
    review_scores_rating,
    review_scores_accuracy,
    review_scores_cleanliness,
    review_scores_checkin,
    review_scores_communication,
    review_scores_location,
    review_scores_value,
    instant_bookable,
    reviews_per_month,
):
    bounded_maximum_nights = min(float(maximum_nights), 10.0)
    payload = merged_payload(
        name=name,
        property_type=property_type,
        room_type=room_type,
        accommodates=int(accommodates),
        bedrooms=float(bedrooms),
        beds=float(beds),
        bathrooms=float(bathrooms),
        bathrooms_text=float(bathrooms),
        amenities=int(amenities),
        neighbourhood_cleansed=neighbourhood_cleansed,
        latitude=float(latitude),
        longitude=float(longitude),
        host_since=int(host_since),
        host_location=host_location,
        host_response_time=host_response_time,
        host_response_rate=int(host_response_rate),
        host_acceptance_rate=int(host_acceptance_rate),
        host_is_superhost=int(host_is_superhost),
        host_total_listings_count=float(host_total_listings_count),
        host_verifications=host_verifications,
        host_has_profile_pic=int(host_has_profile_pic),
        host_identity_verified=int(host_identity_verified),
        minimum_nights=int(minimum_nights),
        maximum_nights=int(maximum_nights),
        minimum_minimum_nights=float(minimum_nights),
        maximum_minimum_nights=float(minimum_nights),
        minimum_maximum_nights=bounded_maximum_nights,
        maximum_maximum_nights=bounded_maximum_nights,
        minimum_nights_avg_ntm=float(minimum_nights),
        maximum_nights_avg_ntm=bounded_maximum_nights,
        availability_30=int(availability_30),
        availability_60=int(availability_60),
        availability_90=int(availability_90),
        availability_365=int(availability_365),
        availability_eoy=int(availability_365),
        number_of_reviews=int(number_of_reviews),
        number_of_reviews_ltm=int(number_of_reviews_ltm),
        number_of_reviews_l30d=int(number_of_reviews_l30d),
        number_of_reviews_ly=int(number_of_reviews_ltm),
        first_review=int(first_review),
        last_review=int(last_review),
        review_scores_rating=float(review_scores_rating),
        review_scores_accuracy=float(review_scores_accuracy),
        review_scores_cleanliness=float(review_scores_cleanliness),
        review_scores_checkin=float(review_scores_checkin),
        review_scores_communication=float(review_scores_communication),
        review_scores_location=float(review_scores_location),
        review_scores_value=float(review_scores_value),
        instant_bookable=int(instant_bookable),
        reviews_per_month=float(reviews_per_month),
    )

    try:
        prediction = predict(PredictionRequest(**payload))
    except Exception as exc:
        return (
            render_price(None),
            "<span class='status-error'>Local model inference failed</span>",
            str(exc),
        )

    submitted = {
        "listing": name,
        "property_type": property_type,
        "room_type": room_type,
        "neighbourhood": neighbourhood_cleansed,
        "accommodates": accommodates,
        "reviews": number_of_reviews,
    }
    return (
        render_price(prediction),
        "<span class='status-ok'>Prediction generated by the local model</span>",
        "\n".join(f"{key}: {value}" for key, value in submitted.items()),
    )


def render_price(value):
    if value is None:
        amount = "--"
    else:
        amount = f"${value:,.0f}"
    return f"""
    <div class="price-card">
        <div class="label">Predicted nightly price</div>
        <div class="value">{amount}</div>
    </div>
    """


def apply_preset(preset_name):
    payload = merged_payload(**PRESETS[preset_name])
    return (
        payload["name"],
        payload["property_type"],
        payload["room_type"],
        payload["accommodates"],
        payload["bedrooms"],
        payload["beds"],
        payload["bathrooms"],
        payload["amenities"],
        payload["neighbourhood_cleansed"],
        payload["host_is_superhost"],
        payload["minimum_nights"],
        payload["maximum_nights"],
        payload["availability_30"],
        payload["availability_60"],
        payload["availability_90"],
        payload["availability_365"],
        payload["review_scores_rating"],
        payload["reviews_per_month"],
    )


with gr.Blocks(
    title="Albany Airbnb Price Predictor",
) as demo:
    gr.HTML(
        """
        <section class="app-header">
            <h1>Albany Airbnb Price Predictor</h1>
            <p>Estimate a nightly listing price from host, location, availability, and review signals.</p>
        </section>
        """
    )

    with gr.Row(equal_height=False):
        with gr.Column(scale=7, min_width=560):
            preset = gr.Dropdown(
                choices=list(PRESETS),
                value="Canal private room",
                label="Demo preset",
            )

            with gr.Tab("Listing"):
                name = gr.Textbox(
                    label="Listing title",
                    value=DEFAULT_PAYLOAD["name"],
                    lines=2,
                )
                with gr.Row():
                    property_type = gr.Dropdown(
                        PROPERTY_TYPES,
                        value=DEFAULT_PAYLOAD["property_type"],
                        label="Property type",
                    )
                    room_type = gr.Dropdown(
                        ["Private room", "Entire home/apt", "Hotel room", "Shared room"],
                        value=DEFAULT_PAYLOAD["room_type"],
                        label="Room type",
                    )
                with gr.Row():
                    accommodates = gr.Slider(1, 16, value=2, step=1, label="Accommodates")
                    bedrooms = gr.Number(value=1.0, minimum=0, label="Bedrooms")
                    beds = gr.Number(value=1.0, minimum=0, label="Beds")
                with gr.Row():
                    bathrooms = gr.Number(value=1.5, minimum=0, label="Bathrooms")
                    amenities = gr.Slider(0, 200, value=25, step=1, label="Amenities count")

            with gr.Tab("Location"):
                with gr.Row():
                    neighbourhood_cleansed = gr.Dropdown(
                        NEIGHBOURHOODS,
                        value=DEFAULT_PAYLOAD["neighbourhood_cleansed"],
                        label="Neighbourhood",
                        allow_custom_value=True,
                    )
                    host_location = gr.Textbox(
                        value=DEFAULT_PAYLOAD["host_location"],
                        label="Host location",
                    )
                with gr.Row():
                    latitude = gr.Number(value=52.38761, label="Latitude")
                    longitude = gr.Number(value=4.89188, label="Longitude")

            with gr.Tab("Host"):
                with gr.Row():
                    host_since = gr.Slider(2009, 2030, value=2023, step=1, label="Host since")
                    host_total_listings_count = gr.Number(
                        value=1.0,
                        minimum=0,
                        label="Host total listings",
                    )
                with gr.Row():
                    host_response_time = gr.Dropdown(
                        HOST_RESPONSE_TIMES,
                        value=DEFAULT_PAYLOAD["host_response_time"],
                        label="Response time",
                    )
                    host_verifications = gr.Dropdown(
                        HOST_VERIFICATIONS,
                        value=DEFAULT_PAYLOAD["host_verifications"],
                        label="Host verifications",
                    )
                with gr.Row():
                    host_response_rate = gr.Slider(0, 100, value=100, step=1, label="Response rate")
                    host_acceptance_rate = gr.Slider(0, 100, value=97, step=1, label="Acceptance rate")
                with gr.Row():
                    host_is_superhost = gr.Radio([1, 0], value=1, label="Superhost")
                    host_has_profile_pic = gr.Radio([1, 0], value=1, label="Profile photo")
                    host_identity_verified = gr.Radio([1, 0], value=1, label="Identity verified")

            with gr.Tab("Stay & Availability"):
                with gr.Row():
                    minimum_nights = gr.Slider(0, 100, value=3, step=1, label="Minimum nights")
                    maximum_nights = gr.Slider(0, 100, value=30, step=1, label="Maximum nights")
                    instant_bookable = gr.Radio([1, 0], value=0, label="Instant bookable")
                with gr.Row():
                    availability_30 = gr.Slider(0, 30, value=2, step=1, label="Availability 30")
                    availability_60 = gr.Slider(0, 60, value=5, step=1, label="Availability 60")
                with gr.Row():
                    availability_90 = gr.Slider(0, 90, value=16, step=1, label="Availability 90")
                    availability_365 = gr.Slider(0, 365, value=17, step=1, label="Availability 365")

            with gr.Tab("Reviews"):
                with gr.Row():
                    number_of_reviews = gr.Number(value=311, minimum=0, label="Total reviews")
                    number_of_reviews_ltm = gr.Number(value=33, minimum=0, label="Reviews last 12 months")
                    number_of_reviews_l30d = gr.Number(value=3, minimum=0, label="Reviews last 30 days")
                with gr.Row():
                    first_review = gr.Slider(2009, 2030, value=2009, step=1, label="First review year")
                    last_review = gr.Slider(2010, 2030, value=2025, step=1, label="Last review year")
                    reviews_per_month = gr.Number(value=1.87, minimum=0, label="Reviews per month")
                with gr.Row():
                    review_scores_rating = gr.Slider(0, 5, value=4.92, step=0.01, label="Overall")
                    review_scores_accuracy = gr.Slider(0, 5, value=4.9, step=0.01, label="Accuracy")
                with gr.Row():
                    review_scores_cleanliness = gr.Slider(0, 5, value=4.94, step=0.01, label="Cleanliness")
                    review_scores_checkin = gr.Slider(0, 5, value=4.95, step=0.01, label="Check-in")
                with gr.Row():
                    review_scores_communication = gr.Slider(0, 5, value=4.93, step=0.01, label="Communication")
                    review_scores_location = gr.Slider(0, 5, value=4.9, step=0.01, label="Location")
                    review_scores_value = gr.Slider(0, 5, value=4.78, step=0.01, label="Value")

        with gr.Column(scale=5, min_width=420, elem_classes="result-panel"):
            price_output = gr.HTML(render_price(None))
            status_output = gr.HTML("Waiting for local model inference.")
            summary_output = gr.Textbox(label="Submitted summary", lines=7, value="", interactive=False)
            submit = gr.Button("Predict price", variant="primary", size="lg")

    preset.change(
        apply_preset,
        inputs=[preset],
        outputs=[
            name,
            property_type,
            room_type,
            accommodates,
            bedrooms,
            beds,
            bathrooms,
            amenities,
            neighbourhood_cleansed,
            host_is_superhost,
            minimum_nights,
            maximum_nights,
            availability_30,
            availability_60,
            availability_90,
            availability_365,
            review_scores_rating,
            reviews_per_month,
        ],
    )

    submit.click(
        predict_price,
        inputs=[
            name,
            property_type,
            room_type,
            accommodates,
            bedrooms,
            beds,
            bathrooms,
            amenities,
            neighbourhood_cleansed,
            latitude,
            longitude,
            host_since,
            host_location,
            host_response_time,
            host_response_rate,
            host_acceptance_rate,
            host_is_superhost,
            host_total_listings_count,
            host_verifications,
            host_has_profile_pic,
            host_identity_verified,
            minimum_nights,
            maximum_nights,
            availability_30,
            availability_60,
            availability_90,
            availability_365,
            number_of_reviews,
            number_of_reviews_ltm,
            number_of_reviews_l30d,
            first_review,
            last_review,
            review_scores_rating,
            review_scores_accuracy,
            review_scores_cleanliness,
            review_scores_checkin,
            review_scores_communication,
            review_scores_location,
            review_scores_value,
            instant_bookable,
            reviews_per_month,
        ],
        outputs=[price_output, status_output, summary_output],
    )


if __name__ == "__main__":
    demo.launch(css=CSS, theme=gr.themes.Soft(primary_hue="teal", neutral_hue="slate"))
