# Data Validation Report

- Generated at: 2026-06-09T22:16:33
- Great Expectations version: 1.17.2
- Suite: albany_airbnb_suite
- Success: True
- Evaluated expectations: 5
- Successful expectations: 5
- Unsuccessful expectations: 0
- Success percent: 100.0

## Expectation Results

| Expectation | Column | Success | Unexpected Count | Observed Value |
| --- | --- | --- | --- | --- |
| expect_column_to_exist | price | True |  |  |
| expect_column_values_to_not_be_null | price | True | 0 |  |
| expect_column_values_to_be_of_type | name | True | 0 |  |
| expect_table_columns_to_match_ordered_list | table | True |  | ['name', 'description', 'host_name', 'host_since', 'host_location', 'host_response_time', 'host_response_rate', 'host... |
| expect_column_values_to_be_between | latitude | True | 0 |  |