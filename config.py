"""系统配置 - 数据源开关与领域标签"""

SOURCE_CONFIG = [
    {'id': 'ai',            'name': '人工智能', 'enabled': True, 'weight': 1.0},
    {'id': 'biotech',       'name': '生物科技', 'enabled': True, 'weight': 1.0},
    {'id': 'quantum',       'name': '量子计算', 'enabled': True, 'weight': 0.8},
    {'id': 'energy',        'name': '新能源',   'enabled': True, 'weight': 0.8},
    {'id': 'space',         'name': '航天科技', 'enabled': True, 'weight': 0.7},
    {'id': 'semiconductor', 'name': '半导体',   'enabled': True, 'weight': 0.8},
]

CATEGORY_LABELS = {
    'ai': '人工智能',
    'biotech': '生物科技',
    'quantum': '量子计算',
    'energy': '新能源',
    'space': '航天科技',
    'semiconductor': '半导体',
}
