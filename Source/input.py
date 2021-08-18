#requirements : install openpyxl, pandas, numpy
import pandas as pd
import numpy as np
#Reading each sheet separately
df = pd.read_excel("Option_3_DataSet.xls", sheet_name='Vol and Swaps Rates usd')

annuity_df = pd.read_excel("Option_3_DataSet.xls", sheet_name='Option_3_DataSet')
annuity_df = annuity_df.drop('Currency', axis = 1)

# Preparing fonctions to interpolate annualities

def addanuity(mydf, expiry, tenor, annuity):
    new_row = pd.Series({'Expiry': expiry, 'UnderlyingTenor': tenor, 'Annuity': annuity})
    mydf = mydf.append(new_row, ignore_index = True)
    return mydf

def getannuity(expi, ten, mydf):
    temp1 = mydf.loc[annuity_df['Expiry'] == expi]
    temp2 = temp1.loc[temp1['UnderlyingTenor'] == ten]
    return temp2.iloc[0]['Annuity']

def interpol(ann1, ann2):
    return (ann1+ann2)/2


# Looping on each expiration to interpolate annuities
for expi in ['1M', '3M', '6M', '1Y', '2Y']:
    #3y
    annuity_df = addanuity(annuity_df, expi, '3Y', interpol(getannuity(expi, '1Y', annuity_df), getannuity(expi, '5Y', annuity_df)))
    #4y
    annuity_df = addanuity(annuity_df, expi, '4Y', interpol(getannuity(expi, '3Y', annuity_df), getannuity(expi, '5Y', annuity_df)))
    #6y
    annuity_df = addanuity(annuity_df, expi, '6Y', interpol(getannuity(expi, '2Y', annuity_df), getannuity(expi, '10Y', annuity_df)))
    #8y
    annuity_df = addanuity(annuity_df, expi, '8Y', interpol(getannuity(expi, '6Y', annuity_df), getannuity(expi, '10Y', annuity_df)))
    #7y
    annuity_df = addanuity(annuity_df, expi, '7Y', interpol(getannuity(expi, '6Y', annuity_df), getannuity(expi, '8Y', annuity_df)))
    #9y
    annuity_df = addanuity(annuity_df, expi, '9Y', interpol(getannuity(expi, '8Y', annuity_df), getannuity(expi, '10Y', annuity_df)))
    #12y
    annuity_df = addanuity(annuity_df, expi, '12Y', interpol(getannuity(expi, '10Y', annuity_df), getannuity(expi, '15Y', annuity_df)))
    #25y
    annuity_df = addanuity(annuity_df, expi, '25Y', interpol(getannuity(expi, '20Y', annuity_df), getannuity(expi, '30Y', annuity_df)))







#Editing the columns names beofre setting them
df.iloc[0] = df.iloc[0].str.replace('USSW', '')
df.iloc[0] = df.iloc[0].str.replace(' Curncy', '')
df.iloc[0] = df.iloc[0].str.replace('USSN', '')
df.iloc[0] = df.iloc[0].str.replace(' CMPN', '')

#Setting the right names for columns
df.columns = df.iloc[0]
df = df.rename(columns={'Time\\ Underlying or Vol': 'Time'})
#Setting right names for rows
df['Time'] = pd.to_datetime(df['Time'])
df = df.set_index('Time')
#Deleting useless columns
df = df.drop(df.columns[[221,220,219,218,217,216,215,214,213,212]], axis=1)
df = df.drop([0])

#Creating a dataset for swaprates
swaprates = df.iloc[:, :15]
#Creating a dataset for volatilities
dfvols = df.iloc[:, 15:211]
#Journalizing the values
dfvols = dfvols.applymap(lambda x: np.sqrt(x/250))
