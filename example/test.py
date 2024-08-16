import lastplot

df = lastplot.data_workflow(
    file_path="Dementia project.xlsx",
    data_sheet="Quantification",
    mice_sheet="Sheet1",
    output_path=".",
    output_file="Remove0",
    control_name="WT",
    experimental_name=["FTLD"],
    mode="remove0",
)

lastplot.log_values_graph_class_average(
    df,
    control_name="WT",
    experimental_name=["FTLD"],
    output_path=".",
    palette="tab20b_r",
    show=True,
    title="Scores for {lipid_class} in {region}",
    output_file="Remove0",
)
