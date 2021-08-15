
## Streamlined data ingestion with pandas
**Importing data from flat files (CSV)**
```py
'''CSV'''

col_names = ['STATEFIPS', 'STATE', 'zipcode', 'agi_stub', 'N1'] # or [0, 1, 2, 3, 4]
tax_data_v1 = pd.read_csv('us_tax_data_2016.csv', sep=",", 
                            usecols=col_names, # parse only this columns
                            nrows=1000, 
                            skiprows=1000, 
                            header=None, 
                            col_names = list(tax_data_first1000), 
                            dtype={"zipcode": str}, 
                            na_values={"zipcode" : 0}, # if 0 then change to None
                            error_bad_lines=False,
                            warn_bad_lines=True
                            )

# header=None means no column names
# col_names new column names
```
**Importing data from Excel files**
```py
# Read the Excel file
survey_data = pd.read_excel("fcc_survey.xlsx",
                            skiprows=2,
                            nrows=1000,
                            usecols="W:AB, AR",
                            sheet_name=['2017', '2012'], # or with index 1, 0, or None
                            )


'''if you use sheet_name=None, it will load all sheets'''
# thats how to combine them
all_responses = pd.DataFrame()

for df in survey_data.values():
  print("Adding {} rows".format(df.shape[0]))
  all_responses = all_responses.append(df)

counts = all_responses.groupby("EmploymentStatus").EmploymentStatus.count()
counts.plot.barh()
plt.show()
```
```py
# Load file with Yes as a True value and No as a False value
survey_subset = pd.read_excel("fcc_survey_yn_data.xlsx",
                              dtype={"HasDebt": bool,
                              "AttendedBootCampYesNo": bool},
                              true_values=['Yes'],
                              false_values=['No'])

# View financial burdens by Boolean group
print(survey_data.groupby('HasDebt').sum())
'''
<script.py> output:
             HasFinancialDependents  HasHomeMortgage  HasStudentDebt
    HasDebt                                                         
    False                     112.0              0.0             0.0
    True                      205.0            151.0           281.0
'''
```
```py
"""PARSING DATES"""
# First method: Just if we have standart columns like 2020-06-25 20:08:53
survey_data = pd.read_excel("fcc_survey.xlsx",
                            parse_dates=['Part1StartTime'])

# Second method: If we want to combine from other columns
date_cols = {"Part1Start": "Part1StartTime", 
             "Part1End": "Part1EndTime",
             "Part2Start": ["Part2StartDate", "Part2StartTime"]}

survey_df = pd.read_excel("fcc_survey.xlsx", parse_dates=date_cols)


# Third method: If the column date data is not standart like 03302016 09:05:06. year = Y
format_string = "%m%d%Y %H:%M:%S"
survey_df["Part2EndTime"] = pd.to_datetime(survey_df["Part2EndTime"], format=format_string)
```
**Importing data from databases**
```py
import pandas as pd
from sqlalchemy import create_engine

engine = create_engine("sqlite:///data.db")
weather = pd.read_sql("weather", engine)
weather = pd.read_sql("SELECT * FROM weather", engine)

query = """SELECT borough, COUNT(*) 
           FROM hpd311calls 
           WHERE complaint_type = 'PLUMBING' 
           GROUP BY borough;"""           
plumbing_call_counts = pd.read_sql(query, engine)

'''
borough         COUNT(*)      
BRONX           20161       
BROOKLYN        27022      
MANHATTAN       14133         
QUEENS          8084  
STATEN ISLAND   178
'''
# select -> from -> join -> where -> order by
```

**Importing JSON Data and Working with APIs**
```py
"""Making Requests"""
import requests
import pandas as pd

api_url = "https://api.yelp.com/v3/businesses/search"

# Set up some neccessary parameters
params = {'term': 'bookstore',
      'location': 'San Francisco'}

# Set up header dictionary API key for authorization
headers = {"Authorization": "Bearer {}".format(API_KEY)}

# call the API
response = requests.get(api_url, params=params, headers=headers)
data = response.json()

cafes = pd.DataFrame(data['businesses'])

print(cafes.dtypes)
```
```py
# json_normalize()
from pandas.io.json import json_normalize

# Isolate the JSON data from the API response
data = response.json()

cafes = json_normalize(data["businesses"],
             sep='_')

print(cafes.head()) # that's pandas df
```
```py
# Appending -> on rows
# Put bookstore datasets together, renumber rows
bookstores = first_20_bookstores.append(next_20_bookstores, ignore_index=True)
print(bookstores.name) # columns

# Merging -> on columns
# Merge crosswalk into cafes on their zip code fields
cafes_with_pumas = cafes.merge(crosswalk, left_on='location_zip_code', right_on='zipcode')
```