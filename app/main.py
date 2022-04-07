# Copyright 2021 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from fastapi import FastAPI, Request, HTTPException
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
