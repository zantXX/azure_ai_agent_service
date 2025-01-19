import os
import gradio as gr
from azure.ai.projects import AIProjectClient
from azure.identity import DefaultAzureCredential
from dotenv import load_dotenv
import json
from utils.gradio_functions import create_agent_gradio, upoload_files, select_agent, delete_agent_gradio, delete_thread_gradio, create_thread_gradio
from utils.agent import list_agents

def create_UI():
    project_client = AIProjectClient.from_connection_string(
        credential=DefaultAzureCredential(),
        conn_str=os.environ["PROJECT_CONNECTION_STRING"],
    )
    list_agents = list_agents(project_client)
    #list_agent_ids = [agent.id for agent in list_agents.data]
    list_agent_ids = ["asst hQFC6d4izGSzirHJluWnQSOH", "agentid2"]
    thread_ids = gr.State(["threadid1", "agentid2"])
    with gr.Blocks() as demo:
        client = gr.State(project_client)
        file_search_vector_stores = gr.State([])
        codeInterpreter_vector_stores = gr.State([])
        with gr.Column():
            with gr.Accordion("Create Agent", open=False):
                gr.Markdown("Create Agent")
                model = gr.Dropdown(json.loads(os.getenv("MODELS",'["NOT LOADED ENV FILE"]')), label="model")
                agent_name = gr.Textbox(label="agent name")
                agent_instructions = gr.TextArea(label="instructions")
                temperature = gr.Slider(0, 1, value=os.getenv("TEMPERATURE",0.2), label="Temperature", info="決定論的な応答を行う確率")
                topP = gr.Slider(0, 1, value=os.getenv("TOP_P",0.2), label="TopP", info="確率の高いトークンを優先")
                gr.Markdown("tools setting")
                file_upload_type = gr.Radio(["basic", "enterprise(not worked)"], value="basic", label="search type")
                with gr.Group():
                    file_search = gr.Checkbox(label="file search", info="chatbot return about your submitted file")
                    file_search_file = gr.Files(type='filepath')
                    file_search_log = gr.Textbox(label="log")
                """
                # Azure AI Search
                with gr.Group():
                    function_calling = gr.Checkbox(label="Azure AI Search", info="")
                    gr.CheckboxGroup(["hotel search", "weather"], label="funcitons")
                """
                with gr.Group():
                    codeInterpreter = gr.Checkbox(label="Code Interperter")
                    codeInterpreter_file = gr.Files(type='filepath')
                    codeInterpreter_log = gr.Textbox(label="log")
                with gr.Group():
                    bing = gr.Checkbox(label="Bing Grounding search")
                with gr.Group():
                    function_calling = gr.Checkbox(label="Function Calling")
                    function_calling_fuctions = gr.CheckboxGroup(json.loads(os.getenv("MY_FUNCTIONS",'["NOT LOADED ENV FILE"]')), label="funcitons")
                button_createAgent = gr.Button("Create Agent", variant="primary")
                button_createAgent.click(
                    fn=create_agent_gradio,
                    inputs=[client, model, agent_name, agent_instructions, temperature, topP, file_search, file_upload_type, file_search_file, codeInterpreter, codeInterpreter_file, bing, function_calling, function_calling_fuctions],
                    outputs=[overall_log, file_search_vector_stores, file_search_log, codeInterpreter_vector_stores, codeInterpreter_log, agent_id])

            gr.Markdown("Select Agent and chat")
            agent_id = gr.Dropdown(list_agent_ids, label="Agent ID")
            agent_id.change(select_agent, inputs=[client, agent_id], outputs=[agent_instructions_reprica, agent_setting])
            agent_instructions_reprica = gr.TextArea(label="instructions")
            agent_setting = gr.JSON(label="Patameta")
            button_deleteAgent = gr.Button("delete agent")
            button_deleteAgent.click(fn=delete_agent_gradio, inputs=[client, agent_id], outputs=[overall_log, agent_id])
            threads = gr.Dropdown(thread_ids, label="thread id")
            with gr.Row():
                button_deleteThread = gr.Button("delete thread")
                button_deleteThread.click(fn=delete_thread_gradio, inputs=[client, threads, thread_ids],  outputs=[overall_log, threads, thread_ids])
                button_newThread = gr.Button("new thread", variant="primary")
                button_newThread.click(fn=create_thread_gradio , inputs=[client, thread_ids], outputs=[overall_log, threads, thread_ids])
            chat = gr.Chatbot(
                    label="Agent",
                    type="messages",
                )
            chat_input = gr.MultimodalTextbox("try chat to agent")
            chat_input.submit(
                add_message, [chat, chat_input], [chat, chat_input]
            )
            with gr.Accordion(label="console log", open=False):
                overall_log = gr.TextArea(label="Log")
    demo.launch()

def add_message(history, message):
    for x in message["files"]:
        history.append({"role": "user", "content": {"path": x}})
    if message["text"] is not None:
        history.append({"role": "user", "content": message["text"]})
    history = generate_response(history)
    return history, gr.MultimodalTextbox(value=None, interactive=False)

def generate_response(history):
    history.append(
        dict(role="assistant",
                    content="The weather API says it is 20 degrees Celcius in New York.",
                    metadata={"title": "🛠️ Used tool Weather API"})
        )
    return history

if __name__ == "__main__":
    load_dotenv(verbose=True)
    create_UI()