
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
