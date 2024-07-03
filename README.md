# Automize Science

## What is it

Automize Science is a Python package designed to elaborate data into graphs coming from lipid extractions (LC/MS).
Starting from a file containing the **pmol/mg** values per each sample, this package streamlines the process of data
analysis and visualization.

## Features

Automize Science includes the following features:

- Data Sanitization: Clean and prepare data for analysis.
- Data Normalization: Normalize values to ensure consistency across samples.
- Normality Check: Use the Shapiro-Wilk test to check for normality of residuals.
- Variance Check: Use Levene's test to assess the equality of variances.
- Statistical Significance Annotation: Annotate boxplots with significance levels using t-test, Welch's t-test, or
  Mann-Whitney test depending on the data requirements.
- Visualization Tools: Create boxplots to aid in data interpretation.

## Installation

You can install the package via pip:

```
pip install automize-science
```

\
Alternatively, you can install the package from the source:

```
git clone https://github.com/elide-b/automize-science.git
cd automize-science
pip install .
```

## Usage

Here are some examples of how to use Automize Science:

```
import automize_science 

# Example usage
result = automize_science.analyze_data('path/to/your/datafile.xlsx')
as.plot_graph(result)
```

## Examples

For more detailed examples, please check the [example](https://github.com/elide-b/automize-science/tree/master/example)
folder.

## Contributing

We welcome contributions!
If you have a suggestion that would make this better, please fork the repo and create a pull request. You can also
simply open an issue with the tag **"enhancement"**.

To contribute:

1. Fork the repository.
2. Create a new branch (`git checkout -b feature-branch`).
3. Commit your changes (`git commit -m 'Add some amazing feature'`).
4. Push to the branch (`git push origin feature-branch`)
5. Open a pull request

## License

Distributed under the MIT License. See `LICENSE.txt` for more information.
