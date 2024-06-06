import gradio as gr
from langchain_community.chat_models import ChatOpenAI
from transformers import load_tool, ReactCodeAgent, Tool
from gradio_agentchatbot import AgentChatbot, stream_from_transformers_agent
# from dotenv import load_dotenv
from web_base import ChatMessage, ThoughtMetadata
from langchain.agents import load_tools

# to load SerpAPI key  ChatMessage
# load_dotenv()


class TaliLLM(ChatOpenAI):
    openai_api_base = f"http://192.168.11.199:1282/v1"
    openai_api_key = "123456"
    model_name = "gpt-4"


# Import tool from Hub
image_generation_tool = load_tool("m-ric/text-to-image")

# def bing_search(ThoughtMetadata):
#     pass


# search_tool = bing_search()
# search_tool = Tool.from_langchain(load_tools(["serpapi"])[0])

# llm_engine = HfEngine("meta-llama/Meta-Llama-3-70B-Instruct")
# Initialize the agent with both tools


# class RequestApi(ThoughtMetadata):
#     tool_name: str = "request_tali_api"

#     def __init__(self):
#         self.name = self.tool_name

#     def req():
#         pass


# call_api = RequestApi()

llm_engine = TaliLLM()

agent = ReactCodeAgent(
    tools=[image_generation_tool], llm_engine=llm_engine)


def interact_with_agent(prompt, messages):
    messages.append(ChatMessage(role="user", content=prompt))
    yield messages
    for msg in stream_from_transformers_agent(agent, prompt):
        messages.append(msg)
        yield messages
    yield messages


with gr.Blocks(title="LN-Crawl Data Platform") as demo:
    chatbot = AgentChatbot(label="Agent")
    text_input = gr.Textbox(lines=1, label="Chat Message")
    text_input.submit(interact_with_agent, [text_input, chatbot], [chatbot])


if __name__ == "__main__":
    demo.launch(debug=True)
