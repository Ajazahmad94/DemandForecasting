#myModule/fileIO.py

#loadCsvExcelFile function 
#This function loads a CSV or Excel file and returns a DataFrame with columns named 'date' and 'value'
#The file must have a header row with column names
#The file must have columns named 'date' and 'value'
#The file must have at least one row of data



def loadCsvExcelFile(file_path):
    import pandas as pd
    '''This function loads a CSV or Excel file and returns a DataFrame with columns named 'date' and 'value'''
    try:
        # Try to import the file as a DataFrames
        if file_path.lower().endswith('.csv'):
            df = pd.read_csv(file_path)
        elif file_path.lower().endswith(('.xls', '.xlsx')):
            df = pd.read_excel(file_path)
        else:
            raise ValueError("Unsupported file format. Please provide a CSV or Excel file.")
        
        # Check if DataFrame has required columns
        if 'date' not in df.columns or 'value' not in df.columns:
            raise ValueError("Data Frame Columns names issue: The DataFrame must have columns named 'date' and 'value.  Please make sure these column names are present in your DataFrame.")
        
        # Return the resulting DataFrame
        return df[['date', 'value']]

    except FileNotFoundError:
        raise FileNotFoundError(f"Error: File not found. Please provide a valid file path: {file_path}")
    except pd.errors.EmptyDataError:
        raise ValueError("Error: The file is empty.")
    except pd.errors.ParserError:
        raise ValueError("Error: Unable to read the file. Please check if it is a valid CSV or Excel file.")
    except Exception as e:
        raise ValueError(f"Error: {e}")



