_author_ = 'Lakshmi'

import pandas as pd
import numpy as np
import math


def add_vol_2004(df, dbh_colname, ht_colname, vol_colname):
    df[vol_colname] = np.nan
    for i, row in df[(df['DBH2004'].notnull()) & (df['HT2004'].notnull())].iterrows():
        if row['HT2004'] > 1.37:
            df.ix[i, 'VOL2004'] = math.pi*((row['DBH2004']/200)**2)*1.37 + \
                             (math.pi/2)*((row['DBH2004']/200)**2)*(row['HT2004']-1.37)
    return df





def cr_table_3(df):

    # Residual trees summary table
    trt_grouper = df[df['first_year'] == 2004].groupby(['trt_clean'])
    res_summary = trt_grouper.agg({'DBH2014': [np.mean, np.std]})

    # Largest 125 trees summary table

#def avg_125_largest(group_df, column):
