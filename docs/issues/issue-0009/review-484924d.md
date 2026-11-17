# 審查報告
- 範圍：完整 PR
- Reviewed BASE SHA：85cc332b2607483862f572c3b5b2687ff968e6f6
- Reviewed HEAD SHA：484924d647eb4994996f71bd6cf5f6dd07636762
- Reviewed patch-id：969c5d4d555ce2a3881d7377fdd8ea7ebc88085f
- 獨立 reviewer：Claude Code subagent（general-purpose）
- Review artifact：docs/issues/issue-0009/review-484924d.md

第二輪審查，2026-11-17。重點是 55f6f97..484924d 的修正，判定針對 BASE..HEAD 的完整 diff。
- 實跑環境：`$TMP` 內的 clone（checkout 484924d），HOME 指向 `$TMP/home*`，下載來源用 `file://$TMP/remote`。
- 沒動到真實的平台目錄與 `~/.local/share`。
- 在 clone 內重跑了根目錄五項檢查，全部通過（test-install 25 個案例、test-evidence OK）。

## 問題與風險

### MUST FIX
無。

### SHOULD FIX

1. **CHANGELOG 寫「安裝失敗時平台目錄不動」，實際只保證 `current` 不動**（CHANGELOG.md:21；同樣的說法也在 scripts/test-install.py:245 的註解）
   - install.sh 是逐個平台、逐個技能覆蓋的，中途失敗時已覆蓋的技能不會還原。
   - 本輪實跑：技能裡的子目錄是 symlink 時，`cp -r` 在 `review` 停下並報「cannot overwrite non-directory」；排序在它前面的技能已經覆蓋完了。多平台安裝時，前一個平台也可能已經裝完，才在下一個平台失敗。
   - 測試用的 v9.3.0 install.sh 一開始就 `exit 1`，所以只證明了「install.sh 還沒寫入就失敗」這種情況。
   - 建議改成：「下載或解壓失敗時 `current` 與平台目錄都不動；install.sh 失敗時 `current` 不切換，已覆蓋的技能不還原（改過的已先備份）」。只是改文字，不需要改程式。

### NICE TO HAVE

1. `supported_version` 依賴 `sort -V`（scripts/get.sh:35-37）。沒有 `-V` 的 sort（例如舊版 macOS 內建的 GNU sort 5.93）會讓比較結果是空字串，結果所有版本都被拒絕，而且錯誤訊息寫「早於 v5.0.0」，會誤導使用者。`valid_version` 已經保證格式是 `vX.Y.Z`，改成在 bash 裡拆欄位做數字比較就不需要外部依賴。
2. 備份遇到兩種 symlink 會以 cp 的原始錯誤中止（scripts/install.sh:181）。一種是技能內有循環 symlink（`cannot copy cyclic symbolic link`），另一種是指向不存在目標的 symlink（`cannot stat`）。中止發生在覆蓋之前，所以不會遺失資料，已實跑確認改過的內容保留；但會留下不完整的備份目錄，訊息也沒說怎麼處理。可以捕捉 cp 失敗，改印「備份 <技能> 失敗，未覆蓋；請處理該技能裡的 symlink 後重跑」，並刪掉不完整的備份。
3. classify 的 `rglob` 不會跟進技能內的子目錄 symlink（scripts/skill_state.py:86 之後的 `tree_files`）。結果 `--check` 和 dry-run 把這種技能列為「kit 版本」，不會預告要備份；正式執行則在 `cp -r` 報錯中止。資料沒有遺失，這個行為在 BASE 就存在。
4. `cp -RL` 的 `-L` 只在技能「內部」有 symlink 檔時才有作用，但 test_backup_edge_cases 只測了技能目錄本身是 symlink。突變測試：把它改成 `cp -a "$target/$name/." "$backup/"`，案例仍然通過，因為結尾的 `/.` 已經會解參照最上層。可以補一個「SKILL.md 是指向使用者檔案的 symlink」的子案例。這屬於證據持久力，不影響本次判定。

## 第一輪問題逐項判定（review-55f6f97）

| 項目 | 判定 | 依據 |
|---|---|---|
| MUST FIX 1 舊版 `--version` | 已修 | `supported_version` 拒絕 v5.0.0 以前的版本，依使用者決定不提供 `--force`。sort -V 實測：v10.0.0、v5.0.0、v5.0.10、v5.1.0 都接受；v4.99.99、v4.13.0 都拒絕。不指定版本而 latest＝v4.13.0 時同樣拒絕，見 s8-github。案例：test_get_failure_leaves_no_partial_state 的 v4.13.0 子案例，s8-red 先紅後綠 |
| MUST FIX 2 symlink 技能目錄 | 已修 | `mkdir -p` 加上 `cp -RL "$target/$name/." "$backup/"`，備份的是內容而不是連結。test_backup_edge_cases 先紅後綠 |
| SHOULD FIX 1 缺 SKILL.md | 已修 | `folder.is_dir()`。突變回原本的判斷後案例失敗。技能名稱是一般檔案時判成 new，接著 `mkdir -p` 失敗而中止，檔案保留（實跑）；技能名稱是指向目錄的 symlink 時，`is_dir()` 會跟進，照常判斷 |
| SHOULD FIX 2 同秒備份 | 已修 | `while [ -e ]` 改用 `-2`、`-3` 等後綴。突變拿掉這段迴圈後，三次重跑全部失敗（實跑 3 次都是 `['第 2 次改']`），可見案例確實在同一秒內觸發了碰撞 |
| SHOULD FIX 3 install.sh 失敗不切換 current | 已修 | v9.3.0（install.sh 直接 `exit 1`）的子案例；s8-mutation 突變 1 有抓到。另見本輪 SHOULD FIX 1 的文件用語 |
| NICE 1 `--list` 切換 current | 已修 | `--list` 改成和 dry-run 一樣在暫存目錄執行。實跑後 current 不變，TMPDIR 裡沒有殘留 |
| NICE 2 包成 main | 已修 | 實跑：只把前 60 行管線給 bash，得到 syntax error，沒有執行任何步驟 |
| NICE 3 壓縮檔缺 install.sh | 已修 | v9.2.0 子案例；s8-mutation 突變 2 有抓到 |
| NICE 4 `--version=` 空值 | 已修 | 會報錯；子案例先紅後綠 |
| NICE 5 INSTALL 第 2 步 | 已修 | `--list` 改用 `get.sh … --list`；正式執行帶 dry-run 第一行印出的版本 |
| NICE 6 雜湊清單路徑含空白 | 已修 | 先 `split(None, 1)`，再 `rsplit(None, 2)`，實測含空白的路徑能正確拆開。歷代 tag 和 HEAD 的 skills/ 都沒有含空白、引號或非 ASCII 的檔名 |
| NICE 7 清單格式與 describe() | 已修／接受不修 | implementation-plan.md 的格式說明已更正；describe() 的範圍只是近似，刻意不改，只影響顯示 |

## 已查核維度

- **驗收與證據**：
  - SCN-001～010 的證據沿用第一輪的查核結果。
  - S8 的新案例：s8-red 有 4 個失敗，原因都對應目標行為（symlink 備份只是連結、舊版與空值沒有被拒絕）。s8-green 25 個案例通過。s8-mutation 的兩個突變都被抓到。
  - 本輪另做 3 個突變：同秒迴圈、`is_dir`、`-L`。前兩個被抓到，`-L` 沒被抓到（NICE 4）。
  - test_backup_edge_cases 在 s8-red 只紅在 symlink 那一段，缺 SKILL.md 與同秒兩段沒有獨立的紅燈，已用突變補驗。沒有發現假綠燈。
- **相關失敗面**：
  - get.sh 的 main 與 trap：`TMP` 沒有宣告 local，是全域變數。trap 用單引號，在 EXIT 時才讀取 `TMP`。`exit` 與 die 都會觸發清理。`$(fetch_kit)` 子 shell 裡的 die 會經 `set -e` 結束主程式。
  - 實跑結果：dry-run 下載失敗後 TMPDIR 是空的；正式安裝下載失敗後資料目錄只剩 `current` 和既有版本，沒有 `.get.*` 殘留；`--check` 走 exec，不涉及 TMP；`--version=v5.0.0 --check` 照常執行。
  - install.sh 備份：
    - 循環 symlink、指向不存在目標的 symlink：都在覆蓋前中止，exit 1，改過的內容保留（NICE 2）。
    - 備份失敗是否在覆蓋前中止：`install_skills` 在 for 迴圈裡直接呼叫，沒有被 `||` 或 if 包住，所以 `set -e` 有效，確認會中止。
    - 技能內的子目錄 symlink：NICE 3。
  - 版本目錄已存在但不完整、路徑穿越：沿用第一輪的結論，程式沒有變動。
- **需求、架構、安全、品質（含跨檔重複與過度設計）**：
  - get.sh 的 main 包裝和參數改成 local，沒有增加不必要的複雜度。
  - `--list` 與 dry-run 共用暫存目錄的分支，沒有重複邏輯。
  - 備份段落只加了 6 行，沒有過度設計。
  - 文件中的最低版本敘述一致：README、README.en 寫「v5.0.0 以後」；CHANGELOG 寫只安裝 v5.0.0 以後、舊版用 clone；get.sh 開頭說明一致。INSTALL 第 2 步正式執行帶的是 dry-run 印出的版本，dry-run 通過就表示版本 ≥ v5.0.0，所以不必另外說明。
- **豁免、待確認與限制**：
  - 未查核：真實 raw.githubusercontent.com 的正式指令（排在發布後）；macOS 與 BusyBox 環境的實機執行（NICE 1 是依各版 sort 的已知行為推論）。
  - 發布順序：v5.0.0 tag 推上去之前，文件上那行指令會拒絕 latest＝v4.13.0（安全，但無法安裝）。發布時 tag 要和 main 合併一起推。

## 流程判定
PASS

PASS 只適用於上列 Reviewed HEAD SHA。之後在這個分支提交 issue README 記帳區段與本報告以外的檔案（例如交接文件），PASS 會失效、需要重新審查；提交前先告知使用者，由使用者決定做法。
