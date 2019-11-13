# radlings
Radlings backend

## Installation

Install [miniconda](https://docs.conda.io/projects/conda/en/latest/glossary.html#miniconda-glossary) to uniformly manage your Python and its packages.

Run the following [command](https://docs.conda.io/projects/conda/en/4.6.0/_downloads/52a95608c49671267e40c689e0bc00ca/conda-cheatsheet.pdf) after cloning the repo.

```bash
$ conda env create -f environment.yml
```

## Running locally
Run this command in your shell first! 
This will store application default credentials on your local machine.
```bash
$ gcloud auth application-default login
```
and 
```bash
$ python main.py
```

To fetch the categories

	Request Type - GET
	End Point - /categories

To fetch the resources
	
	Request Type - POST
	End Point - /fetch_resource
	params - {'category': <name_of_category>}

to test locally.