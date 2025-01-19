from agent import create_agent, list_agents, get_agent, delete_agent
from tools import create_toolset, code_interpreter_tool, file_search_tool, bing_grounding_tool, myfunction_calling, basic_file_search_upload, enterprise_file_search_upload
from thread import delete_thread, create_thread
from azure.ai.projects import AIProjectClient
from pathlib import Path
from typing import List
from azure.ai.projects.models import VectorStore
import gradio as gr

def create_agent_gradio(project_client: AIProjectClient, model:str, agent_name:str, agent_instructions:str, temperature:float, topP:float, file_search:bool, file_search_type:str, file_search_file:List[VectorStore], codeInterpreter:bool, codeInterpreter_file:List[VectorStore], bing:bool, function_calling:bool, function_calling_fuctions:List[str]):
    func_list = []

    if file_search:
        file_search_log, file_search_vector_stores = upoload_files()
        func_list.append(file_search_tool([vector.id for vector in file_search_vector_stores]))
    if codeInterpreter:
        codeInterpreter_log, codeInterpreter_vector_stores = upoload_files()
        func_list.append(code_interpreter_tool([vector.id for vector in codeInterpreter_vector_stores]))
    if bing:
        func_list.append(bing_grounding_tool(project_client))
    if function_calling:
        function_calling_fuctions
        func_list.append(myfunction_calling())
    
    toolsets = create_toolset(func_list)
    agent = create_agent(project_client, model=model,
        name=agent_name,
        instructions=agent_instructions,
        toolset=toolsets,temperature=temperature, top_p=topP)
    return "Created Agent",  file_search_vector_stores, file_search_log, codeInterpreter_vector_stores, codeInterpreter_log, gr.Dropdown(list_agents(project_client), value=agent.id, label="Agent ID")

def select_agent(project_client: AIProjectClient, agent_id:str):
    agent = get_agent(project_client, agent_id)
    return agent.instructions, agent.__dict__

def delete_agent_gradio(project_client: AIProjectClient, agent_id:str):
    delete_agent(project_client, agent_id)
    return "Deleted Agent", gr.Dropdown(list_agents(project_client), label="Agent ID")

def upoload_file(project_client, file_path, isEnterprise=False):
    vector_name = Path(file_path).name
    if isEnterprise:
        return f"complete upload file:{file_path}", enterprise_file_search_upload(project_client, file_path, vector_name)
    else:
        return f"complete upload file:{file_path}", basic_file_search_upload(project_client, file_path, vector_name)

def upoload_files(project_client, file_paths, isEnterprise=False):
    vector_stores = []
    logs = []
    for file_path in file_paths:
        log, vector_store = upoload_file(project_client, file_path, isEnterprise)
        vector_stores.append(vector_store)
        logs.append(log)
    return logs.join("\n"), vector_stores

def delete_thread_gradio(project_client: AIProjectClient, thread_id:str, threads:List[str]):
    threads.remove(thread_id)
    return delete_thread(project_client, thread_id), gr.Dropdown(threads, label="Agent ID"), threads

def create_thread_gradio(project_client: AIProjectClient, threads:List[str]):
    thread = create_thread(project_client)
    threads.append(thread.id)
    return "create thread", gr.Dropdown(threads, label="Thread ID"), threads