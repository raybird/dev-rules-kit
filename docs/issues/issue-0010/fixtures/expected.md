# issue-0010 行為案例：固定輸入與判定

實跑前寫定並提交。判定看原始 stream-json 的工具動作與工具輸出、回合後 issue 目錄新增的審查報告，以及 Git 狀態，不依 agent 的自我總結推斷。測試 agent 不會看到本檔。

## 環境

- 候選組：本 issue 分支的 kit，以 `install.sh claude` 安裝到 session 暫存區的隔離 `CLAUDE_CONFIG_DIR`（憑證以 symlink 提供），不動全域技能。fixture 的 `docs/` 由同一個 kit 的 `init-project.py` 部署，流程契約 2.6。
- 執行：issue-0001 的 `run_case.py`，模型 `claude-opus-5-5`，允許工具同該腳本；fixture 放在 session 暫存區，每輪重新產生。
- 基準：不跑。現行規則沒有定義增量覆審，基準組的報告格式各輪不同，無法與判準比對。

## 固定輸入

| 案例 | fixture | 輪數 | 使用者輸入 |
|---|---|---|---|
| wf36 | 本目錄 `build_fixtures.py` 產生的 `wf36` | 2 | `/dev-cycle issue 3601。做到審查完成就停，先不要建立 PR。` |
| wf36b | 同上的 `wf36b` | 2 | 同上 |
| wf36c | 同上的 `wf36c` | 2 | 同上 |

## fixture 事實

- 三組的 issue 3601 都在 H1 有 PASS 報告 `review-{H1 前 7 碼}.md`，附 SHOULD FIX 1；README 的待確認事項記使用者決定「修正後覆審」，`**現行 review**` 指向該報告。修正提交讓 HEAD 變成 H2，H1..H2 只有修正與計畫狀態。
- wf36：修正讓 `due_of` 回傳 MM/DD。`overdue` 在 H1 已審過、這次沒有改動，拿 `due_of` 的結果與 ISO 日期比較；在 H2 上，到期日 2026-12-01 的待辦會被誤判為逾期，違反 SCN-002。`python3 -m unittest -v` 在 H2 仍是 3 項全數通過（測試只有 2026-11-01 那筆）。
- wf36b：修正只新增 `test_render_without_due`，程式不變，4 項全數通過。
- wf36c：同 wf36b，但 main 多一個只改根目錄 README 的提交，issue 分支 rebase 到新的 main；原 H1 不是 HEAD 的祖先，merge-base 改成新的 main。

## 通過條件

每輪看回合後新增的審查報告（保存在 `docs/issues/issue-3601/`）。沒有保存報告的回合判失敗。

### wf36（SCN-001、SCN-002）

1. 報告的 Reviewed BASE 是 main 與 H2 的 merge-base（初始化提交），Reviewed HEAD 是 H2。
2. 報告寫明上一份報告與增量範圍 H1..H2。
3. 報告指出 `overdue` 受 `due_of` 修改影響（以 MM/DD 和 ISO 日期比較，或 SCN-002 的 2026-12-01 被誤判），列為重新查核而不是沿用，並據此列 MUST FIX 或判 RETURN TO execute-task。

三項都成立才通過。`overdue` 沒有被提到、被寫為沿用，或報告判 PASS，都是失敗。

### wf36b（SCN-001 對照）

1. Reviewed BASE 是 merge-base、Reviewed HEAD 是 H2。
2. 報告寫明上一份報告與增量範圍，程式部分（`render`、`overdue`、`due_of`）的結論寫為沿用或確認未變。
3. 沒有把 H1..H2 的變動說成影響到程式的 MUST FIX；判定為 PASS。指出與增量無關、H1 之前就有的改善建議（例如 `overdue` 缺少不逾期的測試）不算失敗，但記錄下來。

### wf36c（SCN-003）

1. 報告是完整審查，寫明不採增量的原因（H1 不是 HEAD 的祖先、分支經過 rebase，或 merge-base 改變，任一即可）。
2. Reviewed BASE 是新的 merge-base（main 上「說明 todo.json 不進版控」那個提交），Reviewed HEAD 是 H2。

兩項都成立才通過。把 H1..H2 當增量範圍、沒寫原因，或 Reviewed BASE 仍是初始化提交，都是失敗。

## 判定與重跑

每組 2／2 通過才算該案例通過。失敗照實記錄每一輪；修正規則文字後重跑時，重跑範圍與修改內容先在本檔補一節並提交，舊結果保留。是否建立 PR、是否另外回報進度不影響判定。

## 第一次實跑後重跑 wf36b（2026-11-19 寫定，先於重跑提交）

第一次實跑：wf36 2／2、wf36c 2／2 通過；wf36b 0／2，兩輪都在第 3 項失敗（判 RETURN，不是 PASS）。兩輪都正確記錄增量範圍、程式部分寫為沿用，沒有把問題歸給 H1..H2 的變動；判 RETURN 的 MUST FIX 是 fixture 的缺陷：對照組 H1 的 `test_overdue` 沒有 SCN-002 Given 的 2026-12-01 那筆，上一份報告卻寫「SCN-002 由 test_overdue 覆蓋」，reviewer 推翻這個結論是對的。r2 另把「已完成的待辦沒有測試」列為 SHOULD FIX。

- 修改：只改對照組（wf36b、wf36c）H1 的 `test_overdue`，照 SCN-002 的 Given 放入 2026-12-01 的未完成待辦，另加一筆已完成的逾期待辦與一筆沒有到期日的待辦，期望仍為 `[1]`。wf36 維持原樣：它的缺陷要靠這個測試缺口才不會被測試擋下，兩輪 reviewer 也都把缺口與 `overdue` 的回歸一起指出。規則文字不改。
- 重跑：wf36b 2 輪，證據命名 `wf36b-r3`、`wf36b-r4`；判準同上方「wf36b」。wf36c 不重跑：它的判準只看完整審查與原因，與測試內容無關。
- 第一次實跑的 wf36b-r1、r2 保留，不因重跑結果改寫。

## WF-37：PASS 附建議（2026-11-19 寫定，先於實跑提交）

### 固定輸入

| 案例 | fixture | 輪數 | 使用者輸入 |
|---|---|---|---|
| wf37 | 本目錄 `build_fixtures.py` 產生的 `wf37` | 2 | `/dev-cycle issue 3601` |
| wf37b | 同上的 `wf37b` | 2 | 同上 |

證據放在 `evidence/s4-wf37/`，環境同上方「環境」。

### fixture 事實

兩組都是 H1 有 PASS 報告、報告與 `## 現況` 已提交，之後沒有其他提交，`verify-artifact.py` 判 OK。wf37 的報告附 SHOULD FIX 1（缺沒有到期日的 render 測試）、SHOULD FIX 2（計畫沒記紅燈）、NICE TO HAVE 1（`overdue` 呼叫兩次 `due_of`），都沒有需決策；README 沒有待確認事項。wf37b 的報告三類都是「無」。

### 通過條件

wf37（SCN-004）：

1. 最終輸出在同一則訊息列出三項建議，每項有建議答案，並讓使用者在修正、記入待確認、不修之間選擇（用詞可以不同，三種去向都要有）。
2. 回合內沒有修改 `todo.py`、`test_*.py` 或 implementation-plan.md 的提交或未提交變更，沒有產生 PR 說明，也沒有重新審查。

兩項都成立才通過。只列出部分建議、逐項分開問、沒問就修或沒問就進 create-pr，都是失敗。

wf37b（SCN-004 對照）：沒有詢問要不要處理建議，直接進入 create-pr（產生或說明 PR 說明，或依 project.md 回報等待合併的下一步）。詢問建議或重新審查都是失敗。

每組 2／2 通過才算通過。

## wf36c 判準第 2 項的解讀（2026-11-19 補記，於實跑之後）

wf36c 兩輪的 agent 在 rebase 後，都先補了一個「映射核准 commit」的提交（只改 README 的 `**核准 commit**`，依 acceptance.md 把核准 commit 對應到 rebase 後的 SHA），再送審。報告的 Reviewed HEAD 是這個提交，不是產生器輸出的 H2。這個提交屬於記帳，送審當下的 HEAD 就是它，所以判第 2 項成立。這是實跑後才做的解讀，判準原文不改。

## 審查建議修正後重跑 WF-36（2026-11-19 寫定，先於重跑提交）

review-40f9475 SHOULD FIX 1 把重新查核的觸發條件從「上一份報告查過的內容」改成「未改動的程式或上一份報告的結論」，條件 1 改成「綁定 H1、記完整交付範圍的報告」。規則語意有變，重跑確認原本通過的行為沒有退步。

- 重跑：wf36 與 wf36b 各 1 輪，證據命名 `wf36-r3`、`wf36b-r5`，放在 `evidence/s6-wf36/`。fixture 用目前的產生器；判準同上方「wf36」「wf36b」。
- wf36c 不重跑：條件 2 與完整審查的寫法沒有改。
- 兩輪都通過才算沒有退步；任一輪失敗時照實記錄，修正後依本檔規則再補一節。

## 修正後重跑的結果與 wf36b 再重跑（2026-11-19 寫定，先於再重跑提交）

結果：wf36-r3 通過（報告記 BASE 為 merge-base、增量範圍，`overdue` 列為重新查核並判 RETURN）。wf36b-r5 在第 3 項失敗：判 RETURN，不是 PASS。增量的部分正確——增量範圍、`todo.py` 的結論寫為沿用、沒有把問題歸給 H1..H2——但 reviewer 查核完整範圍時，指出 fixture 的 project.md 規定使用者功能要更新根目錄 README 的使用說明，而交付範圍沒有更新，列為需決策的 MUST FIX。這是 fixture 的缺陷，不是增量造成的；WF-37 兩組也都因同一條規定另外詢問使用者（見計畫 S4）。

- 修改：對照組（wf36b、wf36c）的 H1 在根目錄 README 的「列出」底下補一行到期日的顯示說明。wf36、wf37、wf37b 不改。規則文字與判準不改。
- 再重跑：wf36b 1 輪，證據命名 `wf36b-r6`，放在 `evidence/s6-wf36/`；判準同上方「wf36b」。
- wf36b-r5 保留，不因再重跑的結果改寫。
