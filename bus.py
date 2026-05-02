"""Agent消息总线 - 发布/订阅模式，支持实时终端输出"""

import time


class LogEntry:
    __slots__ = ('agent', 'agent_type', 'level', 'message', 'timestamp')

    def __init__(self, agent, agent_type, level, message):
        self.agent = agent
        self.agent_type = agent_type
        self.level = level
        self.message = message
        self.timestamp = time.time()

    @property
    def time_str(self):
        return time.strftime('%H:%M:%S', time.localtime(self.timestamp))


class MessageBus:
    def __init__(self):
        self._subscribers = {}
        self.logs = []

    def publish(self, channel, **kwargs):
        entry = None
        if channel == 'agent-log':
            entry = LogEntry(
                agent=kwargs.get('agent', ''),
                agent_type=kwargs.get('agent_type', ''),
                level=kwargs.get('level', 'info'),
                message=kwargs.get('message', ''),
            )
            self.logs.append(entry)
        for cb in self._subscribers.get(channel, []):
            cb(entry or kwargs)
        for cb in self._subscribers.get('*', []):
            cb(entry or kwargs)

    def subscribe(self, channel, callback):
        self._subscribers.setdefault(channel, []).append(callback)

    def log(self, agent_name, agent_type, level, message):
        entry = LogEntry(agent_name, agent_type, level, message)
        self.logs.append(entry)
        icons = {'info': '○', 'warn': '△', 'error': '✕'}
        colors = {'info': '\033[90m', 'warn': '\033[33m', 'error': '\033[31m'}
        R = '\033[0m'
        D = '\033[90m'
        A = '\033[36m'
        C = colors.get(level, D)
        print(f"  {D}{entry.time_str}{R} {C}{icons.get(level, '○')}{R} {A}[{agent_type}]{R} {C}{message}{R}")
