These additional instructions build upon and are meant to supplement the ppo pipeline instructions created by jdeck88, rodney757 and ramonawalls. The instructions below give additional information for creating a new instance of the pipeline and add more details to supplemental instructions for those who want a deeper understanding of the code, but are currently unfamiliar with the pipeline. The final portion of the notes indicate the current status of the ovt pipeline and what some of the next steps will need to be in order to get it running. 

---

# A high-throughput ontology-based pipeline for data integration

A flexible, scalable pipeline for integration of observation data from multiple sources. Little or no programming is required to adapt the pipeline for use with different kinds of data, ontologies, or reasoning profiles, and output is compatible with any type of storage technology.

Additional instructions to help those unfamiliar with the data pipeline in order to create a new instance.

## Getting Started 

**Downloading and Familiarizing Yourself with the Codebase** 

You can begin by cloning or forking this repository (or the ppo pipeline) and installing it on your laptop or server. The next step is reading through the rest of the documentation and familiarizing yourself with the [configuration files](https://github.com/biocodellc/ppo-data-pipeline/blob/master/README.md#config-files) The configuration files structure the pipeline's connections, so it is important to understand these files. 

**Set Up Your Environment** 

See [Dependencies](https://github.com/algilliland/ovt-data-pipeline#dependencies) on the main readme in order to begin setup of your environment. 

When you run the install and set up of your virtual environment, make sure that you set all flags necessary as the output messages suggest. 

Confirm you are on the correct python version using `python --version`. 

If you run into issues with switching python versions, see if (this)[https://github.com/pyenv/pyenv/issues/896] resolves the issue. 

Currently, the ovt tests are not complete, so you cannot test everything works as expected by running `./pytest.sh`. 

## Running the Process and Running Tests

As said in the main instructions, the process should be run from the root directory (vto-data-pipeline). Run the entire pipeline using `python -m process`. The -m option tells python process is a module.  

Look at [Usage](https://github.com/algilliland/ovt-data-pipeline#usage) on the main readme in order to see the different ways you can run the pipeline. 

You are able to run a single .py file by 
When an import error occurs with the message 'module name cannot be found' and the module is a locally created module, try running with PYTHONPATH=../ python test_config.py. This instructs python to check the directory above as well for the module. 

When an import error occurs for a package not created in ovt, it indicates the package was not available when python tried to run the file depending on it. Try fixing this error through a pip install for the package. This will attempt to download and install the package. 

Example: 

The requests module is required for oft-data-pipeline/process/utils.py. 

Run `pip install requests` to download requests. 

If running a pip install does not work, try googling the package for additional help. 

## Step One: Pre-processing

**Overview**

This step involves transforming the data into a common format for triplifying. This will usually involve writing a custom PreProcessor for each project to be ingested. The preprocessor module contains an abstract class AbstractPreProcessor that can be inherited by the project preprocessor. We suggest adapting one of the projects included in this package as a template from which to start. The purpose of the pre-processor is to configure the data to conform to the structure specified in the headers configuration file.

When creating a new pipeline instance for a different ontology, the headers configuration file will need to be created to fit the ontology you are using. Include all traits you are collecting from all of your data sources. This header file gives you the map connecting all of the data sets you will be integrating to one consistent format. 

You will also need to adapt the AbstractPreProcessor for your data. Inside the AbstractPreprocessor class, there is a list called headers which orders the columns of your data for writing to the output csv. This csv is the standardized output for the preprocessing step. 

**Creating a New Preprocessor** 

Most likely you will have to create a new preprocessor for each dataset you are integrating, so that you can create the unique mapping from the input data to the expected configuration. The easiest way to do this is to create a PreProcessor that inherits from the AbstractPreProcessor. The AbstractPreprocesser contains the functionality to initialize the preprocessor, run the preprocessor, and basic IO. It is initialized with the input directory, output directory and sets the output file as data.csv in the output directory. The run method will check to see if the output directory exists and if it does not, it will create it. Then it will write the column headers to the csv, these are the labels you have placed in your headers list. The next call in run is to process_data, which is not implemented in the AbstractPreprocessor. You must implement process_data in your preprocessor so that your unique data can be formatted. Your process_data method needs to read your data, map the selected trait from each record to the expected column and it writes your data. See Pandas documentation for help using the read/write calls (read_csv/to_csv).

There are a few different points that must be updated so that the new ontology and data set are able to be processed. In process/config.py, the DEFAULT_HEADERS must be updated. These default headers are the columns that will be selected for if headers are not specified in the abstract preprocessor.py. 

If you follow the shown usage for multiprocessing you should run into no issues with having multiprocessing in your preprocessor. When dealing with large data sets, it is vital to enable multiprocessing in order to take advantage of all CPUs available. As long as your environment is set to use the recommended python version 3.5.1, you should not run into any issues. 

## Step Two: Triplifier

## Step Three: Reasoning 

**Updating the Pipeline to Accept a New Ontology**

Ontopilot is utilized to manage ontologies, you can check out their [wiki](https://github.com/stuckyb/ontopilot/wiki/Ontology-development#overview).

Once you have your ontology completed, you are able to integrate it with the data pipeline. The file process/config.py expects a default ontology to be referenced. The OVT's default [ontology](https://raw.githubusercontent.com/futres/ovt/master/ontology/ovt-reasoned.owl) is hosted on GitHub. 

Additional preprocessing can be done to accomplish reasoning that is intractable with ELK reasoning. For example, ppo-data-pipeline adds additional reasoning on the phenophase_descriptions to account for presence traits. 

## Step Four: RdfCsv


## Step Five: Data Loading

The data loading step has not yet been reached for the ovt pipeline, see the point 5 of [ppo's Running the pipeline](https://github.com/biocodellc/ppo-data-pipeline/blob/master/README.md#running-the-pipeline) for information relating to data loading. 

## Testing 
It is important to check all of the pipeline connections in addition to completing data checks. We run these tests by using the purest tool. When running all the pytests, you are ensuring your configurations set up your pipeline correctly and all data validation is working correctly. 

In order to test the new instance you have created you will need to update the old test files.

The test directory under the main pipeline contains the tests which check the configurations, triplifier and validity via the rules being applied appropriately. Each of these corresponds to a .py file in test. For both the ppo and the ovt we used simplified input files and configurations to test the pipeline connections were working. The data-pipeline results can be 

These tests rely on the config subdirectory to check the connections of the pipeline. The config directory should be a copy of the main config file, this is so we can run tests with a pseudo-root (explain differently?). This directory also has an additional file called pop-reasoned-no-imports.owl. 

pytest is the package that we use to support automated testing of the pipeline. It searches for any files starting with test_ or ending with _test. This is a recursive search that will check all subdirectories from the point you start running your tests from. This is important to note when you start duplicating your test files. 

___

## Future Directions 

The ovt-datapipeline is not complete, below are the known areas which must be updated in order for it to be functional. 

The test_triplifier.py, fetch_reasoned.sparql and reasoner.config. still need to be updated. 

The Data Loading step for using elastic search and blaze graph have not been updated for ovt. 

There are several areas in the codebase where identical files are duplicated and stored in different locations. For example, test/data/invalid_input.csv was almost identical to test/invalid_data.csv. Another example is relations.csv and entity.csv existing in multiple locations. I did not determine which copies were necessary and which were redundant, I simply copied the ppo structure. 


