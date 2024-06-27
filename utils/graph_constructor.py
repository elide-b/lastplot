import seaborn as sns
from matplotlib import pyplot as plt
import scipy
import statannot


def zscore_graph_lipid(df_merged, control_name, experimental_name):
    order = [control_name, experimental_name]
    for lipid in df_merged['Lipids'].unique():
        specific_lipid_data = df_merged[df_merged['Lipids'] == lipid]
        for region in specific_lipid_data['Regions'].unique():
            specific_region_data = specific_lipid_data[specific_lipid_data['Regions'] == region]
            sns.boxplot(x='Genotype', y='Z Scores', data=specific_region_data, order=order)
            sns.swarmplot(x='Genotype', y='Z Scores', data=specific_region_data, order=order, color='none', marker='o',
                          edgecolor='k', size=6, linewidth=.5)

            # Add significance annotations
            control_data = specific_region_data[specific_region_data['Genotype'] == control_name]['Z Scores']
            experimental_data = specific_region_data[specific_region_data['Genotype'] == experimental_name]['Z Scores']
            t_stat, p_value = scipy.stats.ttest(control_data, experimental_data)
            if p_value < 0.05:
                significance_level = 'p < 0.05'
                y_max = specific_region_data['Z Scores'].max()
                plt.text(0.5, y_max + 0.1, significance_level, horizontalalignment='center', verticalalignment='center',
                         fontsize=10)
            plt.xlabel('Genotype')
            plt.ylabel('Z Scores')
            plt.title(f'Z Scores Distribution for {lipid} in {region}: {control_name} vs {experimental_name}')
            plt.grid(True)
            plt.tight_layout()
            plt.savefig(f'Z Scores {lipid} in {region}.png', dpi=1200)


def zscore_graph_regions(df_merged, control_name, experimental_name):
    order = [control_name, experimental_name]
    for lipid in df_merged['Lipid Class'].unique():
        specific_lipid_data = df_merged[df_merged['Lipid Class'] == lipid]
        ax = sns.boxplot(x='Lipids', y='Z Scores', hue='Regions', data=specific_lipid_data, order=order,
                         dodge=True)
        sns.swarmplot(x='Lipids', y='Z Scores', hue='Regions', data=specific_lipid_data, order=order, color='none',
                      marker='o', edgecolor='k', size=6, linewidth=0.5, dodge=True)
        statannot.add_stat_annotation(ax, data=specific_lipid_data, x='Regions', y='Z Scores', hue='Genotype',
                                      box_pairs=[((control_name, region), (experimental_name, region)) for region in specific_lipid_data['Region'].unique()],
                                      test="t-test", text_format="star", loc="outside", verbose=2)

    plt.xlabel('Regions')
    plt.ylabel('Z Score')
    plt.title(f'Z Scores Distribution by Region: {control_name} vs {experimental_name}')
    plt.grid(True)
    plt.tight_layout()
    plt.savefig('Z Scores Distribution of Lipid Classes by Region.png', dpi=1200)
    plt.show()
