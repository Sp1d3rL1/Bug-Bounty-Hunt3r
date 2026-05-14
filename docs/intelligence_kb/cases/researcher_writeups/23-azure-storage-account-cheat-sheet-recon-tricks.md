---
type: case
vuln_class: Storage Recon
source_url: https://rodelllemit.medium.com/azure-pentesting-storage-account-cheat-sheets-9f9766845cdd
source_author: ro0taddict
source_date: 2026-03
collected_at: 2026-05-05
freshness: 2026
confidence: high
target_types:
  - Azure Blob Storage
---

# Azure Storage Account Cheat Sheet Recon Tricks

## 链接

https://rodelllemit.medium.com/azure-pentesting-storage-account-cheat-sheets-9f9766845cdd

## 漏洞类型

Storage Recon

## 目标业务场景

Azure Blob Storage

## 关键利用链摘要

Use az storage container list with explicit keys vs anonymous for misconfig

## 可迁移技法

Precise enumeration of Blob access in authorized Azure BB programs

## 为什么值得收藏

- 该案例可作为 `Storage Recon` 的业务前提、影响证明和报告写法参考。
- 只在本地保存链接和摘要；完整复现以原文、靶场或明确授权环境为准。
- 迁移时优先提取“对象/状态/权限边界”而不是照搬请求。

## 安全边界

案例中涉及的目标、账号、数据均不可在未授权环境复现；真实项目中只使用自有测试账号和最小必要证据。
