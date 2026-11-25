# Issue 17 — 實作計畫

## 設計與來源

[README](README.md) 是範圍、驗收與核准的唯一來源；風險與首要驗證依 [README 的風險策略](README.md#風險與首要驗證)。本檔是唯一任務與執行證據來源。

### 核准來源與核准表（acceptance.md）

- 「逐題確認」最後一段：核准來源改為每次核准一句，寫日期、使用者核准的原話與涵蓋的驗收編號；選了建議以外答案的題目引用使用者選的那一項。答案的內容寫進驗收條件；改變範圍卻沒寫進驗收條件的（例如不做什麼）寫在概述或對應章節。解決待確認事項時，結論、選項原文與接受的代價寫在該項的狀態欄。
- 「Gherkin 核准紀錄」：`**核准來源**` 欄位說明改為「每次核准一句」；規格修訂後重新核准時加一句，指向待確認事項編號，不重抄選項。表格只在有 `待核准`／`待重新核准` 時使用；全部回到 `已核准` 時收回單行「全部 Scenario 於 YYYY-MM-DD 核准」，日期寫最後一次核准，各次核准由核准來源與 Timeline 承載。舊單行格式的相容規則（其他區塊出現待核准字樣就展開表格）改成只看核准區塊本身。
- readme-templates.md 的範本與註解、issue-checklist 的核准來源項、new-issue 步驟 4 依上面調整或確認不需改。

### 審查之後的提交（review-evidence.md）

重排成：

1. 一段開頭：報告綁定被審查提交；審查之後可以改、PASS 沿用的是新增本次報告與 issue README 的記帳區段（`**狀態**`、`**核准 commit**`、`## 待確認事項`、`## Timeline`、`## Gate 豁免紀錄`，2.5 起加 `## 現況`）。寫法用一般段落、表格列與清單；verify-artifact 判需重審時，照它指出的行處理。
2. 依流程契約的條件（2.4 起三項、2.5 起的 `## 現況`、2.3 以下單一報告提交），保留判定需要的句子。
3. 凍結內容有錯時：先告知使用者，做法是把更正記在待確認事項（PASS 沿用），或修正後送增量覆審。
4. 不符合條件時的告知與豁免（照舊）。

`<`、`[`、段落、表格、空行與 NBSP 這類邊界移到 `skills/review/references/frozen-content.md`（暫名），由 review 技能步驟 5 與 review-evidence.md 指向它。verify-artifact.py 不修改。docs/AGENTS.md「待確認事項」的寫法限制精簡成一句（一般段落、表格列與清單；不含 `<`；行首不用粗體或 `[`），其餘指向同一份參考檔（README TBD-1）。

### 版本

文件版本 2.17 → 2.18。流程契約預設不升（判定不變，技能不解析核准表），依 README TBD-2 在審查時確認。

## 實作步驟

| 編號 | 工作與產出 | 相依／啟用條件 | 驗收編號 | 完成判準 | 狀態／證據 |
|---|---|---|---|---|---|
| S1 | 現行「審查之後的提交」與 docs/AGENTS.md「待確認事項」的寫法限制逐句拆成判定規則，建立「規則 → 新位置」對照表（首要驗證） | SCN-007 已核准 | SCN-007 | `evidence/s1-rule-map.md` 每一條規則都有編號、原文出處與預定的新位置（review-evidence.md 或技能參考檔）；沒有規則被標為刪除 | ✅ 2026-11-25 [s1-rule-map.md](evidence/s1-rule-map.md)：review-evidence.md 拆成 R1～R26（另拆出 R5a、R7a、R10a），docs/AGENTS.md 拆成 A1～A5、G1，另列新增的 N1～N3；每列都有新位置，沒有一條刪除 |
| S2 | 改寫 review-evidence.md「審查之後的提交」與 docs/AGENTS.md「待確認事項」的寫法限制；新增 review 技能參考檔；SKILL.md 步驟 5 指向它；重產技能歷代雜湊 | S1 | SCN-005、006、007 | 對照表每列的新位置都找得到對應文字；邊界細節只在參考檔；verify-artifact.py 無 diff；test-evidence 全部通過 | ✅ 2026-11-25 review-evidence.md「審查之後的提交」改成先列可以改的內容、再列沿用條件，新增凍結內容寫錯時的兩種做法，約 2150 字減為 1555 字；`<`、`[`、段落與表格的邊界移到新增的 `skills/review/references/frozen-content.md`；docs/AGENTS.md「待確認事項」的寫法限制精簡成一句；review 技能步驟 5 指向參考檔。對照表「S2 核對」欄逐列填上新位置。重產技能歷代雜湊；install.sh 安裝後 review 技能含 `references/frozen-content.md`。五項檢查見 [kit-checks.txt](evidence/kit-checks.txt)（test-evidence 315 項通過，verify-artifact.py 對 `9318f69` 無 diff） |
| S3 | acceptance.md、readme-templates.md 的核准來源與核准表；issue-checklist、new-issue 的影響檢查 | SCN-001～004 已核准 | SCN-001～004 | 靜態核對：「核准來源記原話、日期、題號、建議內容」的要求已移除；單行與表格的使用條件、舊格式相容規則與新規則一致；全 repo 沒有其他要求逐題轉述的寫法 | ✅ 2026-11-25 acceptance.md「逐題確認」改成答案寫進驗收條件、核准來源依核准紀錄只記這次核准；「Gherkin 核准紀錄」的核准來源改為每次核准一句，重新核准時加一句並指向待確認事項；只以逐題答案核准、使用者沒看過驗收條件清單時另寫各題對應的驗收編號（保留 WF-19 追得到題號的需求，不抄選項）。表格只在有待核准或待重新核准時使用，全部核准後收回單行；舊單行的相容規則改成：Timeline 與已解決的待確認事項提過的待核准是歷史，仍為 `待確認` 的項目寫明待核准時與單行矛盾、先核對核准來源。readme-templates 兩份範本的核准來源與註解同步。issue-checklist、new-issue 步驟 4、rules 不需改。`grep` 舊寫法（題號、建議內容、展開表格、同日一次核准）在 docs、rules、skills 只剩 workflow-regression WF-06、WF-19 的期望與 rule-verification-status 的歷史列，由 S5 處理 |
| S4 | WF 案例 fixture、判準與實跑：核准紀錄（SCN-001、002、003、004）、PASS 之後的補記與凍結內容有錯（SCN-005、006） | S2、S3 | SCN-001～006 | 每個案例在隔離設定實跑候選版 2 輪並保存輸出；SCN-005 另跑基準版（main）對照；結果與判準寫在 `evidence/s4-results.md`，未達標的照實記錄 | ⏳ |
| S5 | 文件版本、workflow-regression、CHANGELOG `[未發布]`、rule-verification-status、docs/usage.md、README.md 的影響檢查；五項檢查 | S2～S4 | SCN-001～007 | 五項檢查通過；rule-verification-status 記下沒有下游試用（Gate 豁免）與未達標項目 | ⏳ |
| S6 | 送獨立審查（工具呼叫上限 30 次，固定檢查清單） | S5 | SCN-001～007 | PASS，或已依使用者決定處理 | ⏳ |
