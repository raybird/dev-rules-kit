# Issue 9 — 實作計畫

## 設計與來源

[README](README.md) 是範圍、驗收與核准的唯一來源；風險與首要驗證依 [README 的風險策略](README.md#風險與首要驗證)。本檔是唯一任務與執行證據來源。

### 方案取捨：同名技能怎麼判斷

2026-11-17 比較過兩種做法：

| 做法 | 第一次升級 | 狀態放哪裡 | 結論 |
|---|---|---|---|
| 安裝時在各平台寫安裝基線，更新時比對 | 現有五個平台都是舊版 install.sh 裝的，沒有基線；內容和新版不同時分不出是舊版 kit 還是使用者改過，每個人第一次升級都會卡住 | 平台技能目錄多一份狀態檔 | 不採用 |
| kit 附各技能檔歷代版本的雜湊清單 | 舊版 kit 的檔案都在清單裡，第一次升級也判斷得了 | 清單隨 kit 發布，平台目錄不另寫檔案 | 採用（使用者選定） |

這等於把 INSTALL.md 第 2 步「`git rev-list` 查歷史」的判斷，預先算好放進壓縮檔。同樣的做法已用在 `init-project.py` 的 `PAST_TEMPLATES`（project.md 範本的歷代雜湊）。

### get.sh

```text
get.sh [--version vX.Y.Z] [--dry-run] [--check] [install.sh 的平台與選項…]
```

1. **解析版本**：`--version` 優先；沒指定時讀 `https://github.com/raybird/dev-rules-kit/releases/latest` 的轉址取得 tag。測試以環境變數改寫來源網址與資料目錄（預設 `${XDG_DATA_HOME:-$HOME/.local/share}/dev-rules-kit`）。
2. **取得 kit**：版本目錄已存在就沿用；否則下載 `archive/refs/tags/<tag>.tar.gz` 到暫存目錄、解壓、確認 `scripts/install.sh` 存在，再以 `mv` 放進版本目錄。任何一步失敗都只清掉暫存目錄。
3. **安裝**：執行該版的 `scripts/install.sh`，其餘參數原樣傳入。成功後才以 `ln -sfn` 切換 `current`；失敗時 `current` 不動。
4. **`--dry-run`**：kit 解壓到暫存目錄後執行 `install.sh --dry-run`，結束時刪除暫存，不寫入資料目錄與平台目錄。
5. **`--check`**：印出 `current` 的版本與最新 release，再執行 `current/scripts/install.sh --check`。取不到最新 release 時印出原因，其餘照常列出。

### 雜湊清單與 install.sh

- `scripts/skill-hashes.txt`：每行 `sha256  技能/相對路徑  版本`。版本取包含該內容的最早 tag；只出現在工作區的內容，記為 CHANGELOG 最上面那個版本（發布前 CHANGELOG 條目已先寫好，tag 打在同一個提交上）。
- `scripts/build-skill-hashes.py`：從 Git 歷史的每個 `v*` tag 與工作區產生清單。
- `check-kit.py`：工作區每個技能檔的 sha256 都要在清單裡，缺少時列出檔案並失敗。
- `install.sh` 覆蓋前逐一比對目標技能：與 kit 相同的跳過；每個已存在的檔案都在清單裡就直接覆蓋；有任何檔案不在清單裡，先把整個技能目錄複製到 `<平台設定目錄>/skill-backups/<技能>.bak-<時間>/`（技能目錄之外，避免被當成第二個同名技能載入），再覆蓋。目標多出、kit 沒有的檔案照舊保留。
- `install.sh --check`：唯讀，列出各平台每個技能的版本（取清單裡的版本）或「本地修改」。

### 壓縮檔

`.gitattributes` 對 `docs/issues/` 設 `export-ignore`。`test-evidence.py` 會讀 `docs/issues/` 的 fixture，`check-links.py` 會檢查維護文件（workflow-regression、rule-verification-status、workflow-results）連到 issue 紀錄的連結，兩者在壓縮檔裡都會失敗；它們是給維護者用的檢查，不影響安裝。S5 確認 SCN-008 列的 check-kit、install.sh 與 init-project.py 在解壓後的 kit 照樣可用。

## 實作步驟

| 編號 | 工作與產出 | 相依／啟用條件 | 驗收編號 | 完成判準 | 狀態／證據 |
|---|---|---|---|---|---|
| S1 | test-install.py 先寫失敗案例：同名技能屬於歷代 kit → 直接覆蓋、不備份；不屬於 → 備份內容與覆蓋前逐位元組相同、備份在技能目錄外、輸出列出位置；get.sh 下載或解壓失敗 → 平台目錄與 `current` 不變、資料目錄沒有半套版本 | SCN-003、007 已核准 | SCN-003、007 | 新案例在現行程式下失敗，失敗原因是缺少對應行為 | ✅ 2026-11-17 [s1-red](evidence/s1-red.txt)：`test_modified_skill_backed_up_before_overwrite` 失敗於 dry-run 沒列出備份、正式執行沒產生備份；`test_get_failure_leaves_no_partial_state` 失敗於 get.sh 不存在（127）。`test_previous_kit_version_overwritten_without_backup` 在現行程式下就通過（一律覆蓋），留作 S3 後的回歸保護 |
| S2 | `build-skill-hashes.py` 產生 `skill-hashes.txt`；check-kit 加驗證；test-install 補「改了技能檔沒重產清單 → check-kit 失敗」 | SCN-006 已核准 | SCN-006 | 清單涵蓋所有 `v*` tag 與工作區的技能檔；新案例先紅後綠 | ✅ 2026-11-17 清單 192 筆、涵蓋 58 個 tag 與工作區；[s2-red](evidence/s2-red.txt) 為清單只剩表頭時兩個案例失敗、check-kit 列出缺少的檔案，重產後通過（與原清單逐位元組相同） |
| S3 | install.sh 加上清單判斷、備份與 `--check` | S1、S2 | SCN-003、005、007 | S1 案例轉綠；既有 test-install 案例全部通過；`--check` 不寫入 | ✅ 2026-11-17 [s3-s4-green](evidence/s3-s4-green.txt) 全部 24 個案例通過；另以 v4.9.0 實際安裝後升級：舊版技能列為 kit 版本、改過的 review 被備份。沒有 python3 時 install.sh 與 `--check` 都在寫入前中止（exit 1） |
| S4 | 新增 get.sh（版本解析、下載解壓、切換 `current`、`--dry-run`、`--check`），test-install 以本機壓縮檔與 `file://` 來源覆蓋 SCN-001、002、004、005 | S3 | SCN-001、002、004、005 | 案例先紅後綠；dry-run 前後資料目錄與平台目錄的檔案樹相同；`releases/latest` 轉址另以實際 GitHub 手動確認一次並記錄輸出 | ✅ 2026-11-17 [s3-s4-green](evidence/s3-s4-green.txt)；[s4-github](evidence/s4-github.txt) 以真實 GitHub 在暫存 HOME 跑 `--check`、`--dry-run`：最新 release `v4.13.0`，暫存 HOME 沒有寫入。限制：SCN-001、002、004、005 的三個案例是寫好 get.sh 之後才補上，沒有紅燈；get.sh 不存在時的紅燈只由 S1 的失敗案例取得 |
| S5 | `.gitattributes`；以 `git archive` 產生壓縮檔，解壓後跑 check-kit、check-links、`bash -n`、install.sh（暫存 HOME）與 init-project.py | S2～S4 | SCN-008 | 壓縮檔不含 `docs/issues/`；解壓後的 kit 通過 check-kit、`bash -n`，install.sh 與 init-project.py 成功 | ✅ 2026-11-17 [s5-archive](evidence/s5-archive.txt)：272K、不含 `docs/issues/`；check-kit、`bash -n`、install.sh、init-project.py 通過。check-links 因維護文件連到 issue 紀錄而失敗（59 個連結），已在本節說明並寫入 CHANGELOG |
| S6 | README、INSTALL.md、docs/usage.md 並列 get.sh 與 clone；INSTALL.md 第 2 步依 SCN-010；CHANGELOG（v5.0.0）、rule-verification-status；跑根目錄五項檢查 | S1～S5 | SCN-009、010 | 三份文件的安裝與更新指令一致；五項檢查通過 | ✅ 2026-11-17 [s6-checks](evidence/s6-checks.txt) 五項檢查通過；README、README.en、INSTALL.md、docs/usage.md、skills/README.md 並列兩種方式，INSTALL.md 第 2 步不再出現 `git rev-list`；CHANGELOG [5.0.0]、rule-verification-status v5.0.0；清單以 v5.0.0 重產 |
| S7 | 送獨立審查（工具呼叫上限 30 次） | S6 | SCN-001～010 | PASS，或已依使用者決定處理 | ⏳ |

## 測試策略

- **SCN-001～007**：test-install.py 在暫存 HOME 跑整合測試；get.sh 的下載以本機產生的壓縮檔、`file://` 來源取代網路，所有案例不連網。
- **SCN-008**：以 `git archive` 實際產生壓縮檔並解壓驗證。
- **SCN-009、010**：文件靜態核對。
- `releases/latest` 轉址與 raw.githubusercontent.com 的 `curl | bash` 只能連網驗證：發布前以實際 GitHub 手動跑一次，發布後在暫存 HOME 跑一次正式指令，結果記入 README `## 現況`。依維護指引，本機真實平台目錄不作測試目標。

## 檢查清單

- [x] 根目錄五項檢查通過
- [x] 所有寫入平台目錄的案例都在暫存 HOME 執行
- [x] 發布前重產 `skill-hashes.txt`，check-kit 通過（v5.0.0，2026-11-17；發布前若再改 skills/ 要重產）
