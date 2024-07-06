import os

import matplotlib.pyplot as plt
import scipy.stats as stats
import seaborn as sns
import starbars
from openpyxl import load_workbook


def get_test(shapiro, levene, control_values, experimental_values):
    if shapiro < 0.05 and levene < 0.05:
        stat, pvalue = stats.ttest_ind(control_values, experimental_values)
        test = "T-Test"
    elif shapiro < 0.05 and levene > 0.05:
        stat, pvalue = stats.ttest_ind(control_values, experimental_values, equal_var=False)
        test = "Welch T-Test"
    elif shapiro > 0.05 and levene > 0.05:
        stat, pvalue = stats.mannwhitneyu(control_values, experimental_values)
        test = "Mann Whitney"
    else:
        pvalue = 0
        test = "no test"

    return pvalue, test


# Graphs by Z scores
def zscore_graph_lipid(df_final, control_name, experimental_name, output_path, palette):
    if not os.path.exists(output_path + "/output/zscore_graphs/lipid"):
        os.makedirs(output_path + "/output/zscore_graphs/lipid")
    order = [control_name, experimental_name]
    for (region, lipid), data in df_final.groupby(["Regions", "Lipids"]):
        shapiro = data.iloc[0]["Shapiro Normality"]
        levene = data.iloc[0]["Levene Equality"]
        control_group = data[data["Genotype"] == control_name]
        experimental_group = data[data["Genotype"] != control_name]
        control_values = control_group["Z Scores"]
        experimental_values = experimental_group["Z Scores"]

        print(f"Creating graph for {lipid} in {region}")

        sns.boxplot(x="Genotype", y="Z Scores", data=data, order=order, hue="Genotype", palette=palette)
        sns.stripplot(x="Genotype", y="Z Scores", data=data, order=order, color="k", size=4)

        pvalue, test = get_test(shapiro, levene, control_values, experimental_values)
        pairs = [(control_name, experimental_name, pvalue)]
        plt.xlabel("Genotype")
        plt.ylabel("Z Scores")
        plt.title(f"Z Scores Distribution for {lipid} in {region}: {control_name} vs {experimental_name}")
        starbars.draw_annotation(pairs)
        plt.savefig(output_path + "/output/graphs/" + f"Z Scores for {lipid} in {region}.png", dpi=1200)
        plt.close()

        wb = load_workbook(output_path + "/output/Output file.xlsx")
        ws = wb["Comments"]

        # Append a row of strings
        comment = [f"For {lipid} in {region}, {test} was performed. P-value is {pvalue}."]
        ws.append(comment)
        wb.save(output_path + "/output/Output file.xlsx")


def zscore_graph_lipid_class(df_final, control_name, experimental_name, output_path, palette):
    if not os.path.exists(output_path + "/output/zscore_graphs/lipid_class"):
        os.makedirs(output_path + "/output/zscore_graphs/lipid_class")
    order = [control_name, experimental_name]
    for (region, lipid), data in df_final.groupby(["Regions", "Lipid Class"]):
        shapiro = data.iloc[0]["Shapiro Normality"]
        levene = data.iloc[0]["Levene Equality"]
        control_group = data[data["Genotype"] == control_name]
        experimental_group = data[data["Genotype"] != control_name]
        control_values = control_group["Z Scores"]
        experimental_values = experimental_group["Z Scores"]

        print(f"Creating graph for {lipid} in {region}")
        sns.boxplot(x="Genotype", y="Average Z Scores", hue="Genotype", data=data, order=order, palette=palette)
        sns.stripplot(x="Genotype", y="Average Z Scores", data=data, order=order, color="k", size=4)

        pvalue = get_test(shapiro, levene, control_values, experimental_values)
        pairs = [(control_name, experimental_name, pvalue)]
        plt.xlabel("Genotype")
        plt.ylabel("Z Score")
        plt.title(f"Z Scores Distribution of {lipid} in {region}: {control_name} vs {experimental_name}")
        starbars.draw_annotation(pairs)
        plt.savefig(output_path + f"/output/graphs/Z Scores Distribution of {lipid} by {region}.png", dpi=1200)
        plt.close()


# Graphs by values
def values_graph_lipid(df_final, control_name, experimental_name, output_path, palette):
    if not os.path.exists(output_path + "/output/value_graphs/lipid"):
        os.makedirs(output_path + "/output/value_graphs/lipid")
    order = [control_name, experimental_name]
    for (region, lipid), data in df_final.groupby(["Regions", "Lipids"]):
        shapiro = data.iloc[0]["Shapiro Normality"]
        levene = data.iloc[0]["Levene Equality"]
        control_group = data[data["Genotype"] == control_name]
        experimental_group = data[data["Genotype"] != control_name]
        control_values = control_group["Normalized Values"]
        experimental_values = experimental_group["Normalized Values"]

        print(f"Creating graph for {lipid} in {region}")

        sns.boxplot(x="Genotype", y="Normalized Values", data=data, order=order, hue="Genotype", palette=palette)
        sns.stripplot(x="Genotype", y="Normalized Values", data=data, order=order, color="k", size=4)

        pvalue = get_test(shapiro, levene, control_values, experimental_values)
        pairs = [(control_name, experimental_name, pvalue)]
        plt.xlabel("Genotype")
        plt.ylabel("Normalized Values")
        plt.title(f"Normalized Values Distribution for {lipid} in {region}: {control_name} vs {experimental_name}")
        starbars.draw_annotation(pairs)
        plt.savefig(output_path + "/output/graphs/" + f"Normalized Values for {lipid} in {region}.png", dpi=1200)
        plt.close()


def values_graph_lipid_class(df_final, control_name, experimental_name, output_path, palette):
    if not os.path.exists(output_path + "/output/value_graphs/lipid_class"):
        os.makedirs(output_path + "/output/value_graphs/lipid_class")
    order = [control_name, experimental_name]
    for (region, lipid), data in df_final.groupby(["Regions", "Lipid Class"]):
        shapiro = data.iloc[0]["Shapiro Normality"]
        levene = data.iloc[0]["Levene Equality"]
        control_group = data[data["Genotype"] == control_name]
        experimental_group = data[data["Genotype"] != control_name]
        control_values = control_group["Normalized Values"]
        experimental_values = experimental_group["Normalized Values"]

        print(f"Creating graph for {lipid} in {region}")
        sns.boxplot(x="Genotype", y="Normalized Values", hue="Genotype", data=data, order=order, palette=palette)
        sns.stripplot(x="Genotype", y="Normalized Values", data=data, order=order, color="k", size=4)

        pvalue = get_test(shapiro, levene, control_values, experimental_values)
        pairs = [(control_name, experimental_name, pvalue)]
        plt.xlabel("Genotype")
        plt.ylabel("Normalized Values")
        plt.title(f"Normalized Values Distribution of {lipid} in {region}: {control_name} vs {experimental_name}")
        starbars.draw_annotation(pairs)
        plt.savefig(output_path + f"/output/graphs/Normalized Values Distribution of {lipid} by {region}.png", dpi=1200)
        plt.close()
