from decouple import config
from credential_classes import AzureDevOpsCredentials, TenableCredentials
from vulnerability_fetch import fetch_vulnerabilities
from azure_devops_create import create_ado_work_items

# Tenable API credentials
tenable_credentials = TenableCredentials(
    access_key=config('TENABLE_ACCESS_KEY'),
    secret_key=config('TENABLE_SECRET_KEY'),
    base_url="https://cloud.tenable.com"
)

# Azure DevOps API credentials
ado_credentials = AzureDevOpsCredentials(
    organization=config('ADO_ORGANIZATION'),
    project=config('ADO_PROJECT'),
    personal_access_token=config('ADO_PERSONAL_ACCESS_TOKEN')
)

# Define the filter parameters for critical severity vulnerabilities
filter_params = [
    {"filter": "severity", "quality": "eq", "value": "Critical"}
]

# Fetch vulnerabilities and create Azure DevOps work items
vulnerabilities_data = fetch_vulnerabilities(tenable_credentials, filter_params)
create_ado_work_items(tenable_credentials, ado_credentials, vulnerabilities_data, filter_params)
