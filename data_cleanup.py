import pandas as pd

file = 'Dementia_project.xlsx'
sheet = 'Quantification'


# TODO: check if input file is always the same

def load_data(datapath, sheet_name, micesheet):
    # Getting the values for the lipids
    df = pd.read_excel(datapath, sheet_name=sheet_name, header=2)
    df.dropna(axis=1, how='all', inplace=True)

    # Getting the genotypes and regions of the mice samples
    df_mice = pd.read_excel(datapath, sheet_name=micesheet, header=None).T
    return df, df_mice


def data_cleanup(df, df_mice):
    # Eliminating the 'Internal Standard' samples
    df = df[df['Lipid Class'] != 'Internal Standard']

    index = df.columns.tolist()
    subjects = []
    lipids = []
    values = []
    regions = []
    genotype = []
    lipid_class = []

    for i, lipid in enumerate(df['Short Name']):
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

    df_sorted = pd.DataFrame({'Mouse ID': subjects, 'Lipids': lipids, 'Lipid Class': lipid_class, 'Regions': regions,
                              'Genotype': genotype, 'Values': cleaned_values})

    # TODO: check if <=3 values per lipid is a good criteria
    #  put a more descriptive like not_enough_means=True column in sheet.

    # Filter out rows with less than 3 non-zero values
    df_non_zero = df_sorted[df_sorted['Values'] != 0]
    grouped = df_non_zero.groupby(['Lipids', 'Regions', 'Genotype']).size().reset_index(name='counts')
    filtered_groups = grouped[grouped['counts'] > 3]
    eliminated_lipids = grouped[grouped['counts'] <= 3]
    df_filtered = df_sorted.merge(filtered_groups[['Lipids', 'Regions', 'Genotype']],
                                  on=['Lipids', 'Regions', 'Genotype'])
    df_eliminated = df_sorted.merge(eliminated_lipids[['Lipids', 'Regions', 'Genotype']],
                                    on=['Lipids', 'Regions', 'Genotype'])

    # Replace zero values with 80% of the minimum value for the corresponding group
    def replace_zero_values(row, data):
        if row['Values'] == 0:
            group_df = data[(data['Lipids'] == row['Lipids']) &
                            (data['Regions'] == row['Regions']) &
                            (data['Genotype'] == row['Genotype']) &
                            (data['Values'] != 0)]
            if not group_df.empty:
                min_value = group_df['Values'].min()
                if min_value != 0:
                    return 0.8 * min_value
        return row['Values']

    df_filtered['Values'] = df_filtered.apply(replace_zero_values, axis=1, args=(df_filtered,))

    return df_filtered, df_eliminated
