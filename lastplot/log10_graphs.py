import os

import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import starbars

from lastplot.computing_statistics import get_test, get_pvalue
from lastplot.graph_constructor import mpl_calc_series, mpl_debug_series
from lastplot.saving import save_sheet

__all__ = [
    "log_values_graph_lipid_class",
    "log_values_graph_lipid",
]


# Graphs by log10 values
def log_values_graph_lipid(
        df_final,
        control_name,
        experimental_name,
        output_path,
        palette,
        xlabel=None,
        ylabel=None,
        title=None,
        show=True,
):
    """
    The `log_values_graph_lipid` function generates boxplots and statistical annotations to visualize the distribution of log 10 transformed values of single lipids across regions. It performs the following tasks:

    - Calculates Shapiro-Wilk and Levene's test results for normality and equality of variances.
    - Adds statistical annotations to the boxplots using `starbars.draw_annotation`.
    - Plots boxplots to visualize the distribution of the values for each lipid, distinguishing between control and experimental groups.
    - Customizable plots with appropriate labels and title for better visualization.
    - Saves each plot as a PNG file in the specified `output_path`.
    - Optionally displays the plot (`show=True`).

    The function also saves comments regarding the statistical tests performed for each lipid and region in an Excel sheet named "Comments" within the `output_path`.

    :param df_final: DataFrame containing normalized values and statistical test results.
    :param control_name: Name of the control group.
    :param experimental_name: Name of the experimental group, as a list.
    :param output_path: Path to save output graphs.
    :param palette: Color palette for plotting.
    :param xlabel: Label for the x-axis. If None, defaults to "Genotype".
    :param ylabel: Label for the y-axis. If None, defaults to "Log10 Values".
    :param title: Title for the plot. If None, defaults to "Log10 Values Values for {lipid} in {region}"
    :param show: Whether to display plots interactively (default True).
    """

    group_width = 0.4
    bar_width = 0.0
    bar_gap = 0.02
    palette = sns.color_palette(palette)

    if not os.path.exists(output_path + "/output/log_value_graphs/lipid"):
        os.makedirs(output_path + "/output/log_value_graphs/lipid")

    for (region, lipid), data in df_final.groupby(["Regions", "Lipids"]):
        shapiro = data.iloc[0]["Shapiro Normality"]
        levene = data.iloc[0]["Levene Equality"]
        test = get_test(shapiro, levene)

    test_comment = [f"{test} will be performed for all of the lipids"]
    save_sheet(test_comment, "Comments", output_path)

    for (region, lipid), data in df_final.groupby(["Regions", "Lipids"]):
        print(f"Creating graph for {lipid} in {region}")

        fig, ax = plt.subplots()
        genotype_data = list(data["Genotype"].unique())
        genotype_data.remove(control_name)
        genotype_data.insert(0, control_name)

        bar_width, positions = mpl_calc_series(
            len(lipid),
            len(genotype_data),
            group_width=group_width,
            bar_width=bar_width,
            bar_gap=bar_gap,
        )
        boxplot = []

        for g, genotype in enumerate(genotype_data):
            values = data[data["Genotype"] == genotype]["Log10 Values"]

            bp = ax.boxplot(
                values,
                positions=[g],
                widths=bar_width,
                patch_artist=True,
                boxprops=dict(facecolor=palette[g], color="k"),
                medianprops=dict(color="k"),
            )

            boxplot.append(bp["boxes"][0])

            ax.scatter(
                np.ones(len(values)) * g,
                values,
                color="k",
                s=6,
                zorder=3,
            )

        ax.set_xticks([*range(len(genotype_data))])
        ax.set_xticklabels(genotype_data, rotation=90)

        # Add statistical annotation
        pairs = []
        for element in genotype_data:
            if element != control_name:
                test = get_test(shapiro, levene)
                stat, pvalue = get_pvalue(
                    test,
                    data[data["Genotype"] == control_name]["Log10 Values"],
                    data[data["Genotype"] == element]["Log10 Values"],
                )
                pairs.append((control_name, element, pvalue))
        starbars.draw_annotation(pairs)
        comment = [f"For log 10 values of {lipid} in {region}, P-value is {pvalue}."]
        save_sheet(comment, "Comments", output_path)

        ax.legend(
            boxplot,
            [control_name, *experimental_name],
            loc="center left",
            bbox_to_anchor=(1, 0.5),
        )

        if xlabel:
            ax.set_xlabel(xlabel)
        else:
            ax.set_xlabel("Genotype")
        if ylabel:
            ax.set_ylabel(ylabel)
        else:
            ax.set_ylabel("Log10 Values")
        if title:
            ax.set_title(title)
        else:
            ax.set_title(f"Log10 Values for {lipid} in {region}")

        plt.savefig(
            output_path
            + f"/output/log_value_graphs/lipid/Log10 Values for {lipid} in {region}.png",
            dpi=1200,
        )
        if show:
            plt.show()
        plt.close()


def log_values_graph_lipid_class(
        df_final,
        control_name,
        experimental_name,
        output_path,
        palette,
        xlabel=None,
        ylabel=None,
        title=None,
        show=True,
        debug=False,
):
    """
    The `log_values_graph_lipid_class` function generates boxplots to visualize the distribution of log 10 transformed values across different lipid classes within each region. It performs the following tasks:

    - Iterates through each region in the DataFrame (`df_final`).
    - Plots boxplots to show the distribution of log 10 transformed values for each lipid class in the region, distinguishing between control and experimental groups (`control_name` and `experimental_name`).
    - Customizable plots with appropriate labels and title.
    - Saves each plot as a PNG file in the specified `output_path`.
    - Optionally displays the plot (`show=True`) and closes it after display.


    :param df_final: DataFrame containing normalized values and statistical test results.
    :param control_name: Name of the control group.
    :param experimental_name: Name of the experimental group, as a list.
    :param output_path: Path to save output graphs.
    :param palette: Color palette for plotting.
    :param xlabel: Label for the x-axis. If None, defaults to "Lipid Class"
    :param ylabel: Label for the y-axis. If None, defaults to "Log10 Values"
    :param title: Title for the plot. If None, defaults to "Log10 Values in {region}"
    :param show: Whether to display plots interactively (default True).
    """

    group_width = 0.5  # space a group will take (all expressed in percentages)
    bar_width = 0.03  # width of one boxplot
    bar_gap = 0.01  # space in between groups

    palette = sns.color_palette(palette)

    if not os.path.exists(output_path + "/output/log_value_graphs/lipid_class"):
        os.makedirs(output_path + "/output/log_value_graphs/lipid_class")

    for region, region_data in df_final.groupby("Regions"):
        print(f"Creating graphs for {region}")

        lipid_classes = region_data["Lipid Class"].unique()

        for i, lipid_class in enumerate(lipid_classes):
            fig, ax = plt.subplots()
            data = region_data[region_data["Lipid Class"] == lipid_class]
            lipids = data["Lipids"].unique()
            genotype_data = list(data["Genotype"].unique())
            genotype_data.remove(control_name)
            genotype_data.insert(0, control_name)

            if debug:
                # Draw extra information to visualize the bar width calculations.
                mpl_debug_series(
                    len(lipids),
                    len(genotype_data),
                    group_width=group_width,
                    bar_width=bar_width,
                    bar_gap=bar_gap,
                    ax=ax,
                )

            width, positions = mpl_calc_series(
                len(lipids),
                len(genotype_data),
                group_width=group_width,
                bar_width=bar_width,
                bar_gap=bar_gap,
            )

            boxplot = []

            for j, lipid in enumerate(lipids):
                for g, genotype in enumerate(genotype_data):
                    values = data[
                        (data["Lipids"] == lipid) & (data["Genotype"] == genotype)
                        ]["Log10 Values"]

                    bp = ax.boxplot(
                        values,
                        positions=[positions[j][g]],
                        widths=bar_width,
                        patch_artist=True,
                        boxprops=dict(facecolor=palette[g], color="k"),
                        medianprops=dict(color="k"),
                    )

                    boxplot.append(bp["boxes"][0])

                    ax.scatter(
                        np.ones(len(values)) * positions[j][g],
                        values,
                        color="k",
                        s=6,
                        zorder=3,
                    )

            ax.set_xticks([*range(len(lipids))])
            ax.set_xticklabels(lipids, rotation=90)
            ax.legend(
                boxplot,
                [control_name, *experimental_name],
                loc="center left",
                bbox_to_anchor=(1, 0.5),
            )

            if xlabel:
                ax.set_xlabel(xlabel)
            else:
                ax.set_xlabel(lipid_class)

            if ylabel:
                ax.set_ylabel(ylabel)
            else:
                ax.set_ylabel("Log10 Values")

            if title:
                ax.set_title(title)
            else:
                ax.set_title(f"Log10 Values Values in {region}")

            plt.tight_layout()
            plt.savefig(
                f"{output_path}/output/log_value_graphs/lipid_class/Log10 Values {region} {lipid_class}.png",
                dpi=1200,
            )
            if show:
                plt.show()

            plt.close()
