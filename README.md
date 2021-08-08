# All about data engineering 
*Learn, Practice, Apply*

<!-- 
What data engineer should know:
Need to have an experience on Python (data science related, OOP), ETL (Extract, Transform, Load) process, data warehousing (Snowflake), Databases (MSSQL/Postgre/MySQL), SQL+ORM, REST/SOAP/GraphQL APIs, Django/Flask/FastAPI, Azure, AWS, Airflow, Big Data 
-->

Keywords: data pipeline, ETL process, data lake & warehouse, data scheduling

Tech: Python, SQL, Linux, Cloud, Airflow, PySpark

- [Introduction](#Introduction)
- [ETL (Extract, Load, Transform)](#ETL)
- [Streamlined Data Ingestion with pandas](#Streamlined-Data-Ingestion-with-pandas)

## Introduction
<a href="https://www.youtube.com/watch?v=xC-c7E5PK0Y"> <img src="img/data_jobs.jpg" width=600 alt="Who is the Data Engineer actually?"></a>

> **Data engineer** develops, constructs, tests, and maintance architecture such as databases and large-scale processing systems. The data engineer moves data from several sources, processes or cleans it and finally loads it into an analytical databases. ETL process.

**Data Engineer** | **Data Scientist**
------------------|------------------
Develop sclalable data architecture | Mining data for patterns
Streamline data acquisition | Statistical modeling
Set up processes to bring together data | Predictive models using machine learning
Clean corrupt data | Monitor business processes
Well versed in cloud technology | Clean outliers in data

**Data workflow**
- Data Collection & Storage `Data Engineer`
- Data Preperation `Data Scientist`
- Exploration & Visualization `Data Scientist`
- Experimentation & Prediction `Data Scientist`

**Data engineer deliver:**
- the correct data
- in the right form
- to the right people
- as efficiently as possible

**The data pipeline**
- Ingest -> Process -> Store
- Need pilelines to automate data flow:
    - Extraction
    - Transforming
    - Combining
    - Validating
    - Loading
- The main objective, when setting up **data pipelines**, is to improve the efficiency with which data flows, from its ingestion to the final users.
- <img src="img/pipeline.png" width=600>

Data engineers use parallel and cloud computing to keep pipelines flowing smoothly.

ETL           | Data pipelines
------------- | -------------
Framework for designing data pipelines  | Move data from one system to another
**Extract** data to make it ready for processing | May follow ETL
**Transform** extracted data | Data may not be transformed
**Load** transformed data to another databse | Data may be directly loaded in applications

**A data lake** - all data from all data sources,
**a data warehouse** - part of data from data lake used for analysis. Type of database.

**Processing data** == data transorming, converting raw data into meaningful information. Most of the data processing steps are *transformation* steps including selecting, encoding, calculating new values, sorting and ordering, joining data from multiple sources, aggregating, pivoting tables, splitting one table into several ones, removing duplicate values.

**Schedules**

**Manual** | **Time** | **Condition (Sensor)**
-----------|----------|-----------
Manually update the employee table. | Update at 6 AM everyday. | Update departments table when the new employee was added.

Batches (records are grouped and processed at intervals) or streams (records are sent individually right away).


**Batch** | **Stream** 
-----------|----------
Adding new employee to a table. | Updating the count of followers when user subscribes to it.
Reducing access to premium features when someone unsubscribe. | When user listening to music Apple Watch and downwards the song.

**Cloud computing**

<img src="img/cloud_computing.png" width=600>

So we use S3 to store cover albums, EC2 to process songs, and RDS to store employees information.

- **Databases** MySQL, PostgreSQL
- **Processing** Apache Spark
    - Clean data
    - Aggregate data - any process in which data is brought together and conveyed in a summary form.
    - Join data
- **Schedules** Apache Airflow
- **Data pipeline**
    - <img src="img/data_pipeline.png" width=500>
    
## ETL
<img src="img/etl.png" width=800>

First of all, it's nice to have your ETL behavior encapsulated into a clean `etl()` function. Let's say we have a `extract_table_to_df()` function, which extracts a PostgreSQL table into a pandas DataFrame. Then we could have one or many transformation functions that takes a pandas DataFrame and transform it by putting the data in a more suitable format for analysis. This function could be called `split_columns_transform()`, for example. Last but not least, a `load_df_into_dwh()` function loads the transformed data into a PostgreSQL database. We can define the resulting `etl()` function as follows. The result of `extract_table_to_df()` is used as an input for the transform function. We then use the output of the transform as input for `load_df_into_dwh`.

Now that we have a python function that describes the full ETL, we need to make sure that this function runs at a specific time. Apache Airflow is **a workflow scheduler** written in Python.

<img src="img/dag_airflow.png" width=800><br>
<img src="img/dag_airflow2.png" width=800>

### Extract
- Extract from text files, like `.txt` or `.csv`
- Extract from APIs of web services in `.json` semi-structured data
- Extract from a database, like a SQL application database for customer data
```py
import requests

resp = requests.get("https://hacker-news.firebaseio.com/v0/item/16222426.json")
print(resp.json())

post_score = resp.json()["score"]
print(post_score)
```
```py
import json
result = json.loads('{"key_1":"value_1","key_2":"value_2"}')
print(result["key_1"])
```
```py
import sqlalchemy
import pandas as pd
# postgresql://[user[:password]@][host][:port][/database]
connection_uri = "postgresql://repl:password@localhost:5432/pagila"
db_engine = sqlalchemy.create_engine(connection_uri)
pd.read_sql("SELECT * FROM customer", db_engine)
```

### Transform
- Data transformation = data processing
- Data transformation mostly done with parallel computing. 

customer_id | email | state | created_at
:------------:|-------|-------|-----------
1 | aurora@gmail.com | California | 2019-01-08 07:23:00

- Selection of attribute (e.g. 'email')
- Transition of code value (e.g. 'New York' -> 'NY')
- Data validation (e.g. data input in 'created_at')
- Splitting columns into multiple columns
- Joining from multiple sources
- Cleaning
- Aggregating

### Load
Analytics database | Application database
----------|------------
Efficient to aggregate queries on subset of columns | Efficient for lots of transaction, saving one record
Online analytical processing (OLAP) | Online transaction processing (OLTP)
Column-oriented | Row-oriented
<img src="img/column_oriented.png" width=200> | <img src="img/row_oriented.png" width=200>


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
