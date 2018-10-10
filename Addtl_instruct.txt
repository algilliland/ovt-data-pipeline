10/10/18
Author: Ali Gilliland 
Builds upon the instructions contributed to by jdeck88, rodney757 and ramonawalls.

# A high-throughput ontology-based pipeline for data integration

A flexible, scalable pipeline for integration of observation data from multiple sources. Little or no programming is required to adapt the pipeline for use with different kinds of data, ontologies, or reasoning profiles, and output is compatible with any type of storage technology.

Additional instructions to help those unfamiliar with the data pipeline in order to create a new instance.

## Getting Started 
TODO: Add more support 
Discuss setting flags for Pyenv and also switching/checking python versions

## Step One - Pre-processing

**Overview**
This step involves transforming the data into a common format for triplifying. This will usually involve writing a custom PreProcessor for each project to be ingested. The preprocessor module contains an abstract class AbstractPreProcessor that can be inherited by the project preprocessor. We suggest adapting one of the projects included in this package as a template from which to start. The purpose of the pre-processor is to configure the data to conform to the structure specified in the headers configuration file.

When creating a new pipeline instance for a different ontology, the headers configuration file will need to be created to fit the ontology you are using. Include all traits you are collecting from all of your data sources. This header file gives you the structure to map all of the data sets you will be integrating to one consistent format. 

**Creating a new preprocessor** 

Most likely you will have to create a preprocessor for each dataset you are integrating, so that you can create the unique mapping from the input data to the expected configuration. 
 

