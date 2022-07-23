#!/usr/bin/python3
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap

plt.rcParams["axes.edgecolor"] = "#FA6E4F"
plt.rcParams["font.family"] = "monospace"
import seaborn as sns
from scipy import stats
import statsmodels.api as sm
import statsmodels.stats.api as sms
from statsmodels.stats.diagnostic import het_white
from statsmodels.graphics.gofplots import qqplot
from scipy.stats import shapiro, normaltest, anderson
import warnings

warnings.filterwarnings("ignore")


def build_linear_model(stat_df, var="log_pdc_mean"):
    # calculating binned statistics
    print("Calculating binnes statistics")
    nbins = 50
    std_bin, bin_edge, bin_number = stats.binned_statistic(
        stat_df.Tmag, stat_df[var], "std", bins=nbins
    )
    mean_bin, _, _ = stats.binned_statistic(
        stat_df.Tmag, stat_df[var], "mean", bins=nbins
    )
    tmag_bin, _, _ = stats.binned_statistic(
        stat_df.Tmag, stat_df[var], "mean", bins=nbins
    )
    print()

    # scatter plot of the variables with errors on variable for each bin of Tmag
    print("Plotting")
    fig, ax = plt.subplots(figsize=(4, 2), dpi=300)
    ax.scatter(stat_df.Tmag, stat_df.log_pdc_mean, color="grey", marker="o", s=0.1)
    ax.errorbar(tmag_bin, mean_bin, std_bin, fmt=".", color="r", ms=1, linestyle="None")
    ax.invert_xaxis()
    plt.xlabel("Tmag")
    plt.ylabel(var)
    plt.show()
    print()

    # dropping rows with na values
    print("Dropping rows with na")
    stat_df_no_na = stat_df.dropna()
    stat_df_no_na.isna().sum()
    print()

    # adding a constant to get intercept
    print("Adding a constant to get intercept")
    Tmag_sm = sm.add_constant(stat_df_no_na.Tmag)
    print()

    # Ordinary Least Squares fitting
    print("Building linear regression model")
    lr = sm.OLS(stat_df_no_na[var], Tmag_sm).fit()
    print()

    print("*" * 10 + "Linear regression estimated parameters" + "*" * 10)
    print(lr.params)
    print()

    print("*" * 10 + "Linear regression model summary" + "*" * 10)
    print(lr.summary())
    print()

    print("Plotting with linear model")
    incpt = lr.params.const
    slp = lr.params.Tmag
    fig, ax = plt.subplots(figsize=(4, 2), dpi=300)
    ax.scatter(stat_df.Tmag, stat_df[var], color="grey", marker="o", s=0.1)
    ax.plot(stat_df.Tmag, incpt + slp * stat_df.Tmag, color="b", ls="--")
    ax.invert_xaxis()
    plt.xlabel("Tmag")
    plt.ylabel(var)
    plt.show()
    print()

    print("Calculating residuals")
    # Predicting
    var_pred = lr.predict(Tmag_sm)

    # Creating residuals
    res = stat_df_no_na[var] - var_pred
    print()

    print("Visual examination of residual distribution")
    # plotting histogram for visual examination
    fig = plt.figure()
    sns.distplot(res, bins=50)
    plt.title("Error Terms", fontsize=15)
    plt.xlabel("Y - Y_pred", fontsize=15)
    plt.show()
    print()

    print("Scatter plot for checking patterns in residuals")
    plt.scatter(stat_df_no_na.Tmag, res)
    plt.show()
    print()

    print("Q-Q plot")
    qqplot(res, line="s")
    print()

    print("Statistical tests for normality of residuals")
    print("\t1. Shapiro-Wilk Test")
    # Shapiro-wilk test
    stat, p = shapiro(res)
    print("\t\tStatistics=%.3f, p=%.3f" % (stat, p))
    # interpret
    alpha = 0.05
    if p > alpha:
        print("\t\tSample looks Gaussian (fail to reject H0)")
    else:
        print("\t\tSample does not look Gaussian (reject H0)")
    print("\t2. D'Agostino's K^2 Test")
    stat, p = normaltest(res)
    print("\t\tStatistics=%.3f, p=%.3f" % (stat, p))
    # interpret
    alpha = 0.05
    if p > alpha:
        print("\t\tSample looks Gaussian (fail to reject H0)")
    else:
        print("\t\tSample does not look Gaussian (reject H0)")
    print("\t3. Anderson-Darling test")
    result = anderson(res)
    print("\t\tStatistic: %.3f" % result.statistic)
    p = 0
    for i in range(len(result.critical_values)):
        sl, cv = result.significance_level[i], result.critical_values[i]
        if result.statistic < result.critical_values[i]:
            print("\t\t%.3f: %.3f, data looks normal (fail to reject H0)" % (sl, cv))
        else:
            print("\t\t%.3f: %.3f, data does not look normal (reject H0)" % (sl, cv))
    print()

    print("Testing homoscedasticity of residuals")
    print("\t1. Breusch-Pagan test")
    bp_test = pd.DataFrame(
        sms.het_breuschpagan(res, lr.model.exog),
        columns=["value"],
        index=["Lagrange multiplier statistic", "p-value", "f-value", "f p-value"],
    )
    print(bp_test)
    print("\t2. Goldfeld-Quandt test")
    gq_test = pd.DataFrame(
        sms.het_goldfeldquandt(res, lr.model.exog)[:-1],
        columns=["value"],
        index=["F statistic", "p-value"],
    )
    print(gq_test)
    print("\t3. White test")
    white_test = pd.DataFrame(
        het_white(res, lr.model.exog),
        columns=["value"],
        index=[
            "Test Statistic",
            "Test Statistic p-value",
            "F-Statistic",
            "F-Test p-value",
        ],
    )
    print(white_test)
