# 審查報告
- 範圍：完整 PR
- Reviewed BASE SHA：85cc332b2607483862f572c3b5b2687ff968e6f6
- Reviewed HEAD SHA：f7c84c229a457c5550b78dba7f6600c2a777779d
- Reviewed patch-id：6777f0049d4c3ab1d54cd3b89d9d13322b7e9ca9
- 獨立 reviewer：Claude Code subagent（general-purpose）
- Review artifact：docs/issues/issue-0009/review-f7c84c2.md

第四輪審查，2026-11-17。本輪的 diff 只有 3a0e8b9..f7c84c2：install.sh 改了一行訊息、新增一個測試案例、記帳。其餘維度沿用第三輪（review-ccb5abd）的結論。實跑在 `$TMP` 內的 clone（checkout f7c84c2），HOME 指向 `$TMP/home`，沒有動到真實平台目錄。

## 問題與風險

### MUST FIX
無。

### SHOULD FIX

1. **失敗的就是第一個或唯一的平台時，「前面列出的平台已安裝完成」會誤導**（scripts/install.sh:183）
   - 實跑：codex、claude 都已安裝，codex 的 review 有壞連結。
   - 自動偵測時的輸出：
     - 第一行：「偵測到已安裝的平台：codex claude」
     - 失敗訊息：「~/.codex/skills/ 尚未覆蓋任何技能；前面列出的平台已安裝完成」
   - 這時實際上沒有任何平台安裝完成。輸出裡唯一「前面列出的平台」就是偵測那一行，這句話可以讀成 codex、claude 都已裝好，和前半句互相矛盾。
   - 只指定 `codex` 時，同一句話也照樣印出，但前面沒有任何平台。
   - 沒有資料遺失。前半句點名的目錄是對的，也是第三輪 SHOULD FIX 1 要求的修正。
   - 建議：在主迴圈 `install_skills` 成功後，把平台名稱記進陣列。訊息只在陣列不是空的時候寫「已安裝完成：codex」，空的時候省略這半句。補一個「第一個平台就失敗」的案例。

### NICE TO HAVE
無新增。第三輪的 NICE TO HAVE（dry-run 預告不到壞連結）依 S12 的理由不改：正式執行會在覆蓋前中止。同意。

## 已查核維度

- **驗收與證據**：
  - 第三輪 SHOULD FIX 1（多平台時說「尚未覆蓋任何技能」）在「後面的平台失敗」這個情況已修好；第一個或唯一平台的情況見本輪 SHOULD FIX 1。
  - s12-red 先紅，失敗原因是訊息沒有指出平台，對應目標行為。s12-green 的 27 個案例通過。
  - 新案例 test_backup_failure_message_names_platform 確實驗證了兩件事：
    - codex 已安裝：codex 的 create-commit 與改過的 kit 來源逐位元組相同。
    - claude 沒被覆蓋：claude 的 create-commit 不等於新來源，仍是上一次安裝的內容。
    - 案例在 kit 端修改 create-commit，製造兩個平台之間可以觀察的差異，判準獨立於訊息字串，不是同義反覆。
    - 只涵蓋第二個平台失敗的情況。
  - 在 clone 內重跑 test-install（OK）、check-kit、check-links、`bash -n` 都通過。test-evidence 本輪沒有重跑：diff 沒有動到它讀取的範圍，採 s12-green 的結果。
- **相關失敗面**：
  - 後面的平台失敗：訊息正確，案例有涵蓋。
  - 第一個平台失敗、只有單一平台：訊息會誤導，沒有案例（SHOULD FIX 1）。
  - `${target/#$HOME/\~}` 在測試環境裡，經 install.sh 內 `$HOME` 被替換成 `$INSTALL_TEST_ROOT` 之後，仍然輸出 `~/` 開頭的形式，與正式環境一致。
- **需求、架構、安全、品質（含跨檔重複與過度設計）**：只改了一行訊息，沒有新的程式邏輯，也沒有重複或過度設計。記帳的 S11～S13 列與 README Timeline 都和實際經過一致。
- **豁免、待確認與限制**：
  - 其餘維度（get.sh、雜湊清單、備份分支、版本比較、文件）沿用第三輪的結論，本輪沒有重查。
  - 沿用前幾輪已說明的兩點：真實 GitHub 上的正式安裝指令尚未實跑；發布時 v5.0.0 的 tag 要和 main 合併一起推。

## 流程判定
PASS

PASS 只適用於上列 Reviewed HEAD SHA。之後在這個分支提交 issue README 記帳區段與本報告以外的檔案（例如交接文件），PASS 會失效、需要重新審查；提交前先告知使用者，由使用者決定做法。
