# Azure DevOps Work Item Creation from Tenable Data

## Overview

This document provides detailed information on the process of creating Azure DevOps work items (tasks) from Tenable vulnerability data. The integration aims to streamline the tracking of critical vulnerabilities identified by Tenable within an Azure DevOps project.

## Architecture

![Architecture](img\architecture.png)

## Prerequisites
Before proceeding, ensure that the following prerequisites are met:

**Tenable API Credentials:**

- Tenable Access Key
- Tenable Secret Key
- Tenable API Base URL (e.g., https://cloud.tenable.com)

**Azure DevOps Credentials:**

- Azure DevOps Organization
- Azure DevOps Project
- Personal Access Token (PAT) with the necessary permissions

These credentials must be added to a .env file so the python script can access it, as shown below:

TENABLE_ACCESS_KEY=[]
TENABLE_SECRET_KEY=[]
BASE_URL=https://cloud.tenable.com
ADO_ORGANIZATION=[]
ADO_PROJECT=[]
ADO_PERSONAL_ACCESS_TOKEN=[]

## Workflow

The integration workflow can be summarized as follows:

### Python Script:

- Initiates the integration process.
- Calls API Endpoint 1 to fetch vulnerability data from Tenable.

### API Endpoint 1 (Tenable):

- Receives the request from the Python script.
- Retrieves vulnerability data from Tenable.

### Python Script:

- Processes the vulnerability data.
- Loops through assets with critical vulnerabilities.
- For each asset:
    - Calls API Endpoint 2 to retrieve asset details.
    - Creates a work item (task) in Azure DevOps based on asset information.

### API Endpoint 2 (Tenable):

- Receives the request from the Python script.
- Retrieves asset details, including plugin information, from Tenable.

### Azure DevOps:

- Creates a work item based on the received information.
- Returns a response indicating whether the work item creation was successful or encountered an error.


## Configuration

In the Python script (azure_devops_tenablesync.py), configure the following variables:

- Tenable API Credentials
- Azure DevOps API Credentials
- Tenable API Filter Parameters
- Azure DevOps Project-specific details (e.g., work item type)

### Error Handling

In case of errors during the integration process, appropriate error messages will be displayed, and the process will continue for other assets.

## Conclusion

This documentation outlines the process of integrating Tenable vulnerability data with Azure DevOps work item creation. Following the provided guidelines and configuring the script correctly will enable efficient tracking and management of critical vulnerabilities within your Azure DevOps project.