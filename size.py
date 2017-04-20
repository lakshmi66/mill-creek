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

    # Largest 125 trees summary table
    grouper = df.groupby(['stand', 'trt_clean'])
    large_df = grouper.apply(take_125_largest).reset_index(drop=True)
    large_grouper = large_df.groupby('trt_clean')
    large_summary = large_grouper.agg({'DBH2014': [np.mean, np.std], 'HT2014': [np.mean, np.std], 'VOL2014': [np.mean, np.std]})
    large_summary = large_summary.stack(0)
    large_summary.columns = ['Largest 125 Mean', 'Largest 125 SD']

    # All trees summary table
    all_grouper = df.groupby('trt_clean')
    all_summary = all_grouper.agg({'DBH2014': [np.mean, np.std], 'HT2014': [np.mean, np.std], 'VOL2014': [np.mean, np.std]})
    all_summary = all_summary.stack(0)
    all_summary.columns = ['Total Mean', 'Total SD']

    table_3 = pd.concat([res_summary, large_summary, all_summary], axis=1)

    return table_3


def count_dbh2014_damage(df):

    all_grouper = df.groupby('trt_clean')
    count_df = all_grouper.agg({'DBH_damage_2014': [np.sum, 'count']})
    count_df.columns = count_df.columns.get_level_values(0)
    count_df.columns = ['excluded', 'total']
    return count_df


def make_stacked_dbh_hist_tables(df):

    dbh_range = range(10, 80, 10)

    # create Low df
    low_df = df[df['trt_clean'] == 'L']

    # Low 2004
    l4_counts = pd.DataFrame()
    l4_counts['size_bin_max'] = dbh_range
    for i, row in l4_counts.iterrows():
        l4_counts.loc[i, '2004_cohort'] = low_df[(low_df['DBH2004'] > (l4_counts.loc[i, 'size_bin_max'] - 10)) &
                                                 (low_df['DBH2004'] <= l4_counts.loc[i, 'size_bin_max'])].shape[0]
    l4_counts.to_csv('dbh_l4_for_hist.csv', index=False)

    # Low 2008
    l8_counts = pd.DataFrame()
    l8_counts['size_bin_max'] = dbh_range
    for i, row in l8_counts.iterrows():
        l8_counts.loc[i, '2004_cohort'] = low_df[(low_df['first_year'] == 2004) &
                                                 (low_df['DBH2008'] > (l8_counts.loc[i, 'size_bin_max'] - 10)) &
                                                 (low_df['DBH2008'] <= l8_counts.loc[i, 'size_bin_max'])].shape[0]

    for i, row in l8_counts.iterrows():
        l8_counts.loc[i, '2008_cohort'] = low_df[(low_df['first_year'] <= 2008) &
                                                 (low_df['DBH2008'] > (l8_counts.loc[i, 'size_bin_max'] - 10)) &
                                                 (low_df['DBH2008'] <= l8_counts.loc[i, 'size_bin_max'])].shape[0]

    l8_counts.to_csv('dbh_l8_for_hist.csv', index=False)

    # Low 2014

    l14_counts = pd.DataFrame()
    l14_counts['size_bin_max'] = dbh_range
    years = [2004, 2008, 2014]

    for year in years:
        for i, row in l14_counts.iterrows():
            l14_counts.loc[i, '_'.join([year, 'cohort'])] = low_df[(low_df['first_year'] <= year) &
                                                 (low_df['DBH2014'] > (l14_counts.loc[i, 'size_bin_max'] - 10)) &
                                                 (low_df['DBH2014'] <= l14_counts.loc[i, 'size_bin_max'])].shape[0]

    l14_counts.to_csv('dbh_l14_for_hist.csv', index=False)

    # Mod 2004

    # Mod 2008

    # Mod 2014

    # Control 2004

    # Control 2008

    # Control 2014


    # fill dataframe by iterating over columns, then rows within columns




