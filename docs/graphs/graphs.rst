Graphs
======

.. toctree::
   :maxdepth: 1

   z-scores/graph_lipid
   z-scores/graph_class
   z-scores/graph_class_average
   log_values/graph_lipid
   log_values/graph_class
   log_values/graph_class_average


Description
-----------

These functions generate boxplots and overlaying scatter plots for visualizing log10 values across different regions and lipids, distinguishing between control and experimental groups.

- **Customization:**
  - X axis, Y axis, and titles of every plot are changeable with their respective parameters ``xlabel, ylabel, and title``. When giving an argument to these parameters it's important to remember that the argument given will be applied to all of the plots resulting from that function. To still have the information reguarding the lipid, lipid class or region in them, these names should be between curly brackets:

.. code-block:: python

    lastplot.zscores_graph_class_average(
    df,
    control_name="WT",
    experimental_name=["FTD", "BPD", "HFD"],
    output_path=".",
    palette="tab20b_r",
    show=True,
    title="Scores for {lipid_class} in {region}",
)
   In this case the title displayed will have the corresponding plotted lipid class and region in the title.

  - Plot colors are customizable by choosing a qualitative palette. Matplotlib suggested palettes are ``['Pastel1', 'Pastel2', 'Paired', 'Accent', 'Dark2', 'Set1', 'Set2', 'Set3', 'tab10', 'tab20', 'tab20b', 'tab20c']``. For black and white plots, the color palettes are ``['gray', 'Greys']``. For more information, refer to `Matplotlib Qualitative Color Maps <https://matplotlib.org/stable/users/explain/colors/colormaps.html#qualitative>`_.
