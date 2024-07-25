import lastplot

df = lastplot.data_workflow(
    file_path="My project.xlsx",
    data_sheet="Data Sheet",
    mice_sheet="Mice ID Sheet",
    output_path=".",
    control_name="WT",
    experimental_name=["FTD", "BPD", "HFD"],
)

lastplot.zscore_graph_lipid(
    df,
    control_name="WT",
    experimental_name=["FTD", "BPD", "HFD"],
    output_path=".",
    palette="Set3",
    show=False,
)
