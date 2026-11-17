# 審查報告
- 範圍：完整 PR
- Reviewed BASE SHA：85cc332b2607483862f572c3b5b2687ff968e6f6
- Reviewed HEAD SHA：55f6f97e625e88a6d2ab870e82d8d7481641f9fa
- Reviewed patch-id：69df9b9fc24ac652cb17a947bbc1ea3f0dc6a31a
- 獨立 reviewer：Claude Code subagent（general-purpose）
- Review artifact：docs/issues/issue-0009/review-55f6f97.md

審查日期 2026-11-17。實跑都在 `$TMP`（mktemp -d）內，HOME 指向 `$TMP/home`，來源以 `file://$TMP/remote` 提供 `git archive` 產生的 v5.0.0（HEAD）與 v4.13.0（tag）壓縮檔；未動真實平台目錄與 `~/.local/share`。

## 問題與風險

### MUST FIX

1. **`get.sh --version` 可以裝 v5.0.0 以前的版本，改過的技能沒備份就被覆蓋**（scripts/get.sh:48、72、113）`需決策`
   - 實跑：先以 get.sh 裝 v5.0.0，把 `review/SKILL.md` 改成使用者內容，再執行 `get.sh --version v4.13.0 claude`，exit 0；`review/SKILL.md` 被換回 kit 原文，`skill-backups/` 不存在，`current` 改指 v4.13.0。之後 `get.sh --check` 執行 `current/scripts/install.sh --check`，輸出「錯誤：未知選項 --check」。
   - 原因：`valid_version` 只查 `vX.Y.Z` 格式；舊版壓縮檔裡的 install.sh 沒有備份邏輯，也沒有 `--check`。
   - 影響：違反 SCN-003（「執行安裝或更新」時改過的技能先備份）與 SCN-005；也就是 README 列的最大風險。另外，從 main 合併到 v5.0.0 tag 推上去之前，文件上的那行 `curl … | bash` 會解析到 releases/latest＝v4.13.0（s4-github 證據就是如此），照樣不保護。
   - 建議：解壓後確認 kit 有 `scripts/skill_state.py`（或版本 ≥ v5.0.0），沒有就拒絕並說明，必要時另給 clone 的做法；發布程序寫明 v5.0.0 tag 要和 main 合併一起推。要直接拒絕舊版、還是警告後允許，由使用者決定。補一個「指定舊版 → 拒絕且不寫入」的案例。

2. **技能目錄是 symlink 時，備份只複製到連結本身，內容照樣被覆蓋，輸出卻說已備份**（scripts/install.sh:174）
   - 實跑：`~/.claude/skills/review` 是 symlink，指向使用者自己的目錄，`SKILL.md` 是自訂內容。install 輸出「備份：review（本地修改：SKILL.md）-> ~/.claude/skill-backups/review.bak-…」，但這份備份是指向同一目錄的 symlink（`cp -a` 不解參照）。接著 `cp -r` 寫穿連結，自訂的 `SKILL.md` 被換成 kit 原文，沒有任何地方留下原內容。
   - 影響：屬於資料遺失，而且輸出明確宣稱已有保護。AGENTS.md 要求改部署行為時驗證 symlink，測試沒有這個案例。
   - 建議：備份改成複製解參照後的內容（例如 `mkdir -p "$backup" && cp -a "$target/$name/." "$backup/"`，或用 `cp -aL`），或者偵測到 symlink 的技能目錄（或技能內有 symlink 檔）就停止並請使用者處理。補 symlink 案例。

### SHOULD FIX

1. **同名資料夾存在但缺 `SKILL.md` 時判成 new，資料夾裡改過的檔案沒備份就被覆蓋**（scripts/skill_state.py:85）
   - 實跑：刪掉 `execute-task/SKILL.md`，把 `references/domain-template.md` 改成使用者內容，install 之後該檔被換回 kit 原文，沒有備份。這種狀態不常見，但 classify 的判斷不符合事實（資料夾已存在）。建議改用「資料夾存在」判斷是否已安裝，缺少的 kit 檔照現有邏輯不算修改。

2. **備份路徑只精確到秒，同一秒內重跑時會複製進既有的備份目錄**（scripts/install.sh:165、169、174）
   - 實跑：同一秒內連跑兩次 install，第二次 `cp -a` 把技能複製成 `review.bak-<stamp>/review/`（巢狀）；第三次會蓋掉這個巢狀副本。搭配 MUST FIX 2 的 symlink 情況，第二次的內容直接寫進使用者目錄、蓋掉前一份。建議目標已存在時加序號，或改用 `mktemp -d` 產生唯一目錄。

3. **「install.sh 失敗時 `current` 不動」沒有測試覆蓋**（scripts/get.sh:113-114；scripts/test-install.py 的 get 案例）
   - 突變測試：把 `ln -sfn` 移到 `bash install.sh` 之前，24 個案例全部通過。實作順序目前正確，但計畫第 3 點與 README 風險段承諾的行為沒有任何案例保護。建議補「install.sh 失敗（例如傳入未知選項，或 PATH 裡沒有 python3）→ exit 非 0、`current` 不變」的案例。

### NICE TO HAVE

1. `get.sh --list`（沒有 `--dry-run`）會下載版本、執行 `install.sh --list`（不安裝），之後仍把 `current` 切到新版（實跑：current 變成 v5.0.1，技能仍是舊版）（scripts/get.sh:113-114）。建議 `--list`、`--help` 這類不安裝的選項不切換 `current`，或在 get.sh 層攔下。
2. `curl | bash` 時，下載中斷會讓 bash 執行到一半的腳本。常見做法是把主流程包成 `main "$@"`，放在最後一行呼叫（scripts/get.sh 全檔）。
3. 驗證壓縮檔內容的檢查（`[ -f "$top/scripts/install.sh" ]`）沒有案例：突變刪掉這個檢查，24 個案例全部通過（scripts/get.sh:83）。壓縮檔缺 install.sh 時，會留下已 mv 進去、不完整的版本目錄，之後重跑會停在「已存在但不完整」。
4. `--version=`（值為空）不報錯，改用最新版（scripts/get.sh:30）。
5. INSTALL.md:27「下載安裝尚未有 `<kit>` 時改看 `<kit>/skills/README.md`」語意自相矛盾，可改成 `… | bash -s -- --dry-run --list`（已確認可用）或 GitHub 上的檔案連結。INSTALL 第 2 步的 dry-run 與正式執行各自解析 latest，兩次之間如果有新 release，裝到的版本會和使用者確認過的不同；可以讓正式執行帶上 dry-run 第一行印出的 `--version`。
6. `load_hashes` 用 `line.split()` 拆欄位，kit 技能檔名含空白時會丟例外（scripts/skill_state.py:64）。目前歷代 tag 都沒有含空白的檔名；出錯時 install 會在寫入前中止，不會遺失資料。
7. implementation-plan.md:32 寫清單格式是「`sha256  技能/相對路徑  版本`（最早 tag）」，實作是最早與最晚兩個版本，文件與實作不一致。`describe()` 用最早／最晚的交集推版本範圍，內容回退（重新出現舊 blob）時範圍會失真；只影響顯示。

## 已查核維度

- **驗收與證據**：
  - SCN-001、002：`test_get_install_update_and_init`，另有本次實跑。
  - SCN-003、007：`test_modified_skill_backed_up_before_overwrite` 先紅後綠（s1-red），備份內容逐位元組比對。
  - SCN-004：`test_get_dry_run_writes_nothing`。突變「dry-run 寫入資料目錄」後該案例失敗，證據有效。
  - SCN-005：`test_get_check_and_latest_unreachable`；真實轉址見 s4-github。
  - SCN-006：s2-red 先紅後綠；CI 已設 `fetch-depth: 0`，`test_skill_hashes_cover_released_versions` 會實際執行。突變「忽略雜湊清單」後兩個案例失敗。
  - SCN-008：s5-archive。
  - SCN-009、010：靜態核對 README、README.en、INSTALL、usage、skills/README，五份文件的指令一致；`| bash -s -- --dry-run` 與 `--check` 寫法正確；INSTALL 不再出現 `git rev-list`。
  - CHANGELOG [5.0.0] 的敘述與實作一致，但「指定版本」沒有提到舊版不受保護（見 MUST FIX 1）。
  - S4 的限制已揭露：get.sh 的三個案例沒有紅燈，S1 的 127 屬缺檔，不算目標行為的紅燈。依 verification.md，揭露限制不構成缺失。本次以突變測試補驗：dry-run 與雜湊判斷的案例確實抓得到缺陷；install 失敗後 `current` 的保護、壓縮檔缺檔的檢查兩處抓不到（SHOULD FIX 3、NICE 3）。沒有發現假綠燈。
- **相關失敗面**：
  - 目標多出檔案：install 用 `cp -r` 只覆蓋 kit 自己的檔案，多出的檔案保留，classify 忽略多出的檔案是安全的。符合預期。
  - 目標缺檔：不算修改，符合預期。只有缺 `SKILL.md` 時誤判成 new（SHOULD FIX 1）。
  - `__pycache__`、`.pyc` 在 classify 與雜湊產生兩端用同一個 `skipped()` 判斷，一致。`skills/` 第一層的檔案在兩端都排除。
  - 檔名含空白或 tab：使用者端多出的檔名不參與判斷，TSV 的最後一欄由 `read` 收下其餘內容，不影響狀態欄。kit 端見 NICE 6。
  - stamp 衝突：SHOULD FIX 2。
  - dry-run：classify 唯讀，備份只印出，不寫入，案例覆蓋到。
  - get.sh 下載失敗或解壓失敗：`$(fetch_kit)` 內的 die 只結束子 shell，但賦值的回傳值會觸發 `set -e`，trap 清掉暫存目錄。案例確認資料目錄、平台目錄與 `current` 都不變。暫存目錄建在 `$DATA_DIR` 內，與版本目錄在同一個檔案系統，`mv` 是原子操作。
  - 壓縮檔缺 install.sh：程式有檢查，但沒有案例（NICE 3）。
  - install.sh 失敗：`current` 不變，程式順序正確但沒有案例（SHOULD FIX 3）。
  - 已存在但不完整的版本目錄：停止並說明。
  - `--version` 只接受 `^v\d+\.\d+\.\d+$`，擋住路徑穿越。
  - stdin：install.sh 與 skill_state.py 都不讀 stdin（`read` 都接 here-string），`curl | bash` 不會吃掉剩下的腳本。
  - releases/latest 轉址解析：s4-github 以真實 GitHub 確認；沒有 release 時 sed 留下整串網址，被 `valid_version` 擋下。
  - 舊版 tag：MUST FIX 1。symlink：MUST FIX 2。
- **需求、架構、安全、品質**：
  - skill_state.py 由 install.sh 與 check-kit 共用，build-skill-hashes.py 沿用它的 `skipped`、`version_key`、`changelog_version`，沒有跨檔重複判斷。`test_skill_hashes_cover_released_versions` 以 `git show` 另外走一遍 tag，是獨立實作，不是同義反覆。
  - `describe()` 的「多個版本混合」稍嫌多餘，但只有幾行，不構成過度設計。
  - 雜湊範圍：最早／最晚以 `version_key` 比較。工作區內容標為 CHANGELOG 最上面的版本；如果 CHANGELOG 沒有先寫新版條目，新內容會標成上一個已發布的版本，只影響顯示，check-kit 仍然通過。
  - 安全：版本值經過驗證；下載內容沒有簽章或雜湊驗證，這是 `curl | bash` 型安裝程式的常態，未列為問題。
- **豁免、待確認與限制**：
  - 未查核：真實 raw.githubusercontent.com 的 `curl | bash` 正式指令（計畫排在發布後）；Codex、Cursor 等平台的實機載入。
  - `test-evidence.py` 與 `check-links.py` 沒有在本次重跑，採 s6 證據。本次只在 `$TMP` 的 clone 跑了 4 次突變版 test-install。
  - 舊版是否允許安裝，需要使用者決策（MUST FIX 1）。

## 流程判定
RETURN TO execute-task
