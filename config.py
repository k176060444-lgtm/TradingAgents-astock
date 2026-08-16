"""TradingAgents-astock 角色模型配置（用户自定义）。

三个 provider:
  - minimax-cn:  astock 内置 provider "minimax"（中国区 api.minimaxi.com/v1）
  - opencode-go: 走 openai_compatible + backend_url + 角色级 api_key
  - cliproxy:    走 openai_compatible + backend_url + 角色级 api_key
"""
import os

# 从 .env 读取（不硬编码 key 明文）
MINIMAX_KEY = os.environ.get("MINIMAX_API_KEY", "")
OPENCODE_GO_KEY = os.environ.get("OPENCODE_GO_API_KEY", "")
CLIPROXY_KEY = os.environ.get("CLIPROXY_API_KEY", "")

OPENCODE_GO_URL = "https://opencode.ai/zen/go/v1"
CLIPROXY_URL = "http://127.0.0.1:8317/v1"

# 角色分配（用户指定）
ROLE_LLMS = {
    # 分析师团队
    "market": {"provider": "minimax", "model": "minimax-m3"},
    "social": {"provider": "openai_compatible", "backend_url": OPENCODE_GO_URL,
               "api_key": OPENCODE_GO_KEY, "model": "qwen3.7-plus"},
    "news": {"provider": "openai_compatible", "backend_url": OPENCODE_GO_URL,
             "api_key": OPENCODE_GO_KEY, "model": "mimo-v2.5"},
    "fundamentals": {"provider": "minimax", "model": "minimax-m3"},
    "policy": {"provider": "openai_compatible", "backend_url": OPENCODE_GO_URL,
               "api_key": OPENCODE_GO_KEY, "model": "deepseek-v4-pro"},
    "hot_money": {"provider": "openai_compatible", "backend_url": OPENCODE_GO_URL,
                  "api_key": OPENCODE_GO_KEY, "model": "deepseek-v4-flash"},
    "lockup": {"provider": "openai_compatible", "backend_url": CLIPROXY_URL,
               "api_key": CLIPROXY_KEY, "model": "gemini-pro-agent"},
    # 质量门控
    "quality_gate": {"provider": "openai_compatible", "backend_url": CLIPROXY_URL,
                     "api_key": CLIPROXY_KEY, "model": "gemini-3.6-flash-high"},
    # 研究员
    "bull": {"provider": "openai_compatible", "backend_url": CLIPROXY_URL,
             "api_key": CLIPROXY_KEY, "model": "gemini-3.6-flash-high"},
    "bear": {"provider": "openai_compatible", "backend_url": OPENCODE_GO_URL,
             "api_key": OPENCODE_GO_KEY, "model": "deepseek-v4-flash"},
    "research_manager": {"provider": "openai_compatible", "backend_url": OPENCODE_GO_URL,
                         "api_key": OPENCODE_GO_KEY, "model": "gpt-5.6-luna"},
    # 交易
    "trader": {"provider": "openai_compatible", "backend_url": OPENCODE_GO_URL,
               "api_key": OPENCODE_GO_KEY, "model": "deepseek-v4-flash"},
    # 风控
    "risk_aggressive": {"provider": "openai_compatible", "backend_url": OPENCODE_GO_URL,
                        "api_key": OPENCODE_GO_KEY, "model": "gpt-5.6-luna"},
    "risk_neutral": {"provider": "openai_compatible", "backend_url": OPENCODE_GO_URL,
                     "api_key": OPENCODE_GO_KEY, "model": "glm-5.2"},
    "risk_conservative": {"provider": "openai_compatible", "backend_url": OPENCODE_GO_URL,
                          "api_key": OPENCODE_GO_KEY, "model": "deepseek-v4-pro"},
    # 最终决策
    "portfolio_manager": {"provider": "openai_compatible", "backend_url": CLIPROXY_URL,
                          "api_key": CLIPROXY_KEY, "model": "claude-opus-4-6-thinking"},
}

from tradingagents.default_config import DEFAULT_CONFIG

# 基于默认配置，只覆盖需要的项
CONFIG = DEFAULT_CONFIG.copy()
CONFIG.update({
    # 主 provider（minimax 走内置中国区端点）
    "llm_provider": "minimax",
    "deep_think_llm": "deepseek-v4-pro",
    "quick_think_llm": "deepseek-v4-flash",
    "role_llms": ROLE_LLMS,
    "output_language": "Chinese",
    "max_debate_rounds": 4,
    "max_risk_discuss_rounds": 4,
})
