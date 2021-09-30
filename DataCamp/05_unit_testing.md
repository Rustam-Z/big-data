
## Unit testing for data science with pytest
- Naming convension file & function names must be with `test_`
- `pytest test_this_file.py` to run the test
- use `pytest.approx(expected)` when working with float 
```py
# pytest test_convert_to_int.py

import pytest
from preprocessing_helpers import convert_to_int

def test_on_string_with_one_comma():
  assert convert_to_int("2,081")==2081
```
```py
import pytest
def test_for_missing_area_with_message():    
    actual = row_to_list("\t293,410\n")    
    expected = None    
    message = ("row_to_list('\t293,410\n') "
            "returned {0} instead "
            "of {1}".format(actual,expected))
    assert actual is expected, message
```
```py
import numpy as np
import pytest
from as_numpy import get_data_as_numpy_array

def test_on_clean_file():
  expected = np.array([[2081.0, 314942.0],
                       [1059.0, 186606.0],
  					           [1148.0, 206186.0]])
  actual = get_data_as_numpy_array("example_clean_data.txt", num_columns=2)
  message = "Expected return value: {0}, Actual return value: {1}".format(expected, actual)
  # Complete the assert statement
  assert actual == pytest.approx(expected), message
```


