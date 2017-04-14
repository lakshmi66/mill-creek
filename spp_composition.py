_author_ = 'Lakshmi'

import pandas as pd
import numpy as np

def add_spp_cat(df):

    df['spp_cat'] = np.where(df['Spp'] == 'SESE', 'Redwood',
                                  np.where(df['Spp'] == 'PSME', 'Douglas-fir', 'Other'))

    return df


def cr_table_2(df):

    # Set up the table
    table_2 = pd.DataFrame()
    table_2['Treatment'] = ['C', 'C', 'C', 'M', 'M', 'M', 'L', 'L', 'L']
    table_2['Species Category'] = ['Redwood', 'Douglas-fir', 'Other', 'Redwood', 'Douglas-fir', 'Other', 'Redwood',
                          'Douglas-fir', 'Other']
    table_2['CH'] = np.nan
    table_2['CR'] = np.nan
    table_2['MR'] = np.nan

    stand_list = ['CH', 'CR', 'MR']

    # Fill the table
    for stand in stand_list:
        for i, row in table_2.iterrows():
            # number of trees in numerator species
            spp_count = df.loc[(df['trt_clean'] == row['Treatment']) &
                               (df['spp_cat'] == row['Species Category']) & (df['stand'] == stand), 'DBH2014'].count()
            # total number of trees in that trt in stand
            total_count = df.loc[(df['trt_clean'] == row['Treatment']) & (df['stand'] == stand), 'DBH2014'].count()

            table_2.ix[i, stand] = float(spp_count) / total_count

    # Add treatment means and sd
    table_2['Treatment Mean'] = np.nan
    table_2['Treatment SD'] = np.nan

    for i, row in table_2.iterrows():
        table_2.ix[i, 'Treatment Mean'] = row[['CH', 'CR', 'MR']].mean()
        table_2.ix[i, 'Treatment SD'] = row[['CH', 'CR', 'MR']].std()



    # create summary table
    # spp_summary = df.groupby(['trt_clean', 'spp_cat', 'stand'])['DBH2014'].count().unstack(1).reset_index()
    #
    # # calculate percent each spp
    # spp_summary['total_count'] = spp_summary['Douglas-fir'] + spp_summary['Redwood'] + spp_summary['Other']
    #
    # spp_summary['perc_df'] = spp_summary['Douglas-fir'] / spp_summary['total_count']
    # spp_summary['perc_rw'] = spp_summary['Redwood'] / spp_summary['total_count']
    # spp_summary['perc_oth'] = spp_summary['Other'] / spp_summary['total_count']
    #
    # # drop non-percent columns
    # table_2 = spp_summary.drop(['Douglas-fir', 'Redwood', 'Other', 'total_count'], axis=1)

    return table_2
