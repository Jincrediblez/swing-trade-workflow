# US Stock Research Workflow 美股投研工作流 by Jincredible

> **交易风格**：拐点 / 超级成长 / 大盘科技 / 大趋势  
> **核心方法论**：基本面拐点 + 技术面突破 + 资金/衍生品共振 = 共振买点  
> **适用市场**：美股（Nasdaq / NYSE）  
> **核心数据源**：富途 OpenAPI（行情/资金/期权） + 东方财富（基本面/财务） + 华尔街见闻（宏观）

---

## 工作流总览

```
┌─────────────────┐
│  1. 宏观定方向   │  ← wallstreetcn-news + mx-macro-data
└────────┬────────┘
         ▼
┌─────────────────┐
│  2. 基本面深筛   │  ← mx-finance-data + stock-earnings-review
└────────┬────────┘
         ▼
┌─────────────────┐
│  3. 技术面精筛   │  ← futu-technical-anomaly + futuapi
└────────┬────────┘
         ▼
┌─────────────────────────────────────┐
│ 4. 资金+情绪+衍生品共振（美股核心）  │  ← futu-capital + futu-derivatives + futu-sentiment
└────────────────┬────────────────────┘
                 ▼
┌─────────────────┐
│  5. 制定交易计划 │  ← 手动 + futuapi
└────────┬────────┘
         ▼
┌─────────────────┐
│  6. 持仓跟踪风控 │  ← 持续监控技术/资金/衍生品信号
└─────────────────┘
```

> **美股特色**：Step 4（资金+衍生品）是共振判断的核心，期权市场smart money和卖空数据是美股独有的Alpha来源。

---

## Skills 武器库

### 🔴 核心武器（富途系）
| Skill | 功能 | 美股价值 |
|-------|------|---------|
| `futu-derivatives-anomaly` | 期权大单、IV、PCR、Call/Put流向 | ⭐⭐⭐⭐⭐ 美股期权是核心情绪指标 |
| `futu-capital-anomaly` | 主力净流入、卖空比例、经纪商动向 | ⭐⭐⭐⭐⭐ 卖空数据是美股独有Alpha |
| `futu-technical-anomaly` | K线形态、MACD/RSI/KDJ/CCI/BOLL | ⭐⭐⭐⭐⭐ |
| `futu-stock-digest` | 新闻事件智能解读 | ⭐⭐⭐⭐ |
| `futu-comment-sentiment` | 社区散户情绪 | ⭐⭐⭐⭐ 极端情绪=反向指标 |
| `futu-news-search` | 新闻、公告、研报 | ⭐⭐⭐ |
| `futuapi` | 实时行情、K线、买卖盘 | ⭐⭐⭐ |

### 🟡 辅助武器（东方财富系）
| Skill | 功能 | 美股价值 |
|-------|------|---------|
| `mx-finance-data` | 财务数据、估值PE/PS/PEG | ⭐⭐⭐ 美股财务 |
| `stock-earnings-review` | 业绩点评 | ⭐⭐⭐ 季报解读 |
| `mx-finance-search` | 中文研报、新闻 | ⭐⭐ 中文视角补充 |
| `mx-macro-data` | 宏观数据 | ⭐⭐ CPI/利率 |

### 🟢 辅助工具
| Skill | 功能 |
|-------|------|
| `wallstreetcn-news` | 华尔街见闻宏观/市场新闻 |
| `pdf` | 报告生成 |
| `ima-skill` | 知识库归档 |

### ❌ 美股用不上
- `stock-diagnosis`（仅A股）
- `comparable-company-analysis`（仅A股）
- `industry-research-report`（A股行业）
- `stock-market-hotspot-discovery`（仅A股热点）

---

## Step 1：宏观与行业趋势定方向

**目标**：判断美股大盘周期 + 科技/成长主线位置

### 核心问题
- 美联储利率路径？（降息预期/鹰派/鸽派）
- 10年期美债收益率对成长股的影响？
- QQQ/SPY 处于什么技术位置？
- 当前资金主线？（AI、半导体、云计算、太空、机器人？）
- 美元强弱对跨国科技股的影响？

### 调用 Skills
```
wallstreetcn-news  → 美联储动态、宏观政策
mx-macro-data      → CPI、利率、就业数据
mx-finance-search  → 中文视角宏观解读
```

### 输出
- `templates/us/01_macro_direction.md`

---

## Step 2：基本面深度分析

**目标**：确认"真成长" + 业绩拐点 + Guidance 质量

### 美股基本面关键差异
| 维度 | 美股重点 | 说明 |
|------|---------|------|
| **Guidance** | 比当期业绩更重要 | Forward guidance 决定估值方向 |
| **Non-GAAP** | 核心关注指标 | 剔除非经常性损益后的真实盈利 |
| **FCF** | 超级成长股的命脉 | 自由现金流是估值锚 |
| **TAM/SAM** | 市场空间叙事 | 美股极其看重story |
| **Insider** | 内部人交易信号 | Form 4 买卖是重要情绪指标 |
| **Short Interest** | 空头仓位 | 高空头+利好=逼空行情 |

### 调用 Skills
```
mx-finance-data       → 最近8个季度财务趋势、估值
stock-earnings-review → 最新季报业绩点评
mx-finance-search     → 机构评级、目标价调整
```

### 输出
- `templates/us/02_fundamental.md`

---

## Step 3：技术面精准分析

**目标**：找到"基本面改善"与"技术面突破/企稳"的共振点

### 调用 Skills
```
futu-technical-anomaly → K线形态、指标信号
futuapi               → K线数据、均线、关键价格位
```

### 输出
- `templates/us/03_technical.md`

---

## Step 4：资金 + 情绪 + 衍生品共振（美股核心！）

**目标**：确认smart money进场、情绪未过热、期权市场有聪明钱押注

### 三个维度缺一不可

#### 4.1 资金面（futu-capital-anomaly）
- 大单净流入/净流出趋势
- 主力资金连续流入天数
- **卖空比例变化**（美股独有！高空头+利好=逼空）
- 经纪商买卖动向（谁在买/谁在卖）

#### 4.2 衍生品面（futu-derivatives-anomaly）— 美股核武器
- **异常期权大单**（Call大单=看涨押注，Put大单=对冲或看空）
- **Put/Call Ratio (PCR)**：< 0.7 偏乐观，> 1.2 偏悲观（反向指标）
- **隐含波动率 (IV)**：低位+Call买入=低成本高概率；高位+Call卖出=情绪过热
- **牛熊证街货比例**（港股适用）

#### 4.3 情绪面（futu-comment-sentiment + futu-stock-digest）
- 社区讨论热度
- 散户乐观/悲观比例
- 新闻事件影响方向
- **反向指标**：是否出现"全民看涨"极端情绪？

### 调用 Skills
```
futu-capital-anomaly      → 资金流向、卖空、经纪商
futu-derivatives-anomaly  → 期权大单、IV、PCR
futu-comment-sentiment    → 社区情绪
futu-stock-digest         → 新闻解读
futu-news-search          → 最新新闻/公告
mx-finance-search         → 中文研报覆盖
```

### 输出
- `templates/us/04_capital_sentiment.md`

---

## Step 5：精确交易计划

**目标**：把分析转化为可执行的交易动作

### 美股交易特色
- **盘后/盘前交易**：财报后波动大，可考虑盘后建仓
- **期权策略**：可用Call替代正股（杠杆+风险可控）
- **卖空对冲**：持有正股+买入Put保护

### 输出
- `templates/us/05_trade_plan.md`

---

## Step 6：持仓跟踪与动态风控

**目标**：持续验证"共振"是否依然存在

### 每周检查清单
- [ ] 技术趋势未破位（futu-technical-anomaly）
- [ ] 主力资金未持续流出（futu-capital-anomaly）
- [ ] 卖空比例未异常上升（futu-capital-anomaly）
- [ ] 期权情绪未极端过热（futu-derivatives-anomaly）
- [ ] 无业绩预警或guidance下调
- [ ] 无重大监管/法律风险

### 输出
- `templates/us/06_position_track.md`

---

## 一键指令模板

详见 `scripts/us_workflow_prompts.md`

| 场景 | 指令文件 | 用途 |
|------|---------|------|
| 完整分析 | Template A | 新股首次覆盖 |
| 异动快检 | Template B | 盘中/盘后快速扫描 |
| 持仓跟踪 | Template C | 已有仓位持续监控 |

---

## 美股 vs A股关键差异速查

| 维度 | 美股重点 | A股重点 |
|------|---------|---------|
| **衍生品** | 期权是核心情绪指标 | 期权不成熟 |
| **卖空** | 卖空比例是重要反向指标 | 融券数据有限 |
| **业绩** | Guidance比当期更重要 | 当期业绩为主 |
| **情绪** | PCR + 社区情绪 | 涨停数量 + 龙虎榜 |
| **宏观** | 美联储/美债/美元 | 政策/流动性 |
| **机构** | 13F/分析师评级 | 北向/公募季报 |
| **交易** | 盘前盘后+期权策略 | T+1/涨跌停 |

---

*Last updated: 2026-05-01*  
*For US stocks only. See WORKFLOW.md for general framework.*
