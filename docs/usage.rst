Usage
-----

Before proceeding with the analysis of the data, make sure your data Excel file has a sheet containing the lipid concentrations, and one containing the information of the mice genotype.
For example:

.. image:: _static/data_sheet.png
    :alt: Example data Excel file
    :align: left
    :width: 629

.. image:: _static/mice_sheet.png
    :align: right
    :width: 129


After installing the package and assuring the right Excel file formatting, you can start your data analysis. Here's a simple example:

.. code-block:: python

    import lastplot

    # Example usage
    df = lastplot.data_workflow(
    file_path="My project.xlsx",
    data_sheet="Data Sheet",
    mice_sheet="Mice ID Sheet",
    output_path="C:/Users/[YOUR-USERNAME]/Documents/example",
    control_name="WT",
    experimental_name=["FTD", "BPD", "HFD"])

| In this example "My project.xlsx" is the name of the data sheet to process. In case the sheet isn't in the same folder as your script, remember to use the complete file path with the right orientation slashes (/).
| The same is true for the `output_path`. If you want the output folder to be in the same folder as the script, simply write ".".
| Always write the `experimental_name` between square brackets, even when there's only one.
| Remember that Python is a case-sensitive language and will interpret "Example" differently than "example".

.. code-block:: python

    lastplot.zscore_graph_class_average(
        df_final=df,
        control_name="WT",
        experimental_name=["FTD", "BPD", "HFD"],
        output_path="C:/Users/[YOUR-USERNAME]/Documents/example",
        palette="Set2",
        show=True)

Returns graphs.

If none of the plotting options work for you, you can create your own with any of the other libraries of python. All of the prepared data can be found in `df` (the return value of the previous function).