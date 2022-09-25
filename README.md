# foodpanda assignment submission

## Index
- [Guide to setting up for Questions 1 to 3](GUIDE_TO_Q1_TO_Q3.md)
    - [Question 1 Answer](1_nearest_ports.py)
    - [Question 2 Answer](2_largest_number_of_ports.py)
    - [Question 3 Answer](3_distress_call.py)
- [Question 4](4_testing_and_refactoring.md)
- [Question 5](5_fastapi_review.md)


## Questions

1. What are the 5 nearest ports closest to Singapore's *JURONG ISLAND* port?
Note: Answer should include the columns `port_name` and `distance_in_meters` 
only.
 
2. Which country has the largest number of ports with a `cargo_wharf`? 
Note: Answer should include the columns `country` and `port_count` only.

3. You receive a distress call from the middle of the North Atlantic Ocean. The 
   person on the line gave you a coordinates of `lat: 32.610982`, 
   `long: -38.706256` and asked for the nearest port with `provisions`, 
   `water`, `fuel_oil` and `diesel`. 
Note: Answer should include the columns `country`, `port_name`, `port_latitude` 
and `port_longitude` only.

4. In your own words (short paragraphs conveying your thoughts), answer the 
   following questions:
    a. What is refactoring? When and why should you refactor?
    b. What is testing? When and why should you write test cases?
 
5. Have a browse of https://github.com/tiangolo/fastapi and write down how this 
   repository is structured and why. What improvements do you think can be made?

Notes:
- Followed the instructions here to setup bigquery service account https://codelabs.developers.google.com/codelabs/cloud-bigquery-python#0
- Copied the `geo_international_ports.world_ports` table to personal project
