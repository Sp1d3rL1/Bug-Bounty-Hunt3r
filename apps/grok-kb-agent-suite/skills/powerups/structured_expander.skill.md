# structured_expander

Purpose: Expand compact intelligence items into Obsidian-ready card sections.

Rules:
- Use JSON Schema output only.
- Each card must include destination_path and markdown.
- Technique markdown must include: 核心思路, 前置条件, 完整技法细节, 适用目标画像, 为什么有效, 手工验证流程（授权 / Lab only）, 可自动化部分, 误报/失败条件, 授权边界, 报告 impact 角度, 相关案例链接.
- Case markdown stays link-centric and avoids real-target reproduction.

## Evidence baseline

- Output `verification_status`, `verification_summary`, `conflict_notes`, and `evidence` for every card.
- If existing KB excerpt already matches the source, output only `## 核查结果` in markdown.
- If source conflicts with existing KB excerpt, output a complete corrected card and explain the conflict.
- If a source cannot be verified, use `needs_review` and confidence=low.
