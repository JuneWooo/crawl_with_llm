

from typing import List
import requests
from loguru import logger
from bs4 import BeautifulSoup, UnicodeDammit
from app.utils.run_in_thread import run_in_thread_pool
from app.config.config import settings


def tlspider(urls: List[str]):
    """
    多线程批量处理
    """
    def crawl_html(url, sub_urls) -> list:
        """
        解析单个网页
        """
        try:
            response = requests.get(url, headers=settings.headers)
            if response.status_code == 200:
                response.encoding = 'utf-8'  # 或者根据实际情况指定正确的编码
                html_content = response.text
                dammit = UnicodeDammit(html_content)
                soup = BeautifulSoup(dammit.unicode_markup, 'html.parser')
                a_tags = soup.find_all('a', href=True)
                for a_tag in a_tags:
                    a_href = a_tag["href"]
                    if "tzgg" in a_href and "index" not in a_href and a_href not in sub_urls:
                        # sub_urls.append(urljoin(url, a_href))
                        filter_ = "1.html", "2.html", "3.html"
                        if a_href.endswith(filter_):
                            continue

                        if url == "https://xdz.xa.gov.cn/xwzx/tzgg/1.html" and "https://" not in a_href and "list" not in a_href:
                            join_url = "".join(
                                ["https://xdz.xa.gov.cn", a_href])
                            sub_urls.append(join_url)
                        elif url == "http://scjg.xa.gov.cn/xwzx/tzgg/1.html" and "http://" not in a_href and "list" not in a_href:
                            join_url = "".join(
                                ["http://scjg.xa.gov.cn", a_href])

                            sub_urls.append(join_url)
                        elif url in ["http://gxt.shaanxi.gov.cn/webfile/tzgg/", "https://shxca.miit.gov.cn/xwzx/tzgg/"]:
                            sub_urls.append(a_href)
                            logger.info(f"通知公告的url:{a_href}")
                return sub_urls

        except requests.RequestException as e:
            sub_urls.append("not found sub url")
            print(f'Failed to retrieve {url}. Error: {e}')
            return sub_urls

    params = [{"url": url, "sub_urls": []} for url in urls]
    for result in run_in_thread_pool(crawl_html, params=params):
        yield result
