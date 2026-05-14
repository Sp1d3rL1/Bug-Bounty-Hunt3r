# GitHub Frontier Agent Notes（2026-05）

## 参考对象

- LangGraph：resilient graph agents, durable execution, human-in-the-loop, memory/persistence。
- OpenAI Agents SDK：handoffs, guardrails, tracing, hosted tools。
- PydanticAI：typed tools, structured outputs, validation-first agent design, Grok provider support。
- Mastra：TypeScript-first agents/workflows, evals, observability, workflow suspend/resume。
- CrewAI：role-based multi-agent orchestration，适合快速多角色 pipeline。
- Microsoft AutoGen / Microsoft Agent Framework：multi-agent orchestration，AutoGen 已进入 maintenance，新项目更应关注 successor。

## 提取出的工程准则

1. 不依赖聊天窗口状态；所有 run 都落盘。
2. Structured outputs 优先，减少自然语言解析。
3. tools/skills 要少而精，按任务动态装配。
4. 显式成本/usage 记录。
5. Human review 是能力，不是阻碍。
6. 大批量任务用 batch；交互任务用实时 API。
7. 前后端分离，但 v1 避免构建链依赖。
8. 任何高风险内容用 Lab/authorized/synthetic/minimal-impact 语境约束。
9. 框架可替换，状态协议和数据格式稳定。
10. 失败要可重试、可定位、可恢复。
