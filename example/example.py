from automize_science.graph_constructor import *
from automize_science.workflows import *

file_path = "Dementia project.xlsx"
data_sheet = "Quantification"
mice_sheet = "Sheet1"
output_path = "C:/Users/Elide/Documents/git/automize-science/example"
control_name = "WT"
experimental_name = "FTLD"
palette = "Set2"


df = data_workflow(
    file_path="Dementia project.xlsx",
    data_sheet="Quantification",
    mice_sheet="Sheet1",
    output_path="C:/Users/Elide/Documents/git/automize-science/example",
    control_name="WT",
)

zscore_graph_lipid(
    df_final=df,
    control_name="WT",
    experimental_name="FTLD",
    output_path="C:/Users/Elide/Documents/git/automize-science/example",
    palette="Set2",
    show=True,
)


zscore_graph_lipid_class(
    df_final=df,
    control_name="WT",
    experimental_name="FTLD",
    output_path="C:/Users/Elide/Documents/git/automize-science/example",
    palette="Set2",
    show=True,
)
