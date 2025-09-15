# Project name used for resource naming
project_name = "dprzek-vertex2"

# Your Production Google Cloud project id
prod_project_id = "dprzek-prod"

# Your Staging / Test Google Cloud project id
staging_project_id = "dprzek-stage"

# Your Google Cloud project ID that will be used to host the Cloud Build pipelines.
cicd_runner_project_id = "dprzek-vertex"
# Name of the host connection you created in Cloud Build
host_connection_name = "test-cicd"

# Name of the repository you added to Cloud Build
repository_name = "dprzek-agent_puc"

# The Google Cloud region you will use to deploy the infrastructure
region = "us-central1"

github_pat_secret_id = "github_pat"

create_cb_connection = true