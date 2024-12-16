import os
import json
import requests

from azureml.core import Workspace
from azureml.core.model import Model
from azureml.core.environment import Environment
from azureml.core.conda_dependencies import CondaDependencies
from azureml.core.model import InferenceConfig
from azureml.core.webservice import AciWebservice, Webservice

# laoding the configuration file - standard way - use .env file and load_dotenv from python-dotenv module
config_file_path = "config.json"

# Read JSON data into a dictionary
with open(config_file_path, 'r') as file:
    data = json.load(file)

subscription_id = data["subscription_id"]
resource_group = data["resource_group"]
workspace_name = data["workspace_name"]
region = data["region"]

# Create a workspace

ws = Workspace.create(name=workspace_name,
                      subscription_id=subscription_id,
                      resource_group=resource_group,
                      location=region)

print(f'Workspace {workspace_name} created')

# Specify the path to your  model file
model_path = 'diabetes_model.pkl'

model_name='diabetes_prediction_model'

# Register the model in Azure Machine Learning
registered_model = Model.register(model_path=model_path, model_name=model_name, workspace=ws)
# Create a Conda environment for your scikit-learn model
conda_env = Environment('my-conda-env')
conda_env.python.conda_dependencies = CondaDependencies.create(conda_packages=['scikit-learn'])
# Create an InferenceConfig
inference_config = InferenceConfig(entry_script='score.py', environment=conda_env)
# Specify deployment configuration for ACI
aci_config = AciWebservice.deploy_configuration(cpu_cores=1, memory_gb=1)
service = Model.deploy(workspace=ws,
                       name='diabetes-prediction-service',
                       models=[registered_model],
                       inference_config=inference_config,
                       deployment_config=aci_config)
service.wait_for_deployment(show_output=True)

scoring_uri = service.scoring_uri

print("scoring_uri", scoring_uri)