_author_ = 'Lakshmi'

import numpy as np
import pandas as pd


def clean_millcreek_data(df):

    # Rename "Treatment Area" column
    df = df.rename(columns={'Stand': 'trt_area'})

    # Strip spaces of treatment area names where required
    df['trt_area'] = df['trt_area'].apply(str.strip)

    # Fill in stand name from treatment area name
    df['stand'] = df['trt_area'].apply(fill_stand_names_from_trt_area)

    # Fill in treatment values
    df = fill_trt(df)

    # Add dead column (can be 2008 or 2014)

    df['dead'] = np.nan

    df.loc[(df['DBH2008'] == 0) | (df['CC2008'] == 'DEAD'), 'dead'] = '2008'
    df.loc[(df['DC2008'] == 99) & (df['DC12014'] == 99), 'dead'] = '2008'
    df.loc[(df['DBH2014'] == 0) | (df['CC2014'] == 'DEAD'), 'dead'] = '2014'

    # Replace 0 diameters with NAs.  0 DBH typically indicates dead trees
    df.loc[df['DBH2008'] == 0, ['DBH2008']] = np.nan
    df.loc[df['DBH2014'] == 0, ['DBH2014']] = np.nan

    # Add firstyear column indicating when the tree was first measured/included in dataset
    # This is hood but effective
    df['first_year'] = np.where(df['DBH2004'].notnull(), 2004,
                                  np.where(df['DBH2008'].notnull(), 2008,
                                           np.where(df['DBH2014'].notnull(), 2014, np.nan)))

    return df


def fill_stand_names_from_trt_area(trt_area_name):

    two_letters = [letter for letter in trt_area_name[:2]]
    stand_name = ''.join(two_letters)
    return stand_name

def fill_trt(df):

    # Create a dataframe for each treatment
    l_df = pd.DataFrame()
    l_df['trt_area'] = ['CH1', 'CH4', 'CH5', 'CH6', 'MR3', 'MR4', 'MR5', 'MR8', 'CR1']
    l_df['trt_clean'] = 'L'

    h_df = pd.DataFrame()
    h_df['trt_area'] = ['CH3', 'CH7', 'MR2', 'MR6', 'CR2']
    h_df['trt_clean'] = 'M'

    c_df = pd.DataFrame()
    c_df['trt_area'] = ['CH2', 'CH8', 'MR1', 'MR7', 'CR3']
    c_df['trt_clean'] = 'C'

    # Merge treatment dfs into one df
    trt_df = pd.concat([l_df, h_df, c_df])

    # Merge in treatments with tree df
    df = df.merge(trt_df, how='left', on='trt_area')

    return df