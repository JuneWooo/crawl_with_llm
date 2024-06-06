import json
import asyncio
import time
from typing import AsyncIterable
from langchain.schema import AIMessage, HumanMessage
from app import logger
from app.config.config import settings
from app.utils.tali_spider import tlspider
from app.schemas.utils_chain import classify_chain, model
from langchain_community.document_loaders import AsyncHtmlLoader, AsyncChromiumLoader
# from langchain_community.document_transformers import Html2TextTransformer
from langchain_community.document_transformers import BeautifulSoupTransformer


class SpiderNotify:

    async def extra_info(self, message, history) -> AsyncIterable[str]:
        """
            :return: json str
        """
        data = []
        for human, ai in history:
            data.append(HumanMessage(content=human))
            data.append(AIMessage(content=ai))

        data.append(HumanMessage(content=message))

        if message == "采集数据":
            filer_urls = []
            urls = [str(url) for url in settings.CRAWL_URLS]
            for result in tlspider(urls):
                for url in result:
                    if not url.endswith(".html"):
                        continue
                    if url not in filer_urls:
                        filer_urls.append(url)

            logger.warning(f"所有的子链接:{filer_urls}")
            # load HTML
            loader = AsyncHtmlLoader(filer_urls)
            docs = loader.load()

            # html2text = Html2TextTransformer()
            # docs_transformed = html2text.transform_documents(docs)
            bs_transformer = BeautifulSoupTransformer()
            html2docs = bs_transformer.transform_documents(
                docs, tags_to_extract=["h1", "span", "a", "p"])

            filter_docs = [doc for doc in html2docs if doc.page_content != ""]
            idx = 0
            result = ""
            for doc in filter_docs:
                # 判断文章是否关于最近的中小企业扶助相关
                prompt_value = classify_chain.invoke(
                    {"context": doc.page_content})
                print("prompt_value", prompt_value)
                # 如果是，则总结概要文章内容，返回链接和标题
                if prompt_value == "符合":
                    idx += 1
                    result += f"**{idx}.{doc.metadata['title']}**  [详情]({doc.metadata['source']})<br>"
            
            for i in range(len(result)):
                yield json.dumps({"data": result[:i+1]}, ensure_ascii=False)
                await asyncio.sleep(0.01)
        else:
            gpt_response = model.invoke(data)
            for i in range(len(gpt_response.content)):
                yield json.dumps({
                    "data": gpt_response.content[:i+1]
                }, ensure_ascii=False)
                await asyncio.sleep(0.01)


spider_notify = SpiderNotify()
