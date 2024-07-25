Data Workflow
=============

.. autofunction:: lastplot.data_workflow

Description of data_workflow
----------------------------

The `data_workflow` function is designed to streamline the process of cleaning, analyzing, and normalizing lipid data.
This workflow includes several key steps: data cleanup, statistical testing, and Z score computation.
By following these steps, the `data_workflow` function provides a comprehensive and systematic approach to cleaning, analyzing, and normalizing lipid data, ensuring that the dataset is ready for subsequent statistical analysis and interpretation.
It returns an Excel file for easy visualization of the data, and a final Dataframe for further data manipulation.

Below is a detailed explanation of each step and the overall workflow:

Data Cleanup:
~~~~~~~~~~~~~
Cleans and processes lipid data from the provided DataFrame.

This function performs several steps to clean and process lipid data:

- Removes all 'Internal Standard' samples.
- Filters out lipids with 3 or more missing values per region.
- Further filters the eliminated lipids based on their statistical impact on the Z score of the lipid class across different regions.
- Replaces the remaining zero values with 80% of the minimum value for the corresponding group.
- Transforms the values with a log10.
- Saves the cleaned and eliminated lipid data to an Excel file.

Statistical Tests:
~~~~~~~~~~~~~~~~~~
Performs statistical tests on cleaned lipid data to check for normality and equality of variances.

Depending on the number of experimental groups, the normality of residuals and the equality of variances, the statistical tests used are T-test, Welch T-test, Mann Whitney U test, or two way ANOVA test. In the case of ANOVA and found significance, Tukey is used as a post-hoc test, to find the significant pairs.
This function performs the Shapiro-Wilk test for normality of residuals and Levene's test for equality of variances between control and experimental groups for each combination of region and lipid.

Z Score Computation:
~~~~~~~~~~~~~~~~~~~~
Computes Z scores and average Z scores per lipid class, merging them into the final DataFrame.

Steps:

- Groups the cleaned DataFrame by regions and lipids to calculate mean and standard deviation of log10 values.
- Computes the Z scores for each lipid based on the mean and standard deviation.
- Calculates average Z scores per lipid class, region, and mouse ID.

