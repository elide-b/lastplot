import lastplot

df = lastplot.data_workflow(
    file_path="My project.xlsx",
    data_sheet="data",
    mice_sheet="mice id",
    output_path="./example",
    control_name="WT",
    experimental_name=["FTD", "BPD", "HFD"]
)

lastplot.log_values_graph_lipid_class(
    df,
    control_name="WT",
    experimental_name=["FTD", "BPD", "HFD"],
    output_path="./example",
    palette="Set1",
)
