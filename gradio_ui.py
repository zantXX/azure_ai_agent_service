import os
import gradio as gr
from azure.ai.projects import AIProjectClient
from azure.identity import DefaultAzureCredential
from dotenv import load_dotenv
import json
from .utils.gradio_functions import create_agent, select_agent

def greet(name):
    return "Hello " + name + "!"

def create_UI():
    project_client = AIProjectClient.from_connection_string(
        credential=DefaultAzureCredential(),
        conn_str=os.environ["PROJECT_CONNECTION_STRING"],
    )
    with gr.Blocks() as demo:
        client = gr.State(project_client)
        with gr.Row():
            with gr.Column():
                gr.Markdown("Create Agent")
                model = gr.Dropdown(json.loads(os.getenv("MODELS",'["NOT LOADED ENV FILE"]')), label="model")
                agent_name = gr.Textbox(label="agent name")
                agent_instructions = gr.TextArea(label="instructions")
                temperature = gr.Slider(0, 1, value=os.getenv("TEMPERATURE",0.2), label="Temperature", info="決定論的な応答を行う確率")
                topP = gr.Slider(0, 1, value=os.getenv("TOP_P",0.2), label="TopP", info="確率の高いトークンを優先")
                gr.Markdown("tools setting")
                with gr.Group():
                    file_search = gr.Checkbox(label="file search", info="")
                    file_search_type = gr.Radio(["basic", "enterprise(not worked)"], value="basic", label="search type")
                    file_search_file = gr.File()
                    file_search_log = gr.Textbox(label="log")
                """
                # Azure AI Search
                with gr.Group():
                    function_calling = gr.Checkbox(label="Azure AI Search", info="")
                    gr.CheckboxGroup(["hotel search", "weather"], label="funcitons")
                """
                with gr.Group():
                    codeInterpreter = gr.Checkbox(label="Code Interperter", info="")
                    codeInterpreter_file = gr.File()
                    codeInterpreter_log = gr.Textbox(label="log")
                with gr.Group():
                    bing = gr.Checkbox(label="Bing Grounding search", info="")
                with gr.Group():
                    function_calling = gr.Checkbox(label="Function Calling", info="")
                    function_calling_fuctions = gr.CheckboxGroup(["hotel search", "weather"], label="funcitons")
                button_createAgent = gr.Button("Create Agent", variant="primary")
                button_createAgent.click(fn=create_agent, inputs=[client, model, agent_name, agent_instructions, temperature, topP, file_search, file_search_type, file_search_file, codeInterpreter, codeInterpreter_file, bing, function_calling, function_calling_fuctions], outputs=[overall_log, agent])

            with gr.Column():
                gr.Markdown("Select Agent and chat")
                agent = gr.Dropdown(["asst hQFC6d4izGSzirHJluWnQSOH", "agentid"], label="Agent ID")
                agent.change(select_agent, )
                agent_instructions_reprica = gr.TextArea(label="instructions")
                agent_setting = gr.JSON(label="Patameta")
                gr.Dropdown(["thread", "agentid"], label="thread id")
                gr.Button("new chat")
                gr.ChatInterface(
                    greet, type="messages",
                )
        with gr.Row():
            with gr.Column():
                overall_log = gr.TextArea(label="Log")
    demo.launch()

if __name__ == "__main__":
    load_dotenv(verbose=True)
    create_UI()