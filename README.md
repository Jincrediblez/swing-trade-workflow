# Swing Trade 投研工作流

> **基于基本面与技术面共振的拐点捕捉系统**
>
> 适合风格：拐点 / 超级成长 / 大盘科技 / 大趋势 / 美股 Swing Trade

---

## 项目简介

这是一个结构化的投研工作流系统，帮助你在美股做 Swing Trade 时，系统地完成从**宏观定方向**到**精确买卖点**再到**动态风控**的全流程。

核心方法论：**基本面拐点 + 技术面突破 = 共振买点**

---

## 项目结构

```
swing-trade-research-workflow/
├── README.md                      # 本文件
├── WORKFLOW.md                    # 完整 7 步工作流文档
├── templates/                     # 分析模板（可复制使用）
│   ├── 01_macro_direction.md
│   ├── 02_stock_screening.md
│   ├── 03_fundamental_analysis.md
│   ├── 04_technical_analysis.md
│   ├── 05_capital_sentiment.md
│   ├── 06_trade_plan.md
│   ├── 07_risk_management.md
│   └── watchlist.md
├── scripts/                       # 辅助 Python 脚本
│   ├── config.py                  # 配置管理
│   ├── data_formatter.py          # 数据格式化
│   ├── chart_generator.py         # 图表生成
│   ├── report_builder.py          # 报告构建
│   └── run_workflow.py            # 主入口
├── examples/                      # 实战案例
│   └── INTC_20260428.md           # Intel 完整分析案例
└── .github/workflows/
    └── daily_scan.yml             # 可选：GitHub Actions 每日扫描
```

---

## 7 步工作流概览

```
宏观趋势定方向 → 初筛池子 → 基本面深度筛选 → 技术面异动信号 → 资金/情绪共振验证 → 精确买卖点 → 仓位与风控
```

| 步骤 | 目标 | 输出 |
|------|------|------|
| **1. 宏观定方向** | 判断大盘周期 + 科技/成长主线位置 | 方向判断 + 重点关注板块 |
| **2. 初筛股票池** | 从数千只缩到 20-50 只候选 | 候选清单 |
| **3. 基本面深筛** | 确认"真成长" + 拐点验证 | 5-10 只精选池 |
| **4. 技术面精筛** | 找到基本面与技术面共振点 | 3-5 只锁定标的 |
| **5. 资金+情绪共振** | 聪明钱进场？情绪不过热？ | 1-3 只最终标的 |
| **6. 制定交易计划** | 买点、止损、目标、仓位 | 可执行交易方案 |
| **7. 持仓跟踪风控** | 持续验证共振，动态调整 | 持仓跟踪表 |

详见 [WORKFLOW.md](./WORKFLOW.md)

---

## 快速开始

### 1. 克隆项目

```bash
git clone https://github.com/YOUR_USERNAME/swing-trade-research-workflow.git
cd swing-trade-research-workflow
```

### 2. 安装依赖

```bash
pip install -r requirements.txt
```

### 3. 配置环境

复制配置模板并填入你的参数：

```bash
cp scripts/config.py scripts/config_local.py
# 编辑 config_local.py 填入你的 API 密钥等
```

### 4. 运行工作流

```bash
# 针对单只股票运行完整工作流
python scripts/run_workflow.py --symbol US.INTC --output ./reports

# 生成观察清单模板
python scripts/run_workflow.py --mode watchlist --output ./watchlist.md
```

### 5. 使用模板手动分析

进入 `templates/` 目录，复制对应步骤的模板，填入你的分析内容。

---

## 实战案例

- [Intel (INTC) 完整投研分析 - 2026.04.28](./examples/INTC_20260428.md)

---

## 配套工具

本项目设计为与以下数据源/工具配合使用：

| 工具 | 用途 | 说明 |
|------|------|------|
| **Futu OpenAPI** | 行情、K线、技术指标、资金流向、期权数据 | 需要安装 OpenD |
| **东方财富数据** | 基本面数据、财务数据、估值数据 | mx-finance-data skill |
| **Futu News** | 新闻、公告、研报检索 | futu-news-search skill |
| **Futu Community** | 社区情绪、散户讨论热度 | futu-comment-sentiment skill |

> 这些工具为本地安装的 Skills，非本项目必需。你也可以使用 TradingView、Yahoo Finance、Bloomberg 等替代数据源。

---

## 贡献指南

欢迎提交 Issue 和 PR：
- 改进分析模板
- 增加新的脚本功能
- 分享实战案例
- 优化文档

---

## 免责声明

本项目仅供学习和研究使用，不构成任何投资建议。金融市场有风险，交易需谨慎。

---

*Created with ❤️ for systematic traders.*
