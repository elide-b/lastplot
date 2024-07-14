import lastplot

file_path = "Dementia project.xlsx"
data_sheet = "Quantification"
mice_sheet = "Sheet1"
output_path = "C:/Users/Elide/Documents/git/lastplot/example"
control_name = "WT"
experimental_name = "FTLD"
palette = "Set1"


df = lastplot.data_workflow(
    file_path="Dementia project.xlsx",
    data_sheet="Quantification",
    mice_sheet="Sheet1",
    output_path="C:/Users/Elide/Documents/git/lastplot/example",
    control_name="WT",
)
