from automize_science.script import *

file_path = "Dementia project.xlsx"
data_sheet = "Quantification"
mice_sheet = "Sheet1"
output_path = "C:/Users/Elide/Documents/git/automize-science/example"
control_name = "WT"
experimental_name = "FTLD"
palette = "Set2"


workflow(file_path, data_sheet, mice_sheet, output_path, control_name, experimental_name, palette)
