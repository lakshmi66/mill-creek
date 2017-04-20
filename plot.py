_author_ = 'Lakshmi'

import pandas as pd
import matplotlib.pyplot as plt


def make_ht_dbh_scatterplot(dbh_col, ht_col, figure_title, output_filepath):
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.scatter(dbh_col, ht_col)
    ax.set_xlabel('DBH (cm)')
    ax.set_ylabel('Height (m)')
    ax.set_title(figure_title)
    fig.savefig(output_filepath)


def make_dbh_histograms(df, output_filepath):
    dbh_hist = plt.figure()

    ax1 = dbh_hist.add_subplot(3, 1, 1)
    ax2 = dbh_hist.add_subplot(3, 1, 2)
    ax3 = dbh_hist.add_subplot(3, 1, 3)

    ax1.hist(df['DBH2004'].dropna().values)
    ax1.set_title('DBH 2004 (cm)')

    ax2.hist(df['DBH2008'].dropna().values)
    ax2.set_title('DBH 2008 (cm)')

    ax3.hist(df['DBH2014'].dropna().values)
    ax3.set_title('DBH 2014 (cm)')

    plt.subplots_adjust(hspace=0.5)

    dbh_hist.savefig(output_filepath)


def make_ht_histograms(df, output_filepath):
    ht_hist = plt.figure()

    ax1 = ht_hist.add_subplot(3, 1, 1)
    ax2 = ht_hist.add_subplot(3, 1, 2)
    ax3 = ht_hist.add_subplot(3, 1, 3)

    ax1.hist(df['HT2004'].dropna().values)
    ax1.set_title('HT 2004 (m)')

    ax2.hist(df['HT2008'].dropna().values)
    ax2.set_title('HT 2008 (m)')

    ax3.hist(df['HT2014'].dropna().values)
    ax3.set_title('HT 2014 (m)')

    plt.subplots_adjust(hspace=0.5)

    ht_hist.savefig(output_filepath)