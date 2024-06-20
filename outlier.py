import pandas as pd
import numpy as np

def treat_outliers_z_score(data, column):
    """
    Treat outliers in a specific column using Z-score treatment.
    
    Parameters:
    - data: pandas DataFrame
    - column: the name of the column to treat outliers
    
    Returns:
    - pandas DataFrame with outliers treated
    """
    mean = data[column].mean()
    std_dev = data[column].std()
    lower_bound = mean - 3 * std_dev
    upper_bound = mean + 3 * std_dev
    
    data[column] = np.where((data[column] < lower_bound) | (data[column] > upper_bound), np.nan, data[column])
    
    return data

def treat_outliers_iqr(data, column):
    """
    Treat outliers in a specific column using IQR treatment.
    
    Parameters:
    - data: pandas DataFrame
    - column: the name of the column to treat outliers
    
    Returns:
    - pandas DataFrame with outliers treated
    """
    Q1 = data[column].quantile(0.25)
    Q3 = data[column].quantile(0.75)
    IQR = Q3 - Q1
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR
    
    data[column] = np.where((data[column] < lower_bound) | (data[column] > upper_bound), np.nan, data[column])
    
    return data

# Example usage:
# Assuming 'df' is your DataFrame and 'column_name' is the column you want to treat

# For Z-score treatment
# df = treat_outliers_z_score(df, 'column_name')

# For IQR treatment
# df = treat_outliers_iqr(df, 'column_name')