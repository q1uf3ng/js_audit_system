import asyncio
import os
import re
from crawler import JSCrawler
from auditor import JSAuditor
from reporter import ReportGenerator
from config import DEEPSEEK_API_KEY


class JSAuditSystem:
    def __init__(self, api_key: str):
        self.crawler = JSCrawler()
        self.auditor = JSAuditor(api_key)
        self.reporter = ReportGenerator()

    async def audit_website(self, website_url: str):
        print(f"开始审计网站: {website_url}")

        #爬取所有JS文件
        print("正在爬取JS文件...")
        js_files = await self.crawler.crawl_js_files(website_url)
        print(f"找到 {len(js_files)} 个JS文件")

        # 为每个站点创建独立目录
        domain = self.clean_domain_name(website_url)
        site_results_dir = f"results/{domain}"
        os.makedirs(site_results_dir, exist_ok=True)


        audit_results = []
        for js_name, js_content in js_files.items():
            print(f"正在审计: {js_name}")

            # 调用DeepSeek审计单个JS文件
            result = await self.auditor.audit_single_js(js_name, js_content)
            audit_results.append(result)
            print(f"完成审计: {js_name}")

            await asyncio.sleep(1)

        site_report_file = f"{site_results_dir}/网站安全审计报告.md"
        self.reporter.generate_site_report(website_url, audit_results, site_report_file)
        print(f"网站审计报告已生成: {site_report_file}")

        return audit_results

    def clean_domain_name(self, url: str) -> str:
        domain = url.replace('https://', '').replace('http://', '').split('/')[0]
        domain = domain.split()[0] if ' ' in domain else domain
        domain = re.sub(r'[<>:"/\\|?*]', '_', domain)
        return domain


def load_websites_from_txt(file_path: str) -> list:
    websites = []
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line:
                    cleaned_url = clean_url(line)
                    if cleaned_url:
                        websites.append(cleaned_url)
    except FileNotFoundError:
        print(f"错误: 找不到文件 {file_path}")
    return websites


def clean_url(url: str) -> str:
    # 匹配http/https开头的URL，遇到空格或异常字符就停止
    match = re.match(r'(https?://[^\s<>"{}\|\\^`\[\]]+)', url)
    if match:
        clean_url = match.group(1)
        if '.' in clean_url.replace('https://', '').replace('http://', ''):
            return clean_url
    return None


async def main():
    system = JSAuditSystem(DEEPSEEK_API_KEY)

    websites = load_websites_from_txt("websites.txt")

    if not websites:
        print("没有找到有效的网站URL，请检查websites.txt文件")
        print("请确保每行只有一个完整的URL，例如: https://example.com")
        return

    print(f"找到 {len(websites)} 个有效网站需要审计")
    for i, website in enumerate(websites, 1):
        print(f"{i}. {website}")
    print()

    for website in websites:
        await system.audit_website(website)
        print(f"完成网站 {website} 的审计\n")


if __name__ == "__main__":
    asyncio.run(main())