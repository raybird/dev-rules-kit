# 審查報告
- 範圍：差異覆審（8d4f21a..5f5fb3e；完整範圍 main..issue-0005-table-continuation）
- Reviewed BASE SHA：c4f9a51e5d0ae8f6b11099ef24f0786375b47660
- Reviewed HEAD SHA：5f5fb3ec50d806e68976bd46f080a26b807a8b2a
- Reviewed patch-id：fddf31b02ac86964a2cf4a5bc8511cc08979482d
- 獨立 reviewer：獨立 subagent（未參與實作）
- Review artifact：docs/issues/issue-0005/review-5f5fb3e.md

## 問題與風險
- MUST FIX：無
- **SHOULD FIX 1**：docs/rule-verification-status.md:327。這一列本 PR 有改，第三格裡的「以 `|` 開頭的行接分隔線」用的是沒有跳脫的 `|`。GFM 在表格儲存格裡會把 code span 中的 `|` 也當成欄位分隔，所以這一列多出一格，被丟棄的那一格（從這裡到列尾的證據文字）不會渲染。
  - 這個問題從 486936a（2026-11-11，已在 main）就存在，不是本輪引入的，但它正好落在清單第 4 項要查的範圍。
  - 建議改成 `` `\|` ``。這是文件修正，不影響判定。
- **NICE TO HAVE 1**：docs/issues/issue-0005/README.md:67。步驟 3 的完成證據仍寫「CHANGELOG 4.10.0（…252 項）」，CHANGELOG.md:53 已改成 260 項。建議改成 260，或註明是第一輪時的數字。第 61 行是步驟 1 的歷史紀錄，保持 252 沒問題。

## 已查核維度
- 驗收與證據：
  - MUST FIX 1（TBD-1）已修正到位。`start` 項目改成 `(section, 'start', before[1], trigger[2])`，describe 會印出「章節「X」「觸發行」所在段落前接的內容（…）」。實測訊息：章節「Timeline」「**風險**: a」所在段落前接的內容（表格列；…）。新測試 `test_start_message_names_paragraph` 會斷言第二段的文字。
  - 使用者答的是「訊息加上段落內容」，實作是引用觸發凍結的那一行。這能區分不同的段落，AC-1 也沒有改。
  - SHOULD FIX 1（TBD-2）已修正到位。flush 時若 `before[1] == '表格列'` 就 append `(section, 'table', head)`；測試 `test_table_head_frozen_when_paragraph_follows_row` 涵蓋這個情況。
  - SHOULD FIX 2 已補上 evidence/s1-rejudge.md，裡面是兩個 fixture 的命令與 OK 輸出（exit 0），路徑用 `<scratchpad>` 佔位。
  - NICE TO HAVE 1 已處理：CHANGELOG 已知限制逐項列出 V4、V6、V7、R9-1、R9-2、R9-3，共六項。
  - NICE TO HAVE 2 已處理：review-evidence.md 補上「渲染相同的變化（例如在標題與段落之間補空行）同樣判需重審」。
  - TBD-1、TBD-2 在 README 待確認事項與 Timeline 如實記錄（2026-11-12 使用者決定）。
  - s3-red.txt 是 2 個新測試失敗，失敗原因分別是訊息沒有段落文字、縮減表頭判 OK，與 README 敘述相符。s3-green.txt 是 260 項 OK，等於 252 加上 2 個方法乘以 4 個類別，與 CHANGELOG、rule-verification-status 一致。
- 相關失敗面：我在 scratchpad/r2/t.py 以 `analyse()` 實測。
  - `before[0]` 只在處理表格列時設成「表格列」，遇到空行或標題就重設。所以 `before[1] == '表格列'` 時，`head` 一定是緊鄰的那張表格的表頭；章節的第一張表格之前、或屬於別的章節的表格，都不會走到這個分支。
  - 實測「別章節的表頭被改」判 SAME，「同一張表格的表頭被改」判 DIFF。同一章節有兩張表格時，第一張表頭改了判 SAME，第二張（段落緊接的那張）改了判 DIFF。凍結項目只記第二張的表頭。
  - 表格列後面直接接 fence 時，也會把表頭一併凍結，這是多凍結一點，補 Timeline 列時仍判 SAME。
  - 一般記帳都沒有被誤判，都判 SAME：
    - Timeline 補列，含範本 `---` 檔尾，以及表格直接接檔尾欄位（下游那 1 份）的排法；
    - 待確認事項補列與改狀態；
    - `## 現況` 改列。
- 需求、架構、安全、品質：
  - 改動是 8 行，加在既有 flush 裡，排在內容、結尾、前接之後，錯誤訊息的優先順序不變。
  - CHANGELOG 4.10.0、review-evidence.md、rule-verification-status 的敘述與實作一致。
  - 五項檢查中跑了三項，都通過：check-kit OK、check-links OK、test-evidence 260 項 OK。
  - Markdown 表格儲存格：README 新增的 TBD 表有 4 列，每列都是 4 欄，`|` 一律改寫成「直線符號」。唯一的問題見 SHOULD FIX 1。
  - 隱私：新增行裡唯一含 `/home/`、`/tmp/claude-` 的是上一輪報告引述的檢查說明，不是實際路徑；s3-red.txt 用 `~/` 寫法。沒有其他專案名稱。三個提交訊息都沒有 AI 署名。
- 豁免、待確認與限制：
  - 沒有 gate 豁免；TBD-1、TBD-2 都已確認。
  - 沒有重跑 AC-2 的 fixture（不在 repo 內），沒有跑 test-install 與 `bash -n`（不在清單內）。
  - 工具呼叫用量 9／30。

## 流程判定
PASS
PASS 只適用於上列 Reviewed HEAD SHA。之後在這個分支提交 issue README 記帳區段與本報告以外的檔案（例如交接文件），PASS 會失效、需要重新審查（流程契約 2.3 以下只有單獨新增本報告的提交可沿用）；提交前先告知使用者，由使用者決定做法。
