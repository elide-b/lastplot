import pandas as pd
import scipy.stats as stats

from lastplot.saving import save_sheet


def get_pvalue(stat, control_values, experimental_values):
    if stat == "Mann Whitney":
        statistics, pvalue = stats.mannwhitneyu(control_values, experimental_values)
    elif stat == "Welch T-Test":
        statistics, pvalue = stats.ttest_ind(
            control_values, experimental_values, equal_var=False
        )
    else:
        statistics, pvalue = stats.ttest_ind(control_values, experimental_values)

    return pvalue


def get_test(shapiro, levene):
    if shapiro < 0.05 and levene < 0.05:
        test = "T-Test"
    elif shapiro < 0.05 and levene > 0.05:
        test = "Welch T-Test"
    else:
        test = "Mann Whitney"

    return test


def get_stat(test):
    if any(value == "Mann Whitney" for value in test):
        stat = "Mann Whitney"
    elif any(value == "Welch T-Test" for value in test):
        stat = "Welch T-Test"
    else:
        stat = "T-Test"

    return stat


def pvalue_to_asterisks(pvalue):
    if pvalue <= 0.0001:
        return "****"
    elif pvalue <= 0.001:
        return "***"
    elif pvalue <= 0.01:
        return "**"
    elif pvalue <= 0.05:
        return "*"
    return "ns"


def statistics_tests(df_clean, control_name, experimental_name):
    """
    Performs statistical tests on cleaned lipid data to check for normality and equality of variances.

    This function performs the Shapiro-Wilk test for normality of residuals and Levene's test for equality
    of variances between control and experimental groups for each combination of region and lipid.
    """

    regions = []
    lipids = []
    shapiro_normality = []
    levene_equality = []

    print(
        "Checking for the normality of the residuals and the equality of the variances"
    )

    # Test for the normality of the residuals and for the equality of variances
    for (region, lipid), data in df_clean.groupby(["Regions", "Lipids"]):
        control_group = data[data["Genotype"] == control_name]
        genotype_names = df_clean.groupby(["Genotype"])["Log10 Values"].apply(list)
        values = data["Log10 Values"]
        shapiro_test = stats.shapiro(values)
        control_data = control_group["Log10 Values"]
        for genotype in experimental_name:
            if genotype != control_name:
                levene = stats.levene(control_data, genotype_names[genotype])
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


def z_scores(df_clean, statistics):
    """
    Computes Z scores and average Z scores per lipid class, merging them into the final DataFrame.

    Steps:
    1. Groups the cleaned DataFrame by regions and lipids to calculate mean and standard deviation of log10 log_values.
    2. Computes the Z scores for each lipid based on the mean and standard deviation.
    3. Calculates average Z scores per lipid class, region, and mouse ID.
    """
    print("Computing the Z scores and the average Z scores per lipid class")

    # Z Scores and average Z Scores per lipid class
    grouped = (
        df_clean.groupby(["Regions", "Lipids"])["Log10 Values"]
        .agg(["mean", "std"])
        .reset_index()
    )
    grouped.rename(columns={"mean": "Mean", "std": "STD"}, inplace=True)
    df_final = pd.merge(df_clean, grouped, on=["Regions", "Lipids"], how="left")
    df_final["Z_Scores"] = (df_final["Log10 Values"] - df_final["Mean"]) / df_final[
        "STD"
    ]

    average_z_scores = (
        df_final.groupby(["Regions", "Lipid Class", "Mouse ID"])["Z_Scores"]
        .mean()
        .reset_index(name="Average Z_Scores")
    )
    df_final = pd.merge(
        df_final, average_z_scores, on=["Lipid Class", "Regions", "Mouse ID"]
    )
    df_final = pd.merge(df_final, statistics, on=["Regions", "Lipids"], how="left")

    average_log_values = (
        df_final.groupby(["Regions", "Lipid Class", "Mouse ID"])["Log10 Values"]
        .mean()
        .reset_index(name="Average Log10 Values")
    )
    df_final = pd.merge(
        df_final, average_log_values, on=["Lipid Class", "Regions", "Mouse ID"]
    )

    return df_final


def lipid_selection(df_final, invalid_df, control_name, output_path):
    """
    Analyzes and filters lipids with missing log_values in some regions based on their statistical impact
    on the Z score of the lipid class across different regions. Removes lipids
    that do not change the interpretation of results.

    The function performs the following steps:
    1. Identifies the lipids with missing log_values in some regions.
    2. Groups data by lipid class and calculates average Z scores.
    3. Computes p-log_values of average Z scores with and without specific lipids using appropriate statistical tests.
    4. Compares the impact of removing each lipid and filters out lipids that do not change the interpretation in all regions.

    The Shapiro-Wilk and Levene tests are used for normality and variance equality assessments.
    """

    unique_lipids = df_final["Lipids"].unique()
    unique_invalid = invalid_df["Lipids"].unique()
    common_values = set(unique_lipids).intersection(set(unique_invalid))
    common_values.add("DPA (n-6)")
    common_values.add("DPA (n-3)")
    genotype_names = list(df_final["Genotype"].unique())
    genotype_data = df_final.groupby(["Genotype"])["Average Z_Scores"].apply(list)
    pvalue_without = []
    pvalue_with = []
    regions_without = []
    lipids_without = []
    regions_with = []
    lipids_with = []
    print(
        "Removing a lipid from all regions based on whether or not it would give the same interpretation."
    )

    # Calculating the pvalues of Average Z Scores without the lipids
    for lipid in common_values:
        df = df_final[df_final["Lipids"] != lipid]
        for region, data in df.groupby(["Regions"]):
            shapiro_without = stats.shapiro(data["Average Z_Scores"])
            control_group = data[data["Genotype"] == control_name]
            control_data = control_group["Average Z_Scores"]
            for genotype in genotype_names:
                if genotype != control_name:
                    levene_without = stats.levene(control_data, genotype_data[genotype])
                    test = get_test(shapiro_without.pvalue, levene_without.pvalue)
                    pvalue = get_pvalue(test, control_data, genotype_data[genotype])
                    pwithout = pvalue_to_asterisks(pvalue)
                    pvalue_without.append(pwithout)
                    regions_without.append(region)
                    lipids_without.append(lipid)

    # Calculating the pvalues of Average Z Scores with the lipids
    for lipid in common_values:
        for region, data in df_final.groupby(["Regions"]):
            shapiro_with = stats.shapiro(data["Average Z_Scores"])
            control_group = data[data["Genotype"] == control_name]
            control_data = control_group["Average Z_Scores"]
            for genotype in genotype_names:
                if genotype != control_name:
                    levene_with = stats.levene(control_data, genotype_data[genotype])
                    test = get_test(shapiro_with.pvalue, levene_with.pvalue)
                    pvalue = get_pvalue(test, control_data, genotype_data[genotype])
                    pwith = pvalue_to_asterisks(pvalue)
                    pvalue_with.append(pwith)
                    regions_with.append(region)
                    lipids_with.append(lipid)

    # Removing a lipid from all regions based on whether or not it would give the same interpretation
    df_without = pd.DataFrame(
        {
            "Regions": regions_without,
            "Lipids": lipids_without,
            "Pvalue Without": pvalue_without,
        }
    )

    df_with = pd.DataFrame(
        {"Regions": regions_with, "Lipids": lipids_with, "Pvalue With": pvalue_with}
    )

    df_compare = pd.merge(df_with, df_without, on=["Lipids", "Regions"])

    for lipid in df_compare:
        if any(df_compare["Pvalue With"] != df_compare["Pvalue Without"]):
            pass
        else:
            df_final = df_final[df_final["Lipids"] != lipid]
            comment = [
                f"{lipid} removed from all regions since it would give the same interpretation"
            ]
            save_sheet(comment, sheet_name="Removed Lipids", output_path=output_path)

    return df_final, df_compare
