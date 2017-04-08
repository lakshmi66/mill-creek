_author_ = 'Lakshmi'

import numpy as np
import pandas as pd

def tree_counts_per_plot(df):

    plot_grouper = df.groupby(['stand', 'trt_clean', 'trt_area', 'Plot'])

    tree_count_df = plot_grouper.agg({'DBH2004': 'count', 'DBH2008': 'count', 'DBH2014': 'count'}).reset_index()

    tree_count_df.columns = ['stand', 'trt_clean', 'trt_area', 'Plot', 'count_2008', 'count_2014', 'count_2004']

    tree_count_df = fill_plot_size(tree_count_df)

    return tree_count_df


def fill_plot_size(tree_count_df):

    # Create pdf for mapping trt to plot size
    plot_map_df = pd.DataFrame()
    plot_map_df['trt_clean'] = ['L', 'M', 'C']
    plot_map_df['plot_size_ha'] = [0.067, 0.067, 0.04]

    # Merge plot size with tree_count_df
    tree_count_df = tree_count_df.merge(plot_map_df, how='left', on='trt_clean')

    return tree_count_df

def cr_table_1(tree_count_df):

    st_trt_grouper = tree_count_df.groupby(['stand', 'trt_clean'])

    table_1 = st_trt_grouper.agg({'count_2004': 'sum',
                                  'count_2008': 'sum',
                                  'count_2014': 'sum',
                                  'plot_size_ha': ['sum', 'count']}).reset_index()

    table_1.columns = table_1.columns.get_level_values(0)

    table_1.columns = ['stand', 'trt_clean', 'count_2004', 'plot_size_ha', 'number_of_plots', 'count_2008', 'count_2014']

    table_1['tpha_2004'] = table_1['count_2004']/table_1['plot_size_ha']
    table_1['tpha_2008'] = table_1['count_2008'] / table_1['plot_size_ha']
    table_1['tpha_2014'] = table_1['count_2014'] / table_1['plot_size_ha']
    table_1['10_yr_change'] = table_1['tpha_2014'] - table_1['tpha_2004']

    return table_1









