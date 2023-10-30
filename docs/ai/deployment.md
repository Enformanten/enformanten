# Deployment
The AI solution is designed to be exposed as a RESTful FastAPI (V0.103.2) web application. The `/ai` folder contains a Dockerfile that can be used to build a Docker image of the application. The image can then be deployed to a cloud-based container service - In our case, Azure Container Registry. The application is designed to be deployed as a single container, but it can be scaled horizontally to multiple instances if needed.


As evident from the figure above, the solution has multiple modules even though the name suggests that it is only a single AI model. The technical specifications for each these modules can be found in `/references`.

## Authentication
In its current state, the solution uses the OAuth2 protocol for authentication. As such, the solution is closed to traffic from unauthorized users. A list of pre-defined users are configured in an environment variabel file and will be created in the in-server sqlite database on initial deployment (Please see `overview` for details on adding an .env file for local development, and the interactive API documentation for details on the authentication process at `<app-url>/docs`). 

## GitHub Actions
The solution is set up with GitHub Actions for continuous integration and deployment. The workflow is triggered on push to the `main` branch. Please see the `.github/workflows` folder for details on the workflow.

## Integration
The solution integrates with Azure Data Factory data flow and the associated (Snowflake) database but is otherwise closed to traffic.

The specifications for the connecting pipeline in Azure Data Factory is shown below. <br>
Note that the pipeline first authenticates using the pre-defined credentials associated with its user and then calls the `train` endpoint. The endpoint is responsible for training the AI model and updating the model registry. The model registry is then used by the `predict` endpoint to return the predicted utilization rate for a given room. <br>
Extracted 30.10.2023

``` json
    {
        "name": "PL_DRIFTOPTIMERINGSMODEL",
        "properties": {
            "description": "This pipelines is responsible for training the AI-model \"Driftoptimeringsmodel\" once a month. ",
            "activities": [
                {
                    "name": "Get token",
                    "type": "WebActivity",
                    "dependsOn": [
                        {
                            "activity": "Get Config",
                            "dependencyConditions": [
                                "Succeeded"
                            ]
                        }
                    ],
                    "policy": {
                        "timeout": "0.12:00:00",
                        "retry": 0,
                        "retryIntervalInSeconds": 30,
                        "secureOutput": false,
                        "secureInput": false
                    },
                    "userProperties": [],
                    "typeProperties": {
                        "url": "https://app-govtech.azurewebsites.net/auth/jwt/login",
                        "method": "POST",
                        "headers": {
                            "accept": "application/json",
                            "Content-Type": "application/x-www-form-urlencoded"
                        },
                        "body": {
                            "value": "@activity('Get Config').output.value",
                            "type": "Expression"
                        }
                    }
                },
                {
                    "name": "Train Model",
                    "type": "Lookup",
                    "dependsOn": [
                        {
                            "activity": "Get token",
                            "dependencyConditions": [
                                "Succeeded"
                            ]
                        },
                        {
                            "activity": "UPDATE_DRIFTOPTIMERING_TRAINING",
                            "dependencyConditions": [
                                "Succeeded"
                            ]
                        }
                    ],
                    "policy": {
                        "timeout": "0.12:00:00",
                        "retry": 0,
                        "retryIntervalInSeconds": 30,
                        "secureOutput": false,
                        "secureInput": false
                    },
                    "userProperties": [],
                    "typeProperties": {
                        "source": {
                            "type": "JsonSource",
                            "storeSettings": {
                                "type": "HttpReadSettings",
                                "requestMethod": "POST",
                                "additionalHeaders": {
                                    "value": "@{concat('Authorization: Bearer ' , activity('Get token').output.access_token)}",
                                    "type": "Expression"
                                },
                                "requestTimeout": "10:00:00"
                            },
                            "formatSettings": {
                                "type": "JsonReadSettings"
                            }
                        },
                        "dataset": {
                            "referenceName": "DS_DRIFTOPTIMERINGSMODEL_TRAIN",
                            "type": "DatasetReference"
                        }
                    }
                },
                {
                    "name": "UPDATE_DRIFTOPTIMERING_TRAINING",
                    "type": "Lookup",
                    "dependsOn": [],
                    "policy": {
                        "timeout": "0.12:00:00",
                        "retry": 0,
                        "retryIntervalInSeconds": 30,
                        "secureOutput": false,
                        "secureInput": false
                    },
                    "userProperties": [],
                    "typeProperties": {
                        "source": {
                            "type": "SnowflakeSource",
                            "query": "CALL \"RAW\".UPDATEFEATURIZDISTINCT('GOVTECH_DB', 'RAW', '4_FEATURIZ_DRIFTOPTIMERING_TRAINING', '3_CLEANSED_DRIFTOPTIMERING_TRAINING')",
                            "exportSettings": {
                                "type": "SnowflakeExportCopyCommand"
                            }
                        },
                        "dataset": {
                            "referenceName": "DS_SNOWFLAKE",
                            "type": "DatasetReference",
                            "parameters": {
                                "database": "GOVTECH_DB",
                                "table": "4_FEATURIZ_DRIFTOPTIMERING_TRAINING",
                                "schema": "RAW"
                            }
                        }
                    }
                },
                {
                    "name": "Get Config",
                    "type": "WebActivity",
                    "dependsOn": [],
                    "policy": {
                        "timeout": "0.12:00:00",
                        "retry": 0,
                        "retryIntervalInSeconds": 30,
                        "secureOutput": false,
                        "secureInput": false
                    },
                    "userProperties": [],
                    "typeProperties": {
                        "url": "<HIDDEN>",
                        "method": "GET",
                        "authentication": {
                            "type": "MSI",
                            "resource": "https://vault.azure.net"
                        }
                    }
                }
            ],
            "folder": {
                "name": "Driftoptimeringsmodel"
            },
            "annotations": [],
            "lastPublishTime": "2023-10-13T12:27:21Z"
        },
        "type": "Microsoft.DataFactory/factories/pipelines"
    }

```


## Remote Resource Specification
Extracted 30.10.2023
``` json
{
    "id": "/subscriptions/<HIDDEN/resourceGroups/rg-govtech/providers/Microsoft.Web/sites/app-govtech",
    "name": "app-govtech",
    "type": "Microsoft.Web/sites",
    "kind": "app,linux,container",
    "location": "West Europe",
    "tags": {},
    "properties": {
        "name": "app-govtech",
        "state": "Running",
        "hostNames": [
            "app-govtech.azurewebsites.net"
        ],
        "webSpace": "rg-govtech-WestEuropewebspace-Linux",
        "selfLink": "<HIDDEN>",
        "repositorySiteName": "app-govtech",
        "owner": null,
        "usageState": 0,
        "enabled": true,
        "adminEnabled": true,
        "afdEnabled": false,
        "enabledHostNames": [
            "app-govtech.azurewebsites.net",
            "app-govtech.scm.azurewebsites.net"
        ],
        "siteProperties": {
            "metadata": null,
            "properties": [
                {
                    "name": "LinuxFxVersion",
                    "value": "DOCKER|acrgovtech.azurecr.io/acrgovtech/production:<HIDDEN>"
                },
                {
                    "name": "WindowsFxVersion",
                    "value": null
                }
            ],
            "appSettings": null
        },
        "availabilityState": 0,
        "sslCertificates": null,
        "csrs": [],
        "cers": null,
        "siteMode": null,
        "hostNameSslStates": [
            {
                "name": "app-govtech.azurewebsites.net",
                "sslState": 0,
                "ipBasedSslResult": null,
                "virtualIP": null,
                "virtualIPv6": null,
                "thumbprint": null,
                "certificateResourceId": null,
                "toUpdate": null,
                "toUpdateIpBasedSsl": null,
                "ipBasedSslState": 0,
                "hostType": 0
            },
            {
                "name": "app-govtech.scm.azurewebsites.net",
                "sslState": 0,
                "ipBasedSslResult": null,
                "virtualIP": null,
                "virtualIPv6": null,
                "thumbprint": null,
                "certificateResourceId": null,
                "toUpdate": null,
                "toUpdateIpBasedSsl": null,
                "ipBasedSslState": 0,
                "hostType": 1
            }
        ],
        "computeMode": null,
        "serverFarm": null,
        "serverFarmId": "/subscriptions/<HIDDEN>/resourceGroups/rg-govtech/providers/Microsoft.Web/serverfarms/ASP-govtech",
        "reserved": true,
        "isXenon": false,
        "hyperV": false,
        "lastModifiedTimeUtc": "2023-10-30T14:43:21.26",
        "storageRecoveryDefaultState": "Running",
        "contentAvailabilityState": 0,
        "runtimeAvailabilityState": 0,
        "dnsConfiguration": {},
        "vnetRouteAllEnabled": false,
        "containerAllocationSubnet": null,
        "useContainerLocalhostBindings": null,
        "vnetImagePullEnabled": false,
        "vnetContentShareEnabled": false,
        "siteConfig": {
            "numberOfWorkers": 1,
            "defaultDocuments": null,
            "netFrameworkVersion": null,
            "phpVersion": null,
            "pythonVersion": null,
            "nodeVersion": null,
            "powerShellVersion": null,
            "linuxFxVersion": "DOCKER|acrgovtech.azurecr.io/acrgovtech/production:<HIDDEN>",
            "windowsFxVersion": null,
            "windowsConfiguredStacks": null,
            "requestTracingEnabled": null,
            "remoteDebuggingEnabled": null,
            "remoteDebuggingVersion": null,
            "httpLoggingEnabled": null,
            "azureMonitorLogCategories": null,
            "acrUseManagedIdentityCreds": false,
            "acrUserManagedIdentityID": null,
            "logsDirectorySizeLimit": null,
            "detailedErrorLoggingEnabled": null,
            "publishingUsername": null,
            "publishingPassword": null,
            "appSettings": null,
            "metadata": null,
            "connectionStrings": null,
            "machineKey": null,
            "handlerMappings": null,
            "documentRoot": null,
            "scmType": null,
            "use32BitWorkerProcess": null,
            "webSocketsEnabled": null,
            "alwaysOn": true,
            "javaVersion": null,
            "javaContainer": null,
            "javaContainerVersion": null,
            "appCommandLine": null,
            "managedPipelineMode": null,
            "virtualApplications": null,
            "winAuthAdminState": null,
            "winAuthTenantState": null,
            "customAppPoolIdentityAdminState": null,
            "customAppPoolIdentityTenantState": null,
            "runtimeADUser": null,
            "runtimeADUserPassword": null,
            "loadBalancing": null,
            "routingRules": null,
            "experiments": null,
            "limits": null,
            "autoHealEnabled": null,
            "autoHealRules": null,
            "tracingOptions": null,
            "vnetName": null,
            "vnetRouteAllEnabled": null,
            "vnetPrivatePortsCount": null,
            "publicNetworkAccess": null,
            "cors": null,
            "push": null,
            "apiDefinition": null,
            "apiManagementConfig": null,
            "autoSwapSlotName": null,
            "localMySqlEnabled": null,
            "managedServiceIdentityId": null,
            "xManagedServiceIdentityId": null,
            "keyVaultReferenceIdentity": null,
            "ipSecurityRestrictions": null,
            "ipSecurityRestrictionsDefaultAction": null,
            "scmIpSecurityRestrictions": null,
            "scmIpSecurityRestrictionsDefaultAction": null,
            "scmIpSecurityRestrictionsUseMain": null,
            "http20Enabled": false,
            "minTlsVersion": null,
            "minTlsCipherSuite": null,
            "supportedTlsCipherSuites": null,
            "scmMinTlsVersion": null,
            "ftpsState": null,
            "preWarmedInstanceCount": null,
            "functionAppScaleLimit": 0,
            "elasticWebAppScaleLimit": null,
            "healthCheckPath": null,
            "fileChangeAuditEnabled": null,
            "functionsRuntimeScaleMonitoringEnabled": null,
            "websiteTimeZone": null,
            "minimumElasticInstanceCount": 0,
            "azureStorageAccounts": null,
            "http20ProxyFlag": null,
            "sitePort": null,
            "antivirusScanEnabled": null,
            "storageType": null,
            "sitePrivateLinkHostEnabled": null
        },
        "daprConfig": null,
        "deploymentId": "app-govtech",
        "slotName": null,
        "trafficManagerHostNames": null,
        "sku": "PremiumV3",
        "scmSiteAlsoStopped": false,
        "targetSwapSlot": null,
        "hostingEnvironment": null,
        "hostingEnvironmentProfile": null,
        "clientAffinityEnabled": false,
        "clientCertEnabled": false,
        "clientCertMode": 0,
        "clientCertExclusionPaths": null,
        "hostNamesDisabled": false,
        "ipMode": "IPv4",
        "vnetBackupRestoreEnabled": false,
        "domainVerificationIdentifiers": null,
        "customDomainVerificationId": "<HIDDEN>",
        "kind": "app,linux,container",
        "managedEnvironmentId": null,
        "inboundIpAddress": "<HIDDEN>",
        "possibleInboundIpAddresses": "<HIDDEN>",
        "ftpUsername": "app-govtech\\$app-govtech",
        "ftpsHostName": "<HIDDEN>",
        "outboundIpAddresses": "<HIDDEN>",
        "possibleOutboundIpAddresses": "<HIDDEN>",
        "containerSize": 0,
        "dailyMemoryTimeQuota": 0,
        "suspendedTill": null,
        "siteDisabledReason": 0,
        "functionExecutionUnitsCache": null,
        "maxNumberOfWorkers": null,
        "homeStamp": "waws-prod-am2-649",
        "cloningInfo": null,
        "hostingEnvironmentId": null,
        "tags": {},
        "resourceGroup": "rg-govtech",
        "defaultHostName": "app-govtech.azurewebsites.net",
        "slotSwapStatus": null,
        "httpsOnly": true,
        "endToEndEncryptionEnabled": false,
        "functionsRuntimeAdminIsolationEnabled": false,
        "redundancyMode": 0,
        "inProgressOperationId": null,
        "geoDistributions": null,
        "privateEndpointConnections": [],
        "publicNetworkAccess": "Enabled",
        "buildVersion": null,
        "targetBuildVersion": null,
        "migrationState": null,
        "eligibleLogCategories": "AppServiceAppLogs,AppServiceAuditLogs,AppServiceConsoleLogs,AppServiceHTTPLogs,AppServiceIPSecAuditLogs,AppServicePlatformLogs,ScanLogs,AppServiceFileAuditLogs,AppServiceAntivirusScanAuditLogs",
        "inFlightFeatures": [],
        "storageAccountRequired": false,
        "virtualNetworkSubnetId": null,
        "keyVaultReferenceIdentity": "SystemAssigned",
        "defaultHostNameScope": 0,
        "privateLinkIdentifiers": null,
        "sshEnabled": null
    }
}
```

## API Documentation
The API documentation is generated by FastAPI and can be accessed at `<app-url>/docs`. The documentation is interactive and allows for testing of the API endpoints. The documentation is also available in JSON format at `<app-url>/openapi.json`. For transparency, the JSON specification is also given below

``` json 
{

    "openapi":"3.1.0",
    "info":{
        "title":"Tilly API",
        "description":"Unsupervised anomaly detection for room usage",
        "version":"54c0cc62-bekkeremil-Oct 30, 15:41"
    },
    "paths":{
        "/":{
            "get":{
                "tags":["dashboard"],
                "summary":"Read Root",
                "description":"Serve the Tilly Dashboard.\n\nThis route returns an HTML response that serves the Tilly dashboard.\n\nArgs:\n    request (Request): The FastAPI request object.\n\nReturns:\n    HTMLResponse: The HTML response containing the rendered Tilly dashboard.\n\nExamples:\n    ```bash\n    curl http://localhost:8000/\n    ```\n\n    This will return the HTML content of the Tilly dashboard.",
                "operationId":"read_root__get",
                "responses":{
                    "200":{
                        "description":"Successful Response",
                        "content":{
                            "text/html":{
                                "schema":{
                                    "type":"string"
                                }
                            }
                        }
                    }
                }
            }
        },
        "/plots_structure":{
            "get":{
                "tags":["dashboard"],
                "summary":"Get Plots Structure",
                "description":"Get Plot Directory Structure.\n\nThis route returns the directory structure of the plots as a JSON object.\nIf the directory structure is invalid, a 404 HTTP error is raised.\n\nReturns:\n    Optional[Dict]: The dictionary representing the directory structure.\n\nExamples:\n    ```bash\n    curl http://localhost:8000/plots_structure\n    ```\n\n    This will return a JSON object representing the directory structure of\n    the plots.",
                "operationId":"get_plots_structure_plots_structure_get",
                "responses":{
                    "200":{
                    "description":"Successful Response",
                    "content":{
                        "application/json":{
                            "schema":{
                                "anyOf":[
                                    {
                                        "type":"object"
                                    },
                                    {
                                        "type":"null"
                                    }
                                ],
                                "title":"Response Get Plots Structure Plots Structure Get"
                            }
                        }
                    }
                }
            }
        }
    },
    "/auth/jwt/login":{
        "post":{
            "tags":["auth"],
            "summary":"Auth:Jwt.Login",
            "operationId":"auth_jwt_login_auth_jwt_login_post",
            "requestBody":{
                "content":{
                    "application/x-www-form-urlencoded":{
                        "schema":{
                                "$ref":"#/components/schemas/Body_auth_jwt_login_auth_jwt_login_post"
                            }
                    }
                },
                "required":true
            },
            "responses":{
                "200":{
                    "description":"Successful Response",
                    "content":{
                        "application/json":{
                            "schema":{
                                "$ref":"#/components/schemas/BearerResponse"
                            },
                            "example":{
                                "access_token":"eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjoiOTIyMWZmYzktNjQwZi00MzcyLTg2ZDMtY2U2NDJjYmE1NjAzIiwiYXVkIjoiZmFzdGFwaS11c2VyczphdXRoIiwiZXhwIjoxNTcxNTA0MTkzfQ.M10bjOe45I5Ncu_uXvOmVV8QxnL-nZfcH96U90JaocI",
                                "token_type":"bearer"
                            }
                        }
                    }
                },
                "400":{
                    "description":"Bad Request",
                    "content":{
                        "application/json":{
                            "schema":{
                                "$ref":"#/components/schemas/ErrorModel"
                            },
                            "examples":{
                                "LOGIN_BAD_CREDENTIALS":{
                                    "summary":"Bad credentials or the user is inactive.",
                                    "value":{
                                        "detail":"LOGIN_BAD_CREDENTIALS"
                                    }
                                },
                                "LOGIN_USER_NOT_VERIFIED":{
                                    "summary":"The user is not verified.",
                                    "value":{
                                        "detail":"LOGIN_USER_NOT_VERIFIED"
                                    }
                                }
                            }
                        }
                    }
                },
                "422":{
                    "description":"Validation Error",
                    "content":{
                        "application/json":{
                            "schema":{
                                "$ref":"#/components/schemas/HTTPValidationError"
                            }
                        }
                    }
                }
            }
        }
    },
    "/auth/jwt/logout":{
        "post":{
            "tags":["auth"],
            "summary":"Auth:Jwt.Logout",
            "operationId":"auth_jwt_logout_auth_jwt_logout_post",
            "responses":{
                "200":{
                    "description":"Successful Response",
                    "content":{
                        "application/json":{
                            "schema":{
                            }
                        }
                    }
                },
                "401":{
                    "description":"Missing token or inactive user."
                }
            },
            "security":[
                {
                    "OAuth2PasswordBearer":[]
                }
            ]
        }
    },
    "/auth/register":{
        "post":{
            "tags":["auth"],
            "summary":"Register:Register",
            "operationId":"register_register_auth_register_post",
            "requestBody":{
                "content":{
                    "application/json":{
                        "schema":{
                            "$ref":"#/components/schemas/UserCreate"
                        }
                    }
                },
                "required":true
            },
            "responses":{
                "201":{
                    "description":"Successful Response",
                    "content":{
                        "application/json":{
                            "schema":{
                                "$ref":"#/components/schemas/UserRead"
                            }
                        }
                    }
                },
                "400":{
                    "description":"Bad Request",
                    "content":{
                        "application/json":{
                            "schema":{
                                "$ref":"#/components/schemas/ErrorModel"
                            },
                            "examples":{
                                "REGISTER_USER_ALREADY_EXISTS":{
                                    "summary":"A user with this email already exists.",
                                    "value":{
                                        "detail":"REGISTER_USER_ALREADY_EXISTS"
                                    }
                                },
                                "REGISTER_INVALID_PASSWORD":{
                                    "summary":"Password validation failed.",
                                    "value":{
                                        "detail":{
                                            "code":"REGISTER_INVALID_PASSWORD",
                                            "reason":"Password should beat least 3 characters"
                                        }
                                    }
                                }
                            }
                        }
                    }
                },
                "422":{
                    "description":"Validation Error",
                    "content":{
                        "application/json":{
                            "schema":{
                                "$ref":"#/components/schemas/HTTPValidationError"
                            }
                        }
                    }
                }
            }
        }
    },
    "/users/me":{
        "get":{
            "tags":["users"],
            "summary":"Users:Current User",
            "operationId":"users_current_user_users_me_get",
            "responses":{
                "200":{
                    "description":"Successful Response",
                    "content":{
                        "application/json":{
                            "schema":{
                                "$ref":"#/components/schemas/UserRead"
                            }
                        }
                    }
                },
                "401":{
                    "description":"Missing token or inactive user."
                }
            },
            "security":[
                {
                    "OAuth2PasswordBearer":[]
                }
            ]
        },
        "patch":{
            "tags":["users"],
            "summary":"Users:Patch Current User",
            "operationId":"users_patch_current_user_users_me_patch",
            "requestBody":{
                "content":{
                    "application/json":{
                        "schema":{
                            "$ref":"#/components/schemas/UserUpdate"
                        }
                    }
                },
                "required":true
            },
            "responses":{
                "200":{
                    "description":"Successful Response",
                    "content":{
                        "application/json":{
                            "schema":{
                                "$ref":"#/components/schemas/UserRead"
                            }
                        }
                    }
                },
                "401":{
                    "description":"Missing token or inactive user."
                },
                "400":{
                    "description":"Bad Request",
                    "content":{
                    "application/json":{
                        "schema":{
                            "$ref":"#/components/schemas/ErrorModel"
                        },
                        "examples":{
                            "UPDATE_USER_EMAIL_ALREADY_EXISTS":{
                                "summary":"A user with this email already exists.",
                                "value":{
                                    "detail":"UPDATE_USER_EMAIL_ALREADY_EXISTS"
                                }
                            },
                            "UPDATE_USER_INVALID_PASSWORD":{
                                "summary":"Password validation failed.",
                                "value":{
                                    "detail":{
                                        "code":"UPDATE_USER_INVALID_PASSWORD",
                                        "reason":"Password should beat least 3 characters"
                                    }
                                }
                            }
                        }
                    }
                }
            },
            "422":{
                "description":"Validation Error",
                "content":{
                    "application/json":{
                        "schema":{
                            "$ref":"#/components/schemas/HTTPValidationError"
                        }
                    }
                }
            }
        },
        "security":[
            {
                "OAuth2PasswordBearer":[]
            }
        ]
    }
},
"/users/{id}":{
    "get":{
        "tags":["users"],
        "summary":"Users:User",
        "operationId":"users_user_users__id__get",
        "security":[
            {
                "OAuth2PasswordBearer":[]
            }
        ],
        "parameters":[
            {
                "name":"id",
                "in":"path",
                "required":true,
                "schema":{
                    "type":"string",
                    "title":"Id"
                }
            }
        ],"responses":{
            "200":{
                "description":"Successful Response",
                "content":{
                    "application/json":{
                        "schema":{
                            "$ref":"#/components/schemas/UserRead"
                        }
                    }
                }
            },
            "401":{
                "description":"Missing token or inactive user."
            },
            "403":{
                "description":"Not a superuser."
            },
            "404":{
                "description":"The user does not exist."
            },
            "422":{
                "description":"Validation Error",
                "content":{
                    "application/json":{
                        "schema":{
                            "$ref":"#/components/schemas/HTTPValidationError"
                        }
                    }
                }
            }
        }
    },
    "patch":{
        "tags":["users"],
        "summary":"Users:Patch User",
        "operationId":"users_patch_user_users__id__patch",
        "security":[
            {
                "OAuth2PasswordBearer":[]
            }
        ],
        "parameters":[
            {
                "name":"id",
                "in":"path",
                "required":true,
                "schema":{
                    "type":"string",
                    "title":"Id"
                }
            }
        ],
        "requestBody":{
            "required":true,
            "content":{
                "application/json":{
                    "schema":{
                        "$ref":"#/components/schemas/UserUpdate"
                    }
                }
            }
        },
        "responses":{
            "200":{
                "description":"Successful Response",
                "content":{
                    "application/json":{
                        "schema":{
                            "$ref":"#/components/schemas/UserRead"
                        }
                    }
                }
            },
            "401":{
                "description":"Missing token or inactive user."
            },
            "403":{
                "description":"Not a superuser."
            },
            "404":{
                "description":"The user does not exist."
            },
            "400":{
                "content":{
                    "application/json":{
                        "examples":{
                            "UPDATE_USER_EMAIL_ALREADY_EXISTS":{
                                "summary":"A user with this email already exists.",
                                "value":{
                                    "detail":"UPDATE_USER_EMAIL_ALREADY_EXISTS"
                                }
                            },
                            "UPDATE_USER_INVALID_PASSWORD":{
                                "summary":"Password validation failed.",
                                "value":{
                                    "detail":{
                                        "code":"UPDATE_USER_INVALID_PASSWORD",
                                        "reason":"Password should beat least 3 characters"
                                    }
                                }
                            }
                        },
                        "schema":{
                            "$ref":"#/components/schemas/ErrorModel"
                        }
                    }
                },
                "description":"Bad Request"
            },
            "422":{
                "description":"Validation Error",
                "content":{
                    "application/json":{
                        "schema":{
                            "$ref":"#/components/schemas/HTTPValidationError"
                        }
                    }
                }
            }
        }
    },
    "delete":{
        "tags":["users"],
        "summary":"Users:Delete User",
        "operationId":"users_delete_user_users__id__delete",
        "security":[
            {
                "OAuth2PasswordBearer":[]
            }
        ],
        "parameters":[
            {
                "name":"id",
                "in":"path",
                "required":true,
                "schema":{
                    "type":"string",
                    "title":"Id"
                }
            }
        ],"responses":{
            "204":{
                "description":"Successful Response"
            },
            "401":{
                "description":"Missing token or inactive user."
            },
            "403":{
                "description":"Not a superuser."},
            "404":{
                "description":"The user does not exist."
            },
            "422":{
                "description":"Validation Error",
                "content":{
                    "application/json":{
                        "schema":{
                            "$ref":"#/components/schemas/HTTPValidationError"
                        }
                    }
                }
            }
        }
    }
},"/train":{
    "post":{
        "tags":["train"],
        "summary":"Train",
        "description":"Initiate training of room-specific ML models for all rooms in data source.\n\nCalls the `training_flow` function as a async background task.\n\n**NOTE**: Authentication is required for this endpoint.\n\nArgs:\n\n    request: Request: FastAPI Request object. Not used, but kept for FastAPI\n        dependency injection.\n\n    background_tasks: FastAPI BackgroundTasks for running functions in the\n        background.\n\n    session: SQLAlchemy Session object for database interactions\n        (injected via FastAPI's dependency system).\n\nReturns:\n\n    dict: A dictionary containing a message indicating that the training\n        sequence has been initialized.\n\nExamples:\n    ```bash\n    curl -X POST http://localhost:8000/train\n    ```\n\n    This will initiate the training sequence and return:\n\n    ```json\n    {\n\"message\": \"Training sequence initialized\"\n    }\n    ```",
            "operationId":"train_train_post",
            "responses":{
                "200":{
                    "description":"Successful Response",
                    "content":{
                        "application/json":{
                            "schema":{}
                        }
                    }
                }
            },
            "security":[
                {
                    "OAuth2PasswordBearer":[]
                }
            ]
        }
    },
    "/predict/":{
        "post":{
        "tags":["predict"],
        "summary":"Predict",
        "description":"Initiatie prediction of room-specific ML models for all rooms in data source.\nThe endpoint triggers a process to retrieve the unscored rooms, scores them\nusing the designated room-specific machine learning model, and stores the\nscored data back into the database.\n\nCalls the `prediction_flow` function as a async background task.\n\n**NOTE**: Authentication is required for this endpoint.\n\nArgs:\n\n    request: The FastAPI request object. This argument is currently not used.\n\n    session (Session, optional): SQLAlchemy session. Defaults to a new\n        session from `get_session`.\n\n    model_registry (ModelRegistry, optional): ML model registry. Defaults to\n        the current model from `get_current_registry`.\n\nReturns:\n\n    dict: A message indicating the completion status of the scoring sequence.\n\n\nExamples:\n    ```bash\n    curl -X POST http://localhost:8000/predict/\n    ```\n\nOutput:\n    ```json\n    {\n        \"message\": \"Scoring sequence completed.\"\n    }\n    ```","operationId":"predict_predict__post","responses":{
            "200":{
                "description":"Successful Response",
                "content":{
                    "application/json":{
                        "schema":{
                            "additionalProperties":{
                                "type":"string"
                            },
                            "type":"object",
                            "title":"Response Predict Predict  Post"
                        }
                    }
                }
            }
        },
        "security":[
            {
                "OAuth2PasswordBearer":[]
            }
        ]
    }
},
"/heartbeat/":{
    "get":{
        "tags":["heartbeat"],
        "summary":"Heartbeat",
        "description":"Heartbeat Endpoint for Health Check and Versioning.\n\nThis route returns a JSON object containing the current version of the service.\nThe version information is retrieved from an environment variable, `GIT_METADATA`,\nwhich is set during a GitHub Actions job.\n\nArgs:\n\n    request (Request): The FastAPI request object. This argument is ignored but\n        included for potential future use.\n\nReturns:\n\n    dict: A dictionary containing the version information, with key \"version\" and\n        value as the short version of the git hash of the last commit.\n\n\nExamples:\n\n    ```bash\n    curl http://localhost:8000/heartbeat/\n    ```\n\nOutput:\n\n    ```json\n    {\n        \"version\": \"abc123\"  # The git hash short version\n    }\n    ```\n\nNote:\n\n    The `GIT_METADATA` environment variable must be set, usually during a\n    GitHub Actions job, for this endpoint to return accurate version information.\n    If run locally, the version will be set to \"local\".",
        "operationId":"heartbeat_heartbeat__get",
        "responses":{
            "200":{
                "description":"Successful Response",
                "content":{
                    "application/json":{
                        "schema":{
                            "type":"object",
                            "title":"Response Heartbeat Heartbeat  Get"
                        }
                    }
                }
            }
        }
    }
}
},
"components":{
    "schemas":{
        "BearerResponse":{
            "properties":{
                "access_token":{
                    "type":"string",
                    "title":"Access Token"
                },
                "token_type":{
                    "type":"string",
                    "title":"Token Type"
                }
            },
            "type":"object",
            "required":[
                "access_token",
                "token_type"
            ],
            "title":"BearerResponse"
        },
        "Body_auth_jwt_login_auth_jwt_login_post":{
            "properties":{
                "grant_type":{
                    "anyOf":[
                        {
                            "type":"string",
                            "pattern":"password"
                        },
                        {
                            "type":"null"
                        }
                    ],
                    "title":"Grant Type"
                },
                "username":{
                    "type":"string",
                    "title":"Username"
                },
                "password":{
                    "type":"string",
                    "title":"Password"
                },
                "scope":{
                    "type":"string",
                    "title":"Scope",
                    "default":""
                },
                "client_id":{
                    "anyOf":[
                        {
                            "type":"string"
                        },
                        {
                            "type":"null"
                        }
                    ],
                    "title":"Client Id"
                },
                "client_secret":{
                    "anyOf":[
                        {
                            "type":"string"
                        },
                        {
                            "type":"null"
                        }
                    ],
                    "title":"Client Secret"
                }
            },
            "type":"object",
            "required":[
                "username",
                "password"
            ],
            "title":"Body_auth_jwt_login_auth_jwt_login_post"
        },
        "ErrorModel":{
            "properties":{
                "detail":{
                    "anyOf":[
                        {
                            "type":"string"
                        },
                        {
                            "additionalProperties":{
                                "type":"string"
                            },
                            "type":"object"
                        }
                    ],
                    "title":"Detail"
                }
            },
            "type":"object",
            "required":["detail"],
            "title":"ErrorModel"
        },
        "HTTPValidationError":{
            "properties":{
               "detail":{
                    "items":{
                        "$ref":"#/components/schemas/ValidationError"
                    },
                    "type":"array",
                    "title":"Detail"
                }
            },
            "type":"object",
            "title":"HTTPValidationError"
        },
        "UserCreate":{
            "properties":{
                "email":{
                    "type":"string",
                    "format":"email",
                    "title":"Email"},
                    "password":{
                        "type":"string",
                        "title":"Password"
                    },
                    "is_active":{
                        "anyOf":[
                            {
                                "type":"boolean"
                            },
                            {
                                "type":"null"
                            }
                        ],
                        "title":"Is Active",
                        "default":true
                    },
                    "is_superuser":{
                        "anyOf":[
                            {
                                "type":"boolean"
                            },
                            {
                                "type":"null"
                            }
                        ],
                        "title":"Is Superuser",
                        "default":false
                    },
                    "is_verified":{
                        "anyOf":[
                            {
                                "type":"boolean"
                            },
                            {
                                "type":"null"
                            }
                        ],
                        "title":"Is Verified",
                        "default":false
                    }
                },
                "type":"object",
                "required":[
                    "email",
                    "password"
                ],
                "title":"UserCreate",
                "description":"Schema for creating a new user. Extends the BaseUserCreate schema provided\nby FastAPI Users.\n\nAttributes:\n    Inherits all attributes from schemas.BaseUserCreate.\n\nExample:\n    >>> create_user = UserCreate(email=\"example@example.com\",\n    >>> password=\"example_password\")"
            },
            "UserRead":{
                "properties":{
                    "id":{
                        "title":"Id"
                    },
                    "email":{
                        "type":"string",
                        "format":"email",
                        "title":"Email"
                    },
                    "is_active":{
                        "type":"boolean",
                        "title":"Is Active",
                        "default":true
                    },
                    "is_superuser":{
                        "type":"boolean",
                        "title":"Is Superuser",
                        "default":false
                    },
                    "is_verified":{
                        "type":"boolean",
                        "title":"Is Verified",
                        "default":false
                    }
                },
                "type":"object",
                "required":[
                    "id",
                    "email"
                ],
                "title":"UserRead",
                "description":"Schema for reading user details. Extends the BaseUser schema provided\nby FastAPI Users.\n\nAttributes:\n    Inherits all attributes from schemas.BaseUser.\n\nExample:\n    >>> read_user = UserRead(email=\"example@example.com\",\n    >>> id=uuid.UUID(\"some-uuid\"))"
            },
            "UserUpdate":{
                "properties":{
                    "password":{
                        "anyOf":[
                            {
                                "type":"string"
                            },
                            {
                                "type":"null"
                            }
                        ],
                        "title":"Password"
                    },
                    "email":{
                        "anyOf":[
                            {
                                "type":"string",
                                "format":"email"
                            },
                            {
                                "type":"null"
                            }
                        ],
                        "title":"Email"
                    },
                    "is_active":{
                        "anyOf":[
                            {
                                "type":"boolean"
                            },
                            {
                                "type":"null"
                            }
                        ],
                        "title":"Is Active"
                    },
                    "is_superuser":{
                        "anyOf":[
                            {
                                "type":"boolean"
                            },
                            {
                                "type":"null"
                            }
                        ],
                        "title":"Is Superuser"
                    },
                    "is_verified":{
                        "anyOf":[
                            {
                                "type":"boolean"
                            },
                            {
                                "type":"null"
                            }
                        ],
                        "title":"Is Verified"
                    }
                },
                "type":"object",
                "required":[
                    "password",
                    "email",
                    "is_active",
                    "is_superuser",
                    "is_verified"
                ],
                "title":"UserUpdate",
                "description":"Schema for updating an existing user's details. Extends the\nBaseUserUpdate schema provided by FastAPI Users.\n\nAttributes:\n    Inherits all attributes from schemas.BaseUserUpdate.\n\nExample:\n    >>> update_user = UserUpdate(email=\"new_example@example.com\")"},
                "ValidationError":{
                    "properties":{
                        "loc":{
                            "items":{
                                "anyOf":[
                                    {
                                        "type":"string"
                                    },
                                    {
                                        "type":"integer"
                                    }
                                ]
                            },
                            "type":"array",
                            "title":"Location"
                        },
                        "msg":{
                            "type":"string",
                            "title":"Message"
                        },
                        "type":{
                            "type":"string",
                            "title":"Error Type"
                        }
                    },
                    "type":"object",
                    "required":[
                        "loc",
                        "msg",
                        "type"
                    ],
                    "title":"ValidationError"
                }
            },
            "securitySchemes":{
                "OAuth2PasswordBearer":{
                    "type":"oauth2",
                    "flows":{
                        "password":{
                            "scopes":{},
                            "tokenUrl":"auth/jwt/login"
                        }
                    }
                }
            }
        }
    }
```

