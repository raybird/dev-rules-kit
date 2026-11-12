# 審查報告
- 範圍：完整 PR（main..issue-0005-table-continuation）
- Reviewed BASE SHA：c4f9a51e5d0ae8f6b11099ef24f0786375b47660
- Reviewed HEAD SHA：8d4f21a494a75074272dbc8498c7ae2ad87ee3a8
- Reviewed patch-id：c3a95ada6b4b54d315dac7f84a239774475fddcc
- 獨立 reviewer：獨立 subagent（未參與實作）
- Review artifact：docs/issues/issue-0005/review-8d4f21a.md

## 問題與風險
- **MUST FIX 1**：skills/review/scripts/verify-artifact.py:191、:284-285。AC-1 寫「錯誤訊息指出是哪個章節的哪一段」，但 `start` 項目只帶章節與前接種類，沒有帶出是哪一段。實測：Timeline 有兩段含凍結內容的段落，只刪掉第二段前的空行，錯誤訊息是「章節「Timeline」含凍結內容的段落前接的內容（空行；…）／（表格列；…）」，看不出是哪一段。新增的測試只斷言訊息含「前接」，所以這個缺口沒被發現。建議二選一：
  - `start` 項目加上段落的觸發行（例如 `trigger[2]`），在 describe 印出，並在測試斷言段落文字；
  - 或者修改 AC-1 的措辭，改成只指出章節。這要使用者重新核准。`需決策`（擇一）
- **SHOULD FIX 1**（`需決策`）：verify-artifact.py:266-271。這是 V3 同類、從段落那一側進來的缺口。被審查版本若已經是「表格後面不空行，直接接含凍結內容的段落」（下游有 1 份是這種排法），段落在 GFM 會渲染成表格的一列，但表頭不凍結，因為只有表格列本身含凍結內容時才凍結表頭。
  - 實測：段落 `**風險**: a | b | c` 接在三欄表格後面，審查後把表頭與分隔列縮成一欄，檢查器判 SAME（有效）。marked 與 micromark 都只渲染出「**風險**: a」，`b`、`c` 被藏住。
  - 前提有兩個：被審查版本就已經不空行，而且凍結行裡含 `|`。是否屬於「要先違反撰寫規範」，由使用者依 #6 的界線決定。
  - 修法很小：flush 時若 `before[1] == '表格列'`，就一併 append `(section, 'table', head)`。若決定不修，就列進 CHANGELOG 4.10.0 的已知限制。
- **SHOULD FIX 2**：docs/issues/issue-0005/README.md 步驟 1 的「AC-2 重判」。wf28b3（`--reviewed 84a544b`）與 wf31（`--reviewed b2bfb79`）判 OK 的結論只寫在 README 的文字裡，evidence/ 沒有保存命令與輸出。AC-2 的檢查方式把這兩項列為必要結果，建議補一份 evidence（命令加上 OK 輸出）。
- **NICE TO HAVE 1**：CHANGELOG.md 4.10.0 的已知限制只點名 V4／V6（落單反引號）與 V7（處理指令、宣告、CDATA），用「這類」概括其他項。#5 在 2026-11-12 的分類列了六項，R9-1（小寫 CDATA）、R9-2（檢查器與渲染器認定不同的 fence）、R9-3（縮排的註解開頭）都沒寫出來。建議逐項列名，或寫明「#5 2026-11-12 分類的六項」。
- **NICE TO HAVE 2**：「標題後直接接段落」改成「標題、空行、段落」，渲染相同也會判需重審（實測 DIFF：start 由「標題」變成「空行」）。這屬於設計上的從嚴，下游 6 份 6 段受影響，一般記帳不會這樣改。可以在 review-evidence.md 補一句，說明渲染相同的前接變化也算。

## 已查核維度
- **驗收與證據**：
  - AC-1：三個紅燈案例確實在實作前失敗。我把 HEAD 的 test-evidence.py 配上 c4f9a51 的 verify-artifact.py 重跑，結果是 3 failures，與 s1-red.txt 一致。HEAD 版本 252 項全部通過，與 s1-green.txt 一致。錯誤訊息沒有指出是哪一段（MUST FIX 1）。
  - AC-2：既有案例通過，新案例 `test_row_appended_before_template_footer_valid` 通過。實跑 fixture 的重判沒有保存證據（SHOULD FIX 2）。
  - AC-3：scan_start.py 與 s2-scan.txt 一致（683 份；前接空行 402 份、標題 6 份、表格列 1 份），README 與 rule-verification-status 引用的數字也相同。
  - 核准來源是 2026-11-12 使用者核准，核准 commit 為 c8165cb。這個提交只新增 README，是 HEAD 的祖先。
- **相關失敗面**（以 `analyse()` 實測）：
  - 段落開頭的各種前接都正確：
    - 表格列後接 fence 的段落判 DIFF（記為表格列）。
    - HTML 註解關閉後同一段的段落併入同一段，開頭以註解前的前接為準。
    - 表格內凍結列後不空行接凍結段落，判 DIFF。
    - 凍結章節之後的記帳章節，一律由標題重設前接。
    - 「檔頭」在記帳章節不會出現。
  - `start` 只在 end 不為 None 時記錄是合理的：表格只會在空行、標題或檔頭之後開始（`not block` 加上 table 旗標），各種前接的渲染都相同。
  - 兩個表頭相同的表格刪掉中間空行判 SAME。凍結列的渲染欄數不變，不構成藏內容。
  - 殘留的同類缺口見 SHOULD FIX 1。
- **誤判**（一般記帳不會被誤判需重審）：
  - Timeline 補列（含後接範本檔尾，以及下游那種表格直接接檔尾的排法）判有效。
  - 待確認事項在凍結項目之前新增一般項目判有效。
  - `## 現況` 與範本檔尾由既有 252 項涵蓋，全部通過。
  - 從嚴的情況只有 NICE TO HAVE 2。
- **需求、架構、安全、品質**：
  - 改動很小，`start` 排在段落內容與結尾之後，內容或結尾不同時錯誤訊息仍先指出它們，與 README 的說明相符。
  - review-evidence.md、CHANGELOG（252 項）、rule-verification-status（3 個子測試先紅後綠、1 份前接表格列）與實作、證據一致。
  - 五項檢查中我跑了三項：check-kit OK、check-links OK、test-evidence 252 項 OK。
  - 隱私：新增行沒有 `/home/`、`/tmp/claude-` 或其他專案名稱；s1-red.txt 裡的路徑是 `~/Documents/...` 相對寫法。兩個提交訊息都沒有 AI 署名。
- **豁免、待確認與限制**：
  - 沒有 gate 豁免。步驟 3 標 ⏳、狀態「實作中」，符合送審前的狀態。
  - 沒有重跑 AC-2 的實跑 fixture，因為 fixture 位置不在 repo 內。
  - 沒有跑 test-install 與 `bash -n`，不在指定清單內。
  - 工具呼叫用量 12／30。

## 流程判定
RETURN TO execute-task
