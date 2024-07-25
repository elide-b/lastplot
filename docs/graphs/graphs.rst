Graphs
======

Description
-----------

These functions generate boxplots and overlaying scatter plots for visualizing log10 or z-score values across different regions, lipids, and/or lipid classes.
In general, they all:

- Plot boxplots to visualize the distribution of the chosen values, distinguishing between control and experimental group(s).
- Perform normality test (Shapiro-Wilk test) and homogeneity of variances test (Levene's test).
- Perform appropriate statistical tests based on the number of groups:

  - If there are two genotypes:

    - Choose the appropriate test (e.g., t-test, Welch t-test, or Mann-Whitney U test) based on the previous tests.
  - If there are more than two genotypes:

    - Perform ANOVA to determine if there are any statistically significant differences between groups.
    - If ANOVA is significant, perform post-hoc Tukey HSD test to find which specific groups differ.

- Annotates the plot with statistical significance indicators using the `starbars.draw_annotation` package.
- Customizable plots with appropriate labels and title for better visualization.
- Saves each plot as a PNG file in the specified `output_path`.
- Optionally displays the plot (`show=True`) and closes it after display.


Customization
-------------

- Plot colors are customizable by choosing a qualitative palette. Matplotlib suggested palettes are ``['Pastel1', 'Pastel2', 'Paired', 'Accent', 'Dark2', 'Set1', 'Set2', 'Set3', 'tab10', 'tab20', 'tab20b', 'tab20c']``. For black and white plots, the color palettes are ``['gray', 'Greys']``. For more information, refer to `Matplotlib Qualitative Color Maps <https://matplotlib.org/stable/users/explain/colors/colormaps.html#qualitative>`_.
- X axis, Y axis, and titles of every plot are changeable with their respective parameters ``xlabel, ylabel, and title``. When giving an argument to these parameters it's important to remember that the argument given will be applied to all of the plots resulting from that function. To still have the information reguarding the lipid, lipid class or region in them, these names should be between curly brackets:

  .. code-block:: python

     lastplot.zscores_graph_class_average(
     df,
     control_name="WT",
     experimental_name=["FTD", "BPD", "HFD"],
     output_path=".",
     palette="tab20b_r",
     show=True,
     title="Scores for {lipid_class} in {region}")

  In this case the title displayed will have the corresponding plotted lipid class and region in the title.
  If no title or axis label is wanted, you can simply put " " as the argument of the parameter.

Graphs available
----------------

.. toctree::
   :maxdepth: 1

   z-scores/graph_lipid
   z-scores/graph_class
   z-scores/graph_class_average
   log_values/graph_lipid
   log_values/graph_class
   log_values/graph_class_average