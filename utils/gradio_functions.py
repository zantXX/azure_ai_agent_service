from .agent import create_agent, list_agents
from .tools import create_toolset, code_interpreter_tool, file_search_tool, bing_grounding_tool, myfunction_calling
from azure.ai.projects import AIProjectClient

def create_agent_gradio(project_client: AIProjectClient, model, agent_name, agent_instructions, temperature, topP, file_search, file_search_type, file_search_file, codeInterpreter, codeInterpreter_file, bing, function_calling, function_calling_fuctions):
    func_list = []

    if file_search:
        file_search_type
        file_search_file
        func_list.append(file_search_tool)
    if codeInterpreter:
        codeInterpreter_file
        func_list.append(code_interpreter_tool())
    if bing:
        func_list.append(bing_grounding_tool())
    if function_calling:
        function_calling_fuctions
        func_list.append(myfunction_calling())
    
    toolsets = create_toolset(func_list)
    agent = create_agent(project_client, model=model,
        name=agent_name,
        instructions=agent_instructions,
        toolset=toolsets,temperature=temperature, top_p=topP)
    return "Created Agent", list_agents(project_client)

def select_agent(client):
    pass