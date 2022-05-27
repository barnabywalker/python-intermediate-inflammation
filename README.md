# Inflam

![Continuous Integration build in GitHub Actions](https://github.com/<your_github_username>/python-intermediate-inflammation/workflows/CI/badge.svg?branch=main)

Inflam is a data management system written in Python that manages trial data used in clinical inflammation studies.

## Main features

Here are some main features of Inflam:

- Provide basic statistical analyses over clinical studies
- Ability to work on trial data in Comma-Separated Value (CSV) format
- Generate plots of trial data
- Analytical functions and views can be easily extended based on its Model-View-Controller architecture

## Prerequisites

Inflam requires the following Python packages:

- [NumPy](https://www.numpy.org/) - makes use of NumPy's statistical functions
- [Matplotlib](https://matplotlib.org/stable/index.html) - uses Matplotlib to generate statistical plots

The following optional packages are required to run Inflam's unit tests:

- [pytest](https://docs.pytest.org/en/stable/) - Inflam's unit tests are written using pytest
- [pytest-cov](https://pypi.org/project/pytest-cov/) - Adds test coverage stats to unit testing

## Installation

Inflam can be installed by cloning from GitHub and installing as a local project:

```
git clone https://github.com/barnabywalker/python-intermediate-inflammation.git
cd python-intermediate-inflammation
pip install -e .
```

## Basic usage

You can interact with Inflam using the command line by specifying an input file and a view.

To plot data from an inflammation trial:

```
python inflammation-analysis.py data/inflammation-01.csv --view visualise
```

To view a record for a particular patient:

```
python inflammation-analysis.py data/inflammation-01.csv --view record --patient 1
```

You can also save a patient record as a json or csv file:

```
python inflammation-analysis.py data/inflammation-01.csv --view serialise --serial-path data/patients.json
python inflammation-analysis.py data/inflammation-01.csv --view serialise --serial-path data/patients.csv
```

Or read a patient's record from a json or csv file:

```
python inflammation-analysis.py data/inflammation-01.csv --view record --patient 1 --serial-path data/patients.json
python inflammation-analysis.py data/inflammation-01.csv --view record --patient 1 --serial-path data/patients.csv
```

## Contributing

Please feel free to contribute anything!

If you have any suggestions for improvements, additional features, or bugs that need fixing, please [raise an issue](https://github.com/barnabywalker/python-intermediate-inflammation/issues).

If you would like to work on any [issues](https://github.com/barnabywalker/python-intermediate-inflammation/issues), please leave a comment in the relevant issue! You can then fork this repository, make your changes, and raise a pull request.