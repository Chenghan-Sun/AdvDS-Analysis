import pandas as pd
import re
import numpy as np

def find_null(item):
    """ fill all missing values or values filled with str "null"
    Param:
        item: one item in dataframe
    Return:
        item: filled item
    """
    if not item or (type(item)!=str and np.isnan(item)) or (type(item)==str 
                                                            and item.strip().lower()in ['null', 'none']):
        return "Unknown"
    return item

def exceptions(data, verbose=False):
    """ raise exceptions if any record doesn't match the pattern in function `find_null`
    Param:
        data: dataframe 
    """
    for column in data.columns:
        for i in range(data.shape[0]):
            try:
                find_null(data[column][i])
            except:
                raise Exception(f"the index {i} in {column}")
    if verbose:
        print('No exceptions detected')
        
def get_open_time(item):
    """ Extract the time intervals when the restaurants open and close
    Param:
        item: one item in dataframe
    Return:
        result: list of time intervals or 'closed'
    """
    if re.search(r'open 24', item.lower()):
        return [[0,24]]
    pattern = r'(\d{1,2}):(\d{2}) ([ap]m)' 
    result = []
    for interval in item.split(','):
        tmp = interval.split('-')
        if len(tmp)!=2:
            return item.strip()
        begin, end = tmp
        open_time = [0,0]
        for i,point in enumerate([begin, end]):
            if re.search(pattern, point.strip()):
                time, half = point.strip().split()
                time_digit = time.split(':')
                numeric_hour = int(time_digit[0]) + int(time_digit[1])/60 + 12 * int(half == 'pm')
                open_time[i] = numeric_hour
            else:
                open_time[i] = point
        result.append(open_time)
    return result

def get_parking(item, parking_type=['street', 'lot', 'garage', 'valet']):
    """ change Parking to four binary vars based on our self defined key words
    Param:
        item: one item in dataframe
    Return:
        Pd.Series of binary response (0 refers 'no such parking type, 1 refers 'such parking type exists'
    """
    result = []
    for park in parking_type:
        if re.search(fr'({park})', item.lower()):
            result.append(1)
        else:
            result.append(0)
    return pd.Series(result)

def grab_start_open(item):
    """ create features based on open time periods function `get_open_time`
    Param:
        item: one item in dataframe
    Return:
        the hour that the restaurants open 
    """
    if type(item) == str:
        return None
    if type(item[0][0]) == str:
        return 0
    return item[0][0]

def grab_end_open(item):
    """ create features based on close time periods function `get_open_time`
    Param:
        item: one item in dataframe
    Return:
        the hour that the restaurants close
    """
    if type(item) == str:
        return None
    if type(item[-1][-1]) == str:
        return 24
    return item[-1][-1]

def get_ZIP(item):
    """ for geo-spatial analysis, extract ZIP code from Address
    Param:
        item: 
    Return:
        ZIP code, Unknown if not exist
    """
    zip_code = item.split(',')[-1]
    if re.search(r'\d{5}', zip_code):
        return zip_code
    else:
        return "Unknown"
