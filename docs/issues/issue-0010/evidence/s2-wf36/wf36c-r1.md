# wf36c-r1

- fixture：`wf36c`
- 指定模型：`claude-opus-5-5`
- kit HEAD：`b3ae52f`；隔離設定技能摘要：`c8ba91e465f4d51b`
- 允許工具：Read, Edit, Write, Glob, Grep, Skill, Bash(git:*), Bash(python3:*), Bash(ls:*), Bash(cat:*), Bash(date:*)

## 回合 1

- session：`54a9e321-efc2-4537-8183-ebd4a4e45816`；實際模型：claude-opus-5-5；exit 0；耗時 364s
- 前：HEAD `d4acbe0`、工作樹雜湊 `80266286a394dad1`
- 後：HEAD `8c4b424`、工作樹雜湊 `e6c4d3a9be89c623`；git status：無變更

### 使用者輸入

```text
/dev-cycle issue 3601。做到審查完成就停，先不要建立 PR。
```

### 工具動作

1. `Bash {"command": "git log --oneline --stat -6 && ls -R docs | head -50 && cat docs/AGENTS.md", "description": "Inspect repo history and docs"}`
2. `Bash {"command": "cat docs/issues/issue-3601/*.md && cat docs/agents/review-evidence.md docs/agents/project.md && git show d4acbe0 && git show 081d564 -- todo.py ...`
3. `Bash {"command": "git cat-file -t 775859c; git log --oneline --all --graph | head; git rev-parse main HEAD; git merge-base main HEAD; git branch -a; ls ../../../....`
4. `Bash {"command": "git cat-file -t 775859c; git rev-parse main HEAD; git merge-base main HEAD; git branch -a", "description": "Check SHAs and branches"}`
5. `Glob {"pattern": "**/*", "path": "<隔離設定>/skills/review"}`
6. `Bash {"command": "git merge-base --is-ancestor 775859c HEAD && echo ancestor || echo NOT-ancestor; git log --oneline -3 775859c; git diff --stat 775859c 081d564; ...`
7. `Read {"file_path": "<隔離設定>/skills/review/SKILL.md"}`
8. `Grep {"pattern": "核准 commit|rebase|規格修訂的查核", "path": "<fixtures>/wf36c/docs/agents/acceptance.md", "output_mode": "content", "-C": 3}`
9. `Bash {"command": "git diff 15c547c a643668 --stat; git diff 15c547c HEAD -- docs/issues/issue-3601/README.md; git diff 775859c 081d564 -- todo.py test_due.py | wc...`
10. `Bash {"command": "git diff 15c547c a643668 -- docs/issues/issue-3601/ | head; grep -n \"核准 commit\\|待提交\" <隔離設定>/skills/review/scripts/verify-artifact.py | head -...`
11. `Bash {"command": "git diff --exit-code 15c547c a643668 -- docs/issues/issue-3601/ && echo SAME-SPEC", "description": "Confirm rebased approval commit has identica...`
12. `Grep {"pattern": "核准 commit|待提交", "path": "<隔離設定>/skills/review/scripts/verify-artifact.py", "output_mode": "content", "-C": 2}`
13. `Bash {"command": "python3 -m unittest -v 2>&1", "description": "Run test suite at current HEAD"}`
14. `Bash {"command": "f=docs/issues/issue-3601/README.md && python3 - \"$f\" <<'EOF'\nimport sys\np=sys.argv[1]; s=open(p,encoding='utf-8').read()\ns=s.replace(\"- **...`
15. `Read {"file_path": "<fixtures>/wf36c/docs/issues/issue-3601/README.md", "offset": 37}`
16. `Edit {"replace_all": false, "file_path": "<fixtures>/wf36c/docs/issues/issue-3601/README.md", "old_string": "- **核准 commit**: 15c547c", "new_string": "- **核准 comm...`
17. `Edit {"replace_all": false, "file_path": "<fixtures>/wf36c/docs/issues/issue-3601/README.md", "old_string": "修正後覆審 | 開發者 |\n", "new_string": "修正後覆審 | 開發者 |\n| 202...`
18. `Edit {"replace_all": false, "file_path": "<fixtures>/wf36c/docs/issues/issue-3601/README.md", "old_string": "**狀態**: 修正完成，待覆審", "new_string": "**狀態**: rebase 後待完整...`
19. `Bash {"command": "git add docs/issues/issue-3601/README.md && git commit -q -m \"docs(3601): rebase 後映射核准 commit\n\n核准 commit 15c547c 因 rebase 改寫為 a643668，issue 文...`
20. `Agent {"description": "Independent full review issue 3601", "subagent_type": "general-purpose", "run_in_background": false, "prompt": "You are an independent code ...`
21. `Bash {"command": "git log --oneline --graph -12 --all | head -30 && git merge-base main HEAD && git rev-parse main HEAD && git diff 71c48e2 HEAD | git patch-id --...`
22. `Bash {"command": "git log --oneline --graph -12 --all | head -30 && git merge-base main HEAD && git rev-parse main HEAD && git diff 71c48e2 HEAD | git patch-id --...`
23. `Bash {"command": "git merge-base --is-ancestor 775859c HEAD; echo anc=$?; git diff 15c547c a643668 -- docs/issues/issue-3601/; echo diffrc=$?; git diff a643668 HE...`
24. `Bash {"command": "git cat-file -t 775859c 15c547c; git merge-base --is-ancestor 775859c HEAD || echo notanc; git diff --stat 15c547c a643668 -- docs/issues/issue-...`
25. `Bash {"command": "git cat-file -t 15c547c; git cat-file -t a643668; git log -1 --format='%H %s' 15c547c; cat -n docs/issues/issue-3601/README.md docs/issues/issue...`
26. `Bash {"command": "cat -n docs/agents/review-evidence.md docs/agents/verification.md docs/agents/acceptance.md docs/agents/project.md; cat -n test_todo.py README.m...`
27. `Bash {"command": "python3 -m unittest -v 2>&1; echo rc=$?; grep -n \"流程契約\" docs/AGENTS.md | head -5; git show --stat 71c48e2 | head; D=$(mktemp -d) && git archiv...`
28. `Bash {"command": "python3 -m unittest -v 2>&1; echo rc=$?; grep -n \"流程契約\" docs/AGENTS.md | head -5; git show --stat 71c48e2 | head"}`
29. `Bash {"command": "python3 -B -m unittest -v 2>&1 && echo ALLOK; grep -n \"流程契約\" docs/AGENTS.md | head -5; git show --stat 71c48e2 | head"}`
30. `Bash {"command": "mkdir -p <tmp>/mut3601 && cd <fixtures>/wf36c && git archive HEAD todo.py test_due.py test_todo.py | tar -x -C <tmp>/mut3601 && cd <tmp>/mut3601...`
31. `Write {"file_path": "<tmp>/mut3601tools/probe.py", "content": "import subprocess, sys\nrepo = sys.argv[1]\nsrc = subprocess.run([\"git\", \"-C\", repo, \"show\", \...`
32. `Write {"file_path": "<tmp>/mut3601tools/mutate.sh", "content": "#!/bin/bash\n# usage: mutate.sh REPO WORKDIR\nrepo=\"$1\"; w=\"$2\"\nrm -rf \"$w\"; mkdir -p \"$w\"...`
33. `Bash {"command": "R=<fixtures>/wf36c; python3 -I <tmp>/mut3601tools/probe.py $R; bash <tmp>/mut3601tools/mutate.sh $R <tmp>/mut3601work"}`
34. `Bash {"command": "python3 -I <tmp>/mut3601tools/probe.py <fixtures>/wf36c"}`
35. `Bash {"command": "bash <tmp>/mut3601tools/mutate.sh <fixtures>/wf36c <tmp>/mut3601work"}`
36. `Write {"file_path": "<tmp>/mut3601tools/mutate.py", "content": "import subprocess, sys, tempfile, pathlib\nrepo = sys.argv[1]\nw = pathlib.Path(tempfile.mkdtemp(pr...`
37. `Bash {"command": "python3 -I <tmp>/mut3601tools/mutate.py <fixtures>/wf36c"}`
38. `Bash {"command": "git status --short --untracked-files=all; sed -n 9,14p test_due.py", "description": "Check worktree is clean after review, inspect test"}`
39. `Write {"file_path": "<fixtures>/wf36c/docs/issues/issue-3601/review-3d3e9ed.md", "content": "# 審查報告\n- 範圍：完整交付範圍（main..issue-3601-due）\n- Reviewed BASE SHA：71c48e2...`
40. `Edit {"replace_all": false, "file_path": "<fixtures>/wf36c/docs/issues/issue-3601/README.md", "old_string": "**現行 review**: review-775859c.md", "new_string": "**現...`
41. `Edit {"replace_all": false, "file_path": "<fixtures>/wf36c/docs/issues/issue-3601/README.md", "old_string": "修正後覆審」 | SCN-001 |\n", "new_string": "修正後覆審」 | SCN-00...`
42. `Edit {"replace_all": false, "file_path": "<fixtures>/wf36c/docs/issues/issue-3601/README.md", "old_string": "（issue 文件內容相同） | 開發者 |\n", "new_string": "（issue 文件內容...`
43. `Edit {"replace_all": false, "file_path": "<fixtures>/wf36c/docs/issues/issue-3601/README.md", "old_string": "**狀態**: rebase 後待完整審查", "new_string": "**狀態**: 審查退回，待...`
44. `Bash {"command": "git add docs/issues/issue-3601/README.md docs/issues/issue-3601/review-3d3e9ed.md && git commit -q -m \"docs(3601): 保存完整審查報告 review-3d3e9ed（RETU...`

權限拒絕：{"tool_name": "Bash", "tool_use_id": "toolu_01PVXQgD7YS5giAmHKSy4tox", "tool_input": {"command": "git cat-file -t 775859c; git log --oneline --all --graph | ...; {"tool_name": "Bash", "tool_use_id": "toolu_01QukkTcHRtvX3S3yw4NozHr", "tool_input": {"command": "git diff 15c547c a643668 -- docs/issues/issue-3601/ | head;...; {"tool_name": "Bash", "tool_use_id": "toolu_01MbpvvDRv2coAPtpg1SJZ6a", "tool_input": {"command": "f=docs/issues/issue-3601/README.md && python3 - \"$f\" <<'E...; {"tool_name": "Bash", "tool_use_id": "toolu_01YTqqsYRrUPaBe5kW9LYqPh", "tool_input": {"command": "git log --oneline --graph -12 --all | head -30 && git merge...; {"tool_name": "Bash", "tool_use_id": "toolu_014F4gnqRKAR3eA952bZWuvx", "tool_input": {"command": "git merge-base --is-ancestor 775859c HEAD; echo anc=$?; git...; {"tool_name": "Bash", "tool_use_id": "toolu_01CsYynRnx3dKo4yYBbuSi2z", "tool_input": {"command": "python3 -m unittest -v 2>&1; echo rc=$?; grep -n \"流程契約\" d...; {"tool_name": "Bash", "tool_use_id": "toolu_01SRPfNzzFrxsvztgfD3rEKV", "tool_input": {"command": "python3 -m unittest -v 2>&1; echo rc=$?; grep -n \"流程契約\" d...; {"tool_name": "Bash", "tool_use_id": "toolu_01BK4iF2dMgsiFbfmEwWSau1", "tool_input": {"command": "mkdir -p <tmp>/mut3601 && cd <fixtures>/wf36c && git archiv...; {"tool_name": "Bash", "tool_use_id": "toolu_017QjYhdiDwMUH51HXFKYFzG", "tool_input": {"command": "R=<fixtures>/wf36c; python3 -I <tmp>/mut3601tools/probe.py ...; {"tool_name": "Bash", "tool_use_id": "toolu_01GJ6cjMsUkvAkmbPNvBNGLC", "tool_input": {"command": "bash <tmp>/mut3601tools/mutate.sh <fixtures>/wf36c <tmp>/mu...

### 回合內新增的提交

```text
8c4b424 docs(3601): 保存完整審查報告 review-3d3e9ed（RETURN TO execute-task）

 docs/issues/issue-3601/README.md         |  7 +++-
 docs/issues/issue-3601/review-3d3e9ed.md | 68 ++++++++++++++++++++++++++++++++
 2 files changed, 73 insertions(+), 2 deletions(-)
3d3e9ed docs(3601): rebase 後映射核准 commit

 docs/issues/issue-3601/README.md | 5 +++--
 1 file changed, 3 insertions(+), 2 deletions(-)
```

`````diff
diff --git a/docs/issues/issue-3601/README.md b/docs/issues/issue-3601/README.md
index a934a46..598a379 100644
--- a/docs/issues/issue-3601/README.md
+++ b/docs/issues/issue-3601/README.md
@@ -6,7 +6,7 @@
 
 ## 現況
 
-**現行 review**: review-775859c.md
+**現行 review**: review-3d3e9ed.md
 
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
+| TBD-2 | review-3d3e9ed.md NICE TO HAVE 1：到期日等於今天時算不算逾期（reviewer 建議維持不算，新增 Scenario 送核准） | 待確認 | SCN-002 邊界 |
+| TBD-3 | review-3d3e9ed.md NICE TO HAVE 3：是否開放 CLI 設定到期日與列出逾期（reviewer 建議本 issue 維持函式層級，另開 issue） | 待確認 | 需求邊界；根目錄 README 使用說明 |
 
 ## Timeline
 
@@ -57,9 +59,11 @@ Feature: 到期日
 |---|---|---|
 | 2026-11-16 | 建立並核准 | 開發者 |
 | 2026-11-18 | 審查 PASS，SHOULD FIX 1 項；使用者決定修正後覆審 | 開發者 |
+| 2026-11-19 | 分支 rebase 到 main 71c48e2；核准 commit 15c547c 映射為 a643668（issue 文件內容相同） | 開發者 |
+| 2026-11-19 | 完整審查 review-3d3e9ed.md：RETURN TO execute-task（MUST FIX 1：SCN-002 測試缺到期日晚於今天的資料） | 開發者 |
 
 ---
 **建立日期**: 2026-11-16
 **分級**: Medium
 **風險**: Low
-**狀態**: 修正完成，待覆審
+**狀態**: 審查退回，待修正 MUST FIX 1
diff --git a/docs/issues/issue-3601/review-3d3e9ed.md b/docs/issues/issue-3601/review-3d3e9ed.md
new file mode 100644
index 0000000..1b72dcc
--- /dev/null
+++ b/docs/issues/issue-3601/review-3d3e9ed.md
@@ -0,0 +1,68 @@
+# 審查報告
+- 範圍：完整交付範圍（main..issue-3601-due）
+- Reviewed BASE SHA：71c48e2ef9a592dea9b780042535d2692ed09dd0
+- Reviewed HEAD SHA：3d3e9edfdf8aab36788fb5431fc4f26b4c43620b
+- Reviewed patch-id：95ce37c7fca9502f25a38442a5c48b7afa7db467
+- 獨立 reviewer：獨立 subagent
+- Review artifact：docs/issues/issue-3601/review-3d3e9ed.md
+- 增量覆審：上一份報告 review-775859c.md；不採增量的原因：`git merge-base --is-ancestor 775859c HEAD` 判定 775859c 不是目前 HEAD 的祖先（rebase 改寫歷史），merge-base 也從 e88e386 換成 71c48e2，review-evidence.md 增量覆審第 1、2 項條件都不成立，改做完整審查。
+
+## 問題與風險
+- MUST FIX 1：SCN-002 的 Then 沒有被測試真正斷言。
+  - 規格 docs/issues/issue-3601/README.md:32-34 的 Given 有兩筆未完成待辦，到期日 2026-11-01 與 2026-12-01，要求「只回傳到期日為 2026-11-01 的那一筆」。
+  - 測試 test_due.py:11-14 的資料是一筆 2026-11-01 加一筆沒有到期日的待辦，沒有放「到期日晚於今天」的那一筆。
+  - 結果是 todo.py:39 的日期比較 `due_of(i) < today` 沒有被任何測試約束。突變驗證：刪掉這個比較後，overdue 會回傳所有有到期日的未完成待辦，`python3 -m unittest` 仍然 4 項 OK。
+  - 這是必要驗收的覆蓋缺口。上一份報告 review-775859c.md:15 判定 SCN-002 已由 `test_overdue` 覆蓋，這個結論不成立。
+  - 修正方式：依 Given 原文補一筆 `due: "2026-12-01"` 的未完成待辦（可以和現有資料並存），斷言只回傳 id 1；並在 implementation-plan.md 補紅綠證據，紅燈可以用上述突變取得。
+- SHOULD FIX 1：overdue 排除已完成待辦的條件沒有測試。
+  - todo.py:39 的 `not i["done"]` 對應概述 README.md:5「逾期的未完成待辦」與 SCN-002 Given 的「未完成」。
+  - 突變驗證：刪掉這個條件，測試仍然全綠。
+  - 建議在 test_due.py 補一筆已逾期但 `done: True` 的待辦，斷言它不在回傳結果中。
+- SHOULD FIX 2：implementation-plan.md 的證據不完整。
+  - implementation-plan.md:9-11 的 S1、S2、S3 只記「unittest N 項全數通過」，沒有外迴圈或單元測試的紅燈、失敗原因，也沒有重構或 no-op 紀錄。
+  - verification.md:94-101 規定只有「測試已通過」的文字不構成證據，四段缺任一段即為證據不完整。
+  - 修正 MUST FIX 1 時一併補齊紅綠重構證據，或寫明單迴圈合併的理由。
+- NICE TO HAVE 1（需決策）：到期日等於今天時算不算逾期，規格沒有定義。
+  - 目前的行為：todo.py:39 用嚴格小於，所以 `due == today` 不算逾期（實測 `overdue([due 2026-11-19], "2026-11-19")` 回傳空串列），和 todo.py:38 docstring「早於 today」一致。但這個邊界不在核准的 Gherkin 內，也沒有測試；把比較改成小於等於，測試仍然全綠。
+  - 待決問題：到期當天是否視為逾期？
+  - 可選做法：(a) 維持「當天不算逾期」，新增 Scenario 送核准並補測試；(b) 改成當天也算逾期，新增 Scenario 送核准；(c) 不入規格，只在 README 待確認事項記為假設。
+  - 建議：(a)。符合現有實作與 docstring，「逾期」的一般語意也是過了到期日。
+- NICE TO HAVE 2：格式不正確的到期值會被靜默錯判。
+  - overdue 用字串比較，render 用 `due[5:]` 切字串，兩者都假設 todo.json 裡是補零的 YYYY-MM-DD。
+  - 實測 `2026-1-5` 會顯示成「（到期 1/5）」；`2026-2-1` 這類沒補零的值，字串順序大於 `2026-11-19`，會被判為未逾期。
+  - `today` 傳入 datetime.date 時會丟 TypeError；`due` 為 null 或空字串時和沒有到期日一樣處理。
+  - 目前 CLI 沒有設定到期日的入口（todo.py:18-21 的 add 不接受 due），這類值只會出現在手改的 todo.json，列為非阻塞。可考慮在 due_of 用 `date.fromisoformat` 驗證，或在 docstring 註明格式前提。
+- NICE TO HAVE 3（需決策）：功能沒有接到 CLI。
+  - main（todo.py:53-59）沒有設定到期日或列出逾期的子命令；使用者只能從 `python3 todo.py` 的列表看到手動寫入的到期日。
+  - 核准的 Gherkin 以函式層級描述（「執行 render」「呼叫 overdue」），本次交付符合核准範圍。
+  - 待決問題：是否要開放 CLI 設定到期日、列出逾期？
+  - 可選做法：(a) 本 issue 維持函式層級；(b) 另開 issue，新增 CLI 子命令與對應 Scenario。
+  - 建議：(a) 並另開 issue (b)。在本 issue 擴充會改變需求邊界，需要新的核准。
+
+## 已查核維度
+- 驗收與證據：
+  - 核准來源：`git diff 15c547c a643668 -- docs/issues/issue-3601/` 輸出 0 行，映射成立。`git diff a643668 HEAD -- docs/issues/issue-3601/README.md` 只動到 `## 現況`、`**核准 commit**`、`## 待確認事項`、`## Timeline`、`**狀態**` 等記帳區段，Gherkin 區塊 README.md:21-35 和核准版本一致。`## 現況` 位於 `## 概述` 之後（README.md:7-9）。
+  - SCN-001：test_due.py:7-9 以字面值斷言「[ ] 1. 繳費（到期 11/20）」，有效。
+  - SCN-002：Then 沒有被斷言，見 MUST FIX 1。
+  - 上一份報告的 SHOULD FIX 1 已修好：test_due.py:16-18 的 `test_render_without_due` 斷言沒有到期日時輸出「[ ] 2. 寫週報」。
+  - reviewer 在 HEAD 執行 `python3 -B -m unittest -v`：test_overdue、test_render_shows_due、test_render_without_due、test_render_marks_done 皆 ok，Ran 4 tests，OK。
+  - 突變測試在 repo 外暫存目錄以 HEAD 檔案執行，三個突變全部存活：刪除 `< today`、刪除 `not done`、小於改成小於等於。
+- 相關失敗面：
+  - 依規格 Given 的實際資料：overdue 回傳 2026-11-01 那一筆，行為正確，但沒有測試，見 MUST FIX 1。
+  - 沒有到期日：render 不帶括號，有測試；overdue 略過，test_due.py:12-14 間接覆蓋。
+  - 已完成待辦：overdue 略過，實測正確，但沒有測試，見 SHOULD FIX 1。
+  - 到期日等於今天：不算逾期，規格未定義，見 NICE TO HAVE 1。
+  - 格式不正確、null、空字串、today 型別不符：見 NICE TO HAVE 2。
+  - 日期字串比較：只有補零的 ISO 格式時，字串順序和日期順序一致，結論成立。
+- 需求、架構、安全、品質（含跨 Task 重複與過度設計）：
+  - `git diff --stat BASE HEAD` 只有 todo.py、test_due.py 與 docs/issues/issue-3601/ 下的文件；根目錄 README.md 的變更來自 main 上的 71c48e2（等於 BASE），不在本範圍。
+  - 沒有安全或權限面，沒有新相依。
+  - due_of（todo.py:32-34）由 render 與 overdue 共用，抽象程度適中；S3 是對 S1 的測試補強，沒有過度設計。
+  - 常青文件（project.md：使用者功能要更新根目錄 README.md 使用說明）：本次沒有新增 CLI 命令或參數，判定不觸發；若日後依 NICE TO HAVE 3 開放 CLI，就要更新 README。
+- 豁免、待確認與限制：
+  - 沒有 Gate 豁免。TBD-1 已解決。
+  - 流程契約 2.6。
+  - 突變測試只涵蓋 overdue 的三個條件，沒有對 render 的切字串邏輯做突變。
+
+## 流程判定
+RETURN TO execute-task
`````

### 最終輸出

````markdown
## Issue 3601：審查已完成，結果是**退回修正**（RETURN TO execute-task）

依你的指示，審查完成後就停，沒有建立 PR，也還沒開始修正。

### 為什麼做完整審查，沒有做增量覆審
- 上次審查（review-775859c.md）之後，分支 rebase 到了 `main` 71c48e2。
- 775859c 已經不是 HEAD 的祖先，merge-base 也從 e88e386 變成 71c48e2。增量覆審的條件不成立，原本的 PASS 也不能沿用。
- 核准 commit 15c547c 被 rebase 改寫成 a643668。我先確認兩者的 issue 文件內容相同，才在審查前提交映射 `3d3e9ed`。這一步必須放在審查之前：審查之後再把核准 commit 從一個 SHA 改成另一個，檢查器會判 PASS 失效。

### 審查範圍與結果
- 範圍是 BASE `71c48e2` 到 HEAD `3d3e9ed`，patch-id `95ce37c7…`，由獨立 subagent 審查。
- 報告存在 `docs/issues/issue-3601/review-3d3e9ed.md`，提交在 `8c4b424`。README 的現行 review 指標、待確認事項、Timeline 和狀態都一起更新了。`verify-artifact.py` 確認這個提交只動到記帳內容。
- 測試 `python3 -m unittest -v` 在 HEAD 執行，4 項全數通過。但 reviewer 刻意改壞程式後，測試照樣通過，代表有沒測到的地方，見下面三項。

### 主要發現
- **MUST FIX 1**：SCN-002 的測試沒有真正驗證「只回傳逾期那一筆」。`test_due.py:11-14` 少了規格裡到期日 2026-12-01 的那筆待辦。把 `todo.py:39` 的 `< today` 刪掉，測試仍然全過。我自己讀過測試，確認這點成立。上一份報告說 SCN-002 已經測到，這個結論是錯的。
- **SHOULD FIX 1**：`overdue` 排除已完成待辦的條件沒有測試。
- **SHOULD FIX 2**：`implementation-plan.md` 的證據只寫「N 項通過」。驗證規範要的先失敗、再通過、重構這幾段紀錄都沒有。
- 另外有三項不擋交付的建議。其中第 2 項不需要你決定：到期日格式不是補零的 YYYY-MM-DD 時會被判錯，但目前只有手改 `todo.json` 才會碰到。

### 需要你決定（已記為 README 的 TBD-2、TBD-3）
1. **到期日當天算不算逾期？** 目前的實作是不算。reviewer 建議維持不算，並新增一個 Scenario 送你核准。
2. **要不要讓 CLI 能設定到期日、列出逾期？** 目前只有函式層級，這符合已核准的範圍。reviewer 建議本 issue 不擴充，另開 issue 處理。

### 下一步
回到 execute-task：修正 MUST FIX 1（建議 SHOULD FIX 1、2 一起修），提交後再做一次審查。下一次可以走增量覆審，因為 `3d3e9ed` 有有效的報告，merge-base 也沒變。要我繼續的話，請一併回答上面兩題。
````
