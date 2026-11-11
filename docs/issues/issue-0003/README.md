# Issue 3 — issue 現況以實查為準，狀態副本不再被當成權威

## 概述

來源：[GitHub #3](https://github.com/raybird/dev-rules-kit/issues/3)。2026-11-10 詢問三個下游專案：流程留下的歷史文件會不會造成 agent 的負擔或誤導。三方結論一致：歷史文件的量多半只是 token 成本，很少讓 agent 得出錯的結論；真正出錯的是外部狀態過時。合併、推送、部署、平台狀態被其他人或其他流程改變，作者那邊的文件沒有人回頭更新，agent 很有信心地引用舊值。同一份狀態又分散在 issue README、交接文件、平台留言與跨 session 記憶，沒有規定哪一份算數。

本 issue 處理三件事：外部狀態以實查為準、issue 現況只有一份權威來源、懸置掃描讀不完時如實回報。2026-11-10 使用者對四個設計題都選擇建議答案；列出推導細節（TBD-1）後回覆「核准」，核准 SCN-001～008 與實作計畫。

不在範圍：審查報告越積越多、單檔過大、規則固定開銷等 token 成本，以及記憶工具本身的改動。本 README 是驗收、核准與範圍的唯一來源；任務與證據只維護於 implementation-plan.md。


## 現況

**現行 review**: review-4d7ba1f.md

## 文件清單

- [implementation-plan.md](implementation-plan.md)

## 關鍵差異

基準為 `46e09a5`（v4.9.0，流程契約 2.4）。

| 項目 | 現況與依據 | 變更後 |
|---|---|---|
| 外部狀態 | 規則只要求證據一致才重用（[rules 第七節](../../../rules/AGENTS.zh-TW.md)、[verification.md「證據重用」](../../agents/verification.md#證據重用)），沒有規定文件、記憶、他人回報裡的合併、推送、部署、平台狀態要先查證 | rules 寫明這些值都是帶日期的線索，對外陳述或據以行動前重新查證；查不到時說明未查證並附線索來源與日期 |
| issue 現況的權威來源 | 任務與證據各有唯一來源，但交接文件、平台留言、記憶另存狀態沒有規範；[待確認事項](../../AGENTS.md#待確認事項)只規定 issue 外文件的待決事項要連回 issue | issue 現況以 README 為準；交接文件、平台留言與記憶只放指向 README 的連結，或錨定 commit 的事件 |
| 現行 review | 報告以被審查 SHA 命名，多輪審查後只能對照 Git 或 Timeline 判斷哪份是現行的 | README 可選的 `## 現況` 節記 `**現行 review**`；review 保存報告的同一個提交更新它 |
| 外部狀態紀錄 | 沒有固定位置；project.md 只登記合併判定方式 | `## 現況` 節的外部狀態表：項目、查證命令、上次結果、查證日期，每項一列、只覆寫；project.md 範本提示登記查證命令 |
| 審查後更新現況 | 記帳區段只有 Timeline、待確認事項、Gate 豁免紀錄與兩個欄位（[審查之後的提交](../../agents/review-evidence.md#審查之後的提交)） | 流程契約 2.5 起 `## 現況` 列入記帳區段，可整節新增或刪除 |
| 懸置掃描 | [pending-scan.md](../../../skills/dev-cycle/references/pending-scan.md)：範圍內全部 issue 都判定過才算完成 | 讀不完時停在已判定範圍，明列已判定、未判定筆數與範圍，建議登記起點或掃描命令，不宣稱全部完成 |

## 設計邊界

- **`## 現況` 節**：可選，有現行 review 或 issue 依賴的外部狀態時才建立，位置在 `## 概述` 之後。內容只有 `**現行 review**` 欄位（本機報告的檔名或平台報告的連結）與外部狀態表；每個外部狀態一列，更新時覆寫該列，舊值交給 Git。`**狀態**` 留在檔尾 metadata，不搬進此節。
- **記帳判定**：流程契約 2.5 起，`## 現況` 與待確認事項、Gate 豁免紀錄一樣可整節新增或刪除，節內一般行與表格列可改；節內的標題、code fence、`**現行 review**` 以外的粗體欄位行一律凍結。`**現行 review**` 寫在 `## 現況` 之外時視為一般粗體欄位，凍結。流程契約 2.4 以下的專案，`## 現況` 視為凍結章節，判定與現行相同。
- **實查的範圍**：合併、推送、部署、平台 issue／PR 狀態這類會被其他人或其他流程改變的狀態。查證命令依 project.md 登記，未登記時從 repo 設定與現有命令取得。查詢模式只回報文件與實查的差異；推進模式同時更新外部狀態表的上次結果與查證日期。
- **懸置掃描**：預設範圍不變，範圍怎麼切仍由 project.md 決定；只改完成判準與回報內容。
- **相容性**：kit 以流程契約 2.5、文件版本 2.9 發布。沒有 `## 現況` 的 README 照現行規則運作；技能宣告的最低契約不變，未更新的專案不會因此被暫停。
- **不變**：核心欄位與狀態字串、`**狀態**` 的位置、review 判定字串、獨立審查與誠實回報要求、審查報告的命名方式。

## 涉及檔案

- `skills/review/scripts/verify-artifact.py`、`scripts/test-evidence.py`：`## 現況` 的記帳判定、契約閘門與正負向測試。
- `docs/agents/review-evidence.md`、`skills/review/SKILL.md`：記帳區段加入 `## 現況`；保存報告時更新現行 review。
- `docs/AGENTS.md`：issue 現況的唯一權威、`## 現況` 的用途、文件版本 2.9、流程契約 2.5 與修訂紀錄。
- `docs/agents/document-types.md`、`docs/agents/readme-templates.md`：README 可選的 `## 現況` 節與兩種範本。
- `docs/agents/project.md`：範本提示登記外部狀態的查證命令。
- `rules/AGENTS.md`、`rules/AGENTS.zh-TW.md`：外部狀態以實查為準。
- `skills/dev-cycle/SKILL.md`、`skills/dev-cycle/references/pending-scan.md`：現況值當線索、以現行 review 找報告、掃描讀不完時的完成判準。
- `CHANGELOG.md`、`docs/workflow-regression.md`、`docs/rule-verification-status.md`、`docs/workflow-results/`：版本說明、回歸案例與實跑紀錄。
- `README.md`、`docs/usage.md`、`INSTALL.md`、`skills/execute-task/SKILL.md`、`skills/create-pr/SKILL.md`：檢查敘述與引用，有語意落差才改。
- `docs/issues/issue-0003/`：本 issue 的規格、計畫與證據。

不涉及安裝器。

## Gherkin 驗收劇本

```gherkin
Feature: issue 現況以實查為準，狀態副本不再被當成權威

  @SCN-001
  Scenario: 審查後只更新現況區塊，PASS 沿用
    Given 專案流程契約為 2.5，issue 的被審查提交 R 經獨立審查判定 PASS
    When R 之後的非 merge 提交只新增 R 的報告，並整節新增 README 的 ## 現況，或修改其中的現行 review 與外部狀態表
    Then verify-artifact.py 回報有效，變更區段列出「現況」
    And 原 PASS 沿用，不重跑審查與程式測試

  @SCN-002
  Scenario: 現況區塊夾帶凍結內容時仍要重審
    Given 專案流程契約為 2.5，被審查提交 R 經獨立審查判定 PASS
    When R 之後的提交在 ## 現況 內加入標題、code fence 或現行 review 以外的粗體欄位，或把其他章節的內容搬進 ## 現況，或出現兩個 ## 現況，或把現行 review 欄位寫在 ## 現況 之外
    Then verify-artifact.py 回報無效，並指出違規的章節與內容
    And 需重新審查

  @SCN-003
  Scenario: 流程契約 2.4 以下的專案維持現行判定
    Given 專案流程契約為 2.4，README 沒有 ## 現況
    When 被審查提交之後的提交新增 ## 現況
    Then verify-artifact.py 回報無效，訊息說明此判定需要流程契約 2.5
    And 只改 Timeline、待確認事項、Gate 豁免紀錄與兩個欄位的提交判定與現行相同
    And 沒有 ## 現況 的 README 在 dev-cycle、review 照常運作，不因缺少此節暫停

  @SCN-004
  Scenario: 現況區塊依需要建立，只覆寫不追加
    Given 一個流程契約 2.5 的 issue
    When review 保存一份新報告，或 agent 記錄 issue 依賴的外部狀態
    Then README 的 ## 現況 位在 ## 概述 之後，現行 review 指向最新報告，每個外部狀態一列，含查證命令、上次結果與查證日期
    And 更新時覆寫原列，不追加歷史列
    And 保存報告與更新現行 review 在同一個提交
    And 沒有 review 也沒有依賴的外部狀態時，不建立 ## 現況
    And **狀態** 仍在檔尾 metadata

  @SCN-005
  Scenario: 文件記錄的外部狀態過時時，以實查為準
    Given issue README 的外部狀態表記錄「尚未併入主幹」，實際上已被其他人併入
    And 對話中的他人回報或跨 session 記憶也寫著尚未併入
    When 使用者問該 issue 的狀態，或 agent 要依這個狀態採取行動
    Then agent 先執行查證命令取得現況，依實查結果回答或行動
    And 回報指出文件記錄與實查不符；推進模式同時更新上次結果與查證日期，查詢模式只回報
    And 查證不到時說明未查證，並附上線索來源與日期，不把文件值當成現況

  @SCN-006
  Scenario: dev-cycle 以現行 review 找審查報告
    Given issue 目錄有多份審查報告，README 的現行 review 指向其中一份
    When dev-cycle 判斷審查是否有效
    Then 只讀現行 review 指向的報告，再依 review-evidence.md 檢查其有效性，不逐份讀舊報告
    And 現行 review 缺漏或指向不存在的檔案時回報這項落差，再依報告綁定的被審查提交找出對應報告

  @SCN-007
  Scenario: issue 以外的地方只放指向 README 的連結
    Given agent 要在交接文件、平台留言或跨 session 記憶裡提到某 issue 的狀態
    When agent 寫入這些地方
    Then 只寫指向該 issue README 的連結，或錨定 commit 的事件，例如「某 commit 已併入主幹」，不另存「目前狀態」
    And 這些地方與 README 不一致時，以 README 的現況與實查為準

  @SCN-008
  Scenario: 懸置掃描讀不完時如實回報
    Given project.md 沒有登記掃描起點與掃描命令，issue 數超過本次能判定的量
    When 使用者查進度而未指定 issue
    Then dev-cycle 判定到能完成的範圍為止，摘要列出已判定、未判定的筆數與未判定的範圍，並建議在 project.md 登記起點或掃描命令
    And 不宣稱全部判定完成
    And 範圍內全部判定完成時，照現行版面回報
```

## Gherkin 核准紀錄

- **核准 commit**: fe43877
- **核准來源**: 2026-11-10 使用者以選項回答四個設計題，全部選擇建議答案：Q1「現行 review＋外部狀態表」（`**狀態**` 留在檔尾、不寫下一步）、Q2「rules＋docs＋project.md」、Q3「改完成判準，可如實回報部分」、Q4「開 #3，用通用措辭」；列出 SCN-001～SCN-008 與推導細節（TBD-1）後明確回覆「核准」，適用 SCN-001～SCN-008 與對應實作計畫。

全部 Scenario 於 2026-11-10 核准。

## 風險與首要驗證

- **最大風險**：`## 現況` 列入記帳區段後，驗收、證據結論或範圍這類語意變更藏進現況區塊而沿用 PASS；其次，「以實查為準」是行為規則，agent 可能照樣直接引用文件值，靜態檢查看不出來。
- **風險等級與理由**：High。這是擴大獨立審查 gate 的豁免範圍，失敗形態是不會報錯的假通過；rules 的改動影響所有使用 kit 的 agent。
- **首要驗證**：改任何規則文字之前，先完成 `verify-artifact.py` 的 `## 現況` 判定與對抗性負向測試（SCN-002、SCN-003 的每種情境，加上把凍結章節的一般行搬進現況）。
- **選擇理由**：假通過的防線就是這支腳本，規則文字與 agent 行為都以它的判定為準；先證明它擋得住，改敘述和跑宿主實測才有意義。
- **完成證據**：`test-evidence.py` 的正負向案例全部通過，每個負向案例都回報無效並指出違規位置；流程契約 2.4 專案的判定與現行相同。行為規則（SCN-004～008）另以新增的回歸案例在宿主新 session 實跑。

## 待確認事項

| 編號 | 事項 | 狀態 | 影響 |
|---|---|---|---|
| TBD-1 | SCN-001～SCN-008 是從 Q1～Q3 的答案推導，其中位置（`## 概述` 之後）、報告與現行 review 同一提交、現行 review 缺漏時的退路、2.4 專案新增現況判無效、掃描摘要的欄位屬推導細節 | 已解決 | 2026-11-10 使用者回覆「核准」，五項推導細節照列出內容採用；SCN-001～SCN-008 全部核准 |
| TBD-2 | review-5c2ca52 MUST FIX 2：SCN-007 維持原文，或放寬為允許帶查證命令與日期的查證結果 | 已解決 | 2026-11-11 使用者選「維持原文」：docs/AGENTS.md 第 6 項改為只寫 README 連結或錨定 commit 的事件，查證結果寫回 README `## 現況`；WF-32 改依原文判定，判準先於重跑提交；既有輪次照實重判 |
| TBD-3 | review-5c2ca52 SHOULD FIX 1：記帳章節的繞過寫法（巢狀容器、編號與引用的粗體、HTML 標籤）本 issue 收緊，或只登記已知限制 | 已解決 | 2026-11-11 使用者選「本 issue 一起收緊」：與 MUST FIX 1 的跨行 HTML 區塊一起改 `verify-artifact.py`，所有記帳章節變嚴；縮排程式碼區塊與表格接 `---` 維持 issue #2 的已知限制。SCN-003 的「判定與現行相同」不含這次對 HTML 與巢狀寫法的收緊（2026-11-11 補註，review-acd488f NICE 8） |
| TBD-4 | review-5c2ca52 的 8 項 NICE TO HAVE | 已解決 | 2026-11-11 使用者選「修有實質影響的」：NICE 1、2、3、5、6、8 修正；NICE 4 的現況位置登記為已知限制；NICE 7 只清掉未用的預設參數 |
| TBD-5 | review-acd488f SHOULD FIX 4：交接文件提交到已審查的 issue 分支會讓 PASS 失效，agent 沒有告知 | 不影響本次交付 | 2026-11-11 使用者選「補紀錄、另開 issue」：本 issue 在證據、回歸紀錄與驗證狀態寫明這個失敗形態，規則不改。追蹤：[#4](https://github.com/raybird/dev-rules-kit/issues/4) |
| TBD-6 | review-4d0df5c：記帳章節的 HTML 判定繼續修補允許清單，或改為含左角括號的行一律凍結 | 已解決 | 2026-11-11 使用者選「一律拒絕含左角括號的行」：不再模擬 CommonMark，只放行行中間的 br、wbr；代價是審查後在記帳內容寫 code span 裡的標籤名或佔位字也要重審，docs/AGENTS.md 寫明改用文字與 {id} |

## Timeline

| 日期 | 異動 | 負責人 |
|---|---|---|
| 2026-11-10 | 依三個下游專案的唯讀回覆建立 issue 與 GitHub #3；使用者對 Q1～Q4 選擇建議答案 | 使用者／Claude Code |
| 2026-11-10 | 使用者回覆「核准」，核准 SCN-001～SCN-008 與實作計畫（TBD-1 解決） | 使用者 |
| 2026-11-10 | S1～S6 完成；基準與候選實跑全部通過，能和 v4.9.0 區分的只有 `## 現況` 列入記帳區段與送審時建立現況，外部狀態實查、交接文件與掃描無法區分 | Claude Code |
| 2026-11-10 | 獨立審查 RETURN TO execute-task（review-5c2ca52.md）：MUST FIX 2 項（記帳章節的跨行 HTML 區塊可藏住凍結章節；SCN-007 未落到規則文字、WF-32 判定過寬，需決策），SHOULD FIX 4 項 | Claude Code |
| 2026-11-11 | 使用者對審查的需決策項目選擇建議答案（TBD-2～TBD-4 解決） | 使用者 |
| 2026-11-11 | S8：依審查修正（`3e448fc`），重跑判準先提交（`9456504`）；重跑 wf29、wf29d、wf31、wf32、WF-28b 通過，wf30c 未執行檢查器；2026-11-10 的 WF-32 兩組依 SCN-007 原文重判為未符合 | Claude Code |
| 2026-11-11 | 獨立覆審 RETURN TO execute-task（review-acd488f.md）：MUST FIX 1 項（記帳章節仍有寫法能藏住凍結章節，例如 `<details` 換行、未追蹤的多行註解），SHOULD FIX 5 項（其一需決策） | Claude Code |
| 2026-11-11 | 使用者對覆審的需決策項目選擇建議答案（TBD-5，另開 #4） | 使用者 |
| 2026-11-11 | S9：依覆審修正（`b2f321f`）；重跑 wf29、wf31、WF-28b 通過，wf30c 未執行檢查器，wf32 4 輪 3 輪通過（不穩定） | Claude Code |
| 2026-11-11 | 第三輪獨立覆審 RETURN TO execute-task（review-4d0df5c.md）：MUST FIX 2 項（允許清單的 `<br>`／行首註解會開出 HTML 區塊；code span 判定與渲染器不一致），SHOULD FIX 2 項 | Claude Code |
| 2026-11-11 | 使用者決定記帳章節含左角括號的行一律凍結（TBD-6） | 使用者 |
| 2026-11-11 | S10：依決定修正（`cff0449`）；重跑 WF-28b、wf31 通過，記帳提交經新檢查器判有效 | Claude Code |
| 2026-11-11 | 第四輪獨立覆審 RETURN TO execute-task（review-4e0177a.md）：MUST FIX 1 項（分行與行尾空白的判定和 CommonMark 不同，不可見字元能改掉渲染），SHOULD FIX 2 項 | Claude Code |
| 2026-11-11 | S11：依第四輪覆審修正分行、凍結章節空行與左方括號開頭的放行（`df2a444`）；重跑 WF-28b、wf31 通過 | Claude Code |
| 2026-11-11 | 第五輪獨立覆審 RETURN TO execute-task（review-ac2183c.md）：MUST FIX 1 項（記帳行能和同一段落的凍結行組成跨行的行內語法，例如連結 title 吞掉檔尾 metadata），SHOULD FIX 1 項 | Claude Code |
| 2026-11-11 | 使用者選擇本 issue 修正第五輪 MUST FIX 再送審；下一輪若只找到 v4.9.0 就有的同類缺口則另開 issue。S12：記帳章節含凍結內容的段落整段凍結，表格逐列判定（`3fc926a`）；重跑 WF-28b、wf31 通過 | Claude Code |
| 2026-11-11 | 第六輪獨立覆審 RETURN TO execute-task（review-20d0847.md）：MUST FIX 1 項（表格欄數計算和 GFM 不同，是 S12 新引入），SHOULD FIX 1 項；另列 v4.9.0 起就有的同類缺口 V1～V4 | Claude Code |
| 2026-11-11 | S13：表格欄數照 GFM 計算，含凍結列的表格表頭與分隔列一併凍結；v4.9.0 起就有的 V3、V4 依使用者先前決定另開 #5（`eea9ac8`）；重跑 WF-28b、wf31 通過 | Claude Code |
| 2026-11-11 | 第七輪獨立覆審 RETURN TO execute-task（review-4d7ba1f.md）：MUST FIX 1 項（表頭只有一個管線的假表格仍被當成表格，S13 沒修完整），SHOULD FIX 2 項；另列 v4.9.0 起就有的 V5、V6 | Claude Code |

---
**建立日期**: 2026-11-10
**分級**: Medium — 規則、範本、一支判定腳本與測試多檔修改，邏輯直接，不需 Phase／Task 拆解
**風險**: High
**狀態**: 實作中
