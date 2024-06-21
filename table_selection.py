import pandas as pd

file = 'Dementia_project.xlsx'
sheet = 'Quantification'
#mice id

# TODO: eliminate lines not needed; log and check if it's normally distributed with a test not too strict;
#  using mean of group for missing data; z-score of each + per class

df = pd.read_excel(file, sheet_name=sheet, header=2)

# Eliminating the 'Internal Standard' samples
df = df[df['Lipid Class'] != 'Internal Standard']

# TODO: eliminate lines where samples have <3 values

df_mice = pd.read_excel(file, sheet_name='Sheet1', header=None).T


index = df.columns.tolist()
subjects = []
lipids = []
values = []
regions = []
genotype = []

for i, lipid in enumerate(df['Short Name']):
    for j, subject in enumerate(df.columns[4:]):
        if j != 0:
            y = index.index(j)
            subjects.append(subject)
            lipids.append(lipid)
            values.append(df.iloc[i, y])
            regions.append(df_mice.iloc[1, j])
            genotype.append(df_mice.iloc[0, j])
        else:
            pass

cleaned_values = [float(value) for value in values]

df_sorted = pd.DataFrame({'Mouse ID': subjects, 'Lipids': lipids, 'Regions': regions, 'Genotype': genotype, 'Values': cleaned_values})

df_output = df_sorted[df_sorted['Values'] != 'Internal Standard']

# TODO: eliminate lipids in which by region the values are <3, put a more descriptive like not_enough_means=True column in second sheet;
#  force all outputs that are excluded=True to nan;
#  log values and test for normalization (->otherwise alternatives)


df_sorted.to_excel('output.xlsx')

# Starting on the mean and std
# group_mice = df_mice.groupby(['region', 'genotype'])
# print(group_mice.first())