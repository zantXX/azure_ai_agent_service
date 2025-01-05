from azure.ai.projects import AIProjectClient
from typing import Literal
from pathlib import Path
from azure.ai.projects.models import MessageAttachment

def create_message(project_client: AIProjectClient, thread_id: str, role: Literal["user", "assistant"], content: str):
    message = project_client.agents.create_message(
        thread_id=thread_id,
        role=role,
        content=content,
    )
    return message

def create_message_with_file(project_client: AIProjectClient, thread_id: str, role: Literal["user", "assistant"], content: str, messaage_file:str = None, tools=None):
    attachment = MessageAttachment(file_id=messaage_file.id, tools=tools.definitions)
    message = project_client.agents.create_message(
        thread_id=thread_id,
        role=role,
        content=content,
        attachments=[attachment]
    )
    return message

def create_and_process_run(project_client: AIProjectClient, thread_id: str, agent_id: str):
    run = project_client.agents.create_and_process_run(
        thread_id=thread_id,
        agent_id=agent_id,
    )
    if run.status == "failed":
        # Check if you got "Rate limit is exceeded.", then you want to get more quota
        print(f"Run failed: {run.last_error}")
    return run

def list_messages(project_client: AIProjectClient, thread_id: str):
    messages = project_client.agents.list_messages(thread_id=thread_id)
    return messages

def get_last_text_message_by_sender(messages, sender="assistant"):
    return messages.get_last_text_message_by_sender(sender)

def get_last_image_content(project_client, messages):
    # Generate an image file for the bar chart
    for image_content in messages.image_contents:
        print(f"Image File ID: {image_content.image_file.file_id}")
        file_name = f"{image_content.image_file.file_id}_image_file.png"
        project_client.agents.save_file(file_id=image_content.image_file.file_id, file_name=file_name)
        print(f"Saved image file to: {Path.cwd() / file_name}")

def get_file_path_annotations(project_client, messages):
    # Print the file path(s) from the messages
    for file_path_annotation in messages.file_path_annotations:
        print(f"File Paths:")
        print(f"Type: {file_path_annotation.type}")
        print(f"Text: {file_path_annotation.text}")
        print(f"File ID: {file_path_annotation.file_path.file_id}")
        print(f"Start Index: {file_path_annotation.start_index}")
        print(f"End Index: {file_path_annotation.end_index}")
        project_client.agents.save_file(file_id=file_path_annotation.file_path.file_id, file_name=Path(file_path_annotation.text).name)