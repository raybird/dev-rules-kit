# 審查報告
- 範圍：差異覆審（a77b097..d49e8fc；完整範圍 main..issue-0007-status-vocabulary）
- Reviewed BASE SHA：81368f7cba13cc24e53284ba052a1a1ce51b9761
- Reviewed HEAD SHA：d49e8fc15e85ffb533a904ddac8c6277e287f067
- Reviewed patch-id：4acc5330d84f36eba00f1480a9aa5e57559d875c
- 獨立 reviewer：獨立 subagent（未參與實作）
- Review artifact：docs/issues/issue-0007/review-d49e8fc.md

## 問題與風險
- MUST FIX：無
- SHOULD FIX：
  1. skills/review/scripts/verify-artifact.py:418-421（`split_row`）：這次修正讓「列不以 `|` 結尾」的情況退步了。現在只有頭尾兩格都是空的才一起去掉，列尾沒有 `|` 時開頭那個空欄會留下來。實測 `split_row('| a | b')` 回 `['', 'a', 'b']`。表頭寫成 `| 編號 | 事項 | 狀態 | 影響`（GFM 允許不寫結尾的 `|`）時，`head[0]` 是空字串，`tbd_rows` 整張表回 `{}`，提醒就默默不出。資料列的 `row[0]` 也會是空的，於是被略過。a77b097 的 `strip('|')` 處理得了這種寫法。判定與 exit code 不受影響，只會漏報提醒。建議頭、尾的空欄各自判斷、各自去掉（`if parts and not parts[0]: parts = parts[1:]`；尾端同樣處理），並補一個表格不寫結尾 `|` 的測試。
  2. docs/issues/issue-0007/README.md:12-15 與 CHANGELOG.md 4.11.0「驗證」第 1 點：s0-scan.txt 重跑後已經是 684 份，A 類 1691 列（344 份），自由描述 375 份，總列數 1691+47+201＝1939。README 的條列仍寫「共 1915 列：1667 列（343 份）」「374 份是三個特殊值以外的自由描述」。CHANGELOG 仍寫「683 份」「1915 列」。舊數字已經沒有對應的證據檔（s0-scan.txt 被覆寫了）。README 括號裡寫的「規定以外與加格式的列數不變」是對的，但其餘數字和證據對不上。建議把條列與 CHANGELOG 改成重跑的數字，或註明哪些是第一次統計的數字。
- NICE TO HAVE：
  1. docs/issues/issue-0007/evidence/scan_vocab.py:50-56：統計腳本只換了去符號規則，切欄仍是 `strip('|').split('|')`，沒有跟檢查器一樣跳過 `\|`。s0-scan.txt 的 C 類開頭詞出現 `\ 3`，看起來是跳脫直線符號造成的錯位。README 寫的「相同的去符號規則」措辭是準確的，所以不構成錯誤。若想讓統計與檢查器完全一致，可以改用同一種切欄方式。

## 已查核維度
- 驗收與證據：
  - NICE TO HAVE 1（跳脫的 `\|` 不切欄）：已修正。用 `importlib` 載入實測：`| a \| x | b |` 切成 `['a \| x', 'b']`；`| TBD-1 | x \| z | 已定案 | y |` 讀到的狀態是 `已定案`；`| TBD-1 | x | 待確認 | |` 的空尾欄會保留。列不以 `|` 結尾的寫法見 SHOULD FIX 1。
  - NICE TO HAVE 2（去符號範圍）：已修正。判不合法：`~~待確認~~ 已定案`、`（待確認）已定案`、`[已解決](x)`、`(待確認)`、`> 已解決`、空字串。判合法：`✅ **已解決**`、`✔️ 已解決`、`` `已解決` ``、`__已解決__`、`_已解決_`、`⚠️ 待確認`、開頭有空白的 `不影響本次交付`。去掉的字元只有空白、tab、`*`、`_`、反引號、U+FE0F 與 So 類圖示。
  - NICE TO HAVE 3：pending-scan.md:71 新增「`tbd[].status` 為待確認事項狀態欄的原文，不先去掉格式或換成規定值」。
  - 紅綠燈：s3-red.txt 跑 32 項、16 項失敗（跳脫 4 項，刪除線、括號、連結 3 個子案例乘 4 類別共 12 項），與 README 敘述一致。s3-green.txt 292 項 OK，即 284 加上 2 個方法乘 4 類別，與 CHANGELOG、rule-verification-status 寫的「8 個測試」一致。我自己重跑 test-evidence.py，也是 292 項 OK。
  - s1-rejudge.md：只改了標題，註明修正後重跑，結果與修正前相同。我沒有重跑這 7 個判定，以證據檔為準。
  - 重跑判準的先後：expected.md 的重跑段落在 e19b10d 提交（11:19:40），重跑結果在 d49e8fc（11:21:57）。s3-wf34 的 r1、r2 都記錄 kit HEAD `e19b10d`，判準先於重跑。
  - 依 expected.md 通過條件逐輪判定：
    - r1：以「待確認狀態不合法」列出 3401，並指出三個合法開頭值。3402、3403 只說明為合法，沒有因狀態被列出。前後 HEAD `80033e3`、工作樹雜湊相同。判定通過。
    - r2：同樣列出 3401，3402、3403 只說明為合法，前後狀態相同。中間有一次 Bash 權限拒絕，但通過條件不把它當失敗，README 也照實寫了。判定通過。
    - 2／2 通過。
- 相關失敗面：
  - 去符號規則四處一致：pending-scan.md 規則、CHANGELOG 4.11.0、scan_vocab.py `strip_marks` 與 `tbd_status_valid` 都是去粗體、反引號、空白與圖示，刪除線、括號與連結不去。文件沒有提到 `_`，但它屬於粗體（`__`）的寫法，可以接受。
  - `main()` 先印判定、處理 INVALID，再呼叫 `tbd_reminders`；`tbd_reminders` 用 `except Exception` 回空串列，所以判定與 exit code 仍不受提醒影響。
  - 列不以 `|` 結尾的退步見 SHOULD FIX 1。
- 需求、架構、安全、品質：
  - 隱私：新增行沒有本機絕對路徑，也沒有其他專案名稱；wf34 證據以 `<fixtures>` 遮蔽路徑。
  - 4 個提交訊息都沒有 AI 署名。
  - 新增的 Markdown 表格列，欄數與表頭一致，沒有未跳脫的 `|`。
  - check-kit OK、check-links OK、test-evidence 292 項 OK。
- 豁免、待確認與限制：
  - TBD-1 記錄如實：寫明使用者 2026-11-13 選「修 1、2、3 並覆審」與收窄後的範圍；第 4、5 項不修的理由是「只影響提醒，第 4 項的措辭早於本 issue」，與 review-a77b097 的內容相符。Timeline 已記「PASS 失效」。
  - `**狀態**` 為「實作中」。
  - 沒有重跑 s1-rejudge 的 7 個判定，也沒有重跑 scan_vocab.py（需要下游路徑清單）。
  - 工具呼叫用量 8／30。

## 流程判定
PASS
