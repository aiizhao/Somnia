# (PRO)SOMNIA
basic_server.py handles saving incoming data in a csv format and visualizing saved data as a graph.

## Setup
The requirements are installation of the Flask framework and Python 3.7 or newer. The necessary
external libraries are pandas and plotly.

## Functionalities
### /test_api
The route accepts POST requests with a JSON body. In the body of the request, the 'data' parameter 
should correspond to a single string (seperated with commas and newline characters) that represents 
a chunk of data. The string is directly appended to one .csv file.

### extract_data(file_name)
The function takes in a .csv filename and reads in the data from the appropriate file.
The format of each line of the data is "Somnia, (datetime), (category), (left value), (right value)".
For each IND line, the values represent an index and the following 8 lines contain the data for that 
index. The function reformats the data and returns two dictionaries (for left/right values), each 
containing 9 lists of values in time order (indices and the 8 categories).

## /test_visualize
The route uses a filename from a GET request with a 'file' parameter and calls extract_data(filename) 
to parse the data to create a plotly figure that graphs 16 lines (the lists of values for each different 
category over the list of indices). The plot is rendered through a html page.
