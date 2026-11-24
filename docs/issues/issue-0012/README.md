# Issue 12 - 審查收斂與報告變輕

## 文件清單
- [implementation-plan.md](./implementation-plan.md)

## 概述

來源：[GitHub #12](https://github.com/raybird/dev-rules-kit/issues/12)。2026-11-20 詢問五個下游專案，照 kit 流程寫出的文件哪些沒人讀、沒有資訊量或會誤導；走 kit issue 流程的四個專案，成本最大的都是審查與它帶出的記帳。#12 留言另補 #11 TBD-10 的案例。本 issue 處理其中三類：

1. **PASS 之後處理建議，審查收不了尾**（問題 2）：使用者選了修正，PASS 就失效、要再審一輪，而 reviewer 每輪都可能對沒動到的內容提出新的小建議。一個下游專案的實際 issue 獨立審查 6 輪（1 輪 RETURN、3 輪 PASS 附建議、2 輪 PASS 無建議），另有 PR 第三方審查 2 輪；最後在 prompt 裡要求 reviewer「不要替沒動到的內容挑新問題」才收斂。kit 的 #11、#13、#15 也都靠同樣的手動要求收斂。依流程契約 2.7，沒有待觀察項目時 `已完成` 寫在最後一輪 PASS 無建議之後，審查不收斂，終態就一直寫不進去。
2. **報告越積越多、固定欄位重複**（問題 1、5）：同一個 issue 最多累積 22 份、334KB 報告（README 才 74KB）。增量覆審仍是每輪一份完整格式，「已查核維度」「限制」逐輪重寫；指向報告自己的 `Review artifact` 行、PASS 適用範圍的固定段落每份逐字重複。
3. **流程文件的格式問題被判 MUST FIX**（問題 3）：核准紀錄沒展開、核准基線欄位這類文件層級問題被判 RETURN，零程式改動也多一輪修正與審查。

問題 4（記帳提交太多）大多已由 #2、#11 處理，剩下的隨上列三項一起減少；問題 6（核准紀錄冗長）、7（凍結規則說明太長）不在本次範圍（TBD-1）。

收錄依據（AGENTS.md「範圍」）：四個下游專案實際發生，kit 自己的 issue 也重複發生；收斂要求目前只靠協調者手動寫進派工 prompt，project.md 登記解決不了跨專案的審查規則。

## 快速導覽

### 當前流程

PASS 附建議 → 使用者選修正 → 修完送增量覆審；reviewer 讀完整範圍，可以對任何內容提新建議，報告照完整格式重寫一份。格式問題由 reviewer 自行判斷輕重，常被列為 MUST FIX。

### 重構後流程

上一份報告是 PASS、這次增量只為處理它的建議時，reviewer 只查核每項修正與修正影響到的地方，新提的 SHOULD FIX／NICE TO HAVE 只限增量引入的問題；MUST FIX 等級的問題照常列出。增量覆審的報告只寫本輪查核的項目，其餘寫一行沿用上一份報告。格式、措辭問題列建議，只有會讓 gate 判斷錯誤時才是 MUST FIX。

## 關鍵差異

| 項目 | 變更前 | 變更後 |
|------|--------|--------|
| 處理建議後的覆審 | 查完整範圍，可對任何內容提新建議 | 只查修正與受影響處；新建議只限增量引入的問題，MUST FIX 照常 |
| 增量覆審報告 | 完整格式，已查核維度與限制逐輪重寫 | 只寫本輪查核的項目與結論，加一行沿用上一份報告 |
| 本機報告的 Review artifact 行 | 必填，指向報告自己 | 只有保存在平台時記連結 |
| PASS 的固定段落 | 每份照抄約 120 字 | 一句話，指向 review-evidence.md |
| 格式問題 | reviewer 自行判斷，常列 MUST FIX | 一律列建議；缺核准或必要證據、不實回報、會讓檢查器或 dev-cycle 判斷錯誤時才是 MUST FIX |

## 涉及檔案

### 規範

- `docs/agents/review-evidence.md` - 增量覆審：處理建議後的查核範圍、精簡報告；Review artifact 的必備欄位；審查強度：格式問題的判定
- `docs/AGENTS.md` - 文件版本 2.16 → 2.17，流程契約 2.7 → 2.8（向後相容）

### 技能

- `skills/review/SKILL.md` - 派工時傳入查核範圍；報告範本刪掉本機的 Review artifact 行、增量時精簡、PASS 固定段落縮成一句；格式問題的判定指向 review-evidence.md
- `skills/dev-cycle/SKILL.md` - PASS 附建議列：修完送增量覆審並寫明只查修正
- 技能歷代雜湊（`scripts/build-skill-hashes.py`）

### 回歸與紀錄

- `docs/issues/issue-0012/fixtures/` - WF-43、WF-44 的 fixture 與判準
- `docs/workflow-regression.md`、`docs/rule-verification-status.md`、`CHANGELOG.md`、`docs/usage.md`

## Gherkin 驗收劇本

```gherkin
Feature: 審查在處理建議後收斂，報告只寫本輪的內容

  Background:
    Given issue 的固定範圍是 BASE..H1，H1 有一份完整範圍的持久化報告

  @SCN-001
  Scenario: 處理建議後的增量覆審只查修正
    Given H1 的報告為 PASS，附 SHOULD FIX 與 NICE TO HAVE，使用者選了修正
    And H1..H2 只修正那些建議，H1 時就存在、H1..H2 沒動到也不受影響的程式有可以改善之處，H1 的報告沒有提到
    When 協調者把上一份報告與 BASE..H2 交給獨立 reviewer 做增量覆審
    Then 報告逐項確認每項建議已修好，並查核修正影響到的地方
    And 報告沒有對那段沒動到、也不受影響的程式提出新的 SHOULD FIX 或 NICE TO HAVE
    And 修正正確時判 PASS

  @SCN-002
  Scenario: 修正本身引入的問題照常提出
    Given 同 SCN-001，但 H1..H2 的修正引入了一個新的缺陷
    When reviewer 做增量覆審
    Then 報告指出這個缺陷，依一般規則判定 MUST FIX 或建議

  @SCN-003
  Scenario: 沒動到的內容有 MUST FIX 等級的問題時照常列出
    Given 同 SCN-001，reviewer 在沒動到的內容看到安全或邏輯錯誤
    When reviewer 做增量覆審
    Then 報告照常列為 MUST FIX，並寫明這是 H1 時就存在的問題

  @SCN-004
  Scenario: 增量覆審的報告只寫本輪查核的內容
    Given 符合增量覆審條件的任何增量覆審
    When reviewer 保存報告
    Then 已查核維度只寫本輪重新查核的項目與結論，另有一行寫明其餘沿用上一份報告的檔名
    And 本機保存的報告沒有 Review artifact 行，PASS 判定之後只有一句適用範圍的提醒
    And verify-artifact 判這份報告有效，create-pr 以它作為完整範圍的審查證據

  @SCN-005
  Scenario: PASS 提醒縮短後仍會先告知使用者
    Given PASS 報告的提醒只有一句
    When 使用者要求把進度寫進交接文件並提交到被審查分支
    Then agent 提交前先說明這會讓 PASS 失效，列出做法與代價，由使用者決定

  @SCN-006
  Scenario: 流程文件的格式問題列為建議
    Given 程式與驗收都正確，issue README 有格式或措辭問題（例如 Timeline 記了一筆完成步驟、核准來源逐題轉述）
    When reviewer 審查
    Then 這些問題列為 SHOULD FIX 或 NICE TO HAVE，沒有其他 MUST FIX 時判 PASS

  @SCN-007
  Scenario: 會讓 gate 判斷錯誤的文件問題仍是 MUST FIX
    Given issue README 缺少新行為的核准來源，或狀態值會讓 dev-cycle 判斷錯誤
    When reviewer 審查
    Then 列為 MUST FIX，判 RETURN TO execute-task
```

## Gherkin 核准紀錄
- **核准 commit**: 05cf010
- **核准來源**: 2026-11-24 使用者選「核准 SCN-001～007（建議）」；範圍與做法依同日逐題確認的選擇：範圍選問題 2、問題 1 與 5、問題 3（建議）；收斂選「只查修正（建議）」；報告選「仍開新檔，精簡格式（建議）」；格式問題選「一律列建議，會讓 gate 誤判才是 MUST FIX（建議）」

全部 Scenario 於 2026-11-24 核准。

## 風險與首要驗證

- **最大風險**：「只查修正」與「格式問題列建議」讓審查 gate 變弱：reviewer 把真正受影響的未改動程式當成「沒動到」而略過，或把會讓 gate 誤判的文件問題降成建議；規則發布後所有下游專案的審查都受影響
- **風險等級與理由**：Medium。失敗是漏報，不會損失資料，可由下一輪審查、回歸或下游試用發現；但 #10 的增量覆審已經放寬過一次，這次再收窄 reviewer 的範圍，累積效果要實測
- **首要驗證**：先寫好 review-evidence.md 的草稿與 WF-43、WF-44 的 fixture 與判準，以隔離設定實跑：WF-43 的誘餌組（沒動到的程式可改善）不提新建議、缺陷組（修正引入缺陷）照常提出；WF-44 的格式組判 PASS、gate 組判 RETURN
- **選擇理由**：直接量測收窄範圍後 reviewer 會不會漏掉該抓的問題，誘餌組與缺陷組、格式組與 gate 組成對比較
- **完成證據**：每組 2／2 符合判準；判準在實跑前提交

## 待確認事項

| 編號 | 事項 | 狀態 | 影響 |
|------|------|------|------|
| TBD-1 | 問題 6（核准紀錄冗長）、問題 7（凍結規則說明太長）不在本次範圍，去向要決定 | 不影響本次交付：追蹤：[GitHub #17](https://github.com/raybird/dev-rules-kit/issues/17)。2026-11-24 使用者選「另開 GitHub issue 追蹤（建議）」，#17 引用 #12 的問題 6、7 原文 | 不影響本次的驗收；GitHub #12 關閉時這兩項沒有去處 |
| TBD-2 | 問題 5 提到的完整 SHA 與 patch-id 不刪 | 不影響本次交付：追蹤：無。verify-artifact 以完整的 Reviewed HEAD SHA 比對報告，create-pr 以 patch-id 核對範圍，兩者都是檢查依據，不是給人讀的雜訊；本次只刪指向報告自己的 Review artifact 行與 PASS 固定段落 | 報告開頭仍有三行機器用欄位；SCN-004 |
| TBD-3 | 發布前的下游試用要用哪個下游專案的哪個 issue | 待確認 | 依 #15 的做法，要在發布前完成；不影響實作與回歸；SCN-001～007 |

## Timeline

| 日期 | 異動 | 負責人 |
|------|------|--------|
| 2026-11-24 | 建立；使用者決定範圍與三項做法 | 使用者／Claude Code |
| 2026-11-24 | 使用者核准 SCN-001～007；問題 6、7 另開 #17 | 使用者 |

---
**建立日期**: 2026-11-24  
**分級**: Medium — 修改 review-evidence.md、review 與 dev-cycle 技能，加兩個回歸案例；不改檢查器、不需 Phase／Task 拆解  
**風險**: Medium\
**狀態**: 實作中
