"""报告导出器 - Markdown / JSON / 日志 / 摘要 / ZIP"""

import json
import os
import zipfile


class ReportExporter:
    def __init__(self, output_dir='output'):
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)

    def _to_markdown(self, report):
        md = f"""# NEXUS 前沿科技日报 — {report['date']}

> 生成时间: {report['generated_at']}  |  总耗时: {report['elapsed']}s

## 全局洞察

{report['global_insight']}

## 统计概览

| 指标 | 数值 |
|------|------|
| 总采集 | {report['metadata']['total_collected']} |
| A类可信度 | {report['metadata']['grade_a']} |
| B类可信度 | {report['metadata']['grade_b']} |
| C类可信度 | {report['metadata']['grade_c']} |
| 高影响力 | {report['metadata']['high_impact']} |
| 上升趋势 | {report['metadata']['up_trend']} |
| 跨域关联 | {report['metadata']['cross_domain_links']} |

## TOP 推荐

"""
        for pick in report['top_picks']:
            md += f"""### #{pick['rank']} {pick['title']}
- **来源**: {pick['source']} | **可信度**: {pick['grade']} ({pick['credibility']*100:.0f}%)
- **趋势**: {pick['trend']} | **影响**: {pick['impact']} | **优先级**: {pick['priority']}
- **洞察**: {pick['insight']}

"""

        md += "## 领域详情\n\n"
        for sec in report['sections']:
            md += f"### {sec['label']} ({len(sec['items'])}条)\n\n"
            md += f"> {sec['digest']}\n\n"
            for item in sec['items']:
                md += f"- **[{item['grade']}]** {item['title']} — {item['insight']}\n"
            md += "\n"

        if report['cross_domain_links']:
            md += "## 跨领域关联\n\n"
            for link in report['cross_domain_links']:
                md += f"- **{link['tag']}**: {link['description']}\n"
                for it in link['items']:
                    md += f"  - {it['title']} ({it['category']})\n"
                md += "\n"

        return md

    def _to_json(self, report):
        return json.dumps(report, ensure_ascii=False, indent=2)

    def _to_log(self, logs):
        lines = []
        for entry in logs:
            if hasattr(entry, 'time_str') and hasattr(entry, 'agent_type') and hasattr(entry, 'agent') and hasattr(entry, 'level') and hasattr(entry, 'message'):
                lines.append(f"[{entry.time_str}] [{entry.agent_type}/{entry.agent}] {entry.level.upper()}: {entry.message}")
        return "\n".join(lines)

    def _to_summary(self, report):
        lines = [
            f"NEXUS 日报摘要 — {report['date']}",
            "=" * 40,
            report['global_insight'],
            "",
            "TOP 推荐:",
        ]
        for pick in report['top_picks'][:3]:
            lines.append(f"  #{pick['rank']} {pick['title'][:40]}...")
        lines.append("")
        dist_parts = [f"{s['label']}({len(s['items'])}条)" for s in report['sections']]
        lines.append(f"领域分布: {', '.join(dist_parts)}")
        return "\n".join(lines)

    def _readme(self):
        return """# NEXUS 日报输出说明

- NEXUS日报_YYYY-MM-DD.md   : 完整Markdown日报
- NEXUS日报_YYYY-MM-DD.json : 结构化JSON数据
- Agent日志_YYYY-MM-DD.txt  : Agent操作日志
- 摘要版_YYYY-MM-DD.txt     : 纯文本快速阅读版
"""

    def export(self, report, logs):
        date = report['date']
        base = f"NEXUS日报_{date}"

        files = {
            f'{base}.md': self._to_markdown(report),
            f'{base}.json': self._to_json(report),
            f'Agent日志_{date}.txt': self._to_log(logs),
            f'摘要版_{date}.txt': self._to_summary(report),
            'README.md': self._readme(),
        }

        for fname, content in files.items():
            path = os.path.join(self.output_dir, fname)
            with open(path, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"  已写入: {path}")

        zip_path = os.path.join(self.output_dir, f'{base}.zip')
        with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zf:
            for fname, content in files.items():
                zf.writestr(f"NEXUS_{date}/{fname}", content.encode('utf-8'))
        return zip_path
