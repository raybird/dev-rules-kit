# Issue 2 — 審查通過後的記帳提交與核准回填

## 概述

來源：[GitHub #2](https://github.com/raybird/dev-rules-kit/issues/2)。2026-11-03 詢問下游專案的使用情況，7 個下游專案都回報同一組成本：審查通過後只為記帳多出的提交讓 PASS 失效、整輪重審，核准 commit 又固定多一個回填提交，而這個回填提交又觸發重審。本 issue 只處理這兩條規則的連鎖，目標是讓記帳不再觸發重審、核准不再單獨製造提交，同時不放過任何語意變更。

2026-11-03 使用者要求「好 開一個 issue 先解決兩調規則的連鎖」，並對兩個設計問題選擇建議做法（見待確認事項 TBD-1、TBD-2）。規劃中推導出的細節列為 TBD-3 後，使用者回覆「核准」，核准 SCN-001～006 與實作計畫。

不在範圍：PASS 帶改善建議時的輕量複審、報告摘要、Small 篇幅、結案提交、先問後探測等其他下游回饋。本 README 是驗收、核准與範圍的唯一來源；任務與證據只維護於 implementation-plan.md。

## 文件清單

- [implementation-plan.md](implementation-plan.md)

## 現況與關鍵差異

基準為 `6bd2504`（v4.8.1，流程契約 2.3）。

| 項目 | 現況與依據 | 變更後 |
|---|---|---|
| PASS 後的提交 | 原「本機 artifact 提交後的有效性」（現為[審查之後的提交](../../agents/review-evidence.md#審查之後的提交)）只接受被審查提交之後恰好一個、只新增該報告的提交；其他任何提交都重審 | 被審查提交之後的非 merge 提交，淨差異只落在該 issue README 的記帳區段（加上該報告）時 PASS 沿用；其餘照舊重審 |
| 核准 commit | [Gherkin 核准紀錄](../../agents/acceptance.md#gherkin-核准紀錄)「未提交先填 `待提交`，首次提交後回填」，實務上常成為只改一行的提交 | 回填搭下一個本來就要做的提交，不單獨開提交；送審時仍是 `待提交`，以最後一個修改 `**核准來源**` 行的提交為基線 |
| 判定工具 | `verify-artifact.py` 只比對「唯一差異是新增該報告」 | 逐區段比對 README，列出變更的區段；依專案流程契約決定採用新判定或現行判定 |

## 設計邊界

- **記帳區段**：該 issue README 的 `## Timeline`、`## 待確認事項`、`## Gate 豁免紀錄` 三節內容（後兩節本來就可整節省略，所以允許新增或刪除整節），以及 `**狀態**`、`**核准 commit**` 兩個欄位的值。
- **一律凍結**：其他章節的內容、所有章節標題與順序、記帳區段內外的其他粗體欄位行（例如 `**分級**`、`**風險**`、`**建立日期**`、`**核准來源**`）、implementation-plan.md、evidence 與其他檔案、該 issue 目錄外的檔案，以及既有報告。標題名稱與範本不同的下游 README，該節一律視為凍結，判定只會更嚴、不會更寬。
- **核准 commit 的值**：只能從 `待提交` 改成被審查提交或它的祖先；從一個 SHA 改成另一個 SHA 屬重新核准，仍要重審。
- **相容性**：專案 `docs/AGENTS.md` 的流程契約達 2.4 才採用新判定，2.3 以下維持現行判定；kit 以流程契約 2.4、文件版本 2.8 發布。技能宣告的最低契約不變，未更新的專案不會因此被暫停。
- **不變**：核心欄位、核准狀態與 review 判定字串、獨立審查與誠實回報要求；非記帳變更仍可依 [Gate 豁免紀錄](../../AGENTS.md#gate-豁免紀錄)由使用者明確決定不重審。

## 涉及檔案

- `skills/review/scripts/verify-artifact.py`、`scripts/test-evidence.py`：區段判定、契約閘門與正負向測試。
- `docs/agents/review-evidence.md`：PASS 後記帳提交的有效性。
- `docs/agents/acceptance.md`：核准 commit 的回填時機與 `待提交` 時的基線。
- `docs/agents/readme-templates.md`：核准 commit 欄位的填寫說明。
- `skills/review/SKILL.md`：步驟 5 的有效性檢查與報告的核准基線欄位。
- `docs/AGENTS.md`：文件版本 2.8、流程契約 2.4 與修訂紀錄。
- `CHANGELOG.md`、`docs/workflow-regression.md`（WF-14 與新案例）、`docs/rule-verification-status.md`、`docs/workflow-results/`：版本說明、回歸案例與實跑紀錄。
- `README.md`、`docs/usage.md`、`skills/execute-task/SKILL.md`、`skills/create-pr/SKILL.md`、`skills/dev-cycle/SKILL.md`：檢查敘述與引用，有語意落差才改。
- `docs/issues/issue-0002/`：本 issue 的規格、計畫與證據。

不涉及安裝器與 `rules/`。

## Gherkin 驗收劇本

```gherkin
Feature: 審查通過後的記帳不觸發重審，核准不單獨製造提交

  @SCN-001
  Scenario: PASS 後只動記帳區段，PASS 沿用
    Given 專案流程契約為 2.4，issue 的被審查提交 R 經獨立審查判定 PASS
    When R 之後的非 merge 提交只新增 R 的報告，並修改該 issue README 的記帳區段
    Then verify-artifact.py 回報有效，並列出變更的區段與欄位
    And 原 PASS 沿用，不重跑審查與程式測試
    And PR 證據與 review 記錄列出被審查 HEAD、目前 HEAD 與變更的區段
    And 報告保存在平台而非本機時，同樣只放行該 issue README 的記帳區段

  @SCN-002
  Scenario: 非記帳的變更仍讓 PASS 失效
    Given 專案流程契約為 2.4，被審查提交 R 判定 PASS
    When R 之後的變更另外動到凍結內容，或核准 commit 從一個 SHA 改成另一個、改成不是 R 祖先的提交，或範圍含 merge 提交、R 已不在目前 HEAD 的祖先
    Then verify-artifact.py 回報無效，並指出違規的檔案、區段或欄位
    And 需要重新審查，或由使用者明確決定不重審並記入 Gate 豁免紀錄
    And 把語意變更藏在記帳區段、改標題或搬動章節的對照，全部判定無效

  @SCN-003
  Scenario: 未更新到 2.4 的專案維持現行判定
    Given 專案流程契約為 2.3
    When 被審查提交之後有只動記帳區段的提交
    Then verify-artifact.py 維持現行判定：只接受恰好一個只新增該報告的提交，其餘無效
    And 回報中指出新判定需要流程契約 2.4

  @SCN-004
  Scenario: 核准回填不單獨開提交
    Given Medium issue 的規格已核准並提交，核准 commit 為待提交
    When agent 推進實作直到送審
    Then 核准 commit 的回填併入下一個有其他內容的提交，沒有只改核准 commit 的提交
    And 實作前的規格比對以承載該次核准的提交為基線

  @SCN-005
  Scenario: 送審時仍為待提交，以核准來源推導基線
    Given 被審查提交上的核准 commit 為待提交
    When 獨立 reviewer 比對核准規格
    Then 以被審查提交之前最後一個修改核准來源行的提交為基線，並把該 SHA 記在報告
    And 協調者隨報告提交回填該 SHA，PASS 依 SCN-001 沿用
    And 找不到核准來源行或推導結果不可達時，判定缺少核准基線，不以目前 HEAD 代替

  @SCN-006
  Scenario: 前後對照證明提交減少且沒有放過語意變更
    Given 同一組 fixture 分別以 v4.8.1 規則與本次規則、相同宿主設定執行
    When 走完規格核准、實作、審查、記錄使用者決策與回填
    Then 本次規則下只為回填或記帳的提交，以及因記帳觸發的重審次數，都少於基準
    And 改動驗收、證據或程式的對照組仍觸發重審
    And 任一語意變更沿用 PASS 都判定回歸失敗，不能以提交減少抵換
```

## Gherkin 核准紀錄

- **核准 commit**: e383a69
- **核准來源**: 2026-11-03 使用者對設計方向選擇建議做法（TBD-1、TBD-2）；列出推導細節（TBD-3）後明確回覆「核准」，適用 SCN-001～SCN-006 與對應實作計畫。

全部 Scenario 於 2026-11-03 核准。

## 風險與首要驗證

- **最大風險**：放寬後把語意變更當成記帳放行，讓未經審查的驗收、證據或程式變更沿用 PASS；其次是推導基線拿錯提交，掩蓋未核准的規格修改。
- **風險等級與理由**：High。這是直接放寬獨立審查的 gate，失敗形態是不會報錯的假通過，全域技能更新後會影響所有已升級的下游專案。
- **首要驗證**：改任何規則文字之前，先完成 `verify-artifact.py` 的區段判定與對抗性負向測試：把語意變更藏進記帳區段、改標題、搬動章節、改其他粗體欄位、改核准 commit、夾帶 merge 或其他檔案，以及 2.3 專案的對照。
- **選擇理由**：假通過的防線就是這支腳本，規則文字與 agent 行為都以它的判定為準；先證明它擋得住，改敘述和跑宿主實測才有意義。
- **完成證據**：`test-evidence.py` 的正負向案例全部通過，每個負向案例都回報無效並指出違規位置，2.3 專案的對照結果與現行判定相同。

## 待確認事項

| 編號 | 事項 | 狀態 | 影響 |
|---|---|---|---|
| TBD-1 | PASS 後哪些變更不讓 PASS 失效 | 已解決 | SCN-001、SCN-002；2026-11-03 使用者選「只放行記帳區段 (Recommended)」：只限該 issue 目錄的報告與 README 狀態、核准 commit、Timeline、待確認事項、Gate 豁免紀錄，其餘變動仍重審，由 verify-artifact.py 逐區段檢查並列出變更區段 |
| TBD-2 | 如何消除單獨的核准回填提交 | 已解決 | SCN-004、SCN-005；2026-11-03 使用者選「回填搭下一個提交 (Recommended)」：欄位保留，`待提交` 留到下一個有其他內容的提交回填；送審時仍是 `待提交` 時，reviewer 以最後一次修改核准來源行的提交為基線並記在報告，協調者隨報告回填 |
| TBD-3 | SCN-001～006 中推導出的細節待核准：允許多個記帳提交以淨差異判定、核准 commit 的值只能由待提交改成 R 或其祖先、待確認事項與 Gate 豁免紀錄可整節新增或刪除、其他粗體欄位一律凍結、平台報告同樣適用、流程契約 2.4 才啟用、推導不到基線時判定缺漏、以 v4.8.1 為基準做前後對照 | 已解決 | SCN-001～006；2026-11-03 使用者回覆「核准」，以上細節全部照列採用 |

## Timeline

| 日期 | 異動 | 負責人 |
|---|---|---|
| 2026-11-03 | 依下游使用調查與使用者要求建立 GitHub #2 與本機規格草案；使用者選定兩項設計方向（TBD-1、TBD-2），SCN-001～006 待核准 | 使用者／Claude Code |
| 2026-11-03 | 使用者回覆「核准」，核准 SCN-001～006 與計畫（TBD-3）；首個步驟為 S1 | 使用者／Claude Code |
| 2026-11-03 | S2、S4 實跑完成：單獨回填提交 1→0、記帳觸發重審 1→0，28b2 重審（檢查器擋下的是計畫檔，審查後更正）；追加 28d；WF-14 未另外實跑 | Claude Code |
| 2026-11-03 | 獨立審查 review-c77928c RETURN（MUST FIX 2 項）；S6 修正腳本與規則文字，S7 以最終規則重跑並新增 28b3、28e | Claude Code |
| 2026-11-03 | 覆審 review-9ee4139 PASS（無 MUST FIX、SHOULD FIX，NICE TO HAVE 5 項）；報告與本列以記帳提交保存 | Claude Code |
| 2026-11-03 | 使用者決定「修正後再覆審一次」：處理 NICE TO HAVE 1～4（計畫結論與已知限制、整節增刪限制、Gate 豁免紀錄書寫建議），NICE 5 維持；再送覆審 | 使用者／Claude Code |
| 2026-11-03 | 覆審 review-93674b1 PASS（無 MUST FIX、SHOULD FIX，NICE TO HAVE 4 項待使用者決定）；報告與本列以記帳提交保存 | Claude Code |
| 2026-11-03 | 使用者決定「修正後覆審，最後一輪」：處理 review-93674b1 的 NICE TO HAVE 1～4；覆審沒有 MUST FIX、SHOULD FIX 即停止 | 使用者／Claude Code |

---
**建立日期**: 2026-11-03
**分級**: Medium — 規則、腳本與測試多檔修改，邏輯直接，不需 Phase／Task 拆解
**風險**: High
**狀態**: 審查中
