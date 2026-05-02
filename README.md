# NEXUS 多Agent前沿数据协调系统

基于多Agent架构的前沿科技日报生成系统，支持数据采集、验证、分析和综合报告生成。

## 功能特性

- **多领域覆盖**：人工智能、生物科技、量子计算、新能源、航天科技、半导体
- **数据验证**：自动去重、交叉验证、可信度评分（A/B/C三级）
- **长链路推理**：事实提取 → 因果链构建 → 趋势推断 → 影响评估 → 优先级排序
- **智能报告**：自动生成Markdown日报、JSON数据、摘要版和Agent日志

## 架构设计

```
┌─────────────────────────────────────────────────────────────┐
│                      NEXUS 协调系统                         │
├─────────────────────────────────────────────────────────────┤
│  CoordinatorAgent  ── 管道编排、状态管理、异常处理           │
├─────────────────────────────────────────────────────────────┤
│  执行管道:                                                  │
│    ScoutAgent    → 多源数据采集与结构化                      │
│    VerifierAgent → 去重、交叉验证、可信度评分                 │
│    AnalystAgent  → 4阶段长链路推理分析                       │
│    SynthesizerAgent → 领域分组、摘要生成、日报格式化          │
├─────────────────────────────────────────────────────────────┤
│  MessageBus      ── 发布/订阅模式，支持实时终端输出          │
└─────────────────────────────────────────────────────────────┘
```

## 快速开始

```bash
# 列出可用数据日期
python main.py --list-dates

# 生成最新日期的日报
python main.py

# 指定日期生成日报
python main.py --date 2025-01-15

# 指定输出目录
python main.py --output ./reports
```

## 输出文件

| 文件 | 说明 |
|------|------|
| `NEXUS日报_YYYY-MM-DD.md` | 完整Markdown日报 |
| `NEXUS日报_YYYY-MM-DD.json` | 结构化JSON数据 |
| `Agent日志_YYYY-MM-DD.txt` | Agent操作日志 |
| `摘要版_YYYY-MM-DD.txt` | 纯文本快速阅读版 |
| `NEXUS日报_YYYY-MM-DD.zip` | 打包压缩文件 |

## 项目结构

```
nexus-agent-system/
├── main.py              # 入口文件
├── config.py            # 系统配置
├── bus.py               # 消息总线
├── exporter.py          # 报告导出器
├── agents/
│   ├── __init__.py
│   ├── base.py          # 基础Agent抽象类
│   ├── coordinator.py   # 协调者Agent
│   ├── scout.py         # 侦察者Agent
│   ├── verifier.py      # 验证者Agent
│   ├── analyst.py       # 分析者Agent
│   └── synthesizer.py   # 综合者Agent
└── data/
    ├── __init__.py
    └── pool.py          # 数据源池（模拟数据）
```

## 技术栈

- Python 3.8+
- 标准库：argparse, json, zipfile, re

## 数据格式

每条数据源包含：
- `id` - 唯一标识
- `title` - 标题
- `source` - 来源
- `source_reliability` - 数据源可信度基线 (0-1)
- `category` - 领域分类
- `content` - 内容
- `importance` - 重要性等级
- `tags` - 标签列表

## License

MIT
