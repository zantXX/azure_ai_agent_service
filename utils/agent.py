from azure.ai.projects import AIProjectClient
def create_agent(project_client: AIProjectClient, model:str, name:str, instructions:str, tools=None, tool_resources=None, toolsets=None, temperature=0.2, top_p=0.2, headers={"x-ms-enable-preview": "true"}):
    agent = project_client.agents.create_agent(
        model=model,
        name=name,
        instructions=instructions,
        tools=tools,
        tool_resources=tool_resources,
        toolset=toolsets,
        temperature=temperature,
        top_p=top_p,
        headers=headers,
    )
    return agent

def delete_agent(project_client: AIProjectClient, agent_id: str):
    # Delete the agent once done
    project_client.agents.delete_agent(agent_id)
    return "deleted agent"

def list_agents(project_client: AIProjectClient):
    agents = project_client.agents.list_agents(order="desc")
    return agents