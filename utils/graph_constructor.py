import scipy
import seaborn as sns
import statannot
from matplotlib import pyplot as plt


def zscore_graph_lipid(df_merged, control_name, experimental_name, output_path):
    order = [control_name, experimental_name]
    for lipid in df_merged['Lipids'].unique():
        specific_lipid_data = df_merged[df_merged['Lipids'] == lipid]
        for region in specific_lipid_data['Regions'].unique():
            specific_region_data = specific_lipid_data[specific_lipid_data['Regions'] == region]
            sns.boxplot(x='Genotype', y='Z Scores', data=specific_region_data, order=order)
            sns.swarmplot(x='Genotype', y='Z Scores', data=specific_region_data, order=order, color='none', marker='o',
                          edgecolor='k', size=6, linewidth=.5)

            plt.xlabel('Genotype')
            plt.ylabel('Z Scores')
            plt.title(f'Z Scores Distribution for {lipid} in {region}: {control_name} vs {experimental_name}')
            plt.grid(True)
            plt.tight_layout()
            plt.savefig(output_path + '/output/graphs/' + f'Z Scores {lipid} in {region}.png', dpi=1200)


def zscore_graph_regions(df_merged, control_name, experimental_name, output_path):
    order = [control_name, experimental_name]
    for lipid in df_merged['Lipid Class'].unique():
        specific_lipid_data = df_merged[df_merged['Lipid Class'] == lipid]
        ax = sns.boxplot(x='Lipids', y='Z Scores', hue='Regions', data=specific_lipid_data, order=order,
                         dodge=True)
        sns.swarmplot(x='Lipids', y='Z Scores', hue='Regions', data=specific_lipid_data, order=order, color='none',
                      marker='o', edgecolor='k', size=6, linewidth=0.5, dodge=True)

    plt.xlabel('Regions')
    plt.ylabel('Z Score')
    plt.title(f'Z Scores Distribution by Region: {control_name} vs {experimental_name}')
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(output_path + '/output/graphs/Z Scores Distribution of Lipid Classes by Region.png', dpi=1200)
    plt.show()
