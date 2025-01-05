from azure.ai.projects import AIProjectClient

def create_thread(project_client: AIProjectClient):
    thread = project_client.agents.create_thread()
    return thread

def get_thread(project_client: AIProjectClient):
    thread = project_client.agents.get_thread()
    return thread

def delete_thread(project_client: AIProjectClient):
    project_client.agents.delete_thread()
    return "Deteted thread"
