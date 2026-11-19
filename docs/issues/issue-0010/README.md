# Issue 10 - 增量覆審與 PASS 後建議的處理

## 文件清單
- [implementation-plan.md](./implementation-plan.md)

## 概述

來源：[GitHub #10](https://github.com/raybird/dev-rules-kit/issues/10)，v5.1.0 發布前的下游試用回報（2026-11-19）。審查 PASS 或 RETURN 之後再修正，kit 只寫「重新審查」，沒有寫怎麼審；每次修正都等於再做一輪完整審查。

2026-11-19 以關鍵字（增量、差異、覆審、上一輪等）粗估 8 個下游專案的審查報告：8 個專案都有增量覆審，googleBooking 218 份、line-oa-plus 84 份、moltbot-lite 32 份、Asura 21 份，其餘各約 10 份；kit 自己的 issue-0007 也用了「差異覆審」。寫法有兩種，互不相容：

- Reviewed BASE 記完整範圍的 merge-base，重點看上一個 Reviewed HEAD 之後的變動。
- Reviewed BASE 記上一個 Reviewed HEAD，再寫「其餘部分沿用 review-A、B、C…」串接。照現行 review-evidence.md 這只是局部審查；v5.1.0 的 create-pr 核對 Reviewed BASE 與 merge-base，會判範圍失效。

連帶兩點：PASS 附 SHOULD FIX／NICE TO HAVE 時，規則沒有寫要不要先問使用者，試用的 agent 逐題問、每題修完各審一輪；推送後另有第三方審查的專案（googleBooking、line-oa-plus 的 README 各有 44、57 份提到），外部審查要求的修正同樣讓 PASS 失效，kit 沒有提到。

收錄依據（AGENTS.md「範圍」）：下游實際發生，且各專案寫法互相矛盾，project.md 登記解決不了跨專案的報告格式。2026-11-19 使用者決定以增量覆審為主、PASS 後建議與外部審查一起處理（外部審查的修正走同一個增量覆審，不另立規則）。

## 現況

**現行 review**: review-186e0c6.md

| 外部狀態 | 查證命令 | 上次結果 | 查證日期 |
|---|---|---|---|
| GitHub #10 | gh issue view 10 --repo raybird/dev-rules-kit --json state -q .state | OPEN | 2026-11-19 |

## 快速導覽

### 當前流程

審查 PASS 或 RETURN → 修正並提交 → 「重新審查」，沒有定義範圍與可沿用的內容；各專案自己決定要整輪重審、只看變動，或串接多份報告。PASS 附建議時 dev-cycle 直接進 create-pr。

### 重構後流程

PASS 附建議時，協調者在同一則訊息列出所有建議，使用者逐項選「修／記入待確認／不修」；選了修的一起修完，送一次增量覆審。RETURN 或任何來源（含外部審查）的修正之後，條件成立就做增量覆審：報告仍記完整範圍，reviewer 讀上一份報告，查核變動與它影響到的既有結論，其餘寫明沿用。條件不成立就完整審查。

## 關鍵差異

| 項目 | 變更前 | 變更後 |
|------|--------|--------|
| 修正後的審查 | 「重新審查」，範圍未定義 | 符合條件時增量覆審：完整範圍的報告，重點查核變動及其影響 |
| 報告的 Reviewed BASE | 各專案自定，有的記上一個 HEAD | 一律是完整範圍的 merge-base；增量另記上一個 Reviewed HEAD |
| PASS 附建議 | 直接開 PR，或逐題問、逐題重審 | 一次列出、使用者逐項選；選了修的修完只做一次增量覆審 |
| 外部審查後的修正 | 未提及 | 與其他修正相同，走增量覆審 |

## 涉及檔案

### 規範

- `docs/agents/review-evidence.md` - 新增「增量覆審」：適用條件、報告欄位、reviewer 的查核責任；權威定義
- `docs/AGENTS.md` - 文件版本與修訂紀錄；流程契約 2.5 → 2.6（向後相容）

### 技能

- `skills/review/SKILL.md` - 協調者傳入上一份報告時依 review-evidence.md 做增量覆審；報告範本加增量欄位
- `skills/dev-cycle/SKILL.md` - PASS 附建議時一次問完；退回與修正後送增量覆審並傳入上一份報告

### 文件與紀錄

- `docs/usage.md`、`docs/workflow-regression.md`、`docs/rule-verification-status.md`、`CHANGELOG.md`

## Gherkin 驗收劇本

```gherkin
Feature: 修正之後以增量覆審取得完整範圍的審查證據

  Background:
    Given issue 的固定範圍是 BASE..H1，BASE 是目標分支與 H1 的 merge-base
    And H1 有一份有效的持久化報告，判定為 PASS 或 RETURN TO execute-task

  @SCN-001
  Scenario: 修正後做增量覆審
    Given 之後的修正提交讓 HEAD 變成 H2，H1 是 H2 的祖先，中間沒有重寫歷史
    And 目標分支與 H2 的 merge-base 仍是 BASE
    When 協調者把上一份報告與 BASE..H2 交給獨立 reviewer
    Then 新報告的 Reviewed BASE 是 BASE、Reviewed HEAD 是 H2、patch-id 依 BASE..H2 計算
    And 報告寫明上一份報告、增量範圍 H1..H2、重新查核的項目與沿用的結論
    And 增量範圍內每個變動檔案都有查核結論，受影響的測試在 H2 重跑並引用輸出
    And create-pr 以這份報告作為完整範圍的證據，不要求另一份完整審查

  @SCN-002
  Scenario: 變動影響到上一份報告查過的內容
    Given H1..H2 修改了一個函式，H1 之前就存在、H1..H2 沒有改動的程式呼叫它
    When reviewer 做增量覆審
    Then 報告指出那段未改動程式的結論受影響，並重新查核，而不是寫為沿用
    And 重新查核發現問題時依一般規則判定 MUST FIX 或建議

  @SCN-003
  Scenario: 條件不成立時完整審查
    Given 下列任一情況：H1 不是新 HEAD 的祖先（rebase 或改寫歷史）、merge-base 不再是 BASE、找不到 H1 的有效報告
    When 協調者送審新 HEAD
    Then reviewer 審查完整範圍，報告寫明不採增量的原因
    And 只記上一個 HEAD 為 Reviewed BASE 的報告仍是局部審查，create-pr 依現行規則回到 review

  @SCN-004
  Scenario: PASS 附建議時一次問完
    Given H1 的報告為 PASS，附有未加註需決策的 SHOULD FIX 或 NICE TO HAVE
    When dev-cycle 推進到 create-pr 之前
    Then 協調者在同一則訊息列出所有建議，每項附建議答案，選項為修正、記入待確認、不修
    And 使用者選了修正的項目一起修完並提交後，只送一次增量覆審
    And 沒有選修正時，決定記入待確認事項或 Timeline 後沿用 PASS，直接進 create-pr
    And project.md 登記了固定做法時照登記，並在同一則訊息說明
    And 報告沒有建議時不提問，直接進 create-pr

  @SCN-005
  Scenario: 外部審查之後的修正
    Given H1 已 PASS，推送後專案的外部 reviewer 要求修改
    When 修正提交讓 HEAD 變成 H2
    Then 協調者依 SCN-001 或 SCN-003 送審 H2，再更新 PR
```

## Gherkin 核准紀錄
- **核准 commit**: ff51536
- **核准來源**: 2026-11-19 使用者對 SCN-001～005 回覆「核准」；範圍與做法依同日三題的回答：範圍選「c 為主，b、d 一起」、增量範圍選「完整範圍、重點看變動」、PASS 後建議選「一次問完再修」

全部 Scenario 於 2026-11-19 核准。

## 風險與首要驗證

- **最大風險**：增量覆審讓 reviewer 只讀變動檔案，漏掉變動對未改動程式的影響；規則一旦發布，所有下游專案的審查 gate 都因此變弱
- **風險等級與理由**：Medium。影響所有下游的審查，但下游已在非正式地做增量覆審，本 issue 是加上條件與查核責任；失敗是漏報，可由下一輪審查或回歸發現，不會損失資料
- **首要驗證**：先寫好 review-evidence.md 的增量覆審草稿，以隔離設定實跑 SCN-002 的 fixture（變動修改被未改動程式呼叫的函式），對照組是變動與其他程式無關
- **選擇理由**：直接量測 reviewer 照新規則會不會查到影響面；靜態審查只能確認文字，看不出 agent 會不會只讀 diff
- **完成證據**：2 輪實跑中，影響組的報告都指出受影響的未改動程式並重新查核；對照組都寫明沿用且沒有誤報；判準在實跑前提交

## 待確認事項

| 編號 | 事項 | 狀態 | 影響 |
|------|------|------|------|
| TBD-1 | 流程契約升到 2.6 後，review、dev-cycle 的最低需求維持現值，契約 2.5 以下的專案沒有「增量覆審」章節時照舊完整審查；這個相容做法要在下游試用確認 | 待確認 | SCN-001、SCN-003 |
| TBD-2 | [review-40f9475](review-40f9475.md) 的 9 項建議怎麼處理 | 已解決：2026-11-19 使用者照建議決定。修正：SHOULD FIX 1～3（3 一併修「需決策」列的同一缺口）、NICE TO HAVE 1、2、4、5、6；不修：NICE TO HAVE 3（根目錄 README 的流程圖本來就省略需決策分支）。SHOULD FIX 1 改了規則語意，重跑 WF-36 影響組與對照組各 1 輪 | SCN-001～004 |
| TBD-3 | [review-09b22fb](review-09b22fb.md) 的 4 項建議怎麼處理 | 已解決：2026-11-19 使用者照建議決定，SHOULD FIX 1、2 與 NICE TO HAVE 1、2 都修正。只改文字、不改規則語意，不重跑 WF | 無 |

## Timeline

| 日期 | 異動 | 負責人 |
|------|------|--------|
| 2026-11-19 | 建立；盤點 8 個下游專案的增量覆審寫法；使用者決定範圍與兩項做法 | 使用者／Claude Code |
| 2026-11-19 | 使用者核准 SCN-001～005 | 使用者 |
| 2026-11-19 | 獨立審查 [review-40f9475](review-40f9475.md) PASS，沒有 MUST FIX；SHOULD FIX 3 項（1 項需決策）、NICE TO HAVE 6 項待使用者決定 | Claude Code |
| 2026-11-19 | 使用者照建議決定審查建議（TBD-2），修正與結論同一提交 | 使用者 |
| 2026-11-19 | 增量覆審 [review-09b22fb](review-09b22fb.md) PASS（上一份 review-40f9475，增量 `40f9475..09b22fb`），沒有 MUST FIX；SHOULD FIX 2 項、NICE TO HAVE 2 項待使用者決定 | Claude Code |
| 2026-11-19 | 使用者照建議決定（TBD-3），修正與結論同一提交 | 使用者 |
| 2026-11-19 | 增量覆審 [review-186e0c6](review-186e0c6.md) PASS（上一份 review-09b22fb，增量 `09b22fb..186e0c6`），沒有任何建議 | Claude Code |

---
**建立日期**: 2026-11-19  
**分級**: Medium — 修改 review-evidence.md、review 與 dev-cycle 技能與相關文件，不改檢查器；不需 Phase／Task 拆解  
**風險**: Medium\
**狀態**: 審查通過，待下游試用
