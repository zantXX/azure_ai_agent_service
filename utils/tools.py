import os
from azure.ai.projects import AIProjectClient
from azure.ai.projects.models import FileSearchTool, VectorStoreDataSource, VectorStoreDataSourceAssetType, FilePurpose
from azure.ai.projects.models import CodeInterpreterTool
from azure.ai.projects.models import BingGroundingTool
from azure.ai.projects.models import AzureAISearchTool
from azure.ai.projects.models import FunctionTool, ToolSet, Tool
from ..files.user_functions import fetch_weather
from typing import Any, Callable, Set, Dict, List, Optional
from pathlib import Path

def code_interpreter_tool(file=None):
    return CodeInterpreterTool(file_ids=[file.id])

def download_interpretter_file(project_client: AIProjectClient, messages, downloads_folder: str):
    # save the newly created file
    for image_content in messages.image_contents:
        file_name = f"{downloads_folder}/{image_content.image_file.file_id}_image_file.png"
        project_client.agents.save_file(file_id=image_content.image_file.file_id, file_name=file_name)
        print(f"Saved image file to: {Path.cwd() / downloads_folder / file_name}") 

def bing_grounding_tool(project_client: AIProjectClient):
    bing_connection = project_client.connections.get(
        connection_name=os.getenv(["BING_CONNECTION_NAME"],"")
    )
    conn_id = bing_connection.id

    # Initialize agent bing tool and add the connection id
    return BingGroundingTool(connection_id=conn_id)

# https://learn.microsoft.com/ja-jp/azure/ai-services/agents/how-to/tools/bing-grounding?tabs=python&pivots=overview#how-to-display-grounding-with-bing-search-results
def get_bing_reference(project_client: AIProjectClient, run_id: str, thread_id: str):
    run_steps = project_client.agents.list_run_steps(run_id=run_id, thread_id=thread_id)
    run_steps_data = run_steps['data']
    return f"Last run step detail: {run_steps_data}"

def basic_file_search_upload(project_client: AIProjectClient, file_path: str, vector_name: str):
    #upload a file
    file = project_client.agents.upload_file_and_poll(file_path=file_path, purpose=FilePurpose.AGENTS)

    # create a vector store with the file you uploaded
    vector_store = project_client.agents.create_vector_store_and_poll(file_ids=[file.id], name=vector_name)
    return vector_store

def enterprise_file_search_upload(project_client: AIProjectClient, file_path: str, vector_name: str):
    # We'll upload the local file to your project Azure Blob Storage container and will use it for vector store creation.
    _, asset_uri = project_client.upload_file(file_path)

    # create a vector store with a file in blob storage and wait for it to be processed
    # ここが動かない
    ds = VectorStoreDataSource(asset_identifier=asset_uri, asset_type=VectorStoreDataSourceAssetType.URI_ASSET)
    vector_store = project_client.agents.create_vector_store_and_poll(data_sources=[ds], name=vector_name)
    return vector_store

def file_search_tool(vector_store_id: str):
    return FileSearchTool(vector_store_ids=[vector_store_id])

def delete_file(project_client: AIProjectClient, file):
    project_client.agents.delete_file(file.id)
    return "Deleted file"

def delete_vector_store(project_client: AIProjectClient, vector_store):
    project_client.agents.delete_vector_store(vector_store.id)
    return "Deleted vector store"

def get_azure_ai_search_connection(project_client: AIProjectClient):
    conn_list = project_client.connections.list()
    conn_id = ""
    for conn in conn_list:
        if conn.connection_type == "CognitiveSearch":
            conn_id = conn.id
            break
    return conn_id
        
def azure_ai_search_tool(conn_id: str, index_name: str):
    ai_search = AzureAISearchTool()
    ai_search.add_index(conn_id, index_name)
    return ai_search

# 独自関数の定義
def myfunction_calling():
    user_functions: Set[Callable[..., Any]] = {
        fetch_weather,
    }
    # Initialize agent toolset with user functions
    functions = FunctionTool(user_functions)
    return functions
    
def create_toolset(fuctions:List[Tool]):
    toolset = ToolSet()
    for tool in fuctions:
        toolset.add(tool)
    return toolset

def get_all_connections(project_client: AIProjectClient):
    return project_client.connections.list()