# wf36c-r2

- fixture：`wf36c`
- 指定模型：`claude-opus-5-5`
- kit HEAD：`b3ae52f`；隔離設定技能摘要：`c8ba91e465f4d51b`
- 允許工具：Read, Edit, Write, Glob, Grep, Skill, Bash(git:*), Bash(python3:*), Bash(ls:*), Bash(cat:*), Bash(date:*)

## 回合 1

- session：`218f19f2-33eb-4376-ae81-a46a887b8394`；實際模型：claude-opus-5-5；exit 0；耗時 413s
- 前：HEAD `d4acbe0`、工作樹雜湊 `80266286a394dad1`
- 後：HEAD `962cd48`、工作樹雜湊 `6bcb261b9be38441`；git status：無變更

### 使用者輸入

```text
/dev-cycle issue 3601。做到審查完成就停，先不要建立 PR。
```

### 工具動作

1. `Bash {"command": "git log --oneline --stat -6 && ls -R docs | head -50", "description": "Show recent commits and docs tree"}`
2. `Bash {"command": "cat docs/issues/issue-3601/*.md && cat docs/agents/review-evidence.md docs/agents/project.md && git show d4acbe0 dc9ac22", "description": "Read ...`
3. `Bash {"command": "git cat-file -t 775859c; git branch -a; git log --oneline --all --graph | head; git merge-base main HEAD; cat docs/.dev-rules-kit.json; grep -n ...`
4. `Bash {"command": "git cat-file -t 775859c; git branch -a; git log --oneline --all --graph; git merge-base main HEAD; cat docs/.dev-rules-kit.json", "description":...`
5. `Grep {"pattern": "流程契約|核心層", "path": "<fixtures>/wf36c/docs/AGENTS.md", "output_mode": "content"}`
6. `Glob {"pattern": "**/*", "path": "<隔離設定>/skills/review"}`
7. `Bash {"command": "git log --oneline -3 775859c; git merge-base --is-ancestor 775859c HEAD; echo ancestor=$?; git diff 775859c 081d564 --stat; git log --oneline ma...`
8. `Bash {"command": "git log --oneline -3 775859c && git merge-base --is-ancestor 775859c HEAD && echo IS_ANCESTOR || echo NOT_ANCESTOR", "description": "Check wheth...`
9. `Bash {"command": "git diff 775859c 081d564 --stat && git reflog -15", "description": "Compare reviewed commit with current feat commit, show reflog"}`
10. `Read {"file_path": "<隔離設定>/skills/review/SKILL.md"}`
11. `Read {"file_path": "<fixtures>/wf36c/docs/agents/acceptance.md"}`
12. `Bash {"command": "git diff 15c547c a643668 && echo ---- && git diff 15c547c HEAD -- docs/issues/issue-3601/README.md && echo ---- && git diff 775859c 081d564 && g...`
13. `Bash {"command": "cat README.md && git diff main HEAD -- todo.py test_due.py", "description": "Show root README and code diff"}`
14. `Read {"file_path": "<fixtures>/wf36c/docs/issues/issue-3601/README.md", "offset": 36}`
15. `Edit {"replace_all": false, "file_path": "<fixtures>/wf36c/docs/issues/issue-3601/README.md", "old_string": "- **核准 commit**: 15c547c", "new_string": "- **核准 comm...`
16. `Edit {"replace_all": false, "file_path": "<fixtures>/wf36c/docs/issues/issue-3601/README.md", "old_string": "修正後覆審 | 開發者 |\n\n---", "new_string": "修正後覆審 | 開發者 |\n...`
17. `Edit {"replace_all": false, "file_path": "<fixtures>/wf36c/docs/issues/issue-3601/README.md", "old_string": "**狀態**: 修正完成，待覆審", "new_string": "**狀態**: 審查中"}`
18. `Bash {"command": "git add docs/issues/issue-3601/README.md && git commit -q -F - <<'EOF'\ndocs(issue-3601): rebase 後映射核准 commit 並轉為審查中\n\n分支 rebase 到 main 71c48e2...`
19. `Bash {"command": "git add docs/issues/issue-3601/README.md && git commit -q -F - <<'EOF'\ndocs(issue-3601): rebase 後映射核准 commit 並轉為審查中\n\n分支 rebase 到 main 71c48e2...`
20. `Bash {"command": "git diff 71c48e2ef9a592dea9b780042535d2692ed09dd0 4853dbc9b53c0b8dff28c6833fab7ae71ea4cb52 | git patch-id --stable", "description": "Compute pat...`
21. `Agent {"description": "Independent full review issue 3601", "subagent_type": "general-purpose", "run_in_background": false, "prompt": "你是 issue 3601 的獨立 reviewer（不...`
22. `Bash {"command": "git rev-parse HEAD main && git merge-base main HEAD && git diff 71c48e2 4853dbc | git patch-id --stable && git log --oneline main..HEAD && ls -R...`
23. `Read {"file_path": "<隔離設定>/skills/review/SKILL.md"}`
24. `Bash {"command": "cat docs/agents/project.md docs/agents/acceptance.md docs/agents/verification.md docs/agents/review-evidence.md"}`
25. `Bash {"command": "git diff 71c48e2 4853dbc -- todo.py test_due.py && cat -n todo.py && cat -n test_due.py && ls -a && cat -n README.md 2>/dev/null"}`
26. `Bash {"command": "cat -n docs/issues/issue-3601/README.md && cat -n docs/issues/issue-3601/implementation-plan.md && cat -n docs/issues/issue-3601/review-775859c....`
27. `Bash {"command": "git diff a643668 4853dbc -- docs/issues/issue-3601/README.md; echo ====; diff <(git show 15c547c:docs/issues/issue-3601/README.md) <(git show a6...`
28. `Bash {"command": "git diff a643668 4853dbc -- docs/issues/issue-3601/README.md; echo ====; git diff 15c547c a643668 -- docs/issues/issue-3601/README.md; echo \"di...`
29. `Bash {"command": "git diff a643668 4853dbc -- docs/issues/issue-3601/README.md; echo ====; git diff --stat 15c547c a643668 -- docs/issues/issue-3601/README.md; ec...`
30. `Bash {"command": "git diff --quiet 15c547c a643668 -- docs/issues/issue-3601/ && echo SAME_ISSUE_DIR; python3 -m unittest -v 2>&1; echo exit=$?; cat -n test_todo....`
31. `Bash {"command": "git diff --quiet 15c547c a643668 -- docs/issues/issue-3601/ && echo SAME_ISSUE_DIR"}`
32. `Bash {"command": "python3 -m unittest -v 2>&1"}`
33. `Bash {"command": "cat -n test_todo.py; git status --short; git diff 71c48e2 4853dbc --name-status; git log --oneline main -3"}`
34. `Bash {"command": "mkdir -p <tmp>/rv3601/base && cd <fixtures>/wf36c && git show 71c48e2:todo.py > <tmp>/rv3601/base/todo.py && git show 4853dbc:test_due.py > <tmp...`
35. `Bash {"command": "mkdir -p <tmp>/rv3601/base && git -C <fixtures>/wf36c show 71c48e2:todo.py > <tmp>/rv3601/base/todo.py && git -C <fixtures>/wf36c show 4853dbc:t...`
36. `Bash {"command": "python3 -B -c '\nimport unittest, todo, test_due\ntodo.overdue = lambda items, today: [i for i in items if todo.due_of(i)]\nr = unittest.TextTes...`
37. `Bash {"command": "sed -n '1,25p' test_due.py | cat -n | sed -n '11,14p'", "description": "Confirm the cited test lines"}`
38. `Write {"file_path": "<fixtures>/wf36c/docs/issues/issue-3601/review-4853dbc.md", "content": "# 審查報告\n- 範圍：完整交付範圍（main..issue-3601-due；TARGET main = BASE）\n- Review...`
39. `Edit {"replace_all": false, "file_path": "<fixtures>/wf36c/docs/issues/issue-3601/README.md", "old_string": "**現行 review**: review-775859c.md", "new_string": "**現...`
40. `Edit {"replace_all": false, "file_path": "<fixtures>/wf36c/docs/issues/issue-3601/README.md", "old_string": "修正後覆審」 | SCN-001 |\n", "new_string": "修正後覆審」 | SCN-00...`
41. `Edit {"replace_all": false, "file_path": "<fixtures>/wf36c/docs/issues/issue-3601/README.md", "old_string": "改做完整重審 | 開發者 |\n", "new_string": "改做完整重審 | 開發者 |\n| 2...`
42. `Edit {"replace_all": false, "file_path": "<fixtures>/wf36c/docs/issues/issue-3601/README.md", "old_string": "**狀態**: 審查中", "new_string": "**狀態**: 審查退回，待修正與決策"}`
43. `Bash {"command": "git add docs/issues/issue-3601/README.md docs/issues/issue-3601/review-4853dbc.md && git commit -q -F - <<'EOF'\ndocs(issue-3601): 保存審查報告 review...`
44. `Bash {"command": "sed -i 's/| 待使用者決定（reviewer 建議/| 待確認：待使用者決定（reviewer 建議/' docs/issues/issue-3601/README.md && grep -n \"TBD-\" docs/issues/issue-3601/README.md ...`
45. `Edit {"replace_all": false, "file_path": "<fixtures>/wf36c/docs/issues/issue-3601/README.md", "old_string": "| 待使用者決定（reviewer 建議不列入", "new_string": "| 待確認：待使用者決定...`
46. `Edit {"replace_all": false, "file_path": "<fixtures>/wf36c/docs/issues/issue-3601/README.md", "old_string": "| 待使用者決定（reviewer 建議維持", "new_string": "| 待確認：待使用者決定（...`
47. `Bash {"command": "git add docs/issues/issue-3601/README.md && git commit -q --amend --no-edit && python3 <隔離設定>/skills/review/scripts/verify-artifact.py --repo . ...`

權限拒絕：{"tool_name": "Bash", "tool_use_id": "toolu_0133eT1589LfDio4GK1VbTSe", "tool_input": {"command": "git cat-file -t 775859c; git branch -a; git log --oneline -...; {"tool_name": "Bash", "tool_use_id": "toolu_01MMJHmM6M3gUhh33wi55Vym", "tool_input": {"command": "git log --oneline -3 775859c; git merge-base --is-ancestor ...; {"tool_name": "Bash", "tool_use_id": "toolu_017zhS74T3FSBeo6ow8hAmKH", "tool_input": {"command": "git add docs/issues/issue-3601/README.md && git commit -q -...; {"tool_name": "Bash", "tool_use_id": "toolu_01EtrSWgjMwPEMZWoh8tRMKe", "tool_input": {"command": "git diff a643668 4853dbc -- docs/issues/issue-3601/README.m...; {"tool_name": "Bash", "tool_use_id": "toolu_01XwSVUxPM7shChMBPGxrzBf", "tool_input": {"command": "git diff a643668 4853dbc -- docs/issues/issue-3601/README.m...; {"tool_name": "Bash", "tool_use_id": "toolu_01Mha3skbLseVG6JeRYQNhUq", "tool_input": {"command": "git diff --quiet 15c547c a643668 -- docs/issues/issue-3601/...; {"tool_name": "Bash", "tool_use_id": "toolu_01DPtadT7YfuukHUcGgmFcq2", "tool_input": {"command": "mkdir -p <tmp>/rv3601/base && cd <fixtures>/wf36c && git sh...; {"tool_name": "Bash", "tool_use_id": "toolu_01WrkDDfsdp7KEXaEuibLgfy", "tool_input": {"command": "mkdir -p <tmp>/rv3601/base && git -C <fixtures>/wf36c show ...; {"tool_name": "Bash", "tool_use_id": "toolu_013tKiHTH8L9nLnU1ctmfsBV", "tool_input": {"command": "sed -i 's/| 待使用者決定（reviewer 建議/| 待確認：待使用者決定（reviewer 建議/' d...

### 回合內新增的提交

```text
962cd48 docs(issue-3601): 保存審查報告 review-4853dbc（RETURN TO execute-task）

 docs/issues/issue-3601/README.md         |   7 +-
 docs/issues/issue-3601/review-4853dbc.md | 139 +++++++++++++++++++++++++++++++
 2 files changed, 144 insertions(+), 2 deletions(-)
4853dbc docs(issue-3601): rebase 後映射核准 commit 並轉為審查中

 docs/issues/issue-3601/README.md | 5 +++--
 1 file changed, 3 insertions(+), 2 deletions(-)
```

`````diff
diff --git a/docs/issues/issue-3601/README.md b/docs/issues/issue-3601/README.md
index a934a46..a6e4817 100644
--- a/docs/issues/issue-3601/README.md
+++ b/docs/issues/issue-3601/README.md
@@ -6,7 +6,7 @@
 
 ## 現況
 
-**現行 review**: review-775859c.md
+**現行 review**: review-4853dbc.md
 
 ## 文件清單
 
@@ -36,7 +36,7 @@ Feature: 到期日
 
 ## Gherkin 核准紀錄
 
-- **核准 commit**: 15c547c
+- **核准 commit**: a643668
 - **核准來源**: 2026-11-16 使用者回覆「核准」
 
 全部 Scenario 於 2026-11-16 核准。
@@ -50,6 +50,8 @@ Feature: 到期日
 | 編號 | 事項 | 狀態 | 影響 |
 |---|---|---|---|
 | TBD-1 | review-775859c.md 的 SHOULD FIX 1 要不要修 | 已解決：2026-11-18 使用者選「修正後覆審」 | SCN-001 |
+| TBD-2 | review-4853dbc.md SHOULD FIX 2：到期日等於今天的未完成待辦，overdue 要不要列出 | 待確認：待使用者決定（reviewer 建議不列入，維持現狀並補 Scenario 與測試） | SCN-002 |
+| TBD-3 | review-4853dbc.md SHOULD FIX 3：本 issue 要不要提供設定到期日、列出逾期的 CLI 入口 | 待確認：待使用者決定（reviewer 建議維持函式層範圍，另開 issue） | SCN-001、SCN-002 |
 
 ## Timeline
 
@@ -57,9 +59,11 @@ Feature: 到期日
 |---|---|---|
 | 2026-11-16 | 建立並核准 | 開發者 |
 | 2026-11-18 | 審查 PASS，SHOULD FIX 1 項；使用者決定修正後覆審 | 開發者 |
+| 2026-11-19 | 分支已 rebase 到 main 71c48e2，原核准 commit 15c547c 改寫為 a643668（驗收區塊比對相同，映射新 SHA）；原報告 review-775859c 的 HEAD 不在新歷史上、merge-base 改變，改做完整重審 | 開發者 |
+| 2026-11-19 | 完整重審 review-4853dbc：RETURN TO execute-task（MUST FIX 1：SCN-002 測試未涵蓋 Given）；SHOULD FIX 2、3 需決策 | 開發者 |
 
 ---
 **建立日期**: 2026-11-16
 **分級**: Medium
 **風險**: Low
-**狀態**: 修正完成，待覆審
+**狀態**: 審查退回，待修正與決策
diff --git a/docs/issues/issue-3601/review-4853dbc.md b/docs/issues/issue-3601/review-4853dbc.md
new file mode 100644
index 0000000..85221a4
--- /dev/null
+++ b/docs/issues/issue-3601/review-4853dbc.md
@@ -0,0 +1,139 @@
+# 審查報告
+- 範圍：完整交付範圍（main..issue-3601-due；TARGET main = BASE）
+- Reviewed BASE SHA：71c48e2ef9a592dea9b780042535d2692ed09dd0
+- Reviewed HEAD SHA：4853dbc9b53c0b8dff28c6833fab7ae71ea4cb52
+- Reviewed patch-id：7f77e7135a4c8724ed5bfc766addc78ae0848562（已在 HEAD 用 `git diff 71c48e2 4853dbc | git patch-id --stable` 重算，結果相同）
+- 獨立 reviewer：獨立 subagent（general-purpose）
+- Review artifact：docs/issues/issue-3601/review-4853dbc.md
+- 增量覆審：有上一份報告 docs/issues/issue-3601/review-775859c.md，但這次做完整審查。原因是增量覆審條件 1、2 都不成立：
+  - 條件 1：分支已 rebase，該報告綁定的 HEAD 775859c 不是目前 HEAD 的祖先，H1 之後歷史已被改寫。
+  - 條件 2：merge-base 由 e88e386 變成 71c48e2，與該報告的 Reviewed BASE 不同。
+
+  該報告的結論都不沿用，全部在 4853dbc 重新查核。
+
+## 問題與風險
+
+### MUST FIX 1：SCN-002 的測試沒有涵蓋 Scenario 的 Given，驗不出「只回傳」
+- 位置：`test_due.py:11-14`；對照 `docs/issues/issue-3601/README.md:30-34`。
+- 落差：
+  - Gherkin 的 Given 是兩筆**都有到期日**的未完成待辦（2026-11-01 與 2026-12-01），Then 是只回傳 11-01 那一筆。
+  - `test_overdue` 用的卻是一筆 11-01，加上一筆**沒有到期日**的待辦。未到期的 12-01 這筆從沒出現在測試裡。
+- 影響：這個測試分不出「已逾期」和「有到期日」。我在記憶體中把 `todo.overdue` 換成突變體 `lambda items, today: [i for i in items if todo.due_of(i)]`（回傳所有有到期日的待辦），`test_due.DueTest.test_overdue` 仍然通過（輸出 `OK`，`mutant(all-with-due) survived: True`）。
+  - 所以 SCN-002 的區別性結果沒有可重現的證據。這是必要驗收的覆蓋缺口，不只是證據持久力不足。
+  - 現行實作本身正確：用 SCN-002 原始 Given 在記憶體探測，`overdue(..., "2026-11-19")` 回傳 `[1]`。所以這屬於證據缺口，不是邏輯錯誤。
+- 建議：
+  - 讓 `test_overdue` 符合 Gherkin：兩筆未完成待辦，到期日 2026-11-01 與 2026-12-01，today 2026-11-19，斷言 id 只有 11-01 那筆。
+  - 沒有到期日的情況可以留著，但改成另一個斷言或另一個案例。
+  - 修好後在 implementation-plan 的 S2 列記錄這次修正的命令與結果。
+
+### SHOULD FIX 1：S1、S2 的紅綠重構證據不完整
+- 位置：`docs/issues/issue-3601/implementation-plan.md:9-10`。
+- 落差：S1、S2 會改變可觀察行為，但只記了「`python3 -m unittest -v` 3 項全數通過」。外迴圈與單元測試的紅燈、失敗原因、被測提交和重構後綠燈都沒記（verification.md「紅綠重構證據」）。
+- 現況：我在 HEAD 重跑測試，綠燈成立（見下方「驗收與證據」）。依指示只讀，這次沒在 BASE 重現紅燈。
+- 建議：修 MUST FIX 1 時一併補上 S2 的紅燈（先在 BASE 或實作前跑新測試並記錄失敗原因）。S1 能從歷史重現紅燈就補記，不能重現就明列限制。
+
+### SHOULD FIX 2（`需決策`）：到期當天算不算逾期，還沒核准
+- 位置：`todo.py:38-39`（`due_of(i) < today`，嚴格小於）。
+- 現況：實作與 docstring 都採「到期日早於 today 才算逾期」，到期當天不列入。這是合理的預設，但 SCN-002 沒有規定這個邊界，屬於規劃時推導出的可觀察行為，依 acceptance.md 應先取得使用者接受。目前也沒有測試鎖住這個邊界。
+- 待決問題：到期日等於今天的未完成待辦，`overdue` 要不要列出？
+- 可選做法：
+  - (a) 不列入（維持現狀）。補一個 Scenario 或 SCN-002 的附註取得核准，並補測試 `due == today → 不回傳`。
+  - (b) 列入。改成 `<=`，同樣補 Scenario 與測試。
+- 建議：採 (a)。「逾期」一般指過了到期日，也和現有 docstring 一致。
+
+### SHOULD FIX 3（`需決策`）：CLI 沒有設定到期日或列出逾期的入口，常青 README 是否需要更新取決於範圍
+- 位置：`todo.py:53-59`（`main` 只有 add／done／列出），`todo.py:18-21`（`add` 不寫入 `due`）；根目錄 `README.md:5-9`。
+- 現況：
+  - 已核准的 Gherkin 只到函式層（「執行 render」「呼叫 overdue」），實作符合核准範圍。
+  - 但概述（`docs/issues/issue-3601/README.md:5`）寫的是使用者功能「待辦可以帶到期日……能列出逾期」。目前使用者只能手改 `todo.json` 才能讓 `due` 出現，`overdue` 也沒有 CLI 指令。
+  - 因為沒有使用者入口，這次變更不會觸發 project.md「使用者功能 → 根目錄 README 使用說明」的更新責任，根目錄 README 不更新可以接受。
+- 待決問題：這個 issue 要不要提供使用者入口？
+- 可選做法：
+  - (a) 維持函式層範圍，另開 issue 做 CLI 入口。在本 issue 的待確認事項記下這個決定。
+  - (b) 在本 issue 新增 Scenario 並核准（例如 `add <標題> --due YYYY-MM-DD`、`overdue` 子命令），連同根目錄 README 使用說明一起交付。
+- 建議：採 (a)，維持已核准範圍，避免未經核准的規格擴張。改採 (b) 時，根目錄 README 必須一起更新。
+
+### NICE TO HAVE 1：沒有測試鎖住「已完成待辦不列入 overdue」
+- 位置：`todo.py:39`（`not i["done"]`）；`test_due.py` 沒有已完成且已過期的案例。
+- 現況：概述寫「逾期的**未完成**待辦」，SCN-002 的 Given 也限定未完成，所以這不是核准 Scenario 的明文結果。實作正確（記憶體探測時，已完成且到期日 11-01 的 id 3 沒有被回傳）。
+- 建議：補一個已完成且已過期、不應回傳的案例，提升回歸防護。
+
+### NICE TO HAVE 2：到期日格式沒有驗證，比較依賴 ISO 補零格式
+- 位置：`todo.py:32-34, 39, 48`。
+- 現況：`overdue` 以字串比較日期，`render` 用 `due[5:]` 切出月日，兩者都假設嚴格的 `YYYY-MM-DD`。
+  - 遇到 `"2026-12-1"` 這類非補零值，字串比較會失真。探測：today `"2026-12-01"` 時回傳 `[]`。若 today 是 `"2026-12-10"`，`"2026-12-1" < "2026-12-10"` 會成立，結果才剛好正確，屬於偶然。
+  - `render` 會顯示補零的 `01/05`。SCN-001 只驗 11/20，沒有規定要不要補零。
+- 評估：目前沒有寫入 `due` 的程式入口，資料只會來自手改 JSON，風險低。
+- 建議：之後加 CLI 入口（見 SHOULD FIX 3）時，在入口處用 `datetime.date.fromisoformat` 驗證並正規化。
+
+### NICE TO HAVE 3：`overdue` 呼叫兩次 `due_of`
+- 位置：`todo.py:39`。
+- 建議：可簡化為 `due_of(i) and due_of(i) < today`，改寫成單次取值，或者直接利用 `"" < today` 恆為真的特性……後者不可行，會把沒有到期日的待辦也列入。所以只建議在可讀性上保持現狀，或用海象運算子取一次值。純可讀性，不阻塞。
+
+## 已查核維度
+
+### 驗收與證據
+- 本次在 HEAD 4853dbc 執行 `python3 -m unittest -v`，exit 0：
+
+  ```
+  test_overdue (test_due.DueTest.test_overdue) ... ok
+  test_render_shows_due (test_due.DueTest.test_render_shows_due) ... ok
+  test_render_without_due (test_due.DueTest.test_render_without_due) ... ok
+  test_render_marks_done (test_todo.RenderTest.test_render_marks_done) ... ok
+  ----------------------------------------------------------------------
+  Ran 4 tests in 0.000s
+
+  OK
+  ```
+
+- SCN-001（`docs/issues/issue-3601/README.md:24-28`）：由 `test_due.py:7-9` 覆蓋。斷言完整行等於 `"[ ] 1. 繳費（到期 11/20）"`，期望值是規格原文的字面值，不是同義反覆。結論：通過。
+- SCN-002（`docs/issues/issue-3601/README.md:30-34`）：`test_due.py:11-14` 沒有涵蓋 Given 的 12-01 未到期待辦，突變體會存活，見 MUST FIX 1。結論：**證據缺口**。實作行為經記憶體探測是正確的。
+- S3（`implementation-plan.md:11`）：上一份報告的 SHOULD FIX 1（沒有到期日時 render 的測試）已處理。
+  - `test_due.py:16-18` 斷言 `"[ ] 2. 寫週報"`，不帶括號，期望值是獨立字面值。
+  - 使用者已選「修正後覆審」（README:52 TBD-1）。
+  - 這是為既有行為補的測試，不改變行為，不需要紅燈。
+  - 結論：已處理。
+- 核准基線：
+  - 核准 commit 已填 `a643668`，不是 `待提交`，所以不用推導。
+  - 我用 `git diff --quiet 15c547c a643668 -- docs/issues/issue-3601/` 確認，原核准 commit 15c547c 與 rebase 後的 a643668 在 issue 目錄內容完全相同（輸出 `SAME_ISSUE_DIR`），驗收區塊也就相同，映射成立。
+  - `git diff a643668 4853dbc -- docs/issues/issue-3601/README.md` 只變更了以下內容：新增 `## 現況`、`**核准 commit**` 由 `待提交` 改為 `a643668`、新增 `## 待確認事項`（TBD-1）、Timeline 兩列、`**狀態**` 由 `待實作` 改為 `審查中`。
+  - Gherkin 的條件、動作、結果都沒變，原核准（2026-11-16 使用者回覆「核准」）有效。
+
+### 相關失敗面
+
+| 輸入／狀態 | 預期 | 現有覆蓋 | 判定 |
+|---|---|---|---|
+| 有到期日、未完成，render | 行尾「（到期 MM/DD）」 | `test_due.py:7-9` | 通過 |
+| 沒有到期日，render | 不帶括號 | `test_due.py:16-18` | 通過 |
+| 已完成且有到期日，render | 顯示 `[x]` 並附到期日 | 無測試；探測輸出 `[x] 1. x（到期 01/05）` | 行為合理，規格未規定，不阻塞 |
+| SCN-002 原始 Given（11-01 與 12-01），overdue | 只回傳 11-01 | 無；現有測試的突變體會存活 | **MUST FIX 1** |
+| 沒有到期日，overdue | 不回傳（`due_of` 回傳 `""`，短路排除） | `test_due.py:12-14` 的 id 2 | 通過 |
+| 已完成且已過期，overdue | 不回傳 | 無測試；探測正確 | NICE TO HAVE 1 |
+| 到期日等於 today，overdue | 未核准；實作不回傳 | 無 | SHOULD FIX 2 `需決策` |
+| 日期字串比較 | ISO `YYYY-MM-DD` 補零時，字串順序等於日期順序，結果正確 | 隱含在現有測試中 | 在補零前提下成立，見 NICE TO HAVE 2 |
+| 非 ISO 或非補零的 due | 規格未定義 | 無；沒有寫入入口 | NICE TO HAVE 2，低風險 |
+| 既有清單輸出回歸（沒有 due 的舊資料） | 輸出與變更前相同 | `test_todo.py:7-9` 仍綠，`test_due.py:16-18` | 通過 |
+
+### 需求、架構、安全、品質
+- 需求：實作符合已核准的函式層 Scenario。使用者入口的範圍有落差，已列為 SHOULD FIX 3 `需決策`。
+- 架構：變更侷限在 `todo.py` 的純函式與新測試檔，`render` 與 `overdue` 共用 `due_of` 取值，沒有越界，也沒有更動資料讀寫。
+- 安全：沒有新的外部輸入、權限、依賴或檔案存取面。不適用。
+- 品質（code-simplify 標準）：
+  - 跨 S1–S3 沒有分歧的重複邏輯，到期日取值集中在 `due_of`。
+  - `due_of` 是很薄的包裝，但兩處共用，而且統一了「沒有 due 時回傳空字串」的語意，不算過度設計。
+  - 只有 NICE TO HAVE 3 這種可讀性細節。
+  - `render` 拆成迴圈，可讀性尚可。
+- 常青文件：CLI 沒有可讓使用者設定 due 或查詢逾期的入口，所以這次不觸發根目錄 `README.md` 使用說明的更新責任。若決定加入口，就會觸發，見 SHOULD FIX 3。
+
+### 豁免、待確認與限制
+- 豁免：沒有 Gate 豁免紀錄。
+- 待確認：TBD-1（`docs/issues/issue-3601/README.md:52`）已解決，對應的修正（S3）已確認完成。
+- 限制：
+  - 依指示只讀，沒有在 BASE 實際重現 S1、S2 的紅燈。
+  - 突變與邊界探測都在記憶體中進行（`python3 -B -c`），沒有寫入 repo。
+- 記帳提醒：`docs/issues/issue-3601/README.md:9` 的 `**現行 review**` 仍指向 review-775859c.md，保存這份報告的提交應改指 review-4853dbc.md。
+
+## 流程判定
+RETURN TO execute-task
+
+原因：MUST FIX 1。SCN-002 的必要驗收證據沒有涵蓋 Scenario 的 Given 與「只回傳」的區別性結果。修正後需要重新審查。屆時若條件 1、2 都成立（4853dbc 為祖先、沒有改寫歷史、merge-base 仍是 71c48e2），可以用這份報告做增量覆審。SHOULD FIX 2、3 的 `需決策` 項目，請協調者依 acceptance.md「逐題確認」取得使用者答案後，記入 README `## 待確認事項`。
`````

### 最終輸出

````markdown
審查已完成。結果是**退回修正（RETURN TO execute-task）**，不是 PASS。依你的指示停在這裡，沒有建立 PR。

## 為什麼重新完整審查
分支之前 rebase 到 main（71c48e2），舊報告 `review-775859c` 審查的提交已不在目前歷史上，基準點也變了，所以舊的 PASS 失效，也不能只看新增的部分。核准 commit 15c547c 被改寫成 a643668。我核對過兩者的 issue 文件內容完全相同，所以沿用原核准，只改記新 SHA（提交 `4853dbc`）。

## 審查結果
報告存在 `docs/issues/issue-3601/review-4853dbc.md`，審查範圍是 `71c48e2..4853dbc`，由獨立 subagent 審查。
- **必須修正 1 項：** `test_due.py:11-14` 跟驗收劇本 SCN-002 的前提條件不一致。劇本是兩筆都有到期日（11-01、12-01），測試的第二筆卻沒有到期日。結果是就算把 `overdue` 寫錯成「回傳所有有到期日的項目」，這個測試也照樣通過，無法證明「只回傳逾期那筆」。我已經看過那幾行，確認屬實。程式本身的行為是正確的，缺的是測試證據。
- **建議修正：** S1、S2 只記了最後通過的結果，缺了測試先失敗、再改到通過的紀錄。另有兩項需要你決定，見下方。
- **可有可無：** 補一個「已完成的待辦不算逾期」的測試；目前沒有驗證到期日格式；`due_of` 在同一行呼叫了兩次。
- 4 項測試在 `4853dbc` 全部通過。上一份報告建議補的「沒有到期日時的顯示」測試已經補上。

## 這次的提交
- `4853dbc`：改記新的核准 commit，狀態改成「審查中」，Timeline 補記 rebase 的經過。
- `962cd48`：保存報告，README 改指向新報告，記下兩項待決事項（TBD-2、TBD-3）並更新狀態。這個提交我 amend 過一次，因為報告格式檢查提醒待決事項的狀態要以「待確認」開頭。改完重跑檢查通過，確認這個提交只動了記錄，不影響審查結果。

## 下一步
修正測試之前，需要你回答兩題，彼此獨立：

1. **TBD-2（影響 SCN-002）：** 到期日剛好是今天的未完成待辦，要算逾期嗎？
   - (a) 不算，維持現在的寫法，補一個 Scenario 和測試。
   - (b) 算，改成 `<=`。
   - 建議選 (a)：一般說「逾期」是指過了到期日，也跟程式裡的說明一致。
2. **TBD-3（影響 SCN-001、SCN-002）：** 這個 issue 要不要做 CLI 入口（設定到期日、列出逾期）？
   - (a) 不做，維持只有函式，另開 issue。
   - (b) 這次一起做，要新增 Scenario 並經你核准，也要更新根目錄 README。
   - 建議選 (a)：不擴大已核准的範圍。

你回答後，我會修正測試和建議項目，再拿 `review-4853dbc` 當上一份報告，只審查新增的修正。
````
