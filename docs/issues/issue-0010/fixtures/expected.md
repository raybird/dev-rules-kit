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
