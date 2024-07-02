from utils.data_cleanup import *
from utils.graph_constructor import *
from utils.statistics import *

# Give example of how to use this


""" Give the location of the file and the name of the datasheet and mouse ID of interest.
    Finally give the location of the output file """
file_path = "Dementia project.xlsx"
data_sheet = "Quantification"
mice_sheet = "Sheet1"
output_path = "C:/Users/Elide/Documents/git/automize-science/example"
control_name = "WT"
experimental_name = "FTLD"
color = sns.color_palette("Set2")

df, df_mice = load_data(file_path, data_sheet, mice_sheet)
df_clean = data_cleanup(df, df_mice, output_path=output_path)
statistics = statistics_tests(df_clean, control_name=control_name)
df_final = z_scores(df_clean, output_path)
exit()
zscore_graph_lipid(df_final, control_name, experimental_name, output_path=output_path)
zscore_graph_regions(df_final, control_name, experimental_name, output_path=output_path)

# All lipids graphs
sns.boxplot(x="Lipids", y="Z Scores", hue="Lipids", data=df_final, palette="Paired")

plt.xlabel("Lipids")
plt.ylabel("Z Score")
plt.title("Z Scores Distribution by Lipids: Control vs Experimental")

plt.grid(True)
plt.tight_layout()
