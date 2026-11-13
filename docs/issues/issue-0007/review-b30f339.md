# 審查報告
- 範圍：差異覆審（d49e8fc..b30f339；完整範圍 main..issue-0007-status-vocabulary）
- Reviewed BASE SHA：81368f7cba13cc24e53284ba052a1a1ce51b9761
- Reviewed HEAD SHA：b30f339cff752f00d4ed92d1fdb9a261b8aeab75
- Reviewed patch-id：eeb8d4080aab506ec421f0ff6e8815b4b04165e1
- 獨立 reviewer：獨立 subagent（未參與實作）
- Review artifact：docs/issues/issue-0007/review-b30f339.md

## 問題與風險
- MUST FIX：無
- SHOULD FIX：
  1. CHANGELOG.md 4.11.0「變更」第 2 點寫「列的開頭與結尾直線符號可省略」，docs/issues/issue-0007/README.md 步驟 1 的 TBD-2 修正說明寫「開頭與結尾的直線符號各自可省略」，兩處都和實際行為不符。`split_row` 本身四種寫法都切得對，但 `tbd_rows`（skills/review/scripts/verify-artifact.py:431）只收 `startswith('|')` 的行，所以不寫開頭 `|` 的表格整張讀不到。實測 `編號 | 事項 | 狀態 | 影響 |` 和 `編號 | 事項 | 狀態 | 影響` 兩種表格，`tbd_rows` 都回 `{}`，提醒不會出現。判定與 exit code 不受影響，只是文件把沒有做到的支援寫成了已支援。建議把措辭收窄成「列的結尾直線符號可省略」。若要真的支援開頭省略，就得放寬收列條件，這是新的行為範圍，依 AGENTS.md「範圍」一節，要先有下游實際案例。scan_vocab.py:57 用同樣的收列條件，所以統計與檢查器一致。
- NICE TO HAVE：
  1. docs/issues/issue-0007/README.md:10 結尾「當時算出規定以外 201 列 75 份）：」多了一個沒有配對的全形右括號。原句的左括號在這次改寫時拿掉了，右括號留著。

## 已查核維度
- 驗收與證據：
  - SHOULD FIX 1（d49e8fc 報告）：已修正。用 importlib 載入實測，`split_row` 對下列寫法都切對：頭尾都有 `|`、省略結尾、省略開頭、兩者都省略、含 `\|`（`| a \| x | b |` 切成 `['a \| x', 'b']`）、最後一格空的（`| a | |` 切成 `['a', '']`）、第一格空的（`| | a |` 切成 `['', 'a']`）。`tbd_rows` 在頭尾都有 `|`、省略結尾、含跳脫、空尾欄四種寫法都讀得到 TBD-1 的狀態。省略開頭的情況見上面的 SHOULD FIX 1。
  - 新測試 `test_tbd_rows_without_trailing_pipe_reminded` 涵蓋這個退步：s4-red.txt 中舊版在 4 個類別都失敗，現版通過。
  - s4-red.txt 有 4 項失敗，s4-green.txt 296 項 OK，與 README 敘述一致。我自己重跑 test-evidence.py，也是 296 項 OK。CHANGELOG 與 rule-verification-status 都寫「9 個測試」、「296 項」，彼此一致（292 加 1 個方法乘 4 類別）。
  - SHOULD FIX 2（d49e8fc 報告）：已修正。README 條列與 CHANGELOG「驗證」的數字和 s0-scan.txt 一致：684 份；自由描述 375 份；A 類 1695 列（345 份）；B 類 47 列（19 份）；C 類 197 列（72 份）；總計 1939 列。README 寫明「以下為重跑的數字」，也註明第一次統計的切欄沒有跳過 `\|`，當時 C 類是 201 列 75 份。第一次統計的其他數字（1915、1667 等）沒有列出，但已標明條列是重跑結果，不會誤導。
  - NICE TO HAVE 1（d49e8fc 報告）：已修正。scan_vocab.py 的 `split_row` 與檢查器的版本在 11 個案例上輸出完全相同。C 類開頭詞裡原本的 `\ 3` 也消失了。
  - s1-rejudge.md 只改了標題，註明兩次修正後各重跑一次，與 README 敘述一致。我沒有重跑這 7 個判定。
- 相關失敗面：
  - `main()` 先印判定、處理 INVALID 並設定 code，之後才呼叫 `tbd_reminders`；`tbd_reminders` 用 `except Exception` 回傳空串列。判定與 exit code 仍不受提醒影響。
  - 本輪差異沒有動到 skills/dev-cycle/ 和 pending-scan.md（`git diff --stat d49e8fc b30f339 -- skills/dev-cycle` 為空）。
- 需求、架構、安全、品質：
  - 隱私：新增行沒有 `/home/` 或使用者名稱，也沒有其他專案名稱。s4-red.txt 的路徑以 `~/` 開頭，與既有的 s1-red.txt、s3-red.txt 慣例相同。
  - d49e8fc..b30f339 範圍內的提交訊息沒有 AI 署名（grep co-authored、claude、anthropic 都沒有命中）。
  - 新增的 TBD-2 列、Timeline 列與 rule-verification-status 列，儲存格內沒有未跳脫的 `|`。
  - check-kit OK、check-links OK、test-evidence 296 項 OK。
- 豁免、待確認與限制：
  - TBD-2 記錄如實：使用者 2026-11-13 選「兩項都修並覆審」，並一併處理了 NICE TO HAVE 1。不重跑 WF-34 的理由是 pending-scan.md 規則文字沒變，我已確認本輪確實沒改這個檔。Timeline 記了「PASS 失效」，也記了上一輪報告沒有照抄 PASS 提醒行。
  - `**狀態**` 為「實作中」。
  - 沒有重跑 scan_vocab.py（需要下游路徑清單），也沒有重跑 s1-rejudge 的 7 個判定。
  - 工具呼叫用量 6／30。

## 流程判定
PASS
PASS 只適用於上列 Reviewed HEAD SHA。之後在這個分支提交 issue README 記帳區段與本報告以外的檔案（例如交接文件），PASS 會失效、需要重新審查（流程契約 2.3 以下只有單獨新增本報告的提交可沿用）；提交前先告知使用者，由使用者決定做法。
