import pandas as pd
import scipy.stats as stats


# TODO: write all of this info into smt


def statistics_tests(df_clean, control_name):

    regions = []
    lipids = []
    shapiro_normality = []
    levene_equality = []

    print("Checking for the normality of the residuals and the equality of the variances")

    # Test for the normality of the residuals and for the equality of variances
    for (region, lipid), data in df_clean.groupby(["Regions", "Lipids"]):
        control_group = data[data["Genotype"] == control_name]
        experimental_group = data[data["Genotype"] != control_name]
        values = data["Normalized Values"]
        shapiro_test = stats.shapiro(values)
        control_data = control_group["Normalized Values"]
        experimental_data = experimental_group["Normalized Values"]
        levene = stats.levene(control_data, experimental_data)

        shapiro_normality.append(shapiro_test.pvalue)
        levene_equality.append(levene.pvalue)
        regions.append(region)
        lipids.append(lipid)

    # Creating a new dataframe with the normality and equality information
    statistics = pd.DataFrame(
        {
            "Regions": regions,
            "Lipids": lipids,
            "Shapiro Normality": shapiro_normality,
            "Levene Equality": levene_equality,
        }
    )

    return statistics


def z_scores(df_clean, statistics, output_path):

    print("Computing the Z scores and the average Z scores per lipid class")

    # Z Scores and
    # TODO: fix average Z Scores per lipid class
    grouped = df_clean.groupby(["Regions", "Lipids"])["Normalized Values"].agg(["mean", "std"]).reset_index()
    grouped.rename(columns={"mean": "Mean", "std": "STD"}, inplace=True)
    df_final = pd.merge(df_clean, grouped, on=["Regions", "Lipids"], how="left")
    df_final["Z Scores"] = (df_final["Values"] - df_final["Mean"]) / df_final["STD"]
    average_z_scores = df_final.groupby(["Regions", "Lipid Class"])["Z Scores"].mean().reset_index(name="Average Z")
    df_final = pd.merge(df_final, average_z_scores, on=["Lipid Class", "Regions"])
    df_final = pd.merge(df_final, statistics, on=["Regions", "Lipids"], how="left")

    # Save the eliminated lipids and the normalized data with the Z Scores
    with pd.ExcelWriter(output_path + "/output/Output file.xlsx") as writer:
        df_final.to_excel(writer, sheet_name="Data for Correlations")
    print("Saving to output file")

    return df_final
