from automize_science.computing_statistics import *
from automize_science.data_cleanup import *
from automize_science.graph_constructor import *
from automize_science.saving import *


def workflow(file_path, data_sheet, mice_sheet, output_path, control_name, experimental_name, palette="Set2"):
    """
    Automatically processes lipidomics data.

    :param file_path: Path of the Excel file containing the data.
    :param data_sheet: Name of the sheet containing the data.
    :param mice_sheet: Name of the sheet containing the information about the subjects.
    :param output_path: Path of where to save the outputs.
    :param control_name: Name of the control subject group.
    :param experimental_name: Name of the experimental subject group.
    :param palette: Color of the graphs.
    """

    df, df_mice = load_data(datapath=file_path, sheet_name=data_sheet, mice_sheet=mice_sheet)
    df_clean = data_cleanup(df=df, df_mice=df_mice, output_path=output_path)
    statistics = statistics_tests(df_clean=df_clean, control_name=control_name)

    df_final = z_scores(df_clean=df_clean, statistics=statistics)
    save_values(df_final=df_final, output_path=output_path)
    save_zscores(df_final=df_final, output_path=output_path)
    wb = load_workbook(output_path + "/output/Output file.xlsx")
    wb.create_sheet(title="Comments")
    wb.save(output_path + "/output/Output file.xlsx")
    zscore_graph_lipid(df_final, control_name, experimental_name, output_path=output_path, palette=palette)
    zscore_graph_lipid_class(df_final, control_name, experimental_name, output_path=output_path, palette=palette)
