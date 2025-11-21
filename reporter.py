import time
import os


class ReportGenerator:
    def generate_site_report(self, website: str, audit_results: list, output_file: str):
        with open(output_file, 'w', encoding='utf-8') as f:
            # 报告头部
            f.write("# 网站安全审计报告\n\n")
            f.write("## 基本信息\n")
            f.write(f"- **目标网站**: {website}\n")
            f.write(f"- **生成时间**: {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"- **审计JS文件数**: {len(audit_results)}\n\n")

            success_count = sum(1 for r in audit_results if r['status'] == 'success')
            failed_count = sum(1 for r in audit_results if r['status'] == 'failed')
            error_count = sum(1 for r in audit_results if r['status'] == 'error')

            f.write("## 审计统计\n")
            f.write(f"- **成功审计**: {success_count} 个文件\n")
            f.write(f"- **失败审计**: {failed_count} 个文件\n")
            f.write(f"- **错误审计**: {error_count} 个文件\n\n")

            f.write("## 详细审计结果\n\n")

            for i, result in enumerate(audit_results, 1):
                f.write(f"### {i}. {result['js_name']}\n")
                f.write(f"- **文件大小**: {result.get('content_length', 'N/A')} 字符\n")
                f.write(f"- **审计状态**: {result['status']}\n")
                f.write(
                    f"- **审计时间**: {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(result['timestamp']))}\n\n")

                f.write("#### 审计结果:\n")
                f.write("```\n")
                f.write(result['audit_result'])
                f.write("\n```\n\n")

                f.write("---\n\n")

            # 风险汇总
            f.write("## 风险汇总\n")
            f.write("> 注：以上为所有JS文件的详细审计结果，请重点关注高风险和中风险问题。\n")