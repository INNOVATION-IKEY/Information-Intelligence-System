#!/usr/bin/env python3
"""NEXUS 多Agent前沿数据协调系统 - 入口"""

import argparse
import os
import sys
import time

from bus import MessageBus
from agents.coordinator import CoordinatorAgent
from config import SOURCE_CONFIG
from exporter import ReportExporter


def main():
    parser = argparse.ArgumentParser(description='NEXUS 多Agent前沿数据协调系统')
    parser.add_argument('--date', type=str, default=None, help='目标日期 YYYY-MM-DD')
    parser.add_argument('--list-dates', action='store_true', help='列出可用数据日期')
    parser.add_argument('--output', type=str, default='output', help='输出目录')
    args = parser.parse_args()

    from data.pool import DATA_SOURCE_POOL

    import re

    if not DATA_SOURCE_POOL:
        print("错误: 数据源为空")
        sys.exit(1)

    if args.list_dates:
        dates = sorted(DATA_SOURCE_POOL.keys())
        print("可用数据日期:")
        for d in dates:
            print(f"  {d} ({len(DATA_SOURCE_POOL[d])}条)")
        return

    if args.date and not re.match(r'^\d{4}-\d{2}-\d{2}$', args.date):
        print(f"错误: 日期格式不正确，请使用 YYYY-MM-DD 格式")
        sys.exit(1)

    target_date = args.date or (sorted(DATA_SOURCE_POOL.keys())[-1])

    if target_date not in DATA_SOURCE_POOL:
        print(f"错误: 日期 {target_date} 无可用数据")
        print(f"可用: {', '.join(sorted(DATA_SOURCE_POOL.keys()))}")
        sys.exit(1)

    bus = MessageBus()
    coordinator = CoordinatorAgent(bus)

    print("=" * 64)
    print("  NEXUS 多Agent前沿数据协调系统")
    print("=" * 64)
    print(f"  目标日期: {target_date}")
    enabled = [s['name'] for s in SOURCE_CONFIG if s['enabled']]
    print(f"  启用领域: {', '.join(enabled)}")
    print("=" * 64)
    print()

    t0 = time.time()
    report = coordinator.run_pipeline({'date': target_date})
    elapsed = time.time() - t0

    print()
    print("-" * 64)
    print("  导出报告")
    print("-" * 64)
    exporter = ReportExporter(args.output)
    zip_path = exporter.export(report, bus.logs)

    print(f"  总耗时: {elapsed:.1f}s")
    print(f"  输出目录: {os.path.abspath(args.output)}")
    print(f"  ZIP文件: {zip_path}")
    print()
    print("=" * 64)
    print("  NEXUS 管道执行完成")
    print("=" * 64)


if __name__ == '__main__':
    main()
