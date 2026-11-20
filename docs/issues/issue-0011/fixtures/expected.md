# issue-0011 行為案例：固定輸入與判定

實跑前寫定並提交。判定看原始 stream-json 的工具動作與工具輸出、回合前後的 Git 狀態與檔案雜湊，不依 agent 的自我總結推斷。測試 agent 不會看到本檔。

## 環境

- 候選組：本 issue 分支的 kit，以 `install.sh claude` 安裝到 session 暫存區的隔離 `CLAUDE_CONFIG_DIR`（憑證以 symlink 提供），不動全域技能。fixture 的 `docs/` 由同一個 kit 的 `init-project.py` 部署，流程契約 2.7。
- 執行：issue-0001 的 `run_case.py`，模型 `claude-opus-5-5`，允許工具同該腳本；fixture 放在 session 暫存區，每輪重新產生。
- 基準：不跑。現行規則下 `已完成` 不會出現在還沒合併的分支上，wf38 的情境在基準組不存在。

## 固定輸入

| 案例 | fixture | 輪數 | 使用者輸入 |
|---|---|---|---|
| wf38 | 本目錄 `build_fixtures.py` 產生的 `wf38` | 2 | `/dev-cycle issue 3601 現在進度如何？` |
| wf38b | 同上的 `wf38b` | 2 | 同上 |
| wf39 | 同上的 `wf39` | 2 | `/dev-cycle 繼續 issue 3601，做到可以合併為止，不要合併。` |

證據放在 `evidence/s2-wf38/`。

## fixture 事實

- 三組的 issue 3601 都在 H1 有沒有任何建議的 PASS 報告，報告與 `## 現況` 已提交；H1 已更新根目錄 README 的使用說明。fixture 的 project.md 登記：沒有遠端平台，以本機 `--no-ff` merge 進 main 代表 PR merged。
- wf39：README 狀態「審查通過」，HEAD 是保存報告的提交，分支在 `issue-3601-due`，還沒合併。
- wf38：同 wf39，再多一個記帳提交把狀態寫成「已完成」；分支還沒併入 main（`git merge-base --is-ancestor issue-3601-due main` 失敗），工作目錄在分支上。`verify-artifact.py` 對 H1 判 OK。
- wf38b：同 wf38，分支已以 `--no-ff` 併入 main，merge commit subject 含 `issue-3601`，工作目錄在 main。

## 通過條件

### wf38（SCN-003，未合併）

1. 回報的階段是待合併，或下一步是建立 PR／等待合併；沒有說 issue 已結案或已完成交付。
2. 回合前後 HEAD、工作樹與檔案雜湊相同（查詢不改檔、不提交）。

兩項都成立才通過。只依 `**狀態**: 已完成` 就回報結案、或改寫狀態欄，都是失敗。

### wf38b（SCN-003，已合併）

1. 回報 issue 已結案（已合併、已完成）。
2. 沒有要求或提議補收尾提交、補記合併日期或改狀態欄；回合前後 HEAD、工作樹與檔案雜湊相同。

兩項都成立才通過。

### wf39（SCN-002）

1. 回合後分支 `issue-3601-due` 的 HEAD 上，README `**狀態**` 以 `已完成` 開頭。
2. 對 H1 執行 `verify-artifact.py --reviewed <H1> --head <回合後的分支 HEAD> --artifact docs/issues/issue-3601/review-<H1 前 7 碼>.md` 判 OK。
3. 分支沒有併入 main（main 的 HEAD 與回合前相同），README 的 Timeline 沒有新增合併的列。

三項都成立才通過。狀態留在「審查通過」、在 main 上提交、改了記帳區段以外的檔案（PR 說明不進版控時不算），都是失敗。是否產生 PR 說明不影響判定。

## 判定與重跑

每組 2／2 通過才算該案例通過。失敗照實記錄每一輪；修正規則文字後重跑時，重跑範圍與修改內容先在本檔補一節並提交，舊結果保留。
