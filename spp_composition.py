_author_ = 'Lakshmi'

import pandas as pd
import numpy as np

def add_spp_cat(df):

    df['spp_cat'] = np.where(df['Spp'] == 'SESE', 'Redwood',
                                  np.where(df['Spp'] == 'PSME', 'Douglas-fir', 'Other'))

    return df


def cr_table_2(df):

    # create summary table
    spp_summary = df.groupby(['trt_clean', 'spp_cat', 'stand'])['DBH2014'].count().unstack(1).reset_index()

    # calculate percent each spp
    spp_summary['total_count'] = spp_summary['Douglas-fir'] + spp_summary['Redwood'] + spp_summary['Other']

    spp_summary['perc_df'] = spp_summary['Douglas-fir'] / spp_summary['total_count']
    spp_summary['perc_rw'] = spp_summary['Redwood'] / spp_summary['total_count']
    spp_summary['perc_oth'] = spp_summary['Other'] / spp_summary['total_count']

    # drop non-percent columns
    table_2 = spp_summary.drop(['Douglas-fir', 'Redwood', 'Other', 'total_count'], axis=1)

    return table_2
