# Issue 10 — 實作計畫

## 設計與來源

[README](README.md) 是範圍、驗收與核准的唯一來源；風險與首要驗證依 [README 的風險策略](README.md#風險與首要驗證)。本檔是唯一任務與執行證據來源。

### 增量覆審的定義（寫進 review-evidence.md）

- **適用條件**：上一份報告有效（PASS 或 RETURN）、它的 Reviewed HEAD 是新 HEAD 的祖先且中間沒有改寫歷史、目標分支與新 HEAD 的 merge-base 仍是原 BASE。任一不成立就完整審查，報告寫原因。
- **報告**：Reviewed BASE／HEAD／patch-id 照完整範圍記，create-pr 與 verify-artifact.py 都不用改。另記「上一份報告」「增量範圍」「重新查核」「沿用」四項。
- **reviewer 的責任**：讀上一份報告；增量範圍內每個變動檔案都有結論；變動會影響上一份報告查過的內容時（呼叫端、共用設定、測試前提），那部分重新查核，不寫為沿用；受影響的測試在新 HEAD 重跑。任何獨立 reviewer 都可以做，不限同一位。
- **修正來源**：kit 審查的退回與建議、使用者決定，或外部審查的要求，都走同一套。

不採「串接多份報告」：create-pr 要另外檢查整條報告鏈涵蓋完整範圍，verify-artifact.py 也要改；下游串接寫法的報告照舊算局部審查。

### 相容性

docs/AGENTS.md 文件版本 2.14，流程契約 2.5 → 2.6（minor，向後相容的新增能力）。review、dev-cycle 的最低需求維持現值：技能寫「流程契約 2.6 起可增量覆審，2.5 以下完整審查」。升最低需求會讓沒更新 docs 的下游 dev-cycle 全部暫停（v5.1.0 發布時已評估過同樣的取捨）。這個做法記在 README TBD-1，下游試用時確認。

### PASS 附建議

dev-cycle 狀態表在「有效 PASS → create-pr」之前加一列：PASS 附未加註需決策的建議，且待確認事項沒有對應結論時，依 acceptance.md「逐題確認」第 3 點把所有建議合併在一則訊息。記錄決定的提交只動記帳區段，PASS 沿用；選了修正的修完後送增量覆審。

### 回歸案例

- **WF-36**（SCN-002、SCN-003）：Medium issue，H1 有 PASS 報告，附 SHOULD FIX；H1..H2 是依建議的修正。影響組：修正讓 `due_of` 改回傳 MM/DD，H1 已審過、這次未改動的 `overdue` 拿它和 ISO 日期比較，SCN-002 因此失敗，但現有測試照樣通過。對照組：修正只新增測試。36c：同對照組，分支 rebase 到新的 main（H1 不是祖先）。
- **WF-37**（SCN-004）：PASS 報告附 2 項 SHOULD FIX、1 項 NICE TO HAVE，都沒有需決策；要求 `/dev-cycle` 推進。對照組：PASS 沒有建議。

fixture 以 issue-0003 的 `build_fixtures.py` 方式建立，放在本 issue 的 `fixtures/`；判準寫進 `fixtures/expected.md`，實跑前提交。實跑依 [workflow-regression](../../workflow-regression.md)，用隔離設定載入工作樹的技能，每組 2 輪。

## 實作步驟

| 編號 | 工作與產出 | 相依／啟用條件 | 驗收編號 | 完成判準 | 狀態／證據 |
|---|---|---|---|---|---|
| S1 | review-evidence.md 新增「增量覆審」；review 技能「輸入與範圍」指向它，送審時傳入上一份報告，報告範本加增量欄位；docs/AGENTS.md 2.14／契約 2.6 與修訂紀錄（fixture 由 init-project.py 部署，S2 需要契約 2.6）；WF-36 fixture 與 expected.md 先提交 | SCN-001～003 已核准 | SCN-001～003 | 文字涵蓋上方定義的條件、報告與責任；fixture 的影響組在 H2 上 `overdue` 確實會壞（以腳本執行確認）；判準在 S2 前提交 | ✅ 2026-11-19 review-evidence.md「增量覆審」（條件三項、報告欄位、reviewer 責任、不成立時完整審查）；review 技能輸入與範圍、送審步驟、報告範本兩處欄位；docs/AGENTS.md 2.14／契約 2.6。[s1-fixture](evidence/s1-fixture.txt)：三組在 H2 測試全數通過；wf36 的 `overdue` 在 H2 回傳 [1, 2]（2026-12-01 被誤判），wf36b、wf36c 回傳 [1]；wf36c 的原 H1 不是 HEAD 祖先、merge-base 改為新的 main。判準 [expected.md](fixtures/expected.md) 與本步驟同一提交 |
| S2 | 隔離設定實跑 WF-36 影響組、對照組、36c，各 2 輪 | S1 | SCN-001～003 | 影響組 2／2 指出 `overdue` 受影響並重新查核；對照組 2／2 寫明沿用、沒有把無關內容列為受影響；36c 2／2 完整審查並寫原因；報告的 Reviewed BASE 都是 merge-base。未達成時修正文字後重跑，記錄每一輪 | 待開始 |
| S3 | dev-cycle 狀態表加「PASS 附建議」列；docs/usage.md「PR 與 review」；WF-37 fixture 與 expected.md 先提交 | S2、SCN-004、005 已核准 | SCN-004、005 | dev-cycle 的新列與既有「需決策」「RETURN」列不互相遮蔽（逐列走過三種報告）；判準在 S4 前提交 | 待開始 |
| S4 | 隔離設定實跑 WF-37 與對照組，各 2 輪 | S3 | SCN-004 | 2／2 在一則訊息列出 3 項建議、附建議答案與三個選項，未提問前不改檔、不開 PR；對照組 2／2 不提問直接進 create-pr | 待開始 |
| S5 | workflow-regression 新增 WF-36、37；rule-verification-status 記實跑結果；CHANGELOG（未發布的 5.2.0）；跑根目錄五項檢查 | S4 | SCN-001～005 | 五項檢查通過；CHANGELOG 寫明 SCN-005 只做靜態覆核 | 待開始 |
| S6 | 送獨立審查（工具呼叫上限 30 次，固定檢查清單：條件三項、報告四欄、SCN-002 的影響查核、狀態表列序、相容做法） | S5 | SCN-001～005 | PASS，或已依使用者決定處理 | 待開始 |
| S7 | 發布前以候選版在一個下游實際 issue 試用，至少走到一次增量覆審；結果記在 README `## 現況` | S6 | SCN-001、SCN-004、TBD-1 | 試用回報記錄增量覆審報告的範圍欄位、有無漏查，以及 docs 為 2.5 時的行為 | 待開始 |
