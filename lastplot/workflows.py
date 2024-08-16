from lastplot.computing_statistics import *
from lastplot.data_cleanup import *
from lastplot.saving import *


def data_workflow(
    file_path,
    data_sheet,
    mice_sheet,
    output_path,
    output_file,
    mode,
    control_name,
    experimental_name,
):
    """
    Automatically processes lipidomics data.

    :param file_path: Path of the Excel file containing the data. The path should be written with right orientation slashes ->/
    :param data_sheet: Name of the sheet containing the data.
    :param mice_sheet: Name of the sheet containing the information about the subjects.
    :param output_path: Path of where to save the outputs.
    :param output_file: Name of the desired output file.
    :param mode: "80percent" or "keep0" or "remove0"
    :param control_name: Name of the control subject group.
    :param experimental_name: Name(s) of the experimental subject group(s). Should be in the form of a list.
    """

    df, df_mice = load_data(
        datapath=file_path, sheet_name=data_sheet, mice_sheet=mice_sheet
    )
    df_clean = data_cleanup(
        df=df,
        df_mice=df_mice,
        mode=mode,
        output_path=output_path,
        output_file=output_file,
    )
    statistics = statistics_tests(
        df_clean=df_clean,
        control_name=control_name,
        experimental_name=experimental_name,
    )
    df_final = z_scores(
        df_sorted=df_clean,
        statistics=statistics,
        output_file=output_file,
        output_path=output_path,
    )

    # Alain's thing maybe not needed
    # if mode == "80percent":
    #     df_final, df_compare = lipid_selection(
    #         df_mid,
    #         invalid_df=invalid_df,
    #         control_name=control_name,
    #         output_path=output_path,
    #     )
    # else:
    #     df_final = df_mid.copy()

    save_zscores(df_final=df_final, output_path=output_path, output_file=output_file)

    return df_final
