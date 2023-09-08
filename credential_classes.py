class AzureDevOpsCredentials:
    def __init__(self, organization, project, personal_access_token):
        self.organization = organization
        self.project = project
        self.personal_access_token = personal_access_token

class TenableCredentials:
    def __init__(self, access_key, secret_key, base_url):
        self.access_key = access_key
        self.secret_key = secret_key
        self.base_url = base_url
