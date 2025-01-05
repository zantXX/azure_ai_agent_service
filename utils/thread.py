from azure.ai.projects import AIProjectClient
from azure.ai.projects.models import FileSearchTool, VectorStoreDataSource, VectorStoreDataSourceAssetType
from azure.identity import DefaultAzureCredential

def create_thread(project_client: AIProjectClient):
    thread = project_client.agents.create_thread()
    return thread
