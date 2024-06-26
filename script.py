from utils.data_cleanup import *
from utils.robot import *
from utils.graph_constructor import *


''' Give the location of the file and the name of the datasheet and mouse ID of interest.
    Finally give the location of the output file'''
file_path = 'Dementia_project.xlsx'
data_sheet = 'Quantification'
mice_sheet = 'Sheet1'
output_path = 'C:/Users/Elide/Documents/git/automize-science'
control_name = 'WT'
experimental_name = 'FTD'
color = sns.color_palette('Set2')

df, df_mice = load_data(file_path, data_sheet, mice_sheet)
df_final, df_eliminated = data_cleanup(df, df_mice)
df_merged = robot_layer(df_final, df_eliminated, control_name, output_path=output_path)
zscore_graph_lipid(df_merged, control_name, experimental_name, color)
zscore_graph_regions(df_merged, control_name, experimental_name, color)

# All lipids graphs
sns.boxplot(x='Lipids', y='Z Scores', hue='Lipids', data=df_merged, palette='Paired')

plt.xlabel('Lipids')
plt.ylabel('Z Score')
plt.title('Z Scores Distribution by Lipids: Control vs Experimental')

plt.grid(True)
plt.tight_layout()
