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
    location = os.environ.get('GOOGLE_CLOUD_LOCATION')
    workflow = os.environ.get('WORKFLOW_NAME')
    
    source = event_request.headers.get('ce-subject')
    tab_element_source = source.split("/")
    workflows_argument = {"serviceName": tab_element_source[-1]}
    print(workflows_argument)
    print(tab_element_source[-1])
    """Execute a workflow and print the execution results."""
    # [START workflows_api_quickstart]

    # TODO(developer): Uncomment these lines and replace with your values.
    # project = 'my-project-id'
    # location = 'us-central1'
    # workflow = 'myFirstWorkflow'

    # if not (project and location and workflow):
    #     raise HTTPException(status_code=500, detail="GOOGLE_CLOUD_PROJECT, GOOGLE_CLOUD_LOCATION, WORKFLOW_NAME env var are required.")
  
    # Set up API clients.
    execution_client = executions_v1beta.ExecutionsClient()
    workflows_client = workflows_v1beta.WorkflowsClient()

    # Construct the fully qualified location path.
    parent = workflows_client.workflow_path(project, location, workflow)

    # Execute the workflow.
    execution = Execution(argument = json.dumps(workflows_argument))
    # response = execution_client.create_execution(request={"parent": parent})
    response = execution_client.create_execution(parent=parent, execution=execution)

    return "The workflow has been launched successfully", response.name

    # # Wait for execution to finish, then print results.
    # execution_finished = False
    # backoff_delay = 1  # Start wait with delay of 1 second
    # print('Poll every second for result...')
    # while (not execution_finished):
    #     execution = execution_client.get_execution(request={"name": response.name})
    #     execution_finished = execution.state != executions.Execution.State.ACTIVE

    #     # If we haven't seen the result yet, wait a second.
    #     if not execution_finished:
    #         print('- Waiting for results...')
    #         time.sleep(backoff_delay)
    #         backoff_delay *= 2  # Double the delay to provide exponential backoff.
    #     else:
    #         print(f'Execution finished with state: {execution.state.name}')
    #         print(execution.result)
    #         return execution.result
    # # [END workflows_api_quickstart]
