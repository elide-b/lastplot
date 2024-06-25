import numpy as np
import pandas as pd
import scipy


def robot_layer(df_filtered, df_eliminated, control_name, output_path):
    # Normalization test of the data
    log_values = np.log10(df_filtered['Values'])
    k2, p = scipy.stats.normaltest(log_values)
    alpha = 0.05
    # TODO: check normalization and put comment on the type of normalization done
    '''if p < alpha:
        transformed_data = preprocessing.normalize(np.array(df_filtered['Values']))
        k2, p = scipy.stats.normaltest(transformed_data)
        df_filtered['Normalized Values'] = transformed_data
    else:
        norm_data = log_values
        df_filtered['Normalized Values'] = log_values'''
    df_filtered['Normalized Values'] = np.log10(df_filtered['Values'])  # TODO: Remove after fixing

    # Z Scores and average Z Scores per lipid class
    wt_stats = df_filtered[df_filtered['Genotype'] == control_name].groupby(['Regions', 'Lipids'])[
        'Normalized Values'].agg(['mean', 'std']).reset_index()
    wt_stats.rename(columns={'mean': 'Control Mean', 'std': 'Control STD'}, inplace=True)
    df_merged = pd.merge(df_filtered, wt_stats, on=['Regions', 'Lipids'])
    df_merged['Z Score'] = (df_merged['Normalized Values'] - df_merged['Control Mean']) / df_merged['Control STD']

    # TODO: ask about her z-score calculations
    average_z_scores = df_merged.groupby(['Mouse ID', 'Lipid Class'])['Z Score'].mean().reset_index(name='Average Z')
    df_merged = pd.merge(df_merged, average_z_scores, on=['Lipid Class', 'Mouse ID'])

    # Save the eliminated lipids and the normalized data with the Z Scores
    with pd.ExcelWriter('Output.xlsx') as writer:
        df_eliminated.to_excel(writer, sheet_name='Eliminated Lipids')
        df_merged.to_excel(writer, sheet_name='Data for Correlations')

#
#     # TODO: graphs
