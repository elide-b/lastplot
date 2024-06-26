import seaborn as sns
from statannot import add_stat_annotation
from matplotlib import pyplot as plt


def zscore_graph_lipid(df_merged, control_name, experimental_name, color):
    for lipid in df_merged['Lipids']:
        specific_lipid_data = df_merged[df_merged['Lipids'] == lipid]
        order = [control_name, experimental_name]
        ax = sns.boxplot(x='Genotype', y='Z Scores', data=specific_lipid_data, order=order, palette=color)
        plt.xlabel('Genotype')
        plt.ylabel('Z Score')
        plt.title(f'Z Scores Distribution for {lipid}: {control_name} vs {experimental_name}')
        add_stat_annotation(ax, x='Genotype', y='Z Scores', data=specific_lipid_data, order=order,
                            box_pairs=[(control_name, experimental_name)],
                            test='Mann-Whitney', text_format='star', loc='outside', verbose=2)
        plt.grid(True)
        plt.tight_layout()
        plt.savefig(f'Z Scores for {lipid}.png')
        plt.show()


def zscore_graph_regions(df_merged, control_name, experimental_name, color):
    sns.boxplot(x='Regions', y='Z Scores', hue='Lipid', data=df_merged, palette=color)
    plt.xlabel('Regions')
    plt.ylabel('Z Score')
    plt.title(f'Z Scores Distribution by Region: {control_name} vs {experimental_name}')
    plt.grid(True)
    plt.tight_layout()
    plt.savefig('Z Scores Distribution by Region.png')
    plt.show()