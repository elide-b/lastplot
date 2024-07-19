Data Workflow
=============

.. autofunction:: lastplot.data_workflow

Description of data_workflow
============================

The `data_workflow` function is designed to streamline the process of cleaning, analyzing, and normalizing lipid data.
This workflow includes several key steps: data cleanup, statistical testing, and Z score computation.
Below is a detailed explanation of each step and the overall workflow:

Detailed Descriptions of Each Step
----------------------------------

Data Cleanup:
~~~~~~~~~~~~~
Cleans and processes lipid data from the provided DataFrame.

This function performs several steps to clean and process lipid data:
- Removes 'Internal Standard' samples.
- Transforms and reshapes the data to long format.
- Filters out lipids with 3 or more missing values per region.
- Replaces zero values with 80% of the minimum value for the corresponding group.
- Logs 10 the cleaned values.
- Saves the cleaned and eliminated lipid data to an Excel file.

Lipid Selection:
~~~~~~~~~~~~~~~~
Analyzes and filters lipids with missing values in some regions based on their statistical impact on the Z score of the lipid class across different regions. Removes lipids that do not change the interpretation of results.

The function performs the following steps:
- Identifies the lipids with missing values in some regions.
- Groups data by lipid class and calculates average Z scores.
- Computes p-values of average Z scores with and without specific lipids using appropriate statistical tests.
- Compares the impact of removing each lipid and filters out lipids that do not change the interpretation in all regions.

The Shapiro-Wilk and Levene tests are used for normality and variance equality assessments.

Statistical Tests:
~~~~~~~~~~~~~~~~~~
Performs statistical tests on cleaned lipid data to check for normality and equality of variances.

This function performs the Shapiro-Wilk test for normality of residuals and Levene's test for equality of variances between control and experimental groups for each combination of region and lipid.

Z Score Computation:
~~~~~~~~~~~~~~~~~~~~
Computes Z scores and average Z scores per lipid class, merging them into the final DataFrame.

Steps:
- Groups the cleaned DataFrame by regions and lipids to calculate mean and standard deviation of log10 values.
- Computes the Z scores for each lipid based on the mean and standard deviation.
- Calculates average Z scores per lipid class, region, and mouse ID.

By following these steps, the `data_workflow` function provides a comprehensive and systematic approach to cleaning, analyzing, and normalizing lipid data, ensuring that the dataset is ready for subsequent statistical analysis and interpretation.

It returns an Excel file for easy visualization of the data, and a final Dataframe for further data manipulation.