import numpy as np
import pandas as pd
import scipy.stats as stats
import statsmodels.api as sm
from sklearn.linear_model import LinearRegression

# TODO: write all of this info into smt


def robot_layer(df_clean, df_eliminated, control_name, output_path):
    df_clean['Values'] = df_clean['Values'].astype(np.float16)

    # Normalization test of the residuals
    genotype_groups = df_clean['Genotype'].unique()
    for genotype in genotype_groups:
        # Select data for this genotype
        group_data = df_clean[df_clean['Genotype_WT'] == genotype]

        # Fit a model (assuming a simple linear regression with Lipids as the predictor)
        X = group_data[['Lipids']]  # Predictor(s)
        y = group_data['Values']  # Response variable
        X = sm.add_constant(X)  # Adds a constant term to the predictor

        model = sm.OLS(y, X).fit()
        residuals = model.resid

    shapiro_test = stats.shapiro(residuals)
    print(f'Shapiro-Wilk Test for {genotype}:', shapiro_test)
    if shapiro_test.pvalue > 0.05:
        print(f'Residuals for {genotype} are normally distributed (Shapiro-Wilk).\n')
    else:
        print(f'Residuals for {genotype} are not normally distributed (Shapiro-Wilk).\n')

    # Kolmogorov-Smirnov Test
    ks_test = stats.kstest(residuals, 'norm')
    print(f'Kolmogorov-Smirnov Test for {genotype}:', ks_test)
    if ks_test.pvalue > 0.05:
        print(f'Residuals for {genotype} are normally distributed (Kolmogorov-Smirnov).\n')
    else:
        print(f'Residuals for {genotype} are not normally distributed (Kolmogorov-Smirnov).\n')

    # Anderson-Darling Test
    ad_test = stats.anderson(residuals, dist='norm')
    print(f'Anderson-Darling Test for {genotype}:', ad_test)
    critical_values = ad_test.critical_values
    significance_level = 0.05  # 5% significance level
    if ad_test.statistic < critical_values[2]:  # 3rd value corresponds to 5% level
        print(f'Residuals for {genotype} are normally distributed (Anderson-Darling).\n')
    else:
        print(f'Residuals for {genotype} are not normally distributed (Anderson-Darling).\n')


    # Test for the equality of variances
    control_group = df_clean[df_clean['Lipids'] == control_name]
    experimental_group = df_clean[df_clean['Lipids'] != control_name]
    statistic, p_value = stats.levene(control_group, experimental_group)
    print(f'Levene’s test statistic: {statistic}')
    print(f'p-value: {p_value}')

    # Z Scores and average Z Scores per lipid class
    grouped = df_clean.groupby(['Regions', 'Lipids'])['Values'].agg(['mean', 'std']).reset_index()
    grouped.rename(columns={'mean': 'Mean', 'std': 'STD'}, inplace=True)
    df_final = pd.merge(df_clean, grouped, on=['Regions', 'Lipids'], how='left')
    df_final['Z Scores'] = (df_final['Values'] - df_final['Mean']) / df_final['STD']
    average_z_scores = df_final.groupby(['Mouse ID', 'Lipid Class'])['Z Scores'].mean().reset_index(name='Average Z')
    df_final = pd.merge(df_final, average_z_scores, on=['Lipid Class', 'Mouse ID'])

    # Save the eliminated lipids and the normalized data with the Z Scores
    with pd.ExcelWriter(output_path) as writer:
        df_eliminated.to_excel(writer, sheet_name='Eliminated Lipids')
        df_final.to_excel(writer, sheet_name='Data for Correlations')


    return df_final
