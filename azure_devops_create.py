import base64
import requests
import click

# ANSI escape codes for text color
RED = '\033[91m'
RESET = '\033[0m'

def create_ado_work_items(tenable_credentials, ado_credentials, vulnerabilities_data, filter_params):
    total_assets = len(vulnerabilities_data['assets'])
    created_count = 0  # Counter for created work items

    # Initialize the progress bar message
    progress_message = f"Azure DevOps work items: {created_count}/{total_assets}"

    # Create a progress bar using Click
    with click.progressbar(vulnerabilities_data['assets'], label=progress_message, length=total_assets) as assets:
        for asset in assets:
            asset_id = asset['id']

            # Fetch asset details including plugin information for each asset
            asset_info_url = f"{tenable_credentials.base_url}/workbenches/assets/{asset_id}/vulnerabilities?"
            for idx, filter_param in enumerate(filter_params):
                asset_info_url += f"filter.{idx}.filter={filter_param['filter']}&filter.{idx}.quality={filter_param['quality']}&filter.{idx}.value={filter_param['value']}"

            asset_info_response = requests.get(asset_info_url, headers={
                "X-ApiKeys": f"accessKey={tenable_credentials.access_key}; secretKey={tenable_credentials.secret_key}"
            })

            if asset_info_response.status_code == 200:
                asset_info_data = asset_info_response.json()

                # Define the work item title based on the asset information and vulnerability state
                vulnerability_state = "Unknown"  # Default value
                for vulnerability in asset_info_data['vulnerabilities']:
                    if 'vulnerability_state' in vulnerability:
                        vulnerability_state = vulnerability['vulnerability_state']
                        break

                work_item_title = f"Vulnerability ({vulnerability_state}) on Asset ID: {asset_id}"
                work_item_description = f"Asset ID: {asset_id}\n"

                # Iterate through the vulnerability data and extract plugin information
                for vulnerability in asset_info_data['vulnerabilities']:
                    plugin_info = {
                        "Plugin ID": vulnerability['plugin_id'],
                        "Plugin Name": vulnerability['plugin_name'],
                        "Plugin Family": vulnerability['plugin_family']
                    }
                    work_item_description += (
                        f"<div>Plugin ID: {plugin_info['Plugin ID']}<div>"
                        f"Plugin Name: {plugin_info['Plugin Name']}<div>"
                        f"Plugin Family: {plugin_info['Plugin Family']}<div>\n"
                    )

                # Create the work item payload
                work_item_payload = [
                    {
                        "op": "add",
                        "path": "/fields/System.Title",
                        "value": work_item_title
                    },
                    {
                        "op": "add",
                        "path": "/fields/System.Description",
                        "value": work_item_description
                    }
                ]

                # Create a base64-encoded personal access token
                token_bytes = f":{ado_credentials.personal_access_token}".encode('utf-8')
                token_base64 = base64.b64encode(token_bytes).decode('utf-8')

                # Set the request headers (including authorization)
                headers = {
                    "Content-Type": "application/json-patch+json",
                    "Authorization": f"Basic {token_base64}"
                }

                create_work_item_url = f"https://dev.azure.com/{ado_credentials.organization}/{ado_credentials.project}/_apis/wit/workitems/$Task?api-version=7.1"

                # Create the work item using the Azure DevOps REST API
                response = requests.post(
                    create_work_item_url,
                    json=work_item_payload,
                    headers=headers
                )

                created_count += 1

                if response.status_code == 200:
                    # Update the progress bar message
                    progress_message = f"Azure DevOps work items: {created_count}/{total_assets}"
                    assets.label = progress_message  # Update the label
                else:
                    # Update the progress bar message with an error message
                    progress_message = f"{RED}Azure DevOps work items: {created_count}/{total_assets} - Failed{RESET}"
                    assets.label = progress_message  # Update the label
                    click.secho(f" - Response Content: {response.text}", fg='red', nl=False)
            else:
                # Update the progress bar message with an error message
                progress_message = f"{RED}Azure DevOps work items: {created_count}/{total_assets} - Failed{RESET}"
                assets.label = progress_message  # Update the label
                click.secho(f" - Failed to fetch asset details for Asset ID: {asset_id}", fg='red', nl=False)
        