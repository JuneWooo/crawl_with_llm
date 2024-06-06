
import argparse
import gradio as gr
from utils import ApiRequest


def predict(message, history):
    api = ApiRequest()
    r = api.spider_notify(message, history)
    for t in r:
        yield t


iface = gr.ChatInterface(
    fn=predict,  # 实现输入输出的函数
    chatbot=gr.Chatbot(height=530),
    theme="soft",
    textbox=gr.Textbox(
        placeholder="Ask me a yes or no question", container=False, scale=7),
    title="LingNeng Platform",
    description="Tali LN Crawl Data V0.1",
    examples=["采集数据"],  # gradio直接给设计了examples这个属性
).queue()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--host", type=str, default="0.0.0.0")
    parser.add_argument("--port", type=int, default=7860)

    args = parser.parse_args()
    # logger.info(f"args: {args}")

    iface.launch(
        server_name=args.host,
        server_port=args.port,
        max_threads=200
    )
