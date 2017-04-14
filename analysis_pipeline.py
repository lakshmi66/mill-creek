_author_ = 'Lakshmi'

import pandas as pd
import data_cleaning as dc
import density as dens
import spp_composition as sp
import size as sz

# Read in the most recent datafile. Unfortunately, this was manually manipulated after the most recent export from the
# access database. # TODO: Add notes to readme

# Data reading and cleaning

df = pd.read_table('treedata2.txt')

df = dc.clean_millcreek_data(df)

# Density table (Table 1)

tree_count_df = dens.tree_counts_per_plot(df)

table_1 = dens.cr_table_1(tree_count_df)

table_1.to_csv('table_1.csv', index=False)

# Spp composition table (Table 2)

df = sp.add_spp_cat(df)

table_2 = sp.cr_table_2(df)

table_2.to_csv('table_2.csv', index=False)

# Size by treatment table (Table 3)

df = sz.add_vol(df, 'DBH2014', 'HT2014', 'VOL2014')

# Output for size histograms

# Coefficient of variation plot

# Output for creating coefficient of variation plot