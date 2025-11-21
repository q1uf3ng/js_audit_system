js_audit_system



本工具是一款AI驱动的js自动化审计工具，它能够自动爬取目标URL列表中的js文件，并利用AI进行审计，以识别诸如XSS等非静态常规安全漏洞，帮助渗透测试项目或SRC项目中快速定位攻击面并产出报告。



项目结构

```
js_audit_system/
├── main.py
├── crawler.py
├── auditor.py
├── reporter.py          
├── config.py
├── websites.txt
├── results/
│   ├── unionback.youdao.com/
│   │   └── 网站安全审计报告.md    
│   └── union.youdao.com/
│       └── 网站安全审计报告.md    
└── requirements.txt
```



使用：

复制你的url到websites.txt

```
pip install -r  requirements.txt
python3 main.py
```



tips:现在txt可以自动提取里面的http/s 你不需要把他格式化放入 随意粘贴就行



todo:

考虑要不要加静态第一波审计

优化审计报告



运行图(以目前来看消耗的token钱数忽略不计)



