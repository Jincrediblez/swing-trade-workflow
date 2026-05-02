# 美股投研一键指令模板

> 复制对应模板，把 `US.XXX` 替换成目标股票代码即可使用。

---

## Template A：完整 7 步分析（推荐）

**用途**：新股首次覆盖、深度研究

```
请按照 WORKFLOW_US.md 的投研工作流，对 US.XXX 进行完整分析：

Step 1 宏观：结合 wallstreetcn-news 和 mx-macro-data，判断当前宏观环境（美联储、利率、大盘）对成长股的影响。

Step 2 基本面：用 mx-finance-data 查最近8个季度的营收、毛利率、运营利润率、EPS、自由现金流和估值（PE/PS/PEG/EV/EBITDA）。用 stock-earnings-review 做最新季报业绩点评。关注Guidance质量和Short Interest数据。

Step 3 技术：用 futu-technical-anomaly 检测技术信号（K线形态、MACD、RSI、KDJ、均线排列）。用 futuapi 查K线确认趋势和关键价格位。

Step 4 资金+情绪+衍生品（重点）：
  - 用 futu-capital-anomaly 分析资金流向（主力净流入、卖空比例、经纪商动向）
  - 用 futu-derivatives-anomaly 分析期权信号（异常大单、IV、PCR、Call/Put流向）
  - 用 futu-comment-sentiment 看社区情绪
  - 用 futu-stock-digest 解读最新新闻影响
  - 用 mx-finance-search 查中文研报覆盖

Step 5 交易计划：基于以上分析，制定具体买点（3个方案）、止损、目标位、仓位和可选期权策略。

请按 templates/us/ 里的格式输出完整报告，保存到 reports/US_XXX_YYYYMMDD.md
```

---

## Template B：异动快检（盘中/盘后快速扫描）

**用途**：快速筛选、异动发现、日常扫描

```
请对 US.XXX 做异动快速检查：

1. futu-technical-anomaly — 有什么技术信号？（金叉、底背离、突破、超买超卖？）
2. futu-capital-anomaly — 资金有什么异常？（主力流入？卖空比例变化？）
3. futu-derivatives-anomaly — 期权市场有什么大单押注？（PCR、IV、异常Call/Put？）
4. futu-stock-digest — 最新新闻解读和影响方向
5. 综合判断：
   - 是否有交易机会？
   - 评分（1-5星）
   - 是否需要进入完整分析？

请按 templates/us/07_quick_scan.md 格式输出，保存到 output/US_XXX_quickscan_YYYYMMDD.md
```

---

## Template C：持仓跟踪（已有仓位）

**用途**：持有期间持续监控

```
我正在持有 US.XXX，成本 $XX，当前浮盈/亏 ___%：

1. futu-technical-anomaly — 技术趋势是否仍然完好？（均线、形态、动量）
2. futu-capital-anomaly — 主力资金是否还在流入？卖空比例变化？
3. futu-derivatives-anomaly — 期权情绪是否过热或恐慌？（PCR、IV）
4. futu-news-search — 有什么新的催化或风险？（财报、产品、监管）
5. 综合判断：
   - 继续持有 / 加仓 / 减仓 / 清仓
   - 理由
   - 新的止损价建议
   - 下次跟踪时间建议

请按 templates/us/06_position_track.md 格式更新跟踪记录。
```

---

## Template D：财报前分析

**用途**：财报发布前的风险评估和仓位决策

```
US.XXX 即将在 ___ 发布财报，请做财报前分析：

1. mx-finance-data — 查历史财报数据（过去4个季度营收、EPS、毛利率趋势）
2. stock-earnings-review — 历史业绩点评，看公司财报beat/miss规律
3. mx-finance-search — 当前市场预期（共识EPS/营收预期）
4. futu-derivatives-anomaly — 期权市场押注（straddle价格、PCR、异常大单方向）
5. futu-capital-anomaly — 资金是否在财报前流入/流出
6. 风险评估：
   - 如果beat预期，合理涨幅？
   - 如果miss预期，合理跌幅？
   - 当前仓位是否需要调整？（减仓/对冲/维持）
   - 建议的期权对冲策略（如有）
```

---

## Template E：板块轮动扫描

**用途**：发现当前热点板块和领涨个股

```
请扫描当前美股市场：

1. wallstreetcn-news — 最新宏观和市场热点
2. mx-macro-data — 近期关键宏观数据（CPI、就业、利率）
3. mx-finance-search — 中文视角下的美股热点板块
4. 对以下板块做 quick scan（用 futu-technical-anomaly + futu-capital-anomaly）：
   - AI/半导体（NVDA, AMD, AVGO, TSM）
   - 云计算（MSFT, AMZN, GOOGL, CRM）
   - 太空（RKLB, ASTS, VORB）
   - 机器人（TSLA, ROK, ISRG）
   - 生物科技（LLY, NVO, VRTX）
5. 输出：
   - 当前最强板块排名
   - 每个板块最值得关注的前3只个股
   - 技术面+资金面的综合评分

请按观察清单格式输出。
```

---

## 使用建议

| 场景 | 推荐模板 | 预计耗时 |
|------|---------|---------|
| 首次研究新股 | Template A | 15-30分钟 |
| 每日盘后扫描 | Template B | 3-5分钟/只 |
| 持仓跟踪 | Template C | 5-10分钟/只 |
| 财报前决策 | Template D | 10-15分钟 |
| 周末板块复盘 | Template E | 20-30分钟 |
