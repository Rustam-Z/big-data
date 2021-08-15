# All about data engineering 
*Learn, Practice, Apply*

<!-- 
What data engineer should know:
Need to have an experience on Python (data science related, OOP), ETL (Extract, Transform, Load) process, data warehousing (Snowflake), Databases (MSSQL/Postgre/MySQL), SQL+ORM, REST/SOAP/GraphQL APIs, Django/Flask/FastAPI, Azure, AWS, Airflow, Big Data 
-->

    Keywords: data pipeline, ETL process, data lake, date warehouse, data scheduling
    
    Tech: Python, SQL, Linux Bash, Cloud, Airflow, PySpark

- [Introduction](#Introduction)
- [ETL (Extract, Load, Transform)](#ETL)
- [Streamlined data ingestion with Pandas](01_streamlined_data_ingestion.md)
- [Writing efficient code in Python](02_writing_efficient_code.md)
- [Writing functions in Python](03_writing_functions.md) 
- [Introduction to shell](04_bash_scripting.md/#Introduction-to-shell)
- [Data processing in shell](04_bash_scripting.md/#Data-Processing-in-Shell)
- [Introduction to bash scripting](04_bash_scripting.md/#Introduction-to-bash-scripting)
- [Unit testing for data science](05_unit_testing.md)

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
    - <img src="img/data_pipeline.pnEg" width=500>
    
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
```
```py
result = json.loads('{"key_1":"value_1","key_2":"value_2"}')
print(result["key_1"])
```
```py
import sqlalchemy
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

```py
"""LOAD"""
connection_uri = "postgresql://repl:password@localhost:5432/dwh"
db_engine_dwh = sqlalchemy.create_engine(connection_uri)

film_pdf_joined = film_pdf.join(recommendations)

film_pdf_joined.to_sql("film", db_engine_dwh, schema="store", if_exists="replace")

pd.read_sql("SELECT film_id, recommended_film_ids FROM store.film", db_engine_dwh)
```