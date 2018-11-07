10/10/18
Author: Ali Gilliland 

Builds upon the instructions contributed to by jdeck88, rodney757 and ramonawalls.

# A high-throughput ontology-based pipeline for data integration

A flexible, scalable pipeline for integration of observation data from multiple sources. Little or no programming is required to adapt the pipeline for use with different kinds of data, ontologies, or reasoning profiles, and output is compatible with any type of storage technology.

Additional instructions to help those unfamiliar with the data pipeline in order to create a new instance.

## Getting Started 
TODO: Add more support 

Discuss setting flags for Pyenv and also switching/checking python versions
https://github.com/pyenv/pyenv/issues/896

## Step One - Pre-processing

**Overview**

This step involves transforming the data into a common format for triplifying. This will usually involve writing a custom PreProcessor for each project to be ingested. The preprocessor module contains an abstract class AbstractPreProcessor that can be inherited by the project preprocessor. We suggest adapting one of the projects included in this package as a template from which to start. The purpose of the pre-processor is to configure the data to conform to the structure specified in the headers configuration file.

When creating a new pipeline instance for a different ontology, the headers configuration file will need to be created to fit the ontology you are using. Include all traits you are collecting from all of your data sources. This header file gives you the map connecting all of the data sets you will be integrating to one consistent format. 

You will also need to adapt the AbstractPreProcessor for your data. Inside the AbstractPreprocessor class, there is a list called headers which orders the columns of your data for writing to the output csv. This csv is the standardized output for the preprocessing step. 

**Creating a new preprocessor** 

Most likely you will have to create a new preprocessor for each dataset you are integrating, so that you can create the unique mapping from the input data to the expected configuration. The easiest way to do this is to create a PreProcessor that inherits from the AbstractPreProcessor. The AbstractPreprocesser contains the functionality to initialize the preprocessor, run the preprocessor, and basic IO. It is initialized with the input directory, output directory and sets the output file as data.csv in the output directory. The run method will check to see if the output directory exists and if it does not, it will create it. Then it will write the column headers to the csv, these are the labels you have placed in your headers list. The next call in run is to process_data, which is not implemented in the AbstractPreprocessor. You must implement process_data in your preprocessor so that your unique data can be formatted. Your process_data method needs to read your data, map the selected trait from each record to the expected column and it writes your data. See Pandas documentation for help using the read/write calls (read_csv/to_csv).

There are a few different points that must be updated so that the new ontology and data set are able to be processed. In process/config.py, the DEFAULT_HEADERS must be updated. These default headers are the columns that will be selected for if headers are not specified in the abstract preprocessor.py. 


# TODO: discuss multiprocessing (more)  
multiprocessing.Pool() objects are not conte/Users/algilliland/Documents/VertPLxt managers in python < Python 3.3, so you cannot use the """ with """ key word. You will need to use Python 3.3+ or manage your context explicitly. It is not necessary to worry about this as long as you utilize the recommended Python version 3.5.1.  

## Running the Process

**
run process from the root dir (vto-data-pipeline) using python -m process 

Pip install requests because it was not available when trying to run it! Need it for process/utils.py import requests 

pip install rfc3987

Basically if you hit an import error from a import dependency google installing dependency or attempt pip install dependency. 


## Updating the Pipeline to Accept a New Ontology 

Ontopilot is utilized to manage ontologies, you can check out their wiki or this basic ontology development reference page to begin the process of creating a new ontology. https://github.com/stuckyb/ontopilot/wiki/Ontology-development#column-names-for-all-ontology-entities

Once you have your ontology completed, you are able to integrate it with the data pipeline. process/config.py expects a default ontology to be referenced. The OVT's default ontology is hosted on GitHub. 



