"""运行 TradingAgents-astock 分析。

用法:
    python run.py 688017 [YYYY-MM-DD]
"""
import sys
from pathlib import Path

# 加载 .env
from dotenv import load_dotenv
load_dotenv(Path(__file__).parent / ".env")

from config import CONFIG
from tradingagents.graph.trading_graph import TradingAgentsGraph


def main():
    ticker = sys.argv[1] if len(sys.argv) > 1 else "688017"
    date = sys.argv[2] if len(sys.argv) > 2 else None

    ta = TradingAgentsGraph(debug=True, config=CONFIG)
    final_state, decision = ta.propagate(ticker, date)
    print("\n=== 最终决策 ===")
    print(decision)
    return decision


if __name__ == "__main__":
    main()
