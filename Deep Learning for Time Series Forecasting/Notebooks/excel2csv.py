import os
import pandas as pd
import xlrd

def read_excel(filesourcepath: str, resample = None):
    
    # read the excel file using pandas
    df = pd.read_excel(filesourcepath)

    # sometimes, excel does not return the value to the cell to which it was called; 
    # sometimes it returns it to a cell below
    if df.loc[4, 'Stock'] == 'Date':
        df = pd.read_excel(filesourcepath, header = 5, engine='openpyxl')
    elif df.loc[5, 'Stock'] == 'Date':
        df = pd.read_excel(filesourcepath, header = 6, engine='openpyxl')

    # delete all columns with NaN as values
    # df = df.dropna(axis = 0, how = 'all')
    df = df.dropna(axis = 0)

    # we create a function that will transform the values of the numerical dates 
    # from excel into python datetime
    def read_date(date):
        return xlrd.xldate.xldate_as_datetime(date, 0)

    # apply the read_date function to the dataframe to convert the date column into datetime
    df['Date'] = pd.to_datetime(df['Date'].apply(read_date), errors='coerce')
    df.set_index(keys = 'Date', inplace = True)

    # delete all columns with NaN as values
    df = df.dropna(axis = 0)
    
    # resample the dataframe
    if resample == 'W':
        df = df.resample(rule = 'W').mean()
    elif resample == 'M':
        df = df.resample(rule = 'M').mean() 
    
    return df

def excel2csv(sourcepath: str):
    for file in os.listdir(sourcepath):
        print(file)
        filesourcepath = sourcepath + '/' + file
        
        # read the excel file and output a dataframe
        df = read_excel(filesourcepath)

        endfilesourcepath = "..\Data\csv" + '/' + file
        endfilesourcepath = endfilesourcepath.replace('.xlsx','.csv')
        df.to_csv(endfilesourcepath)
        
# run conversion
if __name__ == "__main__":
    excel2csv("..\Data\excel")

    