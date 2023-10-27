# Overview

There have been used 3 main components to store informations, data and files.


## Storage Account

All raw files that is being fetched from API's and has been collected as historical data are stored in an Azure Storage Account. In this storage account there has been setup a folder structure dividing files into their types and which municipality they are belonging to. Furthermore the storage account also contains the config-files for the pipelines. An example/template of the Azure Ressource can be seen in the template json-file.


## Snowflake

The main datastorage for both data in raw tables and also processed data is a Snowflake database. The snowflake database has been setup and hosted through the existing dataplatform. Therefore it would be necessary to setup a new instance to do run the transformations and store data on a municipality specific environment. 

## Azure Key Vault

An Azure Key Vault has been used to store all credentials for e.g. API's securely. An example/template of the Azure Ressource can be seen in the template json-file.