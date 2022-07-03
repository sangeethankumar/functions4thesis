#!/usr/bin/python3

import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pylab as plt


def read_taranga_lc(path2lc):
    """
    given path to the taranga light curve, returns a pandas dataframe

    _extended_summary_

    :param path2lc: _description_
    :type path2lc: _type_
    :return: _description_
    :rtype: _type_
    """
    taranga_lc = pd.read_csv(path2lc)
    return taranga_lc


def plot_lc(taranga_lc, plot_val="pdc"):
    fig = plt.figure(figsize=(6, 6), dpi=300)
    plt.plot(
        taranga_lc["bjd"],
        taranga_lc[plot_val],
        color="k",
        marker=".",
        linestyle="None",
        ms=1.0,
    )
    plt.xlabel("BJD - 2457000 [days]")
    plt.ylabel(plot_val)


def plot_pdcm_pdcc(taranga_lc):
    """
    plots pdcm and pdcc for comparison

    _extended_summary_

    :param taranga_lc: _description_
    :type taranga_lc: _type_
    """
    fig = plt.figure(figsize=(6, 6))
    outlier_corr_applied = taranga_lc["pdcm"] - taranga_lc["pdcc"]
    colors = np.where(outlier_corr_applied == 0, "k", "r")

    ax1 = plt.subplot(211)
    plt.plot(
        taranga_lc["bjd"],
        taranga_lc["pdcm"],
        color=colors,
        marker="o",
        ms=1.0,
        linestyle="None",
    )
    plt.ylabel("PDCM")
    ax2 = plt.subplot(212, sharey=ax1)
    plt.plot(
        taranga_lc["bjd"],
        taranga_lc["pdcc"],
        color="k",
        marker="o",
        ms=1.0,
        linestyle="None",
    )
    plt.ylabel("PDCC")
    plt.xlabel("BJD - 2457000")
