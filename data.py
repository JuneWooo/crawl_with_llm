import io
import requests
import datetime
from loguru import logger
import asyncio
import json
from bs4 import BeautifulSoup
from langchain_core.output_parsers import StrOutputParser
from langchain_community.chat_models import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_community.document_loaders import FireCrawlLoader
from langchain_community.document_loaders import SpiderLoader



class TaliLLM(ChatOpenAI):
    openai_api_base = f"http://192.168.11.199:1282/v1"
    openai_api_key = "123456"
    model_name = "gpt-4"


prompt = ChatPromptTemplate.from_template(
    """
### 背景
你是一名公司规模50人左右的行政专员，主要负责从政策网站的通知公告中筛选符合公司申报的项目，现在我提供了政策网站的通知公告。

### 通知公告
{context}

### 目标
筛查出关于中小型公司申报项目的通知公告。

### 受众
主要受众是公司的行政人员查看，请针对该群体在选择申报项目时的典型关注点来定制内容。

### 响应
保持内容的简洁而具有影响力。
"""
)
llm = TaliLLM()
parser = StrOutputParser()
chain = prompt | llm | parser


td = datetime.datetime.today().strftime("%Y-%m-%d")


def fetch_and_parse_notice_details(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}

    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            text = str()
            soup = BeautifulSoup(response.text, 'html.parser')

            # 假设我们想提取公告的标题和发布时间，这里需要根据实际页面结构调整选择器
            # 请根据实际页面结构调整选择器
            title = soup.find('div', class_='c-content-title').text
            content = soup.find('div', id="content").text  # 同样需要根据实际页面调整

            # 打印或保存提取的信息
            print(f"Title: {title}")
            print(f"Content: {content}")
            text = title + "\n" + content

            for res in chain.stream({
                "context": text
            }):
                print(res, end="", flush=True)
            # 根据需要提取其他信息，如正文、附件等
        else:
            print(
                f"Failed to retrieve notice details, status code: {response.status_code}")
    except Exception as e:
        print(f"An error occurred fetching notice details: {e}")


def fetch_notices(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}

    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            res_info = {}
            soup = BeautifulSoup(response.text, 'html.parser')

            # 假设通知公告链接包含在特定的标签中，这里以<a>标签的class或id为例，请根据实际网页结构调整选择器
            # body > div.c-newslist-container.hidden-xs.hidden-sm > div > div > div.c-newslist-content-right > div:nth-child(2)
            notice_links = soup.select(
                'div.c-newslist-content-right > div')  # 请替换为实际的选择器

            td = "2024-05-27"
            # 取时间
            for div in notice_links:
                tag_time = div.div.text
                tag_name = div.a.text
                tag_url = div.a.get("href")
                if td in tag_time:
                    res_info[tag_time] = f"{tag_name}=>{tag_url}"

            if res_info:
                print(f"今日头条:{res_info}")
            else:
                print(f"{td} 未更更新通知公告")
            # 在这里可以进一步处理每个链接，比如访问详情页获取更多信息

            for k, v in res_info.items():
                url = v.split("=>")[-1]
                fetch_and_parse_notice_details(url)
                time.sleep(1)

        else:
            print(
                f"Failed to retrieve content, status code: {response.status_code}")
    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    import time
    # url_
    base_url = "http://gxt.shaanxi.gov.cn/webfile/tzgg/"
    fetch_notices(base_url)
