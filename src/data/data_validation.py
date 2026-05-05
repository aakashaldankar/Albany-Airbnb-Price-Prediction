import great_expectations as gx
from great_expectations import expectations as gxe
import pandas as pd
import os
from datetime import datetime
from src.logger import get_logger

root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
train_data_path = os.path.join(root_dir,'central_data','raw_data', 'train_data.csv')
reports_dir = os.path.join(root_dir, 'reports')

script=os.path.basename(__file__)
logger=get_logger(script)

def _markdown_value(value):
    if value is None:
        return ""

    value = str(value)
    value = value.replace("|", "\\|").replace("\n", " ")

    if len(value) > 120:
        return f"{value[:117]}..."

    return value


def _write_validation_report(validation_result):
    os.makedirs(reports_dir, exist_ok=True)

    result = validation_result.to_json_dict()
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    report_path = os.path.join(reports_dir, f"data_validation_report_{timestamp}.md")

    statistics = result.get("statistics", {})
    meta = result.get("meta", {})

    lines = [
        "# Data Validation Report",
        "",
        f"- Generated at: {datetime.now().isoformat(timespec='seconds')}",
        f"- Great Expectations version: {meta.get('great_expectations_version', '')}",
        f"- Suite: {result.get('suite_name', '')}",
        f"- Success: {result.get('success')}",
        f"- Evaluated expectations: {statistics.get('evaluated_expectations', 0)}",
        f"- Successful expectations: {statistics.get('successful_expectations', 0)}",
        f"- Unsuccessful expectations: {statistics.get('unsuccessful_expectations', 0)}",
        f"- Success percent: {statistics.get('success_percent', 0)}",
        "",
        "## Expectation Results",
        "",
        "| Expectation | Column | Success | Unexpected Count | Observed Value |",
        "| --- | --- | --- | --- | --- |",
    ]

    for expectation_result in result.get("results", []):
        expectation_config = expectation_result.get("expectation_config", {})
        kwargs = expectation_config.get("kwargs", {})
        expectation_type = expectation_config.get("type", "")
        expectation_result_details = expectation_result.get("result", {})

        lines.append(
            "| {expectation_type} | {column} | {success} | {unexpected_count} | {observed_value} |".format(
                expectation_type=_markdown_value(expectation_type),
                column=_markdown_value(kwargs.get("column", "table")),
                success=_markdown_value(expectation_result.get("success")),
                unexpected_count=_markdown_value(expectation_result_details.get("unexpected_count", "")),
                observed_value=_markdown_value(expectation_result_details.get("observed_value", "")),
            )
        )

    with open(report_path, "w", encoding="utf-8") as report:
        report.write("\n".join(lines))

    return report_path


def validate(df: pd.DataFrame):

    try:
        context = gx.get_context()

        pandas_ds = context.data_sources.add_or_update_pandas(name="pandas_default")

        try:
            dataframe_asset = pandas_ds.get_asset("albany_airbnb_df")
        except LookupError:
            dataframe_asset = pandas_ds.add_dataframe_asset(name="albany_airbnb_df")

        try:
            batch_definition = dataframe_asset.get_batch_definition("whole_dataframe_batch")
        except LookupError:
            batch_definition = dataframe_asset.add_batch_definition_whole_dataframe(name="whole_dataframe_batch")
        
        batch = batch_definition.get_batch(batch_parameters={"dataframe": df})

        suite_name = "albany_airbnb_suite"

        try:
            suite = context.suites.get(name=suite_name)
        except gx.exceptions.DataContextError:
            suite = gx.ExpectationSuite(name=suite_name)

        suite.expectations = []

        ordered_columns = [
            "name","description","host_name","host_since","host_location","host_response_time",
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
            "calculated_host_listings_count_shared_rooms","reviews_per_month"
        ]

        expectations = [
            gxe.ExpectColumnToExist(column="price"),
            gxe.ExpectColumnValuesToBeOfType(column="name", type_="str"),
            gxe.ExpectTableColumnsToMatchOrderedList(column_list=ordered_columns),
            gxe.ExpectColumnValuesToNotBeNull(column="price"),
            gxe.ExpectColumnValuesToBeBetween(column="latitude", min_value=0.0, max_value=1000.0),
        ]

        for expectation in expectations:
            suite.add_expectation(expectation)

        context.suites.add_or_update(suite)

        validation_result = batch.validate(suite)

        report_path = _write_validation_report(validation_result)
        logger.info("data validation report stored at %s", report_path)

        if not validation_result.success:
            raise ValueError("Data Validation Failed")

        logger.info("data validation performed successfully")

    except Exception as e:
        logger.error("unexpected error occurred, %s", e)
        raise


def main():

    df=pd.read_csv(train_data_path)

    validate(df)


if __name__=='__main__':
    main()




    
    

    
