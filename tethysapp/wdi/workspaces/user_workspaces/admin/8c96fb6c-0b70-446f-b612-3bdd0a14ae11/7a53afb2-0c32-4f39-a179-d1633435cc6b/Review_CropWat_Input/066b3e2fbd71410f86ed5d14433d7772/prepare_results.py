#!/opt/tethys-python
import datetime
import json
import os
from pprint import pprint
import pandas as pd

from tethysext.atcore.services.file_database import FileCollectionClient, FileDatabaseClient


# DO NOT REMOVE, need to import all the subclasses of ResourceWorkflowStep for the polymorphism to work.
from tethysapp.wdi.models.resources.model_resource import WdiModelResource
from tethysext.atcore.models.resource_workflow_results import *  # noqa: F401, F403
from tethysext.atcore.models.resource_workflow_steps import *  # noqa: F401, F403
from tethysext.atcore.services.resource_workflows.decorators import workflow_step_job
# END DO NOT REMOVE


@workflow_step_job
def main(resource_db_session, model_db_session, resource, workflow, step, gs_private_url, gs_public_url, resource_class,
         workflow_class, params_json, params_file, cmd_args):
    pprint('Getting Flow Data...')
    # Parse out parameters
    parameters = params_json['Select CropWat Model and Update Model Input']['parameters']
    form_values = parameters['form-values']
    existing_model_id = form_values['existing_cropwat_model']

    # Get base ModelResource from selected base model
    existing_model = resource_db_session.query(WdiModelResource).get(existing_model_id)

    file_database_id = workflow.get_attribute('file_database_id')
    root_directory = workflow.get_attribute('linux_fdb_root')
    database_client = FileDatabaseClient(resource_db_session, root_directory, file_database_id)

    # Find file_collection with adh model files
    print('Retrieving cropwat data files...')
    for file_collection in existing_model.file_collections:
        collection_client = FileCollectionClient(resource_db_session, database_client, file_collection.id)
        for file in collection_client.files:
            if file.endswith('.csv'):
                cropwat_csv = os.path.join(collection_client.path, file)

    cropwat_table = pd.read_csv(cropwat_csv)
    report_result = step.result.get_result_by_codename('cropwat_table')
    report_result.reset()

    # Commit
    resource_db_session.commit()
    print(f'Successfully retrieved data and saved to file_database_id {file_database_id} ')