# S2 實跑結果（2026-11-24）

判準見 [fixtures/expected.md](../fixtures/expected.md)。環境：候選版 kit `e857e33`、基準版 `cd25225`（main，流程契約 2.7），各以 `git archive` 取出並 `install.sh claude` 到 session 暫存區的隔離設定；`run_case.py`，模型 `claude-opus-5-5`；每輪重新產生 fixture。每輪的工具動作與輸出在 `s2-wf*/{案例}-r{n}.md`，回合中保存的報告在 `{案例}-r{n}-review-{SHA}.md`。

| 案例 | 輪次 | 結果 | 說明 |
|---|---|---|---|
| wf43（候選） | r1、r2 | 2／2 通過 | 逐項確認兩項修正；`overdue` 寫為沿用、沒有新建議；判 PASS；沒有 Review artifact 行，有「其餘沿用 review-5bbeb0d.md」，PASS 後一句。新建議只落在增量範圍內：r1 兩項 NICE TO HAVE（README TBD-1 影響欄、計畫 S3 證據），r2 一項 NICE TO HAVE（S3 證據）。報告都已提交，`verify-artifact.py --reviewed 8daeb05 --head HEAD` 兩輪 exit 0 |
| wf43（基準） | r1、r2 | 不判定 | 兩輪也判 PASS、沒有對 `overdue` 提建議；r2 另把 S1、S2 的證據列為「範圍外」的提醒。報告照舊有 Review artifact 行與舊的 PASS 段落 |
| wf43b | r1、r2 | 2／2 通過 | 兩輪都把 `short_date` 去掉前導零列為 MUST FIX，寫明增量引入，判 RETURN |
| wf44 第一次 | r1、r2 | 0／2（fixture 缺陷） | 格式問題都列建議；判 RETURN 的 MUST FIX 是計畫檔沒有紅綠重構證據，r1 另把 Timeline「完成 S1，測試 3 項通過」當成不實回報 |
| wf44 第一次重跑 | r3、r4 | 1／2（fixture 缺陷） | r3 判 PASS；r4 判 RETURN，MUST FIX 是補上的證據前後矛盾（S1 綠燈寫 3 項，S2 的測試之後才加）。兩輪格式問題都列建議 |
| wf44 第二次重跑 | r5、r6 | 2／2 通過 | 格式問題列 SHOULD FIX 或 NICE TO HAVE，判 PASS |
| wf44b | r1～r6 | 6／6 通過 | 三版 fixture 各 2 輪，都把待核准卻已實作的 SCN-002 列 MUST FIX、判 RETURN |
| wf32 | r1、r2 | 2／2 通過 | fixture 報告帶候選版的一句提醒；兩輪都沒有提交，先說明 PASS 會失效並列出四種做法 |

## 觀察

- wf44 的六輪裡，三處格式問題沒有一輪列為 MUST FIX；兩次 fixture 修正都只改計畫檔的證據，規則文字沒改。
- WF-43 的誘餌沒有鑑別力：基準組在流程契約 2.7 的增量覆審規則下，同樣沒有對 `overdue` 提建議。這次實跑能證明候選版沒有變弱（wf43b），以及報告格式的改變；不能證明「只查修正」減少了新建議。
- 報告大小：候選 wf43 3.1KB、5.3KB，基準 4.5KB、5.3KB。精簡格式少掉的主要是固定欄位，「已查核維度」的長度仍隨 reviewer 而變。
