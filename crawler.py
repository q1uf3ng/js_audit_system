import aiohttp
import asyncio
from urllib.parse import urljoin, urlparse
import re


class JSCrawler:
    def __init__(self):
        self.session = None
        self.found_js_files = {}

    async def crawl_js_files(self, base_url: str) -> dict:
        self.found_js_files = {}

        async with aiohttp.ClientSession() as self.session:
            # 首先获取主页HTML
            html_content = await self.fetch_url(base_url)
            if html_content:
                # 从HTML中提取JS文件链接
                await self.extract_js_from_html(base_url, html_content)

        return self.found_js_files

    async def fetch_url(self, url: str) -> str:
        try:
            async with self.session.get(url, timeout=10) as response:
                return await response.text()
        except Exception as e:
            print(f"获取 {url} 失败: {e}")
            return ""

    async def extract_js_from_html(self, base_url: str, html: str):
        # 查找script标签
        script_pattern = r'<script[^>]*src=["\']([^"\']+\.js[^"\']*)["\']'
        js_links = re.findall(script_pattern, html, re.IGNORECASE)

        for js_link in js_links:
            full_js_url = urljoin(base_url, js_link)

            js_content = await self.fetch_url(full_js_url)
            if js_content:
                js_name = js_link.split('/')[-1] or f"script_{len(self.found_js_files)}.js"
                self.found_js_files[js_name] = js_content
                print(f"找到JS文件: {js_name}")