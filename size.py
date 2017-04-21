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

    #TODO: Manually check at least one count per table
    dbh_range = range(10, 80, 10)
    two_years = [2004, 2008]
    all_years = [2004, 2008, 2014]
    # Low df
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
    for year in two_years:
        for i, row in l8_counts.iterrows():
            l8_counts.loc[i, '_'.join([str(year), 'cohort'])] = low_df[(low_df['first_year'] <= year) &
                                                 (low_df['DBH2008'] > (l8_counts.loc[i, 'size_bin_max'] - 10)) &
                                                 (low_df['DBH2008'] <= l8_counts.loc[i, 'size_bin_max'])].shape[0]
    l8_counts.to_csv('dbh_l8_for_hist.csv', index=False)
    # Low 2014
    l14_counts = pd.DataFrame()
    l14_counts['size_bin_max'] = dbh_range
    for year in all_years:
        for i, row in l14_counts.iterrows():
            l14_counts.loc[i, '_'.join([str(year), 'cohort'])] = low_df[(low_df['first_year'] <= year) &
                                                 (low_df['DBH2014'] > (l14_counts.loc[i, 'size_bin_max'] - 10)) &
                                                 (low_df['DBH2014'] <= l14_counts.loc[i, 'size_bin_max'])].shape[0]
    l14_counts.to_csv('dbh_l14_for_hist.csv', index=False)
    # Mod df
    mod_df = df[df['trt_clean'] == 'M']

    # Mod 2004
    m4_counts = pd.DataFrame()
    m4_counts['size_bin_max'] = dbh_range
    for i, row in m4_counts.iterrows():
        m4_counts.loc[i, '2004_cohort'] = mod_df[(mod_df['DBH2004'] > (m4_counts.loc[i, 'size_bin_max'] - 10)) &
                                                 (mod_df['DBH2004'] <= m4_counts.loc[i, 'size_bin_max'])].shape[0]
    m4_counts.to_csv('dbh_m4_for_hist.csv', index=False)
    # Mod 2008
    m8_counts = pd.DataFrame()
    m8_counts['size_bin_max'] = dbh_range
    for year in two_years:
        for i, row in m8_counts.iterrows():
            m8_counts.loc[i, '_'.join([str(year), 'cohort'])] = mod_df[(mod_df['first_year'] <= year) &
                                                                       (mod_df['DBH2008'] > (
                                                                       m8_counts.loc[i, 'size_bin_max'] - 10)) &
                                                                       (mod_df['DBH2008'] <= m8_counts.loc[
                                                                           i, 'size_bin_max'])].shape[0]
    m8_counts.to_csv('dbh_m8_for_hist.csv', index=False)
    # Mod 2014
    m14_counts = pd.DataFrame()
    m14_counts['size_bin_max'] = dbh_range
    for year in all_years:
        for i, row in m14_counts.iterrows():
            m14_counts.loc[i, '_'.join([str(year), 'cohort'])] = mod_df[(mod_df['first_year'] <= year) &
                                                                        (mod_df['DBH2014'] > (
                                                                        m14_counts.loc[i, 'size_bin_max'] - 10)) &
                                                                        (mod_df['DBH2014'] <= m14_counts.loc[
                                                                            i, 'size_bin_max'])].shape[0]
    m14_counts.to_csv('dbh_m14_for_hist.csv', index=False)
    # Control df
    con_df = df[df['trt_clean'] == 'C']

    # Con 2004
    c4_counts = pd.DataFrame()
    c4_counts['size_bin_max'] = dbh_range
    for i, row in m4_counts.iterrows():
        c4_counts.loc[i, '2004_cohort'] = con_df[(con_df['DBH2004'] > (c4_counts.loc[i, 'size_bin_max'] - 10)) &
                                                 (con_df['DBH2004'] <= c4_counts.loc[i, 'size_bin_max'])].shape[0]
    c4_counts.to_csv('dbh_c4_for_hist.csv', index=False)
    # Con 2008
    c8_counts = pd.DataFrame()
    c8_counts['size_bin_max'] = dbh_range
    for year in two_years:
        for i, row in c8_counts.iterrows():
            c8_counts.loc[i, '_'.join([str(year), 'cohort'])] = con_df[(con_df['first_year'] <= year) &
                                                                       (con_df['DBH2008'] > (
                                                                           c8_counts.loc[i, 'size_bin_max'] - 10)) &
                                                                       (con_df['DBH2008'] <= c8_counts.loc[
                                                                           i, 'size_bin_max'])].shape[0]
    c8_counts.to_csv('dbh_c8_for_hist.csv', index=False)
    # Con 2014
    c14_counts = pd.DataFrame()
    c14_counts['size_bin_max'] = dbh_range
    for year in all_years:
        for i, row in c14_counts.iterrows():
            c14_counts.loc[i, '_'.join([str(year), 'cohort'])] = con_df[(con_df['first_year'] <= year) &
                                                                        (con_df['DBH2014'] > (
                                                                            c14_counts.loc[i, 'size_bin_max'] - 10)) &
                                                                        (con_df['DBH2014'] <= c14_counts.loc[
                                                                            i, 'size_bin_max'])].shape[0]
    c14_counts.to_csv('dbh_c14_for_hist.csv', index=False)


def make_stacked_ht_hist_tables(df):

    #TODO: Update this for heights
    #TODO: Manually check at least one count per table
    ht_range = [2.5, 5.0, 7.5, 10.0, 12.5, 15.0, 17.5, 20.0, 22.5, 25.0, 27.5, 30.0]
    two_years = [2004, 2008]
    all_years = [2004, 2008, 2014]
    # Low df
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
    for year in two_years:
        for i, row in l8_counts.iterrows():
            l8_counts.loc[i, '_'.join([str(year), 'cohort'])] = low_df[(low_df['first_year'] <= year) &
                                                 (low_df['DBH2008'] > (l8_counts.loc[i, 'size_bin_max'] - 10)) &
                                                 (low_df['DBH2008'] <= l8_counts.loc[i, 'size_bin_max'])].shape[0]
    l8_counts.to_csv('dbh_l8_for_hist.csv', index=False)
    # Low 2014
    l14_counts = pd.DataFrame()
    l14_counts['size_bin_max'] = dbh_range
    for year in all_years:
        for i, row in l14_counts.iterrows():
            l14_counts.loc[i, '_'.join([str(year), 'cohort'])] = low_df[(low_df['first_year'] <= year) &
                                                 (low_df['DBH2014'] > (l14_counts.loc[i, 'size_bin_max'] - 10)) &
                                                 (low_df['DBH2014'] <= l14_counts.loc[i, 'size_bin_max'])].shape[0]
    l14_counts.to_csv('dbh_l14_for_hist.csv', index=False)
    # Mod df
    mod_df = df[df['trt_clean'] == 'M']

    # Mod 2004
    m4_counts = pd.DataFrame()
    m4_counts['size_bin_max'] = dbh_range
    for i, row in m4_counts.iterrows():
        m4_counts.loc[i, '2004_cohort'] = mod_df[(mod_df['DBH2004'] > (m4_counts.loc[i, 'size_bin_max'] - 10)) &
                                                 (mod_df['DBH2004'] <= m4_counts.loc[i, 'size_bin_max'])].shape[0]
    m4_counts.to_csv('dbh_m4_for_hist.csv', index=False)
    # Mod 2008
    m8_counts = pd.DataFrame()
    m8_counts['size_bin_max'] = dbh_range
    for year in two_years:
        for i, row in m8_counts.iterrows():
            m8_counts.loc[i, '_'.join([str(year), 'cohort'])] = mod_df[(mod_df['first_year'] <= year) &
                                                                       (mod_df['DBH2008'] > (
                                                                       m8_counts.loc[i, 'size_bin_max'] - 10)) &
                                                                       (mod_df['DBH2008'] <= m8_counts.loc[
                                                                           i, 'size_bin_max'])].shape[0]
    m8_counts.to_csv('dbh_m8_for_hist.csv', index=False)
    # Mod 2014
    m14_counts = pd.DataFrame()
    m14_counts['size_bin_max'] = dbh_range
    for year in all_years:
        for i, row in m14_counts.iterrows():
            m14_counts.loc[i, '_'.join([str(year), 'cohort'])] = mod_df[(mod_df['first_year'] <= year) &
                                                                        (mod_df['DBH2014'] > (
                                                                        m14_counts.loc[i, 'size_bin_max'] - 10)) &
                                                                        (mod_df['DBH2014'] <= m14_counts.loc[
                                                                            i, 'size_bin_max'])].shape[0]
    m14_counts.to_csv('dbh_m14_for_hist.csv', index=False)
    # Control df
    con_df = df[df['trt_clean'] == 'C']

    # Con 2004
    c4_counts = pd.DataFrame()
    c4_counts['size_bin_max'] = dbh_range
    for i, row in m4_counts.iterrows():
        c4_counts.loc[i, '2004_cohort'] = con_df[(con_df['DBH2004'] > (c4_counts.loc[i, 'size_bin_max'] - 10)) &
                                                 (con_df['DBH2004'] <= c4_counts.loc[i, 'size_bin_max'])].shape[0]
    c4_counts.to_csv('dbh_c4_for_hist.csv', index=False)
    # Con 2008
    c8_counts = pd.DataFrame()
    c8_counts['size_bin_max'] = dbh_range
    for year in two_years:
        for i, row in c8_counts.iterrows():
            c8_counts.loc[i, '_'.join([str(year), 'cohort'])] = con_df[(con_df['first_year'] <= year) &
                                                                       (con_df['DBH2008'] > (
                                                                           c8_counts.loc[i, 'size_bin_max'] - 10)) &
                                                                       (con_df['DBH2008'] <= c8_counts.loc[
                                                                           i, 'size_bin_max'])].shape[0]
    c8_counts.to_csv('dbh_c8_for_hist.csv', index=False)
    # Con 2014
    c14_counts = pd.DataFrame()
    c14_counts['size_bin_max'] = dbh_range
    for year in all_years:
        for i, row in c14_counts.iterrows():
            c14_counts.loc[i, '_'.join([str(year), 'cohort'])] = con_df[(con_df['first_year'] <= year) &
                                                                        (con_df['DBH2014'] > (
                                                                            c14_counts.loc[i, 'size_bin_max'] - 10)) &
                                                                        (con_df['DBH2014'] <= c14_counts.loc[
                                                                            i, 'size_bin_max'])].shape[0]
    c14_counts.to_csv('dbh_c14_for_hist.csv', index=False)

