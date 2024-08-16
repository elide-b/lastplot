import os

import numpy as np
import pandas as pd

from lastplot.saving import write_excel


def replace_zero_values(row, data):
    if row["Values"] == 0:
        group_df = data[
            (data["Lipids"] == row["Lipids"])
            & (data["Regions"] == row["Regions"])
            & (data["Genotype"] == row["Genotype"])
            & (data["Values"] != 0)
        ]
        if not group_df.empty:
            min_value = group_df["Values"].min()
            if min_value != 0:
                new_value = 0.8 * min_value
                return new_value
    return row["Values"]


def eighty_percent(df_sorted, output_path, output_file):
    print(
        "Replacing the zero values with 80% of the minimum value for the corresponding group"
    )

    # Replace zero values with 80% of the minimum value for the corresponding group
    df_sorted["Values"] = df_sorted.apply(
        lambda row: replace_zero_values(row, df_sorted), axis=1
    )
    df_sorted["Log10 Values"] = np.log10(df_sorted["Values"])

    df_save = df_sorted.pivot_table(
        index=["Regions", "Mouse ID", "Genotype"],
        columns=["Lipids", "Lipid Class"],
        values=["Values", "Log10 Values"],
    )
    df_save.reset_index(inplace=True)

    with write_excel(output_path + "/output/" + output_file + ".xlsx") as writer:
        df_save.to_excel(writer, sheet_name="Values and Transformed Values")
        print("Saving data to new Excel file")

    return df_sorted


def remove_zeros(df_sorted, output_path, output_file):
    # Removing samples with value equal to 0
    print("Removing samples with value equal to 0")

    df_no_zeros = df_sorted.replace(0, pd.NA).dropna()
    df_no_zeros["Log10 Values"] = df_no_zeros["Values"].apply(
        lambda x: np.log10(x) if x != 0 else 0
    )

    df_save = df_no_zeros.pivot_table(
        index=["Regions", "Mouse ID", "Genotype"],
        columns=["Lipids", "Lipid Class"],
        values=["Values", "Log10 Values"],
    )
    df_save.reset_index(inplace=True)

    with write_excel(output_path + "/output/" + output_file + ".xlsx") as writer:
        df_save.to_excel(writer, sheet_name="Values and Transformed Values")
        print("Saving data to new Excel file")

    return df_no_zeros


def keep_zeros(df_sorted, output_path, output_file):
    # Keeping all the missing values = 0
    print("Keeping all the missing values = 0")

    df_sorted["Log10 Values"] = df_sorted["Values"].apply(
        lambda x: np.log10(x) if x != 0 else 0
    )

    df_save = df_sorted.pivot_table(
        index=["Regions", "Mouse ID", "Genotype"],
        columns=["Lipids", "Lipid Class"],
        values=["Values", "Log10 Values"],
    )
    df_save.reset_index(inplace=True)

    with write_excel(output_path + "/output/" + output_file + ".xlsx") as writer:
        df_save.to_excel(writer, sheet_name="Values and Transformed Values")
        print("Saving data to new Excel file")

    return df_sorted


def load_data(datapath, sheet_name, mice_sheet):
    print("Loading data from " + datapath)
    # Getting the values for the lipids
    df = pd.read_excel(datapath, sheet_name=sheet_name, header=2)
    df.dropna(axis=1, how="all", inplace=True)

    # Getting the genotypes and regions of the mice samples
    df_mice = pd.read_excel(datapath, sheet_name=mice_sheet, header=None).T
    return df, df_mice


def data_cleanup(df, df_mice, mode, output_path, output_file):
    """
    Cleans and processes lipid data from the provided DataFrame.

    This function performs several steps to clean and process lipid data:
    1. Removes 'Internal Standard' samples.
    2. Transforms and reshapes the data to long format.
    3. Filters out lipids with 3 or more missing values per region.
    4. Replaces zero values with 80% of the minimum value for the corresponding group.
    5. Logs and normalizes the cleaned values.
    6. Saves the cleaned and eliminated lipid data to an Excel file.

    """

    print("Cleaning data")
    if not os.path.exists(output_path + "/output"):
        os.makedirs(output_path + "/output")

    # Eliminating the 'Internal Standard' samples
    print("Removing the Internal Standard samples")
    df = df[df["Lipid Class"] != "Internal Standard"]

    index = df.columns.tolist()
    subjects = []
    lipids = []
    values = []
    regions = []
    genotype = []
    lipid_class = []

    for i, lipid in enumerate(df["Short Name"]):
        for j, subject in enumerate(df.columns[4:]):
            if j != 0:
                y = index.index(j)
                subjects.append(subject)
                lipids.append(lipid)
                lipid_class.append(df.iloc[i, 3])
                values.append(df.iloc[i, y])
                regions.append(df_mice.iloc[1, j])
                genotype.append(df_mice.iloc[0, j])
            else:
                pass

    cleaned_values = [float(value) for value in values]
    lipids = [string.replace("/", "-") for string in lipids]

    df_sorted = pd.DataFrame(
        {
            "Mouse ID": subjects,
            "Lipids": lipids,
            "Lipid Class": lipid_class,
            "Regions": regions,
            "Genotype": genotype,
            "Values": cleaned_values,
        }
    )

    # Adding short lipid names
    short_names = {
        "Prostaglandin": "Prostaglandins",
        "N-Acyl-Ethanolamine": "NAEs",
        "N-Acyl-Ethanolamine (NAE)": "NAEs",
        "Monoacyl-glycerol": "MAGs",
        "onoacyl-glycerol (MAG)": "MAGs",
        "Fatty acid": "FAs",
        "MAG derived Oxylipin": "MAG-derived Oxylipins",
        "NAE-derived Oxylipin": "NAE-derived Oxylipins",
        "Fatty acid derived Oxylipin": "FA-derived Oxylipins",
        "Fatty acid-derived Oxylipin": "FA-derived Oxylipins",
        "Fatty acid derived Oxylipins": "FA-derived Oxylipins",
        "Specialized pro-resolving mediator": "SPMs",
        "Specialized pro-resolving mediator (SPM)": "SPMs",
        "Leukotriene": "Leukotrienes",
    }

    df_sorted["Class Short Name"] = df_sorted["Lipid Class"].apply(
        lambda name: short_names.get(name, name)
    )

    if mode == "80percent":
        df_clean = eighty_percent(df_sorted, output_path, output_file)
    elif mode == "keep0":
        df_clean = keep_zeros(df_sorted, output_path, output_file)
    elif mode == "remove0":
        df_clean = remove_zeros(df_sorted, output_path, output_file)

    return df_clean
