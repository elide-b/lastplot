import lastplot

df = lastplot.data_workflow(
    file_path="My project.xlsx",
    data_sheet="Data Sheet",
    mice_sheet="Mice Sheet",
    output_path="C:/Users/[YOUR-USERNAME]/Documents/example",
    control_name="WT",
)

lastplot.log_values_graph_lipid_class(
    df,
    control_name="WT",
    experimental_name="BT",
    output_path="C:/Users/[YOUR-USERNAME]/Documents/example",
    palette="Set1",
)