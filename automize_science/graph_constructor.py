import seaborn as sns
from matplotlib import pyplot as plt
from statannotations.Annotator import Annotator

# TODO: graphs for single lipids, graphs for lipid class, one graph for all of them. BY GENOTYPE, BY REGION


def get_test(shapiro, levene):
    if shapiro < 0.05 and levene < 0.05:
        test = "t-test_ind"
    elif shapiro < 0.05 and levene > 0.05:
        test = "t-test_welch"
    elif shapiro > 0.05 and levene > 0.05:
        test = "Mann-Whitney"
    else:
        test = None

    return test


def zscore_graph_lipid(df_final, control_name, experimental_name, output_path):
    for (region, lipid), data in df_final.groupby(["Regions", "Lipids"]):
        shapiro = data.iloc[0]["Shapiro Normality"]
        print(shapiro)
        levene = data.iloc[0]["Levene Equality"]

        print(f"Creating graph for {lipid} in {region}")

        order = [control_name, experimental_name]

        ax = sns.boxplot(x="Genotype", y="Z Scores", data=data, order=order, hue="Genotype", palette="Set1")
        ax = sns.stripplot(x="Genotype", y="Z Scores", data=data, order=order, color="k", size=4)

        test = get_test(shapiro, levene)
        annotator = Annotator(
            ax, pairs=[(control_name, experimental_name)], data=data, x="Genotype", y="Z Scores", order=order
        )
        annotator.configure(test=test, text_format="star", loc="outside")
        annotator.apply_and_annotate()
        plt.xlabel("Genotype")
        plt.ylabel("Z Scores")
        plt.title(f"Z Scores Distribution for {lipid} in {region}: {control_name} vs {experimental_name}")
        plt.grid(True)
        plt.tight_layout()
        plt.show()
        # plt.savefig(output_path + "/output/graphs/" + f"Z Scores for {lipid} in {region}.png", dpi=1200)
        plt.close()


def zscore_graph_regions(df_merged, control_name, experimental_name, output_path):
    order = [control_name, experimental_name]
    for lipid in df_merged["Lipid Class"].unique():
        specific_lipid_data = df_merged[df_merged["Lipid Class"] == lipid]
        ax = sns.boxplot(x="Lipids", y="Z Scores", hue="Regions", data=specific_lipid_data, order=order, dodge=True)
        sns.swarmplot(
            x="Lipids",
            y="Z Scores",
            hue="Regions",
            data=specific_lipid_data,
            order=order,
            color="none",
            marker="o",
            edgecolor="k",
            size=6,
            linewidth=0.5,
            dodge=True,
        )

    plt.xlabel("Regions")
    plt.ylabel("Z Score")
    plt.title(f"Z Scores Distribution by Region: {control_name} vs {experimental_name}")
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(output_path + "/output/graphs/Z Scores Distribution of Lipid Classes by Region.png", dpi=1200)
    plt.show()
