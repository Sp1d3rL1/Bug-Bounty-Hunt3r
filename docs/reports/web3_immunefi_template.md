# Web3 Vulnerability Report Template — Immunefi v2.3

> Bilingual / 双语：用于 Immunefi、Code4rena 直报、Spearbit/Cantina engagement、Sherlock。
> 通用 Web2 见 `english_report_template.md`。

---

## Title

`[Severity] [Vulnerability class] in <Contract>::<function> allows <attacker role> to <impact>`

Examples:
- `[Critical] Reentrancy in Vault::withdrawAll allows attacker to drain all deposits`
- `[High] Signature replay across chains in Bridge::burnAndMint allows attacker to mint duplicate tokens on chain B`

## Severity (Immunefi v2.3)

| Field | Value |
|---|---|
| Immunefi severity | Critical / High / Medium / Low / Information |
| Immunefi impact | Loss of user funds / Permanent freezing / Theft of yield / Griefing / ... |
| Funds at Risk (USD) | <按事故时刻 mainnet TVL 估算 — 例 "$2.3M based on 2026-05-15 oracle price"> |
| Funds at Risk (Token) | <e.g. "1,200 ETH"> |
| Affected chains | Ethereum / Arbitrum / Base / Optimism / Polygon / BNB / Solana / ... |
| Affected protocol version | <commit hash 或 deployed proxy address + impl address> |

## Affected Contracts

| Contract | Address (verified) | Chain | Role |
|---|---|---|---|
| Vault | 0xabc...123 | Ethereum mainnet | User deposit pool |
| Strategy | 0xdef...456 | Ethereum mainnet | Yield strategy |
| (proxy) | 0x... | Ethereum mainnet | EIP-1967 proxy → impl 0x... |

> 全部地址必须在 Etherscan / Arbiscan 等浏览器上"verified"状态，否则报告会被退回。

## Summary

3-5 sentences:
1. Where the bug lives (contract + function name + line)
2. The faulty assumption (e.g. "trust that totalSupply only increases")
3. The exploit primitive (reentrancy / signature replay / oracle manipulation / access control flaw / arithmetic / price)
4. The realised impact (drained / frozen / minted / griefed)

## Vulnerability Detail

### Root Cause

```solidity
// File: contracts/Vault.sol, line 142-160
function withdrawAll() external {
    uint256 amount = balances[msg.sender];
    (bool ok, ) = msg.sender.call{value: amount}("");  // <-- external call before state update
    require(ok, "transfer failed");
    balances[msg.sender] = 0;  // <-- state mutation AFTER external call (CEI violation)
}
```

State changes **after** an external call enables a reentrancy: the receiver
can call `withdrawAll` again before `balances[msg.sender]` is zeroed.

### Attack Path

1. Attacker deploys `Reentrant.sol` and deposits 1 ETH → `balances[attacker] = 1e18`.
2. Attacker calls `Vault.withdrawAll()`.
3. Vault sends 1 ETH → triggers `Reentrant.fallback()`.
4. Inside fallback, attacker calls `Vault.withdrawAll()` again — `balances` is still 1e18.
5. Loop until `Vault` balance = 0 (or attacker chooses to stop).

## Proof of Concept

### Setup
```bash
forge install
forge test -vvv --match-test testReentrancyDrain --fork-url $MAINNET_RPC
```

### Foundry / Hardhat PoC link
- Repo: `https://github.com/<reporter>/<repo>-poc-2026-05-15` (private until disclosure)
- Mainnet fork test file: `test/ReentrancyExploit.t.sol`
- Specific commit: `<git sha>`

### Trace excerpt
```text
Running 1 test for test/ReentrancyExploit.t.sol:ReentrancyExploitTest
[PASS] testReentrancyDrain() (gas: 1,234,567)
Logs:
  Initial vault balance: 1000 ETH
  Attacker initial deposit: 1 ETH
  Final vault balance: 0
  Attacker final balance: 1000 ETH
  Profit: 999 ETH ($2,747,250 @ 2750/ETH)
```

## Recommended Fix

1. Apply Checks-Effects-Interactions: zero `balances[msg.sender]` **before** the external call.
2. Add `nonReentrant` modifier (OpenZeppelin ReentrancyGuard).
3. Add invariant test: `assertEq(vault.balance, sum(balances))` in fork tests.
4. Consider using `withdraw(uint256 amount)` over `withdrawAll()` to limit blast radius.

## References

- SWC-107 — Reentrancy
- OpenZeppelin ReentrancyGuard — https://docs.openzeppelin.com/contracts/4.x/api/security#ReentrancyGuard
- Similar disclosed: <Immunefi Critical 历史报告链接 1-2 个>

## Disclosure / Embargo

- Submitted: <date>
- Embargo requested until: <date> (typically until on-chain fix is mined)
- I will NOT discuss publicly until project confirms safe.
- Bridges / cross-chain only: requesting an emergency call within 4 hours.

---

## 中文要点提示

- **Funds at Risk** 必须给出**美元金额 + token 数量**两个值；只给数字会被退回
- Affected Contracts 表里所有地址必须 verified；如果是 proxy，把 implementation 地址也列上
- PoC 必须能跑，最好用 Foundry / Hardhat fork 真 mainnet 测试，trace 截给 triager
- 关键漏洞（Critical / High）写明请求 emergency call，因为资金风险窗口很小
- 不要在公开 GitHub 留 PoC，用 private repo 邀请 triager 加入
