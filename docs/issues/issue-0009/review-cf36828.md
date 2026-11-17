# 審查報告
- 範圍：完整 PR
- Reviewed BASE SHA：85cc332b2607483862f572c3b5b2687ff968e6f6
- Reviewed HEAD SHA：cf3682809f03a90100cb882a7fc15e4a7d643fd4
- Reviewed patch-id：fbac7b95f095aef4c4fe919fe43ae8347aa6505a
- 獨立 reviewer：Claude Code subagent（general-purpose）
- Review artifact：docs/issues/issue-0009/review-cf36828.md

第六輪審查，2026-11-17，針對 6a3a533..cf36828：發布前下游試用後的四項修正。其餘維度沿用第五輪（review-6a3a533）的結論。實跑在 `$TMP` 內的 clone（checkout cf36828），HOME 指向 `$TMP/home*`，沒有動到真實的平台目錄。

## 問題與風險

### MUST FIX

1. **copy_skill 會寫穿技能內 symlink 的子目錄，改過的檔案沒有備份就被覆蓋**（scripts/install.sh:159-167）
   - **重現步驟**：先正常安裝 claude，再把 `~/.claude/skills/review/scripts` 換成 symlink，指向使用者自己的目錄。該目錄內的 `verify-artifact.py` 尾端加一行 `# USER EDIT`。
   - **cf36828 的結果**：
     - classify 判為 `kit v4.10.0～v5.0.0`，因為 rglob 不跟進子目錄的 symlink。
     - dry-run 沒有預告備份。
     - 正式執行 exit 0，沒有產生 skill-backups。
     - 使用者的 `verify-artifact.py` 被換成 kit 原文，`# USER EDIT` 不見了。
   - **6a3a533 的結果**（同樣的步驟）：舊的 `cp -r "$d." …` 在這裡報「cannot overwrite non-directory … with directory」，exit 1，使用者的檔案保留。
   - **原因**：copy_skill 對目標的 symlink 子目錄執行 `mkdir -p` 會成功，之後的 `cp` 就寫進連結指向的目錄。
   - **影響**：
     - 這是本輪引入的資料遺失回歸，也就是本 issue 列的最大風險。
     - 第二輪 NICE 3 的「接受不改」所依據的 S10 理由是「安裝時會中止、不遺失資料」，這個前提已經不成立。
   - **建議**（擇一，並補一個案例：技能內子目錄是 symlink、指向的檔案改過 → 先備份或中止，不能靜默覆蓋）：
     - (a) copy_skill 在 `$dest/$rel` 的任何一段路徑是 symlink 時 die，恢復原本的中止行為。
     - (b) classify 改為跟進 symlink 子目錄，例如用 `os.walk(followlinks=True)` 並防循環，讓改過的檔案被判成 modified 而先備份。`cp -RL` 已經會備份連結指向的內容。

### SHOULD FIX
無。

### NICE TO HAVE

1. **find 失敗時安裝仍然 exit 0，而且是複製到一半的結果**（scripts/install.sh:166）
   - process substitution `< <(find …)` 的結束碼不受 `set -e` 檢查。
   - 實跑：把 kit 的 `skills/review/scripts` 設成 000 權限，install 印出 find 的 Permission denied，最後仍 exit 0 並報「11 個技能」，目標的 `review/scripts/` 是空的。舊的 `cp -r` 遇到同樣情況會失敗中止。
   - kit 來源是使用者自己解壓或 clone 的，不可讀的目錄幾乎不會出現，所以列為建議。
   - 可以先把 find 的輸出收進陣列，或用 `wait $!` 檢查 find 的結束碼。
2. **來源技能內的 symlink 現在會被略過**：`-type d -o -type f` 不含 `-type l`；舊的 `cp -r` 會把 symlink 照原樣複製。目前 kit 的 skills/ 沒有 symlink（`git ls-files -s` 裡沒有 120000 模式的項目），沒有實際影響。可以在註解寫明「kit 技能不含 symlink」，或在 check-kit 加上檢查。

## 已查核維度

- **驗收與證據**
  - s16-red 三個案例失敗，原因都對應目標行為：`--check` 有差異仍 exit 0、`__pycache__` 被複製、備份行不是完整路徑。s16-green 的 28 個案例通過。
  - 我在 clone 內重跑 test-install，OK。
  - 既有案例的斷言改動有兩處，都對應使用者核准的行為變更，沒有放寬：
    - test_modified_skill_backed_up_before_overwrite：備份路徑從相對路徑的子字串改為完整路徑，同樣嚴格。
    - test_get_check_and_latest_unreachable：有差異時的回傳值從 0 改為 1，另外補了「全部相同時回傳 0」的案例。
  - 其餘案例沒有改斷言。
- **相關失敗面**
  - **copy_skill**

    | 情況 | 結果 |
    |---|---|
    | 目標的檔案是 symlink | `cp` 寫穿連結，與舊行為相同。classify 會跟進檔案 symlink，改過時會先備份（第三輪已確認） |
    | 目標的子目錄是 symlink | 回歸，見 MUST FIX 1 |
    | 空目錄 | 照樣建立 |
    | 檔名含空白或換行 | 實跑 `a b` 與含換行的檔名，都正確複製（`-print0` 搭配 `read -d ''`） |
    | 來源技能內有 symlink | 會被略過，見 NICE 2 |
    | cp 失敗 | while 迴圈本體不在條件判斷的情境裡，`set -e` 有效，會中止 |
    | find 失敗 | 不會中止，見 NICE 1 |
    | `${path#"$src"}` | `$d` 結尾有 `/`，GNU find 輸出 `src/x`，得到 `x`；BSD find 若輸出 `src//x`，得到 `/x`，`$dest//x` 仍然有效 |
    | 目錄與檔案的順序 | find 先輸出目錄、再輸出目錄內容，`mkdir` 一定在 `cp` 之前 |
    | dry-run | 每個技能只印一行，不寫入 |

  - **`--check` 的 exit code**

    | 情況 | 實跑結果 |
    |---|---|
    | 全部相同 | 0 |
    | codex 相同、claude 有 1 個技能不同 | 1，各平台分別印出總結 |
    | 偵測到 cursor 但沒有 skills 目錄 | 列出「不存在」，計入差異，1 |
    | 沒有 python3 | `skill_states` 的 die 經命令替換觸發 `set -e`，exit 1，並印出錯誤原因 |

    - 多平台的差異數會累加到 `CHECK_DIFF`。`[ … ] || diff=…` 在 `set -e` 下沒有問題。
    - `get.sh --check` 經 exec 傳回同一個 exit code。
    - `get.sh --check` 在尚未以 get.sh 安裝時 exit 0：沒有可以比對的 kit，只印出資訊，合理。

  - **文件**
    - README.md:78、README.en.md:82 只說 `--check` 查版本與技能，沒有暗示永遠 exit 0。
    - CHANGELOG 與 skills/README 寫「有不同時 exit 1」，與實作一致。
    - INSTALL.md 沒有把 `install.sh --check` 的結束碼當成判準。
    - INSTALL.md 第 2 步補上了 clone 的版本來源（第 1 步記下的 `git describe`）。
    - rule-verification-status 的新增列與實作一致；INSTALL 第 2 步改列為「已實跑驗證」，附下游試用的來源。
- **需求、架構、安全、品質（含跨檔重複與過度設計）**
  - copy_skill 的 `__pycache__`／`.pyc` 略過條件，與 skill_state 的 `skipped()` 語意一致，兩邊用的語言不同，可以接受這個重複。
  - 改動量合理，沒有過度設計。
  - 備份位置改印完整路徑是使用者勾選的項目。
- **豁免、待確認與限制**
  - 其餘維度沿用前幾輪的結論：get.sh、雜湊清單、版本比較、備份失敗分支。
  - 第二輪 NICE 3 的「接受不改」因 MUST FIX 1 需要重新評估。
  - 真實 GitHub 上的正式指令尚未實跑。

## 流程判定
RETURN TO execute-task
