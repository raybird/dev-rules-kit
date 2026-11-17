# 審查報告
- 範圍：完整 PR
- Reviewed BASE SHA：85cc332b2607483862f572c3b5b2687ff968e6f6
- Reviewed HEAD SHA：ccb5abd9dcf4cb1b817729fa03955013c74559d7
- Reviewed patch-id：0e8eae47a3cfa1993e7c93edef9b3ce1a0cd06ab
- 獨立 reviewer：Claude Code subagent（general-purpose）
- Review artifact：docs/issues/issue-0009/review-ccb5abd.md

第三輪審查，2026-11-17。重點是 2706cfb..ccb5abd 的修正，判定針對 BASE..HEAD 的完整 diff。

- 實跑環境：`$TMP` 內的 clone（checkout ccb5abd），HOME 指向 `$TMP/home`。
- 沒有動到真實的平台目錄與 `~/.local/share`。
- 在 clone 內重跑根目錄五項檢查，全部通過：check-kit、check-links、`bash -n`、test-install、test-evidence。

## 問題與風險

### MUST FIX
無。

### SHOULD FIX

1. **備份失敗時的訊息「尚未覆蓋任何技能」，在多平台安裝時不正確**（scripts/install.sh:183）
   - 實跑：codex 與 claude 都有安裝，未指定平台時走自動偵測，也是 get.sh 預設的路徑。codex 先裝完：改過的 review 已備份並覆蓋成 kit 原文。接著 claude 的 review 有壞連結，備份失敗，輸出「錯誤：備份 review 失敗……，尚未覆蓋任何技能」。
   - 實際上：codex 的技能已經覆蓋；claude 先前備份好的 create-commit 也保留著，只是沒覆蓋。
   - 影響：沒有資料遺失，每個成功的備份都已印出「備份：」那一行。但這句話讓使用者以為所有平台都沒動，和第二輪 SHOULD FIX 1 是同一類過度宣稱。
   - 建議：改為「$name 所在的平台尚未覆蓋任何技能；先前平台已安裝完成，備份位置見上方」之類的說法，只要改一行訊息。

### NICE TO HAVE

1. dry-run 預告不到備份會失敗：壞連結要到正式執行時 `cp -RL` 才會報錯。上例 dry-run 列出 3 個「會備份」、exit 0，正式執行才中止。之後重跑時，前一次已成功的備份會再多出一份，無害。

## 第二輪問題逐項判定（review-484924d）

| 項目 | 判定 | 依據 |
|---|---|---|
| SHOULD FIX 1 CHANGELOG「安裝失敗時平台目錄不動」 | 已修 | CHANGELOG.md:21 改為：下載或解壓失敗時 `current` 與平台目錄不動，install.sh 失敗時只保證 `current` 不切換、中途已覆蓋的技能不還原。test-install 的註解與 rule-verification-status 同步修改。新的訊息問題見本輪 SHOULD FIX 1 |
| NICE 1 sort -V 依賴 | 已修 | 改成純 bash 逐段比較，詳見「已查核維度」 |
| NICE 2 symlink 備份失敗訊息與殘留 | 已修 | `if ! cp -RL …; then rm -rf "$backup"; die …`。s10-red 先紅（只有 cp 的原始錯誤）後綠。突變：拿掉 `rm -rf` 後案例失敗（留下 git-squash.bak-*） |
| NICE 3 子目錄 symlink 判為 kit 版本 | 接受不改 | S10 的理由：BASE 就是這樣，安裝時會中止、不遺失資料。上一輪實跑確認過，同意 |
| NICE 4 `-L` 沒有案例守住 | 已修 | 新增技能內 SKILL.md 是 symlink 的子案例。s10-mutation：改回 `cp -a` 後案例失敗 |

## 已查核維度

- **驗收與證據**：
  - SCN-001～010 沿用前兩輪的查核。
  - S10：s10-red 有兩個失敗，原因都對應目標行為：沒有 sort 時 v10.0.0 被拒絕；備份失敗時沒有「尚未覆蓋」的訊息。s10-green 26 個案例通過。s10-mutation 與本輪的 `rm -rf` 突變都有被案例抓到。
  - 沒有發現假綠燈。
- **相關失敗面**：
  - **supported_version**
    - 已通過 `valid_version` 的值在 `set -euo pipefail` 下實測：v5.0.0、v5.0.1、v5.1.0、v6.0.0、v10.0.0、v5.0.08、v05.0.0、v5.00.000 都接受；v4.99.99、v4.0.0、v0.0.0 都拒絕。
    - `(( ))` 放在 `if` 的條件裡，不會觸發 errexit。
    - 三段都相等時，迴圈最後一個 `if` 的條件不成立、也沒有 else，回傳 0，所以 v5.0.0 本身會被接受。
    - 前導零先由 `valid_version` 放行，再由 `10#` 當成十進位處理，不會被當成八進位而出錯。
    - 呼叫端是 `supported_version … || die`，函式內的非零回傳不會中止腳本。
  - **install.sh 備份失敗分支**
    - `rm -rf` 的對象是 `$backup`。`while [ -e ]` 已保證這個路徑在 `mkdir -p` 之前不存在，所以只可能刪到本次新建的目錄。實跑時，預先放在 skill-backups/ 的無關目錄保留下來。
    - `if !` 讓 cp 失敗不會觸發 errexit，接著 die 會中止整支腳本。
    - 同一平台先前的備份會保留，也已印出；先前平台的技能已經覆蓋（訊息問題見 SHOULD FIX 1）。
    - dry-run 只走 echo 分支，不受影響。
  - **test_get_version_compare_without_sort_v 的 PATH 建法**
    - 把 /usr/local/bin、/usr/bin、/bin 中可執行的檔案逐一 symlink 到暫存的 bin 目錄，排除 sort。
    - ubuntu-latest 的 /bin 是指向 usr/bin 的連結：`iterdir()` 可以讀，重複的名稱以 `not link.exists()` 略過。壞連結因 `os.access` 為假而略過。
    - subprocess 依 env 裡的 PATH 解析 `bash`，curl、tar、gzip、python3 都在 /usr/bin。CI 沒用 setup-python，python3 來自 /usr/bin；就算日後改用 setup-python，/usr/bin/python3 仍在。
    - 判斷可靠。限制：案例沒有斷言暫存 bin 裡確實沒有 sort，不過排除條件是依名稱判斷，可以接受。
- **需求、架構、安全、品質（含跨檔重複與過度設計）**：
  - 版本比較 8 行，沒有外部依賴；備份失敗分支 3 行。都沒有過度設計。
  - CHANGELOG 的「技能目錄或其中的檔案是 symlink 時複製指向的內容」「備份失敗時在覆蓋前中止」，以及 rule-verification-status 的兩列敘述，都與實作一致。「備份失敗時在覆蓋前中止」以平台為單位才正確，CHANGELOG 的字面沒有錯。
- **豁免、待確認與限制**：
  - 未查核：真實 raw.githubusercontent.com 的正式指令（排在發布後）；macOS 實機。
  - NICE 3 接受不改，依 S10 的理由。
  - 發布時 v5.0.0 tag 要和 main 合併一起推（前一輪已說明）。

## 流程判定
PASS

PASS 只適用於上列 Reviewed HEAD SHA。之後在這個分支提交 issue README 記帳區段與本報告以外的檔案（例如交接文件），PASS 會失效、需要重新審查；提交前先告知使用者，由使用者決定做法。
