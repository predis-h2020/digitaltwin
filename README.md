# digitaltwin
A digital twin for predicting waste package evolution. Part of the [H2020 Predis project](https://predis-h2020.eu/predis-project/), [work package 7](https://predis-h2020.eu/work-packages/), subtask 7.4.

## Usage
The package is decomposed into a library part that includes functions that might later be used in a dedicated conda package. Right now there are only some virtual data generation scripts for testing purposes. 
In addition, there is an example folder that shows how the functionality provided in the library is to be used.

## Installation
* First clone the repository. 
* Then install a conda environment using the provided environment file
```
conda env create --prefix ./conda-env -f environment.yml 
```
You could also use mamba (which is usually much faster).

* Activate the environment
```
conda activate ./conda-env
```
* Execute either the tests using 
```
cd tests
pytest 
```
* or call a workflow in the examples section
```
cd examples/virtual_data_generation
doit
```

## Reporting bugs

To report a bug, please go to [digitaltwin's Issues](https://github.com/predis-h2020/digitaltwin/issues/new) and enter a *descriptive title* and *write your issue with enough details*.

Please provide a *minimum reproducible example* to be more efficient in identifying the bug and fixing it. A good syntax when writing your issues is [Markdown](https://guides.github.com/features/mastering-markdown/).

## Contributing with development

The [Fork & Pull Request Workflow](https://docs.github.com/en/get-started/quickstart/contributing-to-projects) is used. Below is a summary of the necessary steps you need to take:

1. Fork this repository
2. Clone the repository at your machine
3. Add your changes in a branch named after what's being done (`lower-case-with-hyphens`)
4. Make a pull request to `predis-h2020/digitaltwin`, targeting the `main` branch