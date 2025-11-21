import aiohttp
import json
import time


class JSAuditor:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.api_url = "https://api.deepseek.com/v1/chat/completions"
        self.headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}"
        }

    async def audit_single_js(self, js_name: str, js_content: str) -> dict:

        truncated_content = js_content[:6000] if len(js_content) > 6000 else js_content

        prompt = f"""
请严格按以下格式分析这个JavaScript文件的安全漏洞，如果存在漏洞请给出20行上下午代码片，如果存在xss给出url和接口调用，没有则不存在：

文件名称
{js_name}

风险概览
[高危/中危/低危/无风险]

详细漏洞分析

1. 信息泄露风险
- [具体风险描述]
- [位置：行号或函数名]
- [风险等级：高/中/低]

2. XSS漏洞
- [具体风险描述]  
- [位置：行号或函数名]
- [风险等级：高/中/低]

3. 接口安全问题
- [具体风险描述]
- [位置：行号或函数名]
- [风险等级：高/中/低]

4. 其他安全问题
- [具体风险描述]
- [位置：行号或函数名]
- [风险等级：高/中/低]

修复建议
[具体的修复方案]

需要审计的JavaScript代码：
{truncated_content}

注意：请只分析上述代码，不要引用其他上下文。
"""

        payload = {
            "model": "deepseek-chat",
            "messages": [
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            "temperature": 0.1,
            "max_tokens": 2000
        }

        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    self.api_url,
                    headers=self.headers,
                    json=payload,
                    timeout=30
                ) as response:

                    if response.status == 200:
                        result = await response.json()
                        return {
                            "js_name": js_name,
                            "content_length": len(js_content),
                            "audit_result": result["choices"][0]["message"]["content"],
                            "status": "success",
                            "timestamp": time.time()
                        }
                    else:
                        return {
                            "js_name": js_name,
                            "audit_result": f"API调用失败: {response.status}",
                            "status": "failed",
                            "timestamp": time.time()
                        }

        except Exception as e:
            return {
                "js_name": js_name,
                "audit_result": f"审计出错: {str(e)}",
                "status": "error",
                "timestamp": time.time()
            }