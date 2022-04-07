from fastapi import FastAPI, Request
import os
import json

from google.cloud import workflows_v1beta
from google.cloud.workflows import executions_v1beta
from google.cloud.workflows.executions_v1beta.types import Execution

app = FastAPI()


@app.post("/")
async def execute_workflow(event_request: Request):
    
    project = os.environ.get('GOOGLE_CLOUD_PROJECT')
    location = os.environ.get('WORKFLOW_LOCATION')
    workflow = os.environ.get('WORKFLOW_NAME')
    
    source = event_request.headers.get('ce-subject')
    tab_element_source = source.split("/")
    workflows_argument = {"serviceName": tab_element_source[-1]}

    """Execute a workflow and print the execution results."""
    # [START workflows_api_quickstart]

    # Set up API clients.
    execution_client = executions_v1beta.ExecutionsClient()
    workflows_client = workflows_v1beta.WorkflowsClient()

    # Construct the fully qualified location path.
    parent = workflows_client.workflow_path(project, location, workflow)

    # Execute the workflow.
    execution = Execution(argument = json.dumps(workflows_argument))
    # response = execution_client.create_execution(request={"parent": parent})
    response = execution_client.create_execution(parent=parent, execution=execution)

    return "The workflow has been launched successfully"
