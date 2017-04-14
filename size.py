_author_ = 'Lakshmi'

import pandas as pd
import numpy as np
import math


def add_vol(df, dbh_colname, ht_colname, vol_colname):
    df[vol_colname] = np.nan
    for i, row in df[(df[dbh_colname].notnull()) & (df[ht_colname].notnull())].iterrows():
        # TODO: double check the above dbh volume calculation
        if row[ht_colname] > 1.37:
            df.ix[i, vol_colname] = math.pi*((row[dbh_colname]/200)**2)*1.37 + \
                             (math.pi/2)*((row[dbh_colname]/200)**2)*(row[ht_colname]-1.37)
    return df


def cr_table_3(df):

    # Residual trees summary table
    res_grouper = df[df['first_year'] == 2004].groupby('trt_clean')
    res_summary = res_grouper.agg({'DBH2014': [np.mean, np.std], 'HT2014': [np.mean, np.std], 'VOL2014': [np.mean, np.std]})

    # Largest 125 trees summary table
    grouper = df.groupby(['trt_clean'])
    large_df = grouper.apply(take_125_largest).reset_index(drop=True)
    large_grouper =large_df.groupby('trt_clean')
    large_summary = large_grouper.agg({'DBH2014': [np.mean, np.std], 'HT2014': [np.mean, np.std], 'VOL2014': [np.mean, np.std]})

    # All trees summary table
    all_summary = grouper.agg({'DBH2014': [np.mean, np.std], 'HT2014': [np.mean, np.std], 'VOL2014': [np.mean, np.std]})

    # Stick them together


def take_125_largest(group_df):
    # TODO: Double check that this worked properly :D  DERP
    sorted_top_125 = group_df.sort_values(by='DBH2014', ascending=False).reset_index()[:125]
    return sorted_top_125
