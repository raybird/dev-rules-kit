# 審查報告
- 範圍：完整交付範圍（增量覆審）
- Reviewed BASE SHA：b26efc5914d2c4f4fdb9dee26b6be2910c56d00e
- Reviewed HEAD SHA：80d52c2fe9de547be8563d7a3e103f7838ca18e6
- Reviewed patch-id：cd0e1b8c09d098795fb8bfc10f2c0b9474b06c31
- 獨立 reviewer：Claude Code 獨立 subagent（claude-opus-5-5）
- 增量覆審：上一份報告 review-a42f00e.md，增量範圍 a42f00e..80d52c2

## 問題與風險

**MUST FIX**：無。

**SHOULD FIX**：無。

**NICE TO HAVE**（三項都是增量引入）

1. `docs/AGENTS.md:139` 同一段裡的「這些寫法」指兩種相反的東西。
   - 「不符合這些寫法」裡，它指規定的寫法：一般段落、表格列與清單，不含 `<`，行首不用粗體或 `[`。
   - 這次補回的「含這些寫法的段落」與「與這些寫法同段落的內容」裡，它指的是被禁止的那些寫法，也就是舊文的用法。
   - 照字面讀後一句，等於「和合規內容同一段落的內容變動也要重審」，會和「照常提交」矛盾。讀者多半讀得懂原意，錯的方向也偏保守，所以影響不大。
   - 建議：後兩處改成「含不符合這些寫法的行的段落」「與這類行同段落的內容」，或直接寫出 `<`、粗體、`[`。

2. `docs/issues/issue-0017/evidence/s4-results.md` 新增的那段寫「同一回合先有一次把 `echo "exit=$?"` 串在後面的呼叫被權限擋下，再單獨執行」。這段緊接在「兩輪相同」之後，讀起來像兩輪都發生。
   - r4 確實如此：`wf48-r4.md` 工具動作第 11 項被擋，第三筆權限拒絕就是這次呼叫，第 12 項才單獨執行。
   - r3 沒有：`wf48-r3.md` 只有第 18 項一次呼叫，三筆權限拒絕分別是第 1、11、16 項，都和 verify-artifact 無關。
   - 建議：寫成「r4 先有一次……」。

3. `docs/agents/acceptance.md:50` 新加的單行前提（每個現存 Scenario 都出現在核准來源的某一句）擋得住分批時誤用單行（`待核准`），擋不住修訂時誤用單行（`待重新核准`）。
   - 原因：`待重新核准` 的 Scenario 仍出現在原本那句核准來源裡，所以這個前提照樣成立。
   - 文字寫的是「前提」，不是充分條件，因此不矛盾；`rule-verification-status.md` 也只說它是用來核對「分批時誤用單行」，敘述正確。
   - 建議擇一：補一句「修訂過的 Scenario 另須出現在重新核准的那一句」，或在 rule-verification-status 那一列註明這個前提不涵蓋修訂。

## 已查核維度

- **逐項確認上一份報告的建議**（依 README TBD-4）
  - SHOULD FIX 1：已修正。
    - `docs/AGENTS.md:139` 補回兩個條件：「新增的內容與含這些寫法的段落之間空一行」，以及「與這些寫法同段落的內容在審查之後變動」。
    - `docs/agents/review-evidence.md:60` 補上「以粗體……開頭」與「code fence」。
    - 與檢查器對照：`frozen-content.md` 視為凍結的行與段落規則，以及 `scripts/test-evidence.py:693` 的 `test_append_to_paragraph_with_frozen_line`，都符合修正後的文字。這個測試裡，粗體開頭那段直接接著補行會判需重審，中間空一行則有效。
  - SHOULD FIX 2：已修正。`docs/agents/readme-templates.md:82` 改為「（SCN-001）」，與範例表的 SCN-002 `待核准` 不再矛盾。
  - NICE TO HAVE 3：已修正。
    - `review-evidence.md:41` 加上「流程契約 2.4 起」，並註明 2.3 以下只接受單一報告提交。
    - 與 `verify-artifact.py:427` 一致：讀不到版本、低於 2.4 或其他 major 時，走舊判定。
  - NICE TO HAVE 4：已依使用者選項處理。前提句加在 `acceptance.md:50`，`rule-verification-status.md` 新增一列，標「僅靜態撰寫」。
  - NICE TO HAVE 5：已列為已知限制，見 `rule-verification-status.md` #17 段新增的一列。內容與 `acceptance.md:41` 的「另寫各題對應的驗收編號」相符。
  - NICE TO HAVE 6：已處理兩處缺口。
    - verify-artifact 的輸出摘進 `s4-results.md`。
    - `CHANGELOG.md` 驗證段補了 SCN-001「只記錄、沒有判定（2 輪中 1 輪有寫）」，與 s4-results 的 wf45 列相符：r1 寫在概述，r2 沒寫。
  - NICE TO HAVE 7：已在 a69a09a 處理。TBD-2 改為 `已解決`，結論是文件版本 2.18、流程契約維持 2.8，與 `docs/AGENTS.md` 的文件版本 2.18 一致。
- **受影響之處與重新查核**
  - 單行前提與相關規定不矛盾：
    - 與 acceptance 同段的其他規則不衝突：「表格收回單行」「依表判定」「先核對核准來源」。
    - 與 readme-templates 不衝突：範本用的是表格形式，不適用單行前提。
    - 與 docs/AGENTS.md「待核准 Scenario 必須有對應項目」不衝突。
    - docs/usage.md、issue-checklist、new-issue 技能都沒有和它矛盾的敘述。
  - 本 issue 自己的 README 核准紀錄符合前提：核准來源一句涵蓋 SCN-001～007，單行「全部 Scenario 於 2026-11-25 核准」。
  - `s4-results.md` 摘入的 verify-artifact 輸出與 fixture 相符：
    - `build_fixtures.py` 的 `build_pass` 在 H1 之後另有一個提交，保存報告、把狀態改成審查通過、新增現況。
    - 回合內的提交只整節新增待確認事項並補一列 Timeline，見 `wf48-r3.md` 的 diff。
    - 兩者合起來就是輸出列出的變更清單。說法不精確的一處見 NICE TO HAVE 2。
  - `s1-rule-map.md` 的 A2、A3、A5 新位置與修正後的文字相符。
  - README 在 a69a09a 新增的 `## 現況` 位在 `## 概述` 之後、`## 快速導覽` 之前，位置正確。
  - verify-artifact.py 從 b26efc5 到 80d52c2 都沒有改動；增量也沒有動到 skills/ 與 scripts/。
  - SHA 與範圍：
    - main 與 HEAD 的 merge-base 仍是 b26efc5。
    - a42f00e 是 HEAD 的祖先，中間兩個非 merge 提交，沒有改寫歷史。
  - 五項檢查我在 80d52c2 重跑過，都通過：check-kit、check-links、`bash -n`、test-install 36 項、test-evidence 315 項。
- 其餘沿用 review-a42f00e.md。
- **限制**
  - 有一點不是增量引入的，依增量覆審的規則不列為建議，只在此記錄。`review-evidence.md:60` 從 a42f00e 起就寫「與它們同段落或同表格的內容，都會被當成凍結內容」。但檢查器的實際判定是：照範本寫成的表格逐列判定，凍結列只連帶凍結表頭與分隔列，凍結列的下一列照樣可以補（`test_rows_after_frozen_table_row_valid`）。所以這句摘要比檢查器嚴，方向保守，不會造成錯誤的 PASS。
  - stream-json 原始檔沒有提交，我沒有讀，摘錄內容只能從工具動作與 fixture 間接比對。

## 流程判定
PASS

PASS 只適用於上列 Reviewed HEAD SHA；之後提交 README 記帳區段與本報告以外的檔案會讓它失效，提交前先告知使用者（review-evidence.md「審查之後的提交」）。
