# PyDataGenerator

PyDataGenerator is a simple script that will generate desired number of random data for the specified attributes.
<br><br>

## How to start:

Clone and import pyDataGenerator to your project. You may directly modify the script and generate data as well.<br>
Modify the following variables: _ATTR_NAME_, _ATTR_RANGE_, _FILE_, and _DECIMAL_

### _ATTR_NAME_: List of attributes <br>

`ATTR_NAME = [name1, name2, ...]`

### _ATTR_RANGE_: List of ranges for each attributes

- The number of elements in the list must match the number of attributes. Order must match as well. <br>
- _Integer_ and _Float_ ranges are stored as a tuple, with min value, max value. Format: (_min1_, _max1_)<br>
- _String_ and _Boolean_ ranges are stored as a list. Format: [_option1_, _options2_, ...]

`ATTR_RANGE = [ [option1, options2, ...], (min1, max1), ... ]`

### (OPTIONAL) _FILE_: Export file path

`FILE = <file_path>.csv`

### (OPTIONAL) _DECIMAL_: Desired number of decimal points for float values. Default is set to 1

`DECIMAL = 1`
<br><br>

## Data Generation

Method `generate()` will accept an integer value for the number of data that needs to be generated and export option. <br>
Export option is set to `True` by default. <br>
Pass in `False` to generate data only, without export.

Following code will generate 100 sample data, no export.

```
pyDataGenerator.generate(100, exporting=False)
```

Following code will manually export the data to file. <br>
No neeed to run this command unless you have passed in False for _export_ in `generate()`

```
pyDataGenerator.export()
```

Following code will print the generated data. <br>
You can pass in start index and end index to print only a portion of the data.<br>
Start index and end index is set to 0 and n-1, respectively, where n = total number of data.

```
pyDataGenerator.print() // print all data
pyDataGenerator.print(start_index=2,end_index=4) // print data between index 2 and 4
```
