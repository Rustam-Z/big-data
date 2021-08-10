# All about data engineering 
*Learn, Practice, Apply*

<!-- 
What data engineer should know:
Need to have an experience on Python (data science related, OOP), ETL (Extract, Transform, Load) process, data warehousing (Snowflake), Databases (MSSQL/Postgre/MySQL), SQL+ORM, REST/SOAP/GraphQL APIs, Django/Flask/FastAPI, Azure, AWS, Airflow, Big Data 
-->

    Keywords: data pipeline, ETL process, data lake, date warehouse, data scheduling
    
    Tech: Python, SQL, Linux, Cloud, Airflow, PySpark

- [Introduction](#Introduction)
- [ETL (Extract, Load, Transform)](#ETL)
- [Streamlined data ingestion with Pandas](#Streamlined-Data-Ingestion-with-pandas)
- [Writing efficient code in Python](#Writing-efficient-code-in-python)
- [Writing functions in Python](#Writing-Functions-in-Python) 
- [Introduction to shell](#Introduction-to-shell)

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

# Finish the connection URI
connection_uri = "postgresql://repl:password@localhost:5432/dwh"
db_engine_dwh = sqlalchemy.create_engine(connection_uri)

# Transformation step, join with recommendations data
film_pdf_joined = film_pdf.join(recommendations)

# Finish the .to_sql() call to write to store.film
film_pdf_joined.to_sql("film", db_engine_dwh, schema="store", if_exists="replace")

# Run the query to fetch the data
pd.read_sql("SELECT film_id, recommended_film_ids FROM store.film", db_engine_dwh)
```

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

## Writing efficient code in Python
```py
""" 
- Use [map, filter, enumerate, zip, list comperehesion] instead of loops'
- itertools, collection library, 'set' build-ins;
- iterator, generator;
""" 

[(i,name) for i,name in enumerate(names)] == [*enumerate(names, start=0)] # true

[sum(row) for row in my_iterable] == [*map(sum, my_iterable)] # true

# https://www.geeksforgeeks.org/difference-between-iterator-vs-generator/
```
```py
"""Timing and profiling code"""
%lsmagic

# runs to 2 (-r2), number of loops to 10 (-n10)
%timeit -r2 -n10 rand_nums = np.random.rand(1000)
%%timeit # for multiple line
times = %timeit -o rand_nums = np.random.rand(1000) # save output into variable

"""pip install line_profiler"""
%load_ext line_profiler
%timeit convert_units(heroes, hts, wts)
# -f means function, then function name, then fuction parameters
%lprun -f convert_units convert_units(heroes, hts, wts)

"""Memory usage"""
%load_ext memory_profiler
%mprun -f convert_units convert_units(heroes, hts, wts)
```
```py
"""Pandas optimizations"""
# 1. iterrows()
df = pd.DataFrame({'c1': [10, 11, 12], 'c2': [100, 110, 120]})

for index, row in df.iterrows(): 
    print(row['c1'], row['c2'])
    # 10 100
    # 11 110
    # 12 120

'''
# no need to specify the index, iterrows takes care about it:
for i, row in df1.iterrows():
    wins = row['W']
    games_played = row['G']
'''
# 2. itertuples() --> efficient
for row in df1.iterrows():
    wins = row.SomeColumn

# 3. .apply() function, column=0, row=1 --> even better
def norm_by_data2(x):
    # x is a DataFrame of group values
    x['data1'] /= x['data2'].sum() 
    return x
print(df.groupby('key').apply(norm_by_data2)) # will send all dataset

'''
# send row by row
df.apply(lambda row: my_function(row[0], row[2])), axis=1)
'''

# 4. Vectorization 
my_df = df1['A'].values - df2['B'].values
```

## Writing functions in Python
**Best practices**
```py
# Docstring - Google style
def function(arg_1, arg_2=42, some_function):
    """Descriptioin of what this function does.

    Args:
        arg_1 (str): Description of arg_1.
            (The string to search).
        arg_2 (int, optional): Write optional when
            argument has default value.
        some_function (callable): The function we want a tooltip for.

    Returns:
        bool: Optional description of the return value.
        Extra lines not indedted.
    
    Raises: 
        ValueError: Include any type of error that the function raises.

    Notes:
        See https://......com for more usage.
        import inspect
        doc = inspect.getdoc(function)
    """
```
```py
# DRY - Do one thing!
# Use functions to avoid repetition.
# Problem: it does multiple things. First, it loads the data. Then it plots the data. You must write seperate functions for them.

# Pass by argument
def foo(var=None): # do not write: var=[]
    if var is None:    
        var = []  
    var.append(1)
    return var
foo()
```

**Context managers** --> initialize, enter, exit --> CONNECT/DISCONNECT, OPEN/CLOSE
```py
"""with"""
# how to write? class-based or function-based.
# Python generator --> yield
@contextlib.contextmanager
def my_context():
    print('hello')
    yield 42 
    print('finished')

with my_context() as foo: # we use 'as' cuz my_context kind of returns yield 42
    print(f'foo is {foo}') # foo is 42

"""nested context manager"""
with stock('NVDA') as nvda:
  # Open "NVDA.txt" for writing as f_out
  with open('NVDA.txt', 'w') as f_out:
    for _ in range(10):
      value = nvda.price()
      print('Logging ${:.2f} for NVDA'.format(value))
      f_out.write('{:.2f}\n'.format(value))
    # Opening stock ticker for NVDA
    # Logging $139.50 for NVDA
    # Logging $139.54 for NVDA
    # Logging $139.61 for NVDA
    # Closing stock ticker

"""try/except/finally to be ensure to finish (close file or disconnect printer) even error"""
def get_printer(ip):
    p = connect_to_printer(ip)

    try:
        yield
    finally:
        p.disconnect()
        print('disconnected from printer')
```

**Functions & Closure**
```py
"""Function = object"""
# 1. Function is object, just reference them to variable
def my_functon():
    print('Hello')
x = my_functon # DO NOT INCLUDE ()
x() # Hello

# 2. List of functions
list_of_funcs = [my_function, open, print] # can also transform to dict
list_of_funcs[2]("Wow working")

# 3. Function as argument
def has_docstring(func):
    """Check to see if function has doc.
    """
    return func.__doc__ is not None
def yes():
    """Returns value 42.
    """
    return 42
has_docstring(yes)

# 4. Function as return values
def get_function():
    def print_me(s):
        print(s)
    return print_me

new_func = get_function()
new_func('This is a sentence')
```
```py
"""Closure"""
def return_a_func(arg1, arg2):
  def new_func():
    print('arg1 was {}'.format(arg1))
    print('arg2 was {}'.format(arg2))
  return new_func
    
my_func = return_a_func(2, 17)

print(my_func.__closure__ is not None)
print(len(my_func.__closure__) == 2)

# Get the values of the variables in the closure
closure_values = [
  my_func.__closure__[i].cell_contents for i in range(2)
]
print(closure_values == [2, 17])
```
**Decorators**
- <img src="img/python_decorator.png" width=300>
- Decorator = wrapper -> modify input, modify output, modify function
- **We should have the same parameters inside wrapper like our function!**
- https://realpython.com/primer-on-python-decorators/
```py
# Template to reuse
import functools

def decorator(func):
    @functools.wraps(func)
    def wrapper_decorator(*args, **kwargs):
        # Do something before
        value = func(*args, **kwargs)
        # Do something after
        return value
    return wrapper_decorator
```
```py
"""Decorator"""
def double_args(func):
    def wrapper(a, b):
        return func(a * 2, b * 2)
    return wrapper

@double_args # same as new_multiply = double_args(multiply)
def multiply(a, b):
    return a * b

multiply(2, 3)
```
```py
"""Anvanced decorator"""
from functools import wraps

def timer(func):
  """A decorator that prints how long a function took to run."""
  @wraps(func)
  def wrapper(*args, **kwargs):
    # When wrapper() is called, get the current time.    
    t_start = time.time()
    # Call the decorated function and store the result.    
    result = func(*args, **kwargs)
    # Get the total time it took to run, and print it.    
    t_total = time.time() - t_start    
    print('{} took {}s'.format(func.__name__, t_total))
    return result
 return wrapper
```
- `duplicate.__wrapped__(3, 5)` - call the original function instead of the decorated one
```py
"""Decorators with arguments"""
# we have to turn it into a function that returns a decorator, rather than a function that is a decorator

# instead of writing decorator function for only 4, we can do for values n
def repeat(num_times):
    def decorator_repeat(func):
        @functools.wraps(func)
        def wrapper_repeat(*args, **kwargs):
            for _ in range(num_times):
                value = func(*args, **kwargs)
            return value
        return wrapper_repeat
    return decorator_repeat

@repeat(num_times=4)
def greet(name):
    print(f"Hello {name}")

greet("World")

"""Project: HTML Generator"""
# instead of doing seperately for bold, italic, we can do like below
def html(open_tag, close_tag):
  def decorator(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
      msg = func(*args, **kwargs)
      return '{}{}{}'.format(open_tag, msg, close_tag)
    # Return the decorated function
    return wrapper
  # Return the decorator
  return decorator

@html("<b>", "</b>")
def hello(name):
  return 'Hello {}!'.format(name)
  
print(hello('Alice'))
```

## Introduction to shell
```shell
$ # when starting with / then it is an absolute path
$ man head # see manual
$ ls -R -F 
$ history # !head, !2
$ cp original.txt duplicate.txt # copy
$ cp seasonal/autumn.csv seasonal/winter.csv backup
$ mv autumn.csv winter.csv # move
$ rm thesis.txt backup/thesis-2017-08.txt # remove
$ mkdir test_dir # make directory
$ rmdir test_dir # remove directory
$ 
$ # HOW TO VIEW FILES CONTENTS
$ cat agarwal.txt
$ less seasonal/spring.csv
$ head -n 10 seasonal/summer.csv # view 10 lines | "tail"
$ grep -c -i -n value seasonal/winter.csv # select lines containing specific values, -v inverting
$ head -n 5 seasonal/winter.csv > bottom.csv # storing output
$ tail -n 3 bottom.csv
$ head -n 5 seasonal/summer.csv | tail -n 3 # combining commands
$ cut -f 2  -d , seasonal/summer.csv | grep -v Tooth | sort -r | uniq -c 
$ cut -d , -f 1 seasonal/* # cut -d , -f 1 seasonal/*.csv
$ # ? one char, [97] chars inside, {s*.txt, *.csv} for comma seperated
$ history | tail -n 3 > steps.txt
$
$ set | grep HOME
$ echo $USER # get the variable
$ for filename in seasonal/*.csv; do echo $filename; done
$ for file in seasonal/*.csv; do head -n 2 $file | tail -n 1; done # many commands inside loop
$
$ nano dates.sh # write some shell commands
$ bash dates.sh
$ # 1. if dates.sh has "sort $@ | uniq", with $@ we can send specific files like "bash dates.sh summer.csv"
$ # 2. or even bash script may have "cut -d , -f $2 $1", then while running it use "bash column.sh seasonal/autumn.csv 1"
$ 
```