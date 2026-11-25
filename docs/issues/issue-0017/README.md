# Issue 17 - 核准紀錄與審查之後的提交規則精簡

## 文件清單
- [implementation-plan.md](./implementation-plan.md)

## 概述

來源：[GitHub #17](https://github.com/raybird/dev-rules-kit/issues/17)，由 #12 的問題 6、7 分出（#12 待確認事項 TBD-1）。2026-11-20 下游專案回報兩項成本：

1. **核准紀錄冗長**：分批核准時必須逐列展開，十幾列同一個日期；核准來源逐題轉述使用者的回答，與待確認事項、Timeline 重複。
2. **凍結規則的說明太長**：review-evidence.md「審查之後的提交」一段近兩千字，agent 怕讓 PASS 失效而不敢補 README；凍結章節的錯誤只能在原文後面附「（更正：…）」。

2026-11-25 唯讀量測本機 7 個下游專案與本 repo 的 issue README（各專案名稱不寫進本 repo）：

- 核准來源：筆數較多的 5 個下游專案與本 repo，中位數 78～236 字，最長 1005 字。最長的幾筆是逐次追加的紀錄：每次規格修訂都把選項原文與接受的代價再寫一次，同一內容另見於待確認事項的狀態欄與 Timeline。原因在 acceptance.md「逐題確認」要求核准來源記「原話、日期、題號、建議內容與對應驗收編號」。
- 列數最多的 8 個 issue，核准表有 16～42 列，其中 7 個只有一個核准日期：曾經分批或修訂就展開成表格，之後沒有收回的規則。
- 「審查之後的提交」約 2150 字，其中一段約 1500 字是檢查器對 `<`、`[`、段落與表格的邊界。下游 issue 文件出現「（更正」的有 3 個檔案。

收錄依據（AGENTS.md「範圍」）：兩項都在下游實際發生，核准來源的轉述是 kit 自己的規則造成的，project.md 的登記解決不了。本 issue 只刪減與重排，不新增 gate；verify-artifact 的判定不變。

## 快速導覽

### 當前流程

核准來源逐題轉述選項，規格修訂時往後追加；核准表一旦展開就一直留著。「審查之後的提交」先寫條件與一長段檢查器邊界，讀者要讀完才知道哪些可以改。

### 重構後流程

每次核准在核准來源寫一句（日期、核准原話、涵蓋的驗收編號），選項原文與代價只寫在它影響的地方。全部核准後核准表收回單行。「審查之後的提交」開頭先列審查後可以改的區段，凍結內容有錯時的兩種做法寫明，檢查器的邊界細節移到 review 技能的參考檔。

## 關鍵差異

| 項目 | 變更前 | 變更後 |
|------|--------|--------|
| 核准來源 | 原話、日期、題號、建議內容與驗收編號；修訂時追加選項原文 | 每次核准一句：日期、核准原話、驗收編號；修訂指向待確認事項編號 |
| 核准表 | 分批或修訂後展開，之後一直保留 | 只在有待核准或待重新核准時用表格；全部核准後收回單行 |
| 審查之後的提交 | 條件與約 1500 字的檢查器邊界寫在同一節 | 先列可以改的區段與凍結內容有錯時的做法；邊界細節在 review 技能的參考檔，判定不變 |

## 涉及檔案

### 下游文件

- `docs/agents/acceptance.md` - 「逐題確認」的核准來源寫法、「Gherkin 核准紀錄」的單行與表格
- `docs/agents/readme-templates.md` - 核准紀錄範本與註解
- `docs/agents/review-evidence.md` - 「審查之後的提交」重排
- `docs/agents/issue-checklist.md` - 核准來源那一項（影響檢查）
- `docs/AGENTS.md` - 文件版本；「待確認事項」的寫法限制精簡成一句，其餘指向 review 技能的參考檔（TBD-1）

### 技能

- `skills/review/references/` - 新增檢查器邊界細節的參考檔
- `skills/review/SKILL.md` - 步驟 5 指向該參考檔
- `skills/new-issue/SKILL.md` - 步驟 4 核准來源的寫法（影響檢查）

### 紀錄與回歸

- `docs/workflow-regression.md` - 新增 WF 案例
- `docs/issues/issue-0017/fixtures/`、`evidence/` - fixture、判準與實跑結果
- `CHANGELOG.md`、`docs/rule-verification-status.md`、`docs/usage.md`、技能歷代雜湊

## Gherkin 驗收劇本

```gherkin
Feature: 核准紀錄與審查之後的提交規則精簡

  @SCN-001
  Scenario: 核准來源每次核准寫一句
    Given 使用者在逐題確認中回答了各題，看過 Scenario 清單後回覆核准
    When agent 寫 Gherkin 核准紀錄
    Then 核准來源寫核准日期、使用者核准的原話與涵蓋的驗收編號
    And 不逐題轉述題目、選項原文與建議內容；選了建議以外答案的題目，只引用使用者選的那一項
    And 改變範圍卻沒有寫進驗收條件的答案（例如不做什麼）寫在 README 的概述或對應章節

  @SCN-002
  Scenario: 規格修訂後重新核准只加一句
    Given 已核准的 issue 因待確認事項 TBD-n 的決定修訂 Scenario
    When 使用者核准修訂
    Then 核准來源加一句：日期、TBD-n 與重新核准的驗收編號
    And 選項原文與接受的代價只寫在 TBD-n 的狀態欄
    And Timeline 那一列記修訂事件、受影響的驗收編號與原基線，不重抄選項

  @SCN-003
  Scenario: 全部核准後核准表收回單行
    Given 核准紀錄是表格，最後幾項待核准的 Scenario 獲得核准
    When agent 更新核准紀錄
    Then 表格改成單行「全部 Scenario 於 YYYY-MM-DD 核准」，日期是最後一次核准的日期
    And dev-cycle 與 review 讀到 Timeline 或待確認事項提過「待核准」時，仍以單行判定全部已核准，不要求展開表格

  @SCN-004
  Scenario: 還有待核准時維持表格
    Given 部分 Scenario 待核准或待重新核准
    When agent 寫核准紀錄
    Then 使用表格，逐列寫出每個 Scenario 的狀態
    And dev-cycle 不把待核准的 Scenario 當成可實作

  @SCN-005
  Scenario: PASS 之後補記 README 記帳區段
    Given 分支有有效 PASS，使用者要求把一項決定記進待確認事項並在 Timeline 補一列
    When agent 提交
    Then agent 在被審查分支提交，不重新審查，以 verify-artifact 確認 PASS 沿用並回報變更區段
    And 不以 PASS 可能失效為由拒絕、延後或要求重新審查

  @SCN-006
  Scenario: PASS 之後發現凍結內容有錯
    Given 分支有有效 PASS，發現 README 的凍結章節（例如關鍵差異）有一處寫錯
    When agent 處理
    Then agent 先告知使用者修改凍結章節會讓 PASS 失效，並列出做法：把更正記在待確認事項（PASS 沿用），或修正後送增量覆審
    And 使用者決定前不提交凍結章節的修改

  @SCN-007
  Scenario: 重排後判定不變
    Given review-evidence.md「審查之後的提交」已重排
    Then 這一節開頭列出審查之後可以改的區段，`<`、`[`、段落與表格的邊界細節只寫在 review 技能的參考檔
    And 現行這一節的每條判定規則都對應到 review-evidence.md 或該參考檔，對照表保存在 evidence
    And verify-artifact.py 沒有修改，test-evidence 全部通過
```

## Gherkin 核准紀錄
- **核准 commit**: `待提交`
- **核准來源**: 2026-11-25 使用者選「核准 SCN-001～007（建議）」；範圍與做法依同日逐題確認 Q1～Q5，Q5 選「只做 WF 實跑」，其餘選建議答案

全部 Scenario 於 2026-11-25 核准。

## 風險與首要驗證

- **最大風險**：重排「審查之後的提交」時漏掉或改動一條判定規則，agent 或 reviewer 依新文字判斷 PASS 是否沿用，與 verify-artifact 的結果不一致；其次是核准表收回單行後，dev-cycle 把仍待核准的項目當成已核准
- **風險等級與理由**：Medium。判定以 verify-artifact 為準，文字錯了會多一輪審查或誤報，不會讓未審查的程式被當成已審查；但核准狀態讀錯會讓未核准的行為進入實作
- **首要驗證**：先把現行「審查之後的提交」逐句拆成判定規則，建立「規則 → 新位置」對照表，再改寫；改寫後逐條核對對照表沒有缺項，verify-artifact.py 不動、test-evidence 全部通過
- **選擇理由**：直接覆蓋最大風險（漏規則），而且不依賴 agent 實跑
- **完成證據**：evidence 的對照表每列都有新位置；test-evidence 通過；WF 實跑 SCN-004 的分批情境不把待核准當可實作

## 待確認事項

| 編號 | 事項 | 狀態 | 影響 |
|------|------|------|------|
| TBD-1 | docs/AGENTS.md「待確認事項」一段也寫了檢查器的寫法限制（`<`、粗體、`[`、表格），是否一併精簡、改指向參考檔 | 已解決：2026-11-25 使用者選「一併精簡（建議）」：只留寫記帳區段都要知道的一句，其餘指向 review 技能的參考檔，S1 的對照表一併涵蓋這段 | 未決定時只做 review-evidence.md 的重排，docs/AGENTS.md 那段照舊；SCN-007 |
| TBD-2 | 流程契約是否升版 | 待確認 | 預設只升文件版本（判定不變、技能不讀核准表格式）；審查時確認。SCN-003、007 |
| TBD-3 | SCN-001～007 等待使用者核准 | 已解決：2026-11-25 使用者核准 SCN-001～007 | 核准前不開始實作；SCN-001～007 |

## Gate 豁免紀錄

- 2026-11-25 豁免下游試用（根目錄 AGENTS.md「改變 agent 行為的版本，先在至少一個下游專案的實際 issue 用過再推送發布」）：使用者在逐題確認 Q5 選「只做 WF 實跑」。殘餘風險：核准來源與核准表的新寫法只在隔離設定的 fixture 驗證，沒有實際 issue 的證據；rule-verification-status 記為限制。

## Timeline

| 日期 | 異動 | 負責人 |
|------|------|--------|
| 2026-11-25 | 建立；使用者決定兩項都現在處理、核准來源與核准表的寫法、重排方式與驗證方式 | 使用者／Claude Code |
| 2026-11-25 | 使用者核准 SCN-001～007 | 使用者 |

---
**建立日期**: 2026-11-25  
**分級**: Medium — 下游文件、review 技能新增參考檔與回歸案例，不改 verify-artifact；不需 Phase／Task 拆解  
**風險**: Medium\
**狀態**: 實作中
