"""跑单只股票，指定交易日期 + 可选分析师集合，报告落盘到 cases/。

用法:
    python run_single.py 600519 2026-08-10
    python run_single.py 159859 2026-08-10 market      # 只跑技术面分析师
    python run_single.py 600519 2026-08-10 market,news # 只跑 market + news
"""
import sys
from pathlib import Path

from dotenv import load_dotenv
load_dotenv(Path(__file__).parent / ".env")

from config import CONFIG
from tradingagents.graph.trading_graph import TradingAgentsGraph
from cli.main import save_report_to_disk

ticker = sys.argv[1]
date = sys.argv[2]
analysts = None
if len(sys.argv) > 3 and sys.argv[3].strip():
    analysts = [a.strip().lower() for a in sys.argv[3].split(",") if a.strip()]
    print(f">>> 启用分析师: {analysts}")

save_path = Path(r"D:\TradingAgents-astock\cases") / f"{ticker}_{date}"

# 不传 selected_analysts 参数 → 走构造器默认（全部 7 个分析师）
# 传了 None 会覆盖默认值导致 setup_graph(None) 报错
ta = TradingAgentsGraph(debug=True, config=CONFIG,
                        selected_analysts=analysts if analysts else ["market", "social", "news", "fundamentals", "policy", "hot_money", "lockup"])
final_state, decision = ta.propagate(ticker, date)
save_report_to_disk(final_state, ticker, save_path)
print("DONE", decision)
