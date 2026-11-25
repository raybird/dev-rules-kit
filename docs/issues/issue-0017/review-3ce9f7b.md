# 審查報告
- 範圍：完整交付範圍（增量覆審）
- Reviewed BASE SHA：b26efc5914d2c4f4fdb9dee26b6be2910c56d00e
- Reviewed HEAD SHA：3ce9f7b24f68240614ec50cddb2452283642611b
- Reviewed patch-id：3244f286ff33b300d944b0f52f7413b37968ed65
- 獨立 reviewer：Claude Code 獨立 subagent（claude-opus-5-5）
- 增量覆審：上一份報告 review-80d52c2.md，增量範圍 80d52c2..3ce9f7b

## 問題與風險

**MUST FIX**：無。

**SHOULD FIX**：無。

**NICE TO HAVE**（一項，增量引入）

1. `docs/agents/acceptance.md:50` 新加的「修訂過的 Scenario 另須出現在重新核准的那一句」，「修訂過的」範圍比原意寬。
   - 同檔「規格修訂的查核」第 76 行規定：差異沒有改變條件、動作、結果或必要檢查時，原核准有效，只記 Timeline，不需要重新核准。
   - 照字面讀，只改措辭的 Scenario 也算「修訂過」，但它不會有重新核准的那一句，單行前提因此不成立，reviewer 可能把合規的單行判成誤用。誤判方向偏嚴，會多一輪往返，不會造成錯誤的 PASS。
   - `docs/rule-verification-status.md:352` 的「修訂過的另須……」也有同樣的寬度。
   - 建議：兩處改成「標過 `待重新核准` 的 Scenario」或「實質修訂過的 Scenario」，與第 77 行的用語對齊。

## 已查核維度

- **逐項確認上一份報告的建議**（依 README TBD-5、計畫 S9）
  - NICE TO HAVE 1：已修正，位置在 `docs/AGENTS.md:139`。
    - 後兩處改成「新增的內容與含不符合這些寫法的行的段落之間空一行」和「或與這類行同段落的內容在審查之後變動」。
    - 現在同一段裡的「這些寫法」都指規定的寫法：一般段落、表格列與清單，不含 `<`，行首不用粗體或 `[`。「這類行」承接前句的「不符合這些寫法的行」，不再有相反的兩種指涉。
  - NICE TO HAVE 2：已修正，位置在 `evidence/s4-results.md:17`，改寫成「r4 先有一次……被權限擋下，再單獨執行；r3 只執行一次」。
    - 對照 `s4-wf48/wf48-r4.md`：工具動作第 11 項是串了 `echo` 的 verify-artifact 呼叫，也是第三筆權限拒絕；第 12 項單獨執行。
    - 對照 `wf48-r3.md`：帶 `--reviewed` 的呼叫只有第 18 項。三筆權限拒絕分別是 ls／cat、find 與 git commit，都不是 verify-artifact。
    - r3 另有第 14 項 `--help`。依上下文，「只執行一次」指的是帶 `--reviewed` 的那次檢查，不算錯。
  - NICE TO HAVE 3：已修正，位置在 `acceptance.md:50` 與 `rule-verification-status.md:352`。單行前提補上修訂過的 Scenario；狀態表那一列也補了「分批或修訂時」，並註明是依 review-80d52c2 NICE TO HAVE 3 補上。用語的寬度見上方 NICE TO HAVE 1。
- **受影響之處與重新查核**
  - docs/AGENTS.md 那一句與檢查器對照：
    - `frozen-content.md` 凍結的行包括標題、code fence、粗體開頭、`[` 開頭、含 `<`。前四種都不屬於「一般段落、表格列與清單」，也就都在「不符合這些寫法的行」之內，所以新寫法涵蓋的範圍不比檢查器窄。
    - 「空一行」與 frozen-content「段落與表格」第一段末句一致。
    - 「照範本寫成的表格可以直接補列」與表格逐列判定一致。
    - docs/AGENTS.md 的 `<` 沒有 `<br>` 例外，比檢查器嚴，方向保守。
    - verify-artifact.py 從 b26efc5 到 3ce9f7b 沒有改動（`git diff --quiet` 的 exit 為 0）。
  - 單行前提與相關規定：
    - 與第 41 行一致：該行規定規格修訂後重新核准時加一句，寫日期、待確認事項編號與驗收編號。
    - 與同段其他規則不矛盾：表格收回單行、依表判定、先核對核准來源。
    - 與 `readme-templates.md` 第 80～89 行不矛盾：範本是表格形式，註解只寫全部核准後改單行。
    - 與「規格修訂的查核」除措辭寬度（NICE TO HAVE 1）外沒有衝突。
    - 全 repo 沒有其他地方重述這個前提。
  - 本 issue 的 README 核准紀錄符合修正後的前提：核准來源一句涵蓋 SCN-001～007，沒有修訂過的 Scenario，單行寫「全部 Scenario 於 2026-11-25 核准」。
  - `evidence/s1-rule-map.md` A3、A5：
    - A3 的第二欄引的是 9318f69 的原文，屬歷史來源，不需要改。
    - 「S2 核對」欄指向的「AG 同一句」仍然正確。
    - A5 引的「同段落的內容在審查之後變動」仍是新句的子字串。
  - 記帳與其他：
    - README 新增 TBD-5，狀態為 `已解決`，有結論與日期。
    - 計畫補了 S9、S10。
    - README 的 `**狀態**` 是 `實作中`，與 a42f00e、80d52c2 被審查時相同。
  - SHA 與範圍：
    - main 與 3ce9f7b 的 merge-base 仍是 b26efc5。
    - 80d52c2..3ce9f7b 是兩個非 merge 提交（5aab45a 保存報告、3ce9f7b 修正），沒有改寫歷史。
    - 增量沒有動到 skills/ 與 scripts/，工作樹乾淨。
  - 五項檢查我在 3ce9f7b 重跑過，都通過，與 `evidence/kit-checks.txt` 的記錄一致：check-kit、check-links、`bash -n`、test-install 36 項、test-evidence 315 項。
- 其餘沿用 review-80d52c2.md（及它沿用的 review-a42f00e.md）。
- **限制**
  - 有一點不是增量引入的：80d52c2 就已存在，3ce9f7b 沒有改到那個部分。依增量覆審的規則不列為建議，只在此記錄。
    - `docs/AGENTS.md:139` 寫「行首不用粗體或 `[`（任務清單、alert 與連結除外）」，沒有排除 `## 現況` 的 `**現行 review**`。
    - 但 `review-evidence.md:44` 明確允許修改這一行，frozen-content 與 verify-artifact 也都放行它。
    - 照字面讀，更新 `**現行 review**` 會被當成需要重審。方向偏嚴，不會造成錯誤的 PASS。
  - stream-json 原始檔沒有提交，我沒有讀；r3、r4 的工具動作只以 `wf48-r3.md`、`wf48-r4.md` 的摘錄比對。

## 流程判定
PASS

PASS 只適用於上列 Reviewed HEAD SHA；之後提交 README 記帳區段與本報告以外的檔案會讓它失效，提交前先告知使用者（review-evidence.md「審查之後的提交」）。
