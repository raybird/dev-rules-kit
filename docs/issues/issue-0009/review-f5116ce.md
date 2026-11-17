# 審查報告
- 範圍：完整 PR
- Reviewed BASE SHA：85cc332b2607483862f572c3b5b2687ff968e6f6
- Reviewed HEAD SHA：f5116cebd53f5205963dddbbf596506c80df75e8
- Reviewed patch-id：e35ea0b309daa4a2b42e9c89051ccf10149436ee
- 獨立 reviewer：Claude Code subagent（general-purpose）
- Review artifact：docs/issues/issue-0009/review-f5116ce.md

第七輪審查，2026-11-17，範圍是 cf36828..f5116ce。其餘維度沿用第六輪（review-cf36828）的結論。實跑在 `$TMP` 內的 clone（checkout f5116ce），HOME 指向 `$TMP/h*`，沒有動到真實的平台目錄。

## 問題與風險

### MUST FIX

1. **tree_files 以 realpath 全域去重，真正的子目錄會被略過，裡面改過的檔案沒備份就被覆蓋**（scripts/skill_state.py:51-55）
   - 去重的集合不分祖先與兄弟：只要同一個實體目錄先經由別的路徑走過，後面遇到的就整個略過，且只記一次。`os.walk(followlinks=True)` 會把指向目錄的 symlink 和一般子目錄一起放進 `dirs`，順序依 scandir，與名稱排序無關。
   - **重現一（同一技能內的別名連結）**：在 `review/` 內建立 `aaa -> scripts`（名稱試過 `aaa` 與 `zzz`，scandir 都把連結排在 `scripts` 前面），再修改真實目錄 `review/scripts/verify-artifact.py`。
     - cf36828 的 classify：`modified scripts/verify-artifact.py`，會先備份。
     - f5116ce 的 classify：`kit v4.10.0～v5.0.0`。改過的檔案被記在 `aaa/verify-artifact.py` 底下，不屬於 kit 擁有的路徑，於是不算修改。正式執行 exit 0、沒有產生備份，`scripts/verify-artifact.py` 被換回 kit 原文。
   - **重現二（兩個連結指向同一處）**：`review/scripts` 與 `review/a-notes` 都指向同一個外部目錄，並修改其中的 `verify-artifact.py`。walk 先走 `a-notes`，`scripts` 被略過，classify 判為 kit，結果同樣是不備份就覆蓋。這正是檢查清單問的「第二個被略過會不會漏判」：會。
   - **影響**：重現一在 cf36828 原本有保護，這次修正把它弄壞了，是本輪新引入的資料遺失回歸。
   - **建議**：
     - 防循環只看目前路徑的祖先：realpath 已出現在祖先鏈上才停止往下走；兄弟路徑指向同一處時照樣走，讓每個 kit 擁有的相對路徑都有雜湊。
     - 可以用遞迴加上祖先集合，或在 `os.walk` 裡依 `folder` 的祖先 realpath 判斷。
     - 補兩個案例：別名連結先於真實目錄，以及兩個連結指向同一處、kit 擁有的那一個排在後面。

### SHOULD FIX
無。

### NICE TO HAVE

1. **copy_skill 的清單暫存檔在 cp 失敗時會殘留**（scripts/install.sh:161-175）。實跑時在 kit 來源放一個指向不存在目標的 symlink：cp 失敗後 `set -e` 直接結束，TMPDIR 留下 1 個暫存檔。find 失敗的那條分支有刪除暫存檔。可以在函式內 `trap` 刪除，或在 cp 失敗時先刪再 die。
2. **來源內指向目錄的 symlink 只會建出空目錄**。`[ -d "$path" ]` 為真時只做 `mkdir`，而 find 沒有加 `-L`，不會走進連結。實跑結果：目標的 `linkdir/` 是空的。CHANGELOG 與 S18 寫「symlink 經 cp 複製連結指向的內容」，只對檔案成立。kit 目前沒有 symlink，沒有實際影響；可以在說明裡限定為檔案，或改用 `find -L`。
3. 讀不到檔案清單時的訊息只提「同一平台排在前面的技能已更新」，沒提前面的平台，與備份失敗訊息用 `DONE_PLATFORMS` 的做法不一致（scripts/install.sh:164）。字面沒有錯。

## 已查核維度

- **驗收與證據**：
  - 上輪 MUST FIX 的重現步驟在 f5116ce 下已修：`review/scripts` 是 symlink、裡面的檔案改過時，輸出「備份：review（本地修改：scripts/verify-artifact.py）」，備份內容就是改過的版本（尾端 `# USER EDIT`），之後才覆蓋。
  - s18-red 的兩個失敗都對應目標行為：dry-run 沒有預告備份；find 失敗仍 exit 0。s18-green 30 個案例通過。
  - 我在 clone 內重跑 test-install、check-kit、check-links、`bash -n`，都通過。
  - 新案例只涵蓋「單一 symlink 子目錄」，沒有涵蓋 MUST FIX 1 的去重情境。
  - test_copy_failure_aborts 以 chmod 0 製造錯誤，root 執行時會失效。CI 的 runner 不是 root，可以接受。
- **相關失敗面**：
  - **classify**：
    - same／kit／modified 的判定邏輯本身沒有改，只換了 `installed` 的來源。
    - 沒有 symlink 的目錄與舊版結果相同：kit 自己的 skills/ 也走 `skill_files`，check-kit 通過，missing_hashes 與 build-skill-hashes 的輸出不受影響。
    - 指向不存在目標的連結：會出現在 `names`，但 `is_file()` 為假，所以略過。
    - 有 symlink 時有去重缺陷，見 MUST FIX 1。
  - **循環連結**：目標內建立 `loop -> ..`，classify 可以結束：會走進上層的 skills/，直到遇到已看過的目錄。之後 backup 的 `cp -RL` 偵測到循環而失敗，在覆蓋前 die，改過的 SKILL.md 保留，exit 1。
  - **copy_skill**：
    - mktemp 失敗：`local list` 與賦值分兩行寫，`set -e` 會中止。
    - 暫存檔為空時：迴圈不執行，只 `mkdir -p "$dest"`。
    - die 分支有刪除暫存檔；cp 失敗或中斷時會殘留（NICE 1）。
- **需求、架構、安全、品質（含跨檔重複與過度設計）**：改動量合理。tree_files 回傳前依相對路徑排序，與舊版一致。
- **豁免、待確認與限制**：
  - 其餘維度沿用前幾輪的結論。
  - 第二輪 NICE 3 的「接受不改」已經不需要：它的前提已因採用 (b) 解決，前提是 MUST FIX 1 一併修正。
  - 真實 GitHub 上的正式指令仍未實跑。

## 流程判定
RETURN TO execute-task
