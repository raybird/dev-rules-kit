# 審查報告
- 範圍：完整 PR
- Reviewed BASE SHA：85cc332b2607483862f572c3b5b2687ff968e6f6
- Reviewed HEAD SHA：3857cae6ce4abff636154f132f8d54a990de41d0
- Reviewed patch-id：b198db9c153ea8c61d4c07462c16566850dbe232
- 獨立 reviewer：Claude Code subagent（general-purpose）
- Review artifact：docs/issues/issue-0009/review-3857cae.md

第八輪審查，2026-11-17，範圍是 f5116ce..3857cae。其餘維度沿用第七輪（review-f5116ce）的結論。實跑都在 `$TMP` 內的 clone（checkout 3857cae），HOME 指向 `$TMP/h*`，沒有動到真實的平台目錄。暫存目錄都保留，沒有刪除。

## 問題與風險

### MUST FIX
無。

### SHOULD FIX
無。

### NICE TO HAVE

1. **目標技能內有不可讀的目錄時，錯誤原因寫錯**（scripts/install.sh 的 skill_states）
   - 實跑：iterdir 丟出 PermissionError，install 在覆蓋前以 exit 1 中止，改過的 SKILL.md 保留，行為正確。
   - 問題在訊息：印出「無法判斷 … 的技能版本（需要 python3）」，原因寫錯；`--check` 也一樣。上方雖然有 Python traceback，但最後一行會誤導。
   - 建議：die 的訊息改成不預設原因，例如「（詳見上方錯誤）」。
2. **技能內有指向 `/` 或家目錄這類大目錄的 symlink 時，會掃描整個目標樹**（scripts/skill_state.py:57-66）
   - classify 會雜湊整個目標樹，備份的 `cp -RL` 也會複製整個樹。f5116ce 已經有這個情況，不是本輪新增。
   - 實際的技能目錄不會這樣做，列為已知限制即可。

## 已查核維度

- **驗收與證據**：
  - 上輪兩個重現在 3857cae 下都會先備份：
    - 別名連結 `aaa -> scripts`：classify 判為 `modified scripts/verify-artifact.py`，正式執行時備份裡是改過的內容（`# U1`）。
    - `scripts` 與 `a-notes` 指向同一個外部目錄：同樣判為 modified，備份內容正確（`# U2`）。
  - s20-red 兩個子案例失敗，原因都是缺少目標行為：沒有備份、備份裡沒有該檔。
  - s20-mutation：cp 失敗的分支拿掉 `rm -f` 後，案例失敗。
  - s20-green：32 個案例通過。
  - 本輪在 clone 內重跑 test-install、check-kit、check-links、`bash -n`，都通過。
- **相關失敗面**：
  - **循環**：
    - 目標內同時有 `loop -> ..` 與 `a/b -> ../a`：classify 在 0.14 秒內結束，判為 modified。
    - 正式執行時，備份的 `cp -RL` 偵測到循環而失敗，在覆蓋前 die，改過的內容保留。
    - 只用祖先鏈判斷時，每往下一層都會加入一個新的 realpath，路徑長度有上限，所以一定會終止。
  - **兄弟連結的展開**：
    - 構造三層、每層 4 個兄弟連結指向下一層（64 條路徑、320 個檔案），classify 0.16 秒。
    - 要到影響使用的程度，需要刻意構造的多層扇出，實際技能目錄不會出現。
  - **不可讀目錄**：PermissionError 讓 classify 失敗，在備份與覆蓋之前中止；訊息問題見 NICE 1。
  - **`__pycache__`**：目標的 `scripts/__pycache__/x.pyc` 會在目錄這一層就被 `skipped()` 略過，classify 判為 same。
  - **kit 自己的清單**：在 clone 內重跑 build-skill-hashes.py，輸出 192 筆，與提交的 scripts/skill-hashes.txt 逐位元組相同（git diff 0 行）。check-kit 通過。
  - **`find -L` 對 kit 來源**（三種情況都另外 clone 一份 kit 實跑，TMPDIR 都沒有殘留暫存檔）：

    | kit 來源的情況 | 結果 |
    |---|---|
    | 循環連結 `loop -> ..` | find 報「File system loop detected」並以非 0 結束，die「讀不到…的檔案清單，…尚未更新」 |
    | 壞連結 | find -L 照樣列出，cp 失敗，die「無法複製到…」 |
    | 指向目錄的連結 | 複製連結指向的內容，目標裡有 `linkdir/f.md` |

    不會靜默略過，也不會無限迴圈。
  - **讀不到清單時的訊息**：已加上 `DONE_PLATFORMS`，與備份失敗時的訊息一致。
- **需求、架構、安全、品質（含跨檔重複與過度設計）**：
  - tree_files 改用遞迴加祖先集合，約 15 行，比 os.walk 加去重更直接，沒有過度設計。
  - copy_skill 的兩個失敗分支都會清掉暫存檔。
- **豁免、待確認與限制**：
  - 其餘維度沿用前幾輪的結論。
  - 真實 GitHub 上的正式安裝指令尚未實跑。
  - 發布時 v5.0.0 的 tag 要和 main 的合併一起推。

## 流程判定
PASS

PASS 只適用於上列 Reviewed HEAD SHA。之後在這個分支提交 issue README 記帳區段與本報告以外的檔案（例如交接文件），PASS 會失效、需要重新審查；提交前先告知使用者，由使用者決定做法。
