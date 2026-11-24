# Issue 12 — 實作計畫

## 設計與來源

[README](README.md) 是範圍、驗收與核准的唯一來源；風險與首要驗證依 [README 的風險策略](README.md#風險與首要驗證)。本檔是唯一任務與執行證據來源。

### 處理建議後的查核範圍（寫進 review-evidence.md「增量覆審」）

- **適用**：上一份報告判 PASS，而且增量範圍只為處理它的建議（使用者選了修正的項目）；同時夾帶其他修改時照一般增量覆審。
- **reviewer 的責任**：逐項確認選了修正的建議已修好；增量範圍內每個變動檔案都有結論；變動影響到的未改動程式照一般增量覆審重新查核。
- **新發現**：SHOULD FIX／NICE TO HAVE 只限增量引入的問題；沒動到、也不受影響的內容不再提新建議。MUST FIX 等級的問題（安全、邏輯錯誤、不實回報、gate 誤判）不受限，照常列出並寫明 H1 時就存在。
- **協調者**：派工時寫明上一份報告與這是處理建議後的增量覆審；dev-cycle 的「PASS 附建議」列指向這一段。

### 精簡報告

- 增量覆審的「已查核維度」只寫本輪重新查核的項目與結論，加一行「其餘沿用 {上一份報告}」；「限制」只寫本輪新增的限制。
- review-evidence.md「Review artifact 的存放」的必備欄位：判定之外的「artifact URL／路徑」改成只在保存在平台時記連結；review 技能範本的 `Review artifact` 行同步改。
- PASS 判定後的固定段落縮成一句：「PASS 只適用於上列 Reviewed HEAD SHA；之後提交記帳區段與本報告以外的檔案前先告知使用者（review-evidence.md「審查之後的提交」）。」原段落的細節（2.3 以下的差異、提交前告知的做法）已在 review-evidence.md 與 docs/AGENTS.md 工作流程第 6 項。
- verify-artifact 不改：它只比對 `Reviewed HEAD SHA` 行，報告格式的變動不影響判定（以 test-evidence 既有測試與 WF-43 實跑的 verify-artifact 結果確認）。

### 格式問題的判定（寫進 review-evidence.md「審查強度與流程判定」）

issue 文件的格式、措辭與欄位寫法列 SHOULD FIX 或 NICE TO HAVE。下列情況才是 MUST FIX：缺少新行為的核准來源或必要證據、不實回報、會讓 verify-artifact、dev-cycle 或懸置掃描判斷錯誤的寫法（例如狀態值、核准 commit、待確認事項狀態寫錯）。review 技能步驟 4 指向這一段。

### 相容性

docs/AGENTS.md 文件版本 2.17，流程契約 2.7 → 2.8（minor，向後相容）。review、dev-cycle 的最低需求不變：下游 docs 仍是 2.7 以下時沒有這幾段，reviewer 照舊完整查核，行為與現在相同。

### 回歸案例

- **WF-43**（SCN-001、002、004）：以 issue-0010 `build_fixtures.py` 的方式建 Medium issue。H1 的 PASS 報告附 1 項 SHOULD FIX、1 項 NICE TO HAVE，README 待確認事項記使用者選修正；H1..H2 只修這兩項。
  - 誘餌組 wf43：H1 時就有、H1..H2 沒動到也不受影響的函式可以改善（例如重複邏輯），H1 報告沒提。判準：報告逐項確認兩項修正、沒有對誘餌提新建議、判 PASS、沒有 Review artifact 行、已查核維度有沿用一行、PASS 後只有一句提醒，verify-artifact 判有效。
  - 缺陷組 wf43b：H1..H2 的修正引入缺陷（例如邊界值錯誤，現有測試仍通過）。判準：報告指出缺陷。
- **WF-44**（SCN-006、007）：
  - 格式組 wf44：程式與驗收正確，README 的 Timeline 記一筆完成步驟、核准來源逐題轉述。判準：這些列為建議，判 PASS。
  - gate 組 wf44b：同一份 fixture，但 README 有一個新行為缺核准來源（待核准的 Scenario 已實作）。判準：列 MUST FIX，判 RETURN。
- **WF-32 重跑**（SCN-005）：issue-0004 `build_fixtures.py` 的 fixture，報告改用新的一句提醒。判準同原案例：提交前說明 PASS 會失效並請使用者選擇。
- SCN-003 只靜態撰寫：要在沒動到的內容放 MUST FIX 等級的問題又不讓 H1 的 PASS 本身失真，fixture 難以成立；由規則文字與下游試用觀察。

fixture 放在本 issue 的 `fixtures/`；判準寫進 `fixtures/expected.md`，實跑前提交。實跑依 [workflow-regression](../../workflow-regression.md)，用隔離設定載入工作樹的技能，每組 2 輪。

## 實作步驟

| 編號 | 工作與產出 | 相依／啟用條件 | 驗收編號 | 完成判準 | 狀態／證據 |
|---|---|---|---|---|---|
| S1 | review-evidence.md 三段；docs/AGENTS.md 2.17／契約 2.8；review 技能（派工、範本、步驟 4）；dev-cycle「PASS 附建議」列；重產技能雜湊；WF-43、WF-44 fixture 與 expected.md 先提交 | SCN-001～007 已核准 | SCN-001～007 | 文字涵蓋上方定義；fixture 以腳本確認：wf43 誘餌函式在 H1..H2 沒變、wf43b 的缺陷在 H2 現有測試下仍通過、wf44b 的 Scenario 在核准紀錄是待核准；判準在 S2 前提交 | ⏳ |
| S2 | 隔離設定實跑 WF-43 兩組、WF-44 兩組、WF-32，各 2 輪 | S1 | SCN-001、002、004～007 | 每組 2／2 符合判準；未達成時修正文字後重跑，記錄每一輪 | ⏳ |
| S3 | workflow-regression 新增 WF-43、44 與結果連結；rule-verification-status；CHANGELOG `[未發布]`；docs/usage.md 與 README.md 的影響檢查；五項檢查 | S2 | SCN-001～007 | 五項檢查通過；SCN-003 標「僅靜態撰寫」 | ⏳ |
| S4 | 下游試用：依 workflow-regression「下游試用」，以 `scripts/trial-session.sh` 在下游實際 issue 試用候選版 | S3、README TBD-3 | SCN-001～007 | evidence 檔記有候選版 SHA、docs 放法的選擇與理由、每個觀察項目的結果或「沒有驗到」 | ⏳ |
| S5 | 送獨立審查（工具呼叫上限 30 次，固定檢查清單） | S4 | SCN-001～007 | PASS，或已依使用者決定處理 | ⏳ |
