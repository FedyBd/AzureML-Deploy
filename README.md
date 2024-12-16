# Diabetes Prediction Model Deployment on Azure

This repository contains code to deploy a diabetes prediction model on **Azure Machine Learning (Azure ML)** using a Flask-based REST API. It includes instructions for setting up the Azure environment, required libraries, and deployment configurations.

## **Prerequisites**
Before running the code, ensure the following prerequisites are met:

1. **Python Installation:**
   - Python 3.6 or later.

2. **Azure Subscription:**
   - An active Azure account with a valid subscription.

3. **Azure ML SDK:**
   - Install the Azure ML SDK:
     ```bash
     pip install azureml-core azureml-sdk
     ```

4. **Other Required Libraries:**
   Install the following Python libraries:
   ```bash
   pip install requests python-dotenv scikit-learn
   ```

## **Steps to Configure Azure**
### 1. Create an Azure Subscription
   - If you don’t have an Azure subscription, you can [create one here](https://azure.microsoft.com/free/).

### 2. Create a Resource Group
   - A resource group is a container that holds related resources. Use the Azure portal or CLI:
     ```bash
     az group create --name <resource_group_name> --location <region>
     ```
     Replace `<resource_group_name>` and `<region>` with your desired resource group name and Azure region (e.g., `eastus`).

### 3. Create an Azure ML Workspace
   - Go to the [Azure portal](https://portal.azure.com/) and create a new **Machine Learning** workspace in your resource group. Alternatively, use the following CLI command:
     ```bash
     az ml workspace create -w <workspace_name> -g <resource_group_name>
     ```
     Replace `<workspace_name>` and `<resource_group_name>` with your desired names.

### 4. Obtain Configuration Details
   - From your Azure portal, note down the following details:
     - Subscription ID
     - Resource Group name
     - Workspace name
     - Region

### 5. Create a `config.json` File
   - Create a `config.json` file with your Azure configuration details:
     ```json
     {
       "subscription_id": "<your_subscription_id>",
       "resource_group": "<your_resource_group>",
       "workspace_name": "<your_workspace_name>",
       "region": "<your_region>"
     }
     ```
     Replace the placeholders with your actual values.

## **Code Overview**

The provided Python code performs the following steps:

1. **Load Configuration:**
   - Reads Azure credentials from the `config.json` file.

2. **Create Workspace:**
   - Creates a new Azure ML workspace (if it does not already exist).

3. **Register Model:**
   - Registers a machine learning model (`diabetes_model.pkl`) to the Azure ML workspace.

4. **Define Environment:**
   - Creates a Conda environment with dependencies (e.g., `scikit-learn`).

5. **Deploy Model:**
   - Deploys the model as a REST API using **Azure Container Instances (ACI)**.

6. **Retrieve Scoring URI:**
   - Outputs the scoring URI for consuming the deployed API.

## **Deployment Requirements**

### Model File:
- Place your trained model file (`diabetes_model.pkl`) in the root directory.

### Entry Script (`score.py`):
- Create a `score.py` file that includes the scoring logic for your model. An example structure:
  ```python
  import joblib
  import numpy as np
  from azureml.core.model import Model

  def init():
      global model
      model_path = Model.get_model_path('diabetes_prediction_model')
      model = joblib.load(model_path)

  def run(raw_data):
      data = np.array(json.loads(raw_data)['data'])
      result = model.predict(data)
      return result.tolist()
  ```

### Required Azure Services:
- **Azure Container Instances (ACI):**
  - Used for deploying the model as a REST API endpoint.

## **How to Run the Code**

1. Clone this repository:
   ```bash
   git clone <repository_url>
   cd <repository_folder>
   ```

2. Create a virtual environment and install dependencies:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. Place your `config.json` file in the root folder.

4. Run the Python script:
   ```bash
   python deploy_model.py
   ```

5. After successful deployment, the **scoring URI** will be printed. Use this URI to send HTTP requests for model predictions.

## **Consuming the Deployed API**
Use the `requests` library to send data to the scoring URI:

```python
import requests

url = "<scoring_uri>"
data = {"data": [[5, 116, 74, 0, 0, 25.6, 0.201, 30]]}  # Example input
response = requests.post(url, json=data)
print(response.json())
```

Replace `<scoring_uri>` with the URI returned after deployment.

## **Troubleshooting**

1. **Workspace Creation Error:**
   - Verify subscription ID, resource group, and region in `config.json`.

2. **Model Registration Error:**
   - Ensure `diabetes_model.pkl` exists in the specified path.

3. **Deployment Failure:**
   - Check logs using:
     ```python
     print(service.get_logs())
     ```

## **Future Improvements**
- Migrate to Azure Kubernetes Service (AKS) for production-grade deployments.
- Add authentication to the API.

---

Feel free to open issues or submit pull requests for any enhancements or bug fixes.

