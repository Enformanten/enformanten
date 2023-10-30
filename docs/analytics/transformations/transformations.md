# Tranformations

The dataload and transformation layer are built on layer-diveded principle. All data sources are as a standard handled in 4 layers:

* 1_RAW
* 2_STANDARD
* 3_CLEANSED
* 4_FEATURIZ

The project have both loaded and transformed data from individual municipalities as well as joined the sources into standardized tabels for cohorent usage and scaleability. 

# Data load

The data load is done by integrating raw tables in Snowflake with the Storage Account setup in Azure. This has been done by using stages that fetches the file from the individual folders in the storage account.

# Specific & General transformations

The specific transformations for the local datasources of each municipality is divided into folders. These transformations contains the ETL-scripts (with inline-comments) used for taking the sources from anywhere between level *1* - *3* of the database layers. From there the transformations seeks to transform the individual municipalities data into a unified schema/table. These scripts are both commented and described in the general folder. In there one may also find the final suggested schemas for each data source.