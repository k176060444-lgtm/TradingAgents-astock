"""llm_timeout / llm_max_retries 透传回归测试（#300705 静默卡死兜底）。

风险辩论节点内同步 llm.invoke() 曾缺少超时保护：provider 请求挂起时节点永不返回，
进程 alive 但静默卡死（无超时、无异常、无 traceback）。补丁把 llm_timeout /
llm_max_retries 经 _get_provider_kwargs → _PASSTHROUGH_KWARGS 透传给客户端，
让请求超时后抛异常而非永久等待。
"""

import pytest

from tradingagents.default_config import DEFAULT_CONFIG
from tradingagents.graph import trading_graph as tg
from tradingagents.llm_clients.openai_client import OpenAIClient


def _graph_with(config):
    graph = tg.TradingAgentsGraph.__new__(tg.TradingAgentsGraph)
    graph.config = config
    return graph


@pytest.mark.unit
class TestProviderKwargsTimeout:
    def test_timeout_and_max_retries_are_forwarded(self):
        g = _graph_with({"llm_timeout": 120, "llm_max_retries": 0})
        kw = g._get_provider_kwargs()
        assert kw["timeout"] == 120
        assert kw["max_retries"] == 0

    def test_max_retries_zero_is_not_dropped(self):
        # max_retries=0 是合法值（不重试）。用 falsy 判断会丢它，必须 is not None。
        g = _graph_with({"llm_max_retries": 0})
        assert g._get_provider_kwargs()["max_retries"] == 0

    def test_absent_keys_are_backward_compatible(self):
        # 没配这两个键时不得返回 None 值，维持原行为。
        g = _graph_with({"max_tokens": 8000})
        kw = g._get_provider_kwargs()
        assert "timeout" not in kw
        assert "max_retries" not in kw


@pytest.mark.unit
class TestTimeoutReachesClient:
    def test_timeout_reaches_chatopenai(self, monkeypatch):
        monkeypatch.setenv("OPENAI_COMPATIBLE_API_KEY", "k")
        client = OpenAIClient(
            "m", base_url="https://relay.example/v1", provider="openai_compatible",
            timeout=120, max_retries=0,
        )
        llm = client.get_llm()
        # langchain 内部把 timeout 映射为 request_timeout 字段。
        assert llm.request_timeout == 120.0
        assert llm.max_retries == 0


@pytest.mark.unit
class TestDefaultConfig:
    def test_default_config_ships_timeout(self):
        # 默认值必须落在 DEFAULT_CONFIG，而非只依赖用户 config.py 覆盖。
        assert DEFAULT_CONFIG["llm_timeout"] == 120
        assert DEFAULT_CONFIG["llm_max_retries"] == 0
