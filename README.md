# Enformanten / GovTech Midtjylland - Smart M<sup>2</sup>

Enformanten is an energy saving tool for getting insights into energy usage (Distrinct Heating & Electricity) as well as analyzing room/booking usage on public schools/buildings. The project has developed two main parts: Analytics & AI.

# Analytics

The analytics part of the project has leveraged an existing platform built by NTT DATA to ingest, transform and visualize data in dashboards. This has resulted in an overall dashboard with pages for getting insights into several views on energy usage spanding from vacation closing of buildings to the usage of energy in passive hours. 

The main output is data pipelines, transformations and a Power Bi Report

![Overview](./docs/analytics/frontend/assets/Overview.png)

# AI
The AI Room Utilization Model (Formally, Driftsoptimeringsmodellen in Danish) is a machine learning anomaly detection solution that uses sensor data to detect whether a given room has been in use (i.e. have had human activity) in a given time 15-minute time interval.

This functionality is wrapped in a FastAPI web application that exposes a REST API for querying the model. The model is deployed to Azure as a Docker container and is hosted on an Azure Web App - But the model can be deployed to any cloud provider that supports Docker containers.

[output-example](./docs/ai/assets/output-example.png)

**NOTE:** The AI booking system (The second AI component in the project) is not included in this repository but in a separate repository under this organization.
