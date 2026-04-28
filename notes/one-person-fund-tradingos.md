# 一人基金公司 Operating System：公司组织功能与 TradingOS 模块对应

可以，而且这个比喻非常准确。

你未来做的不是一个“股票脚本”，而是一个：

> **一人基金公司 Operating System**

你是 CIO / PM，AI agent 是员工，GitHub 是公司知识库和流程系统，数据 API 是外部信息供应商，Markdown 报告是内部投委会材料。

---

## 一、最高层结构：一人基金公司的组织图

```text
你本人
= CIO / Portfolio Manager / 最终风险承担者

Kimi / Codex / ChatGPT
= 研究员 + 工程师 + 运营助理 + 风控助理

GitHub Repo
= 公司制度库 + 研究档案库 + 系统代码库

GitHub Projects / Issues
= 公司任务管理系统

Reports / Notes / Journal
= 投委会材料 + 研究档案 + 交易复盘
```

你不是让 AI 直接替你炒股，而是让它们把一个基金公司的中后台、研究部、数据部、投研流程帮你搭起来。

---

## 二、公司部门 vs TradingOS 模块对应

### 1. 投资委员会 Investment Committee

公司功能：

```text
决定是否值得研究
决定是否进入观察池
决定是否进入交易候选
决定仓位和风险
```

对应模块：

```text
AGENTS.md
investment-policy.md
setup-rules.md
risk-rules.md
```

作用：

这是你的“投资宪法”。

里面写清楚：

```text
我只做美股 swing trade
不做日内高频
不自动交易
只关注基本面 + 技术面共振
单只股票最大风险多少
什么情况下必须放弃
```

这部分必须由你定义，AI 只能辅助整理。

---

### 2. 研究部 Research Department

公司功能：

```text
研究公司
研究行业
研究财报
研究催化剂
判断基本面拐点
```

对应模块：

```text
company-notes/
sector-notes/
earnings/
catalysts/
fundamental-analysis/
```

具体文件：

```text
company-notes/AMD.md
company-notes/INTC.md
sector-notes/AI-Semiconductor.md
earnings/2026-Q1/
catalysts/ai-capex.md
```

这里是你的核心 alpha 来源。

AI 的作用：

```text
总结财报
提炼电话会
找业务变化
比较公司
更新个股卡片
```

---

### 3. 数据部 Data Department

公司功能：

```text
收集行情
收集新闻
收集财报日期
收集宏观数据
保证数据能被系统读取
```

对应模块：

```text
data/
scripts/fetch_prices.py
scripts/fetch_news.py
scripts/fetch_earnings.py
config/api_sources.yaml
```

外部供应商：

```text
yfinance
Finnhub
FMP
Alpha Vantage
FRED
TradingView 手动观察
```

你可以把 API 当成：

> 基金公司外部数据供应商。

这一层的要求不是“越多越好”，而是：

```text
稳定
够用
可替换
不要把数据源写死
```

---

### 4. 新闻情报部 Intelligence Desk

公司功能：

```text
每天读新闻
过滤噪音
发现真正影响预期的事件
判断利好/利空/中性
```

对应模块：

```text
news-filter/
catalyst-ranking/
reports/daily/news-section.md
```

它不应该输出：

```text
今天 AMD 有 30 条新闻
```

而应该输出：

```text
今天 AMD 只有 2 条值得看：
1. 某大客户订单变化
2. 分析师上修 AI GPU 收入预期
```

这就是你的“私人 Bloomberg Desk”。

---

### 5. 技术分析部 Technical Desk

公司功能：

```text
判断趋势
判断买点
判断突破/回踩
判断相对强弱
设置止损参考
```

对应模块：

```text
technical/
setup-score/
scripts/calculate_indicators.py
reports/daily/technical-section.md
```

指标不需要太多，第一版就够：

```text
20日线
50日线
200日线
成交量
20日新高
相对 QQQ 强弱
相对 SMH 强弱
```

技术面模块的作用不是预测，而是回答：

> 基本面故事有没有被价格确认？

---

### 6. 组合经理办公室 Portfolio Management

公司功能：

```text
把研究转化成候选交易
决定优先级
控制仓位
避免过度集中
```

对应模块：

```text
portfolio/
watchlists/
candidate-list.md
position-plan.md
risk-dashboard.md
```

你的系统可以分层：

```text
Core Watchlist
Active Watchlist
Top Setups
Do Not Touch
```

例如：

```text
watchlists/core.yaml
watchlists/active.yaml
watchlists/avoid.yaml
```

这里非常关键，因为你不是要研究全市场，而是要把注意力集中在少数高质量标的上。

---

### 7. 风控部 Risk Management

公司功能：

```text
防止重仓单一叙事
防止追高
防止财报赌博
防止宏观环境错误
防止流动性风险
```

对应模块：

```text
risk/
risk-rules.md
drawdown-log.md
pre-trade-checklist.md
```

风控部的输出不是“买什么”，而是：

```text
今天不该做什么
哪些交易风险收益不划算
哪些 setup 看起来好但风险太大
```

你要让 AI 每天问你：

```text
这笔交易的 invalidation point 是什么？
如果跌破哪里说明你错了？
这是不是追高？
这是不是重复暴露在同一个主题？
```

---

### 8. 交易执行部 Trading Desk

公司功能：

```text
把观点转化成计划
记录入场理由
记录止损
记录退出条件
```

对应模块：

```text
trade-plans/
journal/
execution-checklist.md
```

注意：这里不是自动下单。

你的执行部只输出：

```text
候选交易计划
入场条件
止损条件
退出条件
仓位建议范围
```

最终下单仍然是你人工完成。

---

### 9. 绩效与复盘部 Performance Review

公司功能：

```text
复盘交易
统计错误
发现自己的行为模式
优化系统规则
```

对应模块：

```text
journal/
weekly-reviews/
monthly-reviews/
mistakes.md
lessons-learned.md
```

长期看，这一层可能比新闻系统还值钱。

因为它会告诉你：

```text
你在哪类行情赚钱
在哪类行情亏钱
是不是总在突破失败时亏
是不是总提前卖飞超级成长股
是不是对某些股票有执念
```

这就是你的个人交易数据库。

---

### 10. 运营部 Operations

公司功能：

```text
定时运行
文件归档
GitHub 同步
API key 管理
自动生成报告
系统维护
```

对应模块：

```text
.github/workflows/
README.md
logs/
config/
```

工具：

```text
GitHub Actions
GitHub Secrets
VS Code
Kimi Code
Codex Cloud
```

运营部保证系统每天能跑，而不是每天靠你手工整理。

---

### 11. 工程部 Engineering

公司功能：

```text
搭建系统
修 bug
重构代码
增加模块
维护自动化
```

对应角色：

```text
Kimi Code
Codex
GitHub Issues
GitHub Projects
```

分工：

```text
Kimi = 本地即时工程师
Codex = 云端任务工程师
GitHub Issues = 施工任务单
GitHub Projects = 工程排期表
```

你作为老板，不需要自己写代码，但你要会写清楚任务。

---

## 三、完整对应表

| 一人基金公司功能 | TradingOS 对应模块 | AI 角色 |
|---|---|---|
| CIO / PM | 你本人 | 最终判断 |
| 投资委员会 | AGENTS.md / setup-rules | 整理规则 |
| 研究部 | company-notes / sector-notes | 总结财报、行业分析 |
| 数据部 | data / API / scripts | 抓取和整理数据 |
| 情报部 | news-filter / catalyst-ranking | 新闻去噪 |
| 技术分析部 | technical / setup-score | 技术面扫描 |
| 组合管理 | watchlists / candidates | 排序机会 |
| 风控部 | risk / checklists | 找风险和反例 |
| 交易执行部 | trade-plans / journal | 生成交易计划 |
| 绩效复盘部 | weekly-review / mistakes | 复盘行为 |
| 运营部 | GitHub Actions / README | 自动运行 |
| 工程部 | Kimi / Codex / Issues | 搭建系统 |

---

## 四、你的 GitHub Repo 可以按“公司部门”来设计

建议未来目录这样：

```text
trading-research-os/
│
├── AGENTS.md
├── README.md
│
├── 00-policy/
│   ├── investment-policy.md
│   ├── risk-rules.md
│   └── setup-rules.md
│
├── 01-watchlists/
│   ├── core.yaml
│   ├── active.yaml
│   └── avoid.yaml
│
├── 02-data/
│   ├── raw/
│   ├── processed/
│   └── sources.yaml
│
├── 03-research/
│   ├── company-notes/
│   ├── sector-notes/
│   ├── earnings/
│   └── catalysts/
│
├── 04-signals/
│   ├── fundamental/
│   ├── technical/
│   └── sentiment/
│
├── 05-reports/
│   ├── daily/
│   ├── weekly/
│   └── monthly/
│
├── 06-trade-plans/
│
├── 07-journal/
│   ├── trades.csv
│   ├── weekly-reviews/
│   └── mistakes.md
│
├── 08-automation/
│   ├── github-actions/
│   └── logs/
│
└── scripts/
```

这就非常像一个小型基金公司的内部系统。

---

## 五、每天的“一人基金公司晨会”

你每天可以让系统生成一份晨会材料：

```text
Daily Investment Committee Memo

1. Market Regime
今天适合进攻、防守，还是观望？

2. Overnight Intelligence
昨晚真正重要的新闻是什么？

3. Watchlist Changes
哪些股票的基本面/预期发生变化？

4. Technical Confirmation
哪些股票出现价格确认？

5. Top 3 Setups
今天最值得关注的三个机会

6. Risk Desk Warning
今天最容易犯什么错？

7. PM Decision
等待你手工填写：
- Action
- Position
- Stop
- Reason
```

这就是你每天的基金公司投委会。

---

## 六、你未来的 AI 员工编制

你可以把不同 agent 角色写进 `AGENTS.md`：

```text
1. Market Strategist
负责判断大盘环境。

2. Fundamental Analyst
负责财报、基本面、行业趋势。

3. Technical Analyst
负责趋势、突破、相对强弱。

4. News Analyst
负责新闻去噪和催化剂分类。

5. Risk Officer
负责反驳交易逻辑，找风险。

6. Portfolio Assistant
负责把候选机会排序。

7. Journal Coach
负责复盘我的交易行为。

8. Engineering Agent
负责维护代码和自动化。
```

未来你不是叫“一个 AI”做事，而是叫不同“岗位”做事。

---

## 七、最重要的边界

虽然你可以模拟一人基金公司，但必须记住：

```text
AI 可以做研究部、数据部、运营部、风控助理。
但不能替代 CIO。
```

因为真正的投资责任包括：

```text
承受波动
承担亏损
控制仓位
判断市场情绪
决定是否下注
```

这只能由你做。

---

## 八、最后总结

如果把你的投研工作流比作一人基金公司，那么：

```text
GitHub = 公司总部
AGENTS.md = 公司制度
Projects = 任务看板
Issues = 工作指令
Kimi = 身边研究工程师
Codex = 云端工程团队
API = 数据供应商
Reports = 投委会材料
Journal = 绩效复盘
你 = CIO / PM / 最终风险承担者
```

长期最正确的方向是：

> **不是做一个工具，而是搭一个一人基金公司的操作系统。**
