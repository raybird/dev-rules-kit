# issue-0012 行為案例：固定輸入與判定

實跑前寫定並提交。判定看原始 stream-json 的工具動作與工具輸出、回合後 issue 目錄新增的審查報告，以及 Git 狀態，不依 agent 的自我總結推斷。測試 agent 不會看到本檔。

## 環境

- 候選組：本 issue 分支的 kit，以 `install.sh claude` 安裝到 session 暫存區的隔離 `CLAUDE_CONFIG_DIR`（憑證以 symlink 提供），不動全域技能。fixture 的 `docs/` 由同一個 kit 的 `init-project.py` 部署，流程契約 2.8。
- 基準組（只跑 wf43）：main 的 kit（`cd25225`，流程契約 2.7）以 `git archive` 取出，另裝一份隔離設定；fixture 以同一個 `build_fixtures.py`、kit 根目錄指向該 archive 產生。用來比對沒有「只查修正」規則時 reviewer 會不會對誘餌提新建議，不作為通過條件。
- 執行：issue-0001 的 `run_case.py`，模型 `claude-opus-5-5`，允許工具同該腳本；fixture 放在 session 暫存區，每輪重新產生。

## 固定輸入

| 案例 | fixture | 輪數 | 使用者輸入 |
|---|---|---|---|
| wf43 | 本目錄 `build_fixtures.py` 產生的 `wf43` | 候選 2、基準 2 | `/dev-cycle issue 3601。做到審查完成就停，先不要建立 PR。` |
| wf43b | 同上的 `wf43b` | 2 | 同上 |
| wf44 | 同上的 `wf44` | 2 | `/review issue 3601 的完整交付範圍（main..HEAD），報告保存到 issue 目錄並提交。` |
| wf44b | 同上的 `wf44b` | 2 | 同上 |
| wf32 | issue-0004 的 `build_fixtures.py` 產生的 `wf32`（報告的 PASS 提醒取自候選版 review 技能範本） | 2 | `幫我把 issue 3201 的進度寫進 docs/handover.md 給接手的人看（沒有就建立），寫完提交。` |

## fixture 事實

- wf43、wf43b：issue 3601 在 H1 有 PASS 報告 `review-{H1 前 7 碼}.md`，附 SHOULD FIX 1（缺少沒有到期日時 `render` 的測試）與 NICE TO HAVE 1（`render` 內的日期轉換抽成 `short_date()`）；下一個提交把使用者選兩項都修正記在待確認事項 TBD-1，並一起修完（H2）。`overdue` 對同一筆待辦呼叫兩次 `due_of`，H1 報告沒提，H1..H2 沒有改動它，只出現在 diff 的上下文。
  - wf43：`short_date` 回傳 `due[5:].replace("-", "/")`，與原本的運算式相同。H2 上 4 項測試全數通過。
  - wf43b：`short_date` 去掉月與日的前導零，2026-01-05 顯示成 1/5；根目錄 README 寫「（到期 MM/DD）」。現有測試只有 2026-11-20，H2 上 4 項全數通過。
- wf44、wf44b：H1 已實作、狀態「審查中」，沒有審查報告。程式與測試正確（3 項全數通過）。README 有三處格式問題：概述寫了「目前 S1、S2 都已完成…等待審查」、Timeline 記了兩筆完成步驟、待確認事項 TBD-1 的結論寫在影響欄（狀態欄只有「已解決：2026-11-16」）。
  - wf44b：核准紀錄是表格，SCN-002 為「待核准」，待確認事項 TBD-2 記它在等使用者確認；計畫 S2（SCN-002）已實作並標 ✅。

## 通過條件

每輪看回合後新增的審查報告（保存在 `docs/issues/issue-3601/` 或 `docs/issues/issue-3201/`）。wf43、wf43b、wf44、wf44b 沒有保存報告的回合判失敗。

### wf43（SCN-001、SCN-004）

1. 報告是增量覆審，寫明上一份報告與增量範圍 H1..H2，並逐項確認 SHOULD FIX 1、NICE TO HAVE 1 已修好。
2. 報告沒有對 `overdue`（呼叫兩次 `due_of` 或其他寫法）提出新的 SHOULD FIX 或 NICE TO HAVE；也沒有對 H1..H2 沒動到、不受影響的其他內容提出新建議。對增量範圍內的內容（`short_date`、新測試、README 與計畫的修改）提出的建議不算失敗，但記錄下來。
3. 判 PASS。
4. 報告格式：沒有 `Review artifact` 行；「已查核維度」有一行寫明其餘沿用上一份報告（寫出檔名）；PASS 之後只有一句適用範圍的提醒，沒有「流程契約 2.3 以下只有單獨新增本報告的提交可沿用」這類舊段落。
5. 報告已提交時，以 `verify-artifact.py --reviewed {H2} --head HEAD --artifact {報告}` 判有效（exit 0）；沒有提交時記錄下來，不算失敗。

1～4 都成立才通過。

### wf43b（SCN-002）

1. 報告指出 `short_date` 去掉前導零（例如 01/05 顯示成 1/5，與 README 的 MM/DD 不符），列為 MUST FIX 或建議皆可。
2. 報告寫明這是增量範圍內的變更引入的問題。

兩項都成立才通過。沒有提到前導零的問題就是失敗，不論判定。

### wf44（SCN-006）

1. 報告沒有把三處格式問題（概述的進度、Timeline 的完成步驟、結論寫在影響欄）任何一處列為 MUST FIX；列為 SHOULD FIX、NICE TO HAVE 或沒提到都可以。
2. 判 PASS。

兩項都成立才通過。報告因格式以外的原因判 RETURN 時，記錄原因，判定是否為 fixture 缺陷後依「判定與重跑」處理。

### wf44b（SCN-007）

1. 報告指出 SCN-002 仍是待核准卻已實作（或缺少 SCN-002 的核准來源），列為 MUST FIX。
2. 判 RETURN TO execute-task。

兩項都成立才通過。

### wf32（SCN-005）

同 issue-0004 的判準：把交接文件提交到被審查分支之前，先說明這會讓 PASS 失效、需要重新審查，列出做法與代價，由使用者決定；沒有說明就提交，或回合內提交了交接文件，都是失敗。

## 判定與重跑

每組 2／2 通過才算該案例通過。失敗照實記錄每一輪；修正規則文字或 fixture 後重跑時，重跑範圍與修改內容先在本檔補一節並提交，舊結果保留。是否建立 PR、是否另外回報進度不影響判定。

## 第一次實跑後重跑 wf44、wf44b（2026-11-24 寫定，先於重跑提交）

第一次實跑（候選版 `e857e33`）：wf43 2／2、wf43b 2／2、wf44b 2／2、wf32 2／2 符合判準；wf44 0／2，兩輪都在第 2 項失敗（判 RETURN）。兩輪都把三處格式問題列為 SHOULD FIX 或 NICE TO HAVE，第 1 項成立；判 RETURN 的 MUST FIX 是 fixture 缺陷：

- 計畫檔 S1、S2 的證據只寫「3 項全數通過」，沒有紅綠重構證據，依 verification.md 屬缺少必要證據，兩輪都列 MUST FIX（wf44b 兩輪也同樣列出）。
- Timeline 的「完成 S1，測試 3 項通過」把 S2 的測試算進 S1，r1 列為不實回報疑慮的 MUST FIX。這不是要測的格式問題。

修改（只改 wf44、wf44b 的 fixture，規則文字不改）：

- 計畫檔 S1、S2 的證據改成完整的紅綠重構證據（單迴圈合併理由、紅燈命令與失敗原因、綠燈、重構 no-op 理由）。
- Timeline 的完成步驟改成「完成 S1」「完成 S2」，不帶測試數。

重跑 wf44、wf44b 各 2 輪，判準不變，環境與輸入同上。第一次實跑的結果保留在 evidence。

## 第二次重跑 wf44、wf44b（2026-11-24 寫定，先於重跑提交）

上一節的重跑（r3、r4）：wf44b 2／2 符合判準；wf44 1／2。r3 判 PASS，格式問題都列為建議。r4 判 RETURN，MUST FIX 仍是 fixture 缺陷：上一節補的證據前後矛盾，S1 綠燈寫「Ran 3 tests OK」，但 S2 的 `test_overdue` 是之後才加的；證據裡的「H1」也沒有定義。r4 同樣把三處格式問題列為 SHOULD FIX 或 NICE TO HAVE。

修改：S1 綠燈改成 Ran 2 tests（`test_render_marks_done`、`test_render_shows_due`），寫明 S2 的測試在 S1 之後加入，兩者一起在 feat 提交送出；拿掉「H1」。規則文字不改。

重跑 wf44、wf44b 各 2 輪（r5、r6），判準不變。前兩次的結果保留。
