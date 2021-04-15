import pandas as pd
from numpy import arange

def true_read_csv(func: 'pd.read_csv'=pd.read_csv) ->pd.DataFrame:
    """Wrapper for pd.read_csv."""
    def wrapper(*args, **kwargs: 'pd.read_csv parameters') -> pd.DataFrame:
        """
        Return a DataFrame from csv with true and ordered columns and sort by
        datetime, and display 5 randow rows and df.info().
        """
        df = func(*args, **kwargs)
        
        columns_indeces = kwargs.get(
            'usecols', 
            arange(df.shape[1])
        )
        df = df.iloc[:, columns_indeces]

        df.columns = (df.columns
            .str.strip()
            .str.replace(' ', '_')
            .str.lower()
        )

        if not df.select_dtypes('datetime').isnull:
            date_column = df.select_dtypes('datetime').columns[0]
            df = df.sort_values(date_column).reset_index(drop=True)

        display(
            df.sample(5, random_state=42).sort_index()
        )
        print('---------------------------------')
        df.info(memory_usage='deep')

        return df
    return wrapper