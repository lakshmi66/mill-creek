_author_ = 'Lakshmi'

import pandas as pd
import data_cleaning as dc
import density as dens
import spp_composition as sp
import size as sz

# Enter your output path here

output_path = '/Users/Lakshmi/Google Drive/MillCreek/'

# Read in the most recent datafile. Unfortunately, this was manually manipulated after the most recent export from the
# access database. # TODO: Add notes to readme

# Data reading and cleaning

df = pd.read_table('treedata2.txt')

df = dc.clean_millcreek_data(df)

# Density table (Table 1)

tree_count_df = dens.tree_counts_per_plot(df)

table_1 = dens.cr_table_1(tree_count_df)

table_1.to_csv(output_path + 'table_1.csv', index=False)

# Spp composition table (Table 2)

df = sp.add_spp_cat(df)

table_2 = sp.cr_table_2(df)

table_2.to_csv(output_path + 'table_2.csv', index=False)

# Size by treatment table (Table 3)

df = sz.add_vol(df, 'DBH2014', 'HT2014', 'VOL2014')

table_3 = sz.cr_table_3(df)

table_3.to_csv(output_path + 'table_3.csv')

#create the version of Table 3 excluding trees with bear damage affecting DBH2014 measurements

df_no_dbh_damage = df[df['DBH_damage_2014'] == False]

table_3a = sz.cr_table_3(df_no_dbh_damage)

table_3a.to_csv(output_path + 'table_3a.csv')

#count the number of trees that were excluded per treatment from 3a to 3b

table_3b = sz.count_dbh2014_damage(df)
table_3b.to_csv(output_path + 'table_3b.csv')

# Tables for size histograms

sz.cr_stacked_dbh_hist_tables(df, output_path)

sz.cr_stacked_ht_hist_tables(df, output_path)

# Tables for coefficient of variation plot

cv_table = sz.cr_cv_table(df)

cv_table.to_csv(output_path + 'cv_table.csv')

# Modeling effect of treatment on ht and diameter of 1)residual trees  2) largest trees

# Data exploration for modeling:

    # Look into number of trees per plot, per treatment area
    # Number of large trees per plot?

# Some kind of diversity comparison for different treatments