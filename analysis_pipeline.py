_author_ = 'Lakshmi'

import pandas as pd
import data_cleaning as dc
import density as d

# Read in the most recent datafile. Unfortunately, this was manually manipulated after the most recent export from the
# access database. # TODO: Add notes to readme

# Data reading and cleaning

df = pd.read_table('treedata2.txt')

df = dc.clean_millcreek_data(df)

# Density tables and figures

tree_count_df = d.tree_counts_per_plot(df)

table_1 = d.cr_table_1(tree_count_df)

