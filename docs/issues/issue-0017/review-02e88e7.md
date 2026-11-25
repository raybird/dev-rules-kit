# 審查報告
- 範圍：完整交付範圍（增量覆審）
- Reviewed BASE SHA：b26efc5914d2c4f4fdb9dee26b6be2910c56d00e
- Reviewed HEAD SHA：02e88e7fc16ea97b657f69e8639531bf31296375
- Reviewed patch-id：b5831b42dacdfbf416becef6657fc0aa8eeacf0c
- 獨立 reviewer：Claude Code 獨立 subagent（claude-opus-5-5）
- 增量覆審：上一份報告 review-3ce9f7b.md，增量範圍 3ce9f7b..02e88e7

## 問題與風險

**MUST FIX**：無。

**SHOULD FIX**：無。

**NICE TO HAVE**：無。

## 已查核維度

- **上一份報告的建議與限制**（依 README TBD-6、計畫 S11）
  - **NICE TO HAVE 1 已修正**
    - `docs/agents/acceptance.md:50` 改成「標過 `待重新核准` 的 Scenario 另須出現在重新核准的那一句」。
    - `docs/rule-verification-status.md:352` 改成「標過 `待重新核准` 的另須……」，說明欄註明「review-3ce9f7b 後改用 `待重新核准` 界定範圍」。
    - 與同檔「規格修訂的查核」第 76～77 行一致：
      - 第 76 行：差異沒有改變條件、動作、結果或必要檢查時，原核准有效。這類 Scenario 不會被標成 `待重新核准`，不再被要求出現在重新核准的那一句。
      - 第 77 行：實質改變時，只把受影響項標為 `待重新核准`，輕量 AC 在條目後加 `（待重新核准）`。新寫法的「標過 `待重新核准`」兩種標法都涵蓋。
    - 與第 41 行一致：該行規定重新核准時加一句，寫日期、待確認事項編號與驗收編號。
    - 同句的「Timeline 或已解決的待確認事項提過的待核准是歷史，不改變判定」講的是現在的核准狀態；前提則用歷史上標過的狀態去找重新核准的那一句。兩者不矛盾。
    - 全 repo（不含 docs/issues/）沒有其他地方重述這個前提，也沒有殘留「修訂過的」寫法。
  - **限制記錄的既有問題已修正**
    - `docs/AGENTS.md:139` 的行首例外改成「任務清單、alert、連結與 `## 現況` 的 `**現行 review**` 除外」。
- **檢查清單第 2 項：`**現行 review**` 例外與實際放行範圍是否一致**
  - `review-evidence.md:44`：2.5 起 `## 現況` 節內「一行 `**現行 review**` 可改」。
  - `frozen-content.md:9`：`## 現況` 節內 `**現行 review**` 以外的粗體開頭行凍結。
  - `verify-artifact.py`（b26efc5..02e88e7 沒有改動，`git diff --quiet` 的 exit 為 0）：
    - 第 271 行只在章節為 `現況`、且屬於記帳區段（流程契約 2.5 以上）時放行這個欄位。
    - 第 315 行限定只能有一行。
    - 含 `<` 的行在第 265 行的 `html(line)` 先被凍結。
  - 這次的例外只放寬「行首粗體」那一條，`<` 的限制照舊適用，與 document-types.md 第 27 行「不用 `<網址>`」一致。「一行」的限制由 review-evidence.md 與 document-types.md 規定。
  - 檢查器另外接受包在清單或引用裡的 `**現行 review**`（第 34 行 FIELD 允許容器前綴），比文件寬。文件只寫範本的形式，方向保守，不會造成錯誤的 PASS。
  - 例外放在「待確認事項」這一節是恰當的：
    - 那一句本來就列舉了四個章節（待確認事項、Timeline、Gate 豁免紀錄與 `## 現況`），是所有記帳區段共用的寫法限制。
    - `review-evidence.md:45` 也指定記帳區段「依 docs/AGENTS.md『待確認事項』的寫法書寫」。
    - 例外寫明「`## 現況` 的」，不會被讀成待確認事項或 Timeline 可以用粗體開頭的行。我沒找到新的歧義。
  - 全 repo 沒有其他地方重述「行首不用粗體」的例外清單。`docs/AGENTS.md:129`（Gate 豁免紀錄）講的是那一節自己，與 `**現行 review**` 無關，不需要改。
- **檢查清單第 3 項：README 核准紀錄與記帳區段**
  - 核准紀錄：
    - `**核准 commit**` 是 9318f69。
    - 核准來源一句涵蓋 SCN-001～007。
    - 單行寫「全部 Scenario 於 2026-11-25 核准」。
    - 分支歷史（b26efc5..HEAD）的 README 沒出現過 `待重新核准` 的表格列，所以新前提的「標過」部分不適用，單行成立。
  - 記帳提交 49d303c：
    - 我執行 `verify-artifact.py --reviewed 3ce9f7b --head 49d303c --artifact docs/issues/issue-0017/review-3ce9f7b.md`，結果 OK，exit 0。
    - 它列出的變更是：新增報告、狀態（實作中 → 審查通過）、Timeline、現況、現行 review（review-80d52c2.md → review-3ce9f7b.md）。
  - 修正提交 02e88e7：
    - 新增 TBD-6，狀態為 `已解決`，有結論、日期，並指向計畫 S11。表格列不含 `<`，也不是行首粗體。
    - 把 `**狀態**` 改回 `實作中`，與前兩輪修正時的做法相同。
    - `**現行 review**` 仍指向 review-3ce9f7b.md，由下一個保存報告的提交更新。
    - 計畫補了 S11（✅）與 S12（⏳）。
- **檢查清單第 4 項：五項檢查**
  - 我在 02e88e7 重跑了 `check-kit.py` 與 `check-links.py`，都通過，exit 0。
  - `bash -n`、test-install 36 項、test-evidence 315 項與 verify-artifact 沒有 diff，都引用 `evidence/kit-checks.txt`（S11 後的工作區）。這次增量沒有動到 skills/ 或 scripts/。
- **SHA 與範圍**
  - main 與 HEAD 的 merge-base 仍是 b26efc5。
  - 3ce9f7b..02e88e7 是兩個非 merge 提交：49d303c 保存報告與記帳，02e88e7 是修正。沒有改寫歷史，工作樹乾淨。
- 其餘沿用 review-3ce9f7b.md（及它沿用的 review-80d52c2.md、review-a42f00e.md）。
- **限制**
  - 只查核增量與它影響到的內容。test-install 與 test-evidence 沒有重跑，以 kit-checks.txt 的紀錄為準。
  - 以下這點不是增量引入的，記在這裡供協調者決定，不列為建議：
    - implementation-plan.md 的 S6、S8、S10 都是送審步驟，各自的審查都已 PASS、使用者也已決定處理方式，但狀態仍是 ⏳。
    - 02e88e7 改了計畫，但沒有改這三列。
    - 已合併的 issue-0012（S5）與 issue-0015（S5）也是送審步驟停在 ⏳，前三份報告都沒提，看來是 repo 現行的慣例。
    - dev-cycle 第 38 行「選計畫順序中第一項未完成的 Task」照字面讀可能先選到 S6。實際上 dev-cycle 也會讀 `**現行 review**` 與報告，影響有限。

## 流程判定
PASS

PASS 只適用於上列 Reviewed HEAD SHA；之後提交 README 記帳區段與本報告以外的檔案會讓它失效，提交前先告知使用者（review-evidence.md「審查之後的提交」）。
