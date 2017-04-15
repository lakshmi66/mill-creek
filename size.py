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


def take_125_largest(group_df):
    # TODO: Double check that this worked properly :D  DERP
    sorted_top_125 = group_df.sort_values(by='DBH2014', ascending=False).reset_index()[:125]
    return sorted_top_125


def cr_table_3(df):

    # Residual trees summary table
    res_grouper = df[df['first_year'] == 2004].groupby('trt_clean')
    res_summary = res_grouper.agg({'DBH2014': [np.mean, np.std], 'HT2014': [np.mean, np.std], 'VOL2014': [np.mean, np.std]})
    res_summary = res_summary.stack(0)
    res_summary.columns = ['Residual Mean', 'Residual SD']

    # Largest 125 trees summary table #WTF IS GOING ON???
    grouper = df.groupby(['stand', 'trt_clean'])
    large_df = grouper.apply(take_125_largest).reset_index(drop=True)
    large_grouper = large_df.groupby('stand')
    large_summary = large_grouper.agg({'DBH2014': [np.mean, np.std], 'HT2014': [np.mean, np.std], 'VOL2014': [np.mean, np.std]})
    large_summary = large_summary.stack(0)
    large_summary.columns = ['Largest 125 Mean', 'Largest 125 SD']

    # All trees summary table
    all_summary = grouper.agg({'DBH2014': [np.mean, np.std], 'HT2014': [np.mean, np.std], 'VOL2014': [np.mean, np.std]})
    all_summary = all_summary.stack(0)
    all_summary.columns = ['Total Mean', 'Total SD']

    table_3 = pd.concat([res_summary, large_summary, all_summary], axis=1)

    return table_3

#def make_hist_tables(df, colname_2004, colname_2008, colname_2014, bucket_max_array):

    # create d


