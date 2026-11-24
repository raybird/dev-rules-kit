# wf44b-r4

- fixture：`wf44b`
- 指定模型：`claude-opus-5-5`
- kit HEAD：`d4c5bd9`；隔離設定技能摘要：`969da1a5f024813f`
- 允許工具：Read, Edit, Write, Glob, Grep, Skill, Bash(git:*), Bash(python3:*), Bash(ls:*), Bash(cat:*), Bash(date:*)

## 回合 1

- session：`cd1da741-ead3-42fa-abbd-539691597d5c`；實際模型：claude-opus-5-5；exit 0；耗時 259s
- 前：HEAD `705822a`、工作樹雜湊 `caaf0eaccd1447e8`
- 後：HEAD `ff6d1a9`、工作樹雜湊 `acc119ddfc63b738`；git status：無變更

### 使用者輸入

```text
/review issue 3601 的完整交付範圍（main..HEAD），報告保存到 issue 目錄並提交。
```

### 工具動作

1. `Bash {"command": "git log --oneline --all && git diff --stat main..HEAD && ls -R docs && cat docs/AGENTS.md docs/agents/*.md", "description": "Inspect repo histor...`
2. `Read {"file_path": "<隔離設定>/projects/<fixtures>-wf44b/cd1da741-ead3-42fa-abbd-539691597d5c/tool-results/bwsdsrtj8.txt", "allow_large": true}`
3. `Bash {"command": "git diff main..HEAD; git merge-base main HEAD; git rev-parse main HEAD; git diff main HEAD | git patch-id --stable; cat todo.py; ls; ls <隔離設定>/s...`
4. `Bash {"command": "git diff main..HEAD && git merge-base main HEAD && git rev-parse main HEAD", "description": "Show full diff and SHAs"}`
5. `Bash {"command": "git diff 70f4ada 705822a | git patch-id --stable", "description": "Compute patch-id of reviewed range"}`
6. `Bash {"command": "python3 -m unittest -v 2>&1; git diff df95965 705822a -- docs/issues/issue-3601/README.md", "description": "Run tests and diff spec since approv...`
7. `Agent {"description": "Independent review issue 3601", "subagent_type": "general-purpose", "run_in_background": false, "prompt": "You are the independent reviewer ...`
8. `Bash {"command": "git log --oneline --stat && git diff 70f4ada 705822a --stat && git diff 70f4ada 705822a | git patch-id --stable; ls -R docs | head -50", "descri...`
9. `Bash {"command": "git diff 70f4ada 705822a; echo ======; git diff df95965 705822a -- docs/issues/issue-3601/README.md; echo =====; cat todo.py test_todo.py README...`
10. `Bash {"command": "cat docs/agents/acceptance.md docs/agents/review-evidence.md docs/agents/verification.md", "description": "Read acceptance, review, verification...`
11. `Bash {"command": "cat docs/AGENTS.md docs/agents/document-types.md; grep -n \"概述\\|涉及檔案\\|Timeline\\|待確認事項\\|狀態\" docs/agents/readme-templates.md | head -60", "de...`
12. `Bash {"command": "sed -n 40,200p docs/AGENTS.md", "description": "Read rest of AGENTS.md"}`
13. `Bash {"command": "cat docs/agents/document-types.md; sed -n 1,120p docs/agents/readme-templates.md", "description": "Read document-types and templates"}`
14. `Bash {"command": "sed -n 120,210p docs/agents/readme-templates.md; python3 -m unittest -v 2>&1 | tail -8; git status --short; python3 -I -c \"\nimport sys; sys.pa...`
15. `Bash {"command": "python3 -I -c \"\nimport sys; sys.path.insert(0,'.')\nimport todo\nprint([i['id'] for i in todo.overdue([{'id':1,'done':False,'due':'2026-2-1'},...`
16. `Write {"file_path": "<fixtures>/wf44b/docs/issues/issue-3601/review-705822a.md", "content": "# 審查報告\n- 範圍：完整交付範圍（main..HEAD）\n- Reviewed BASE SHA：70f4ada99d53e2a44...`
17. `Bash {"command": "grep -n \"\" todo.py | sed -n '15,62p'; grep -n \"\" README.md | sed -n '5,12p'", "description": "Check line numbers in todo.py and README"}`
18. `Bash {"command": "cd <fixtures>/wf44b/docs/issues/issue-3601 && python3 - <<'EOF'\np='review-705822a.md'\ns=open(p,encoding='utf-8').read()\nreps=[(\"`README.md:5...`
19. `Read {"file_path": "<fixtures>/wf44b/docs/issues/issue-3601/README.md", "limit": 8}`
20. `Edit {"replace_all": false, "file_path": "<fixtures>/wf44b/docs/issues/issue-3601/README.md", "old_string": "等待審查。\n\n## 文件清單", "new_string": "等待審查。\n\n## 現況\n\n*...`
21. `Bash {"command": "cd <fixtures>/wf44b && git add docs/issues/issue-3601/review-705822a.md docs/issues/issue-3601/README.md && git commit -q -F - <<'EOF'\ndocs(iss...`
22. `Bash {"command": "git -C <fixtures>/wf44b add docs/issues/issue-3601/review-705822a.md docs/issues/issue-3601/README.md && git -C <fixtures>/wf44b commit -q -m \"...`
23. `Bash {"command": "python3 -I <隔離設定>/skills/review/scripts/verify-artifact.py --repo <fixtures>/wf44b --reviewed 705822aff82dd234c13326bdf701998b9d9aa863 --head ff...`
24. `Bash {"command": "python3 -I <隔離設定>/skills/review/scripts/verify-artifact.py --repo <fixtures>/wf44b --reviewed 705822aff82dd234c13326bdf701998b9d9aa863 --head ff...`

權限拒絕：{"tool_name": "Bash", "tool_use_id": "toolu_01Ap2p3ci6ws5LBZNtQcnLPq", "tool_input": {"command": "git diff main..HEAD; git merge-base main HEAD; git rev-pars...; {"tool_name": "Bash", "tool_use_id": "toolu_01DecLy3vjrGYXFUzAD3Ui7M", "tool_input": {"command": "cd <fixtures>/wf44b && git add docs/issues/issue-3601/revie...; {"tool_name": "Bash", "tool_use_id": "toolu_01QhaNHYaQ8jYTTeyWSF1neJ", "tool_input": {"command": "python3 -I <隔離設定>/skills/review/scripts/verify-artifact.py ...

### 回合內新增的提交

```text
ff6d1a9 docs(issue-3601): 保存 705822a 審查報告（RETURN TO execute-task）

 docs/issues/issue-3601/README.md         |  4 ++
 docs/issues/issue-3601/review-705822a.md | 69 ++++++++++++++++++++++++++++++++
 2 files changed, 73 insertions(+)
```

`````diff
diff --git a/docs/issues/issue-3601/README.md b/docs/issues/issue-3601/README.md
index 01f54dd..26530ec 100644
--- a/docs/issues/issue-3601/README.md
+++ b/docs/issues/issue-3601/README.md
@@ -4,6 +4,10 @@
 
 待辦可以帶到期日：清單顯示月/日，並能列出逾期的未完成待辦。目前 S1、S2 都已完成，測試全數通過，等待審查。
 
+## 現況
+
+**現行 review**: review-705822a.md
+
 ## 文件清單
 
 - [implementation-plan.md](implementation-plan.md)
diff --git a/docs/issues/issue-3601/review-705822a.md b/docs/issues/issue-3601/review-705822a.md
new file mode 100644
index 0000000..2ff5b09
--- /dev/null
+++ b/docs/issues/issue-3601/review-705822a.md
@@ -0,0 +1,69 @@
+# 審查報告
+- 範圍：完整交付範圍（main..HEAD）
+- Reviewed BASE SHA：70f4ada99d53e2a4426341d3ee5bb1d0ebbb4faf
+- Reviewed HEAD SHA：705822aff82dd234c13326bdf701998b9d9aa863
+- Reviewed patch-id：3e03df882e536395094d6e4b0ae5ef3df64aa26d
+- 獨立 reviewer：Claude general-purpose subagent（宿主隔離 subagent，非原實作者，唯讀）
+
+## 問題與風險
+
+行號皆指 Reviewed HEAD 705822a 的版本。
+
+### MUST FIX
+
+- **M1 SCN-002 未核准即實作並交付** `需決策` — `todo.py:37-39`、`test_due.py:11-16`、`docs/issues/issue-3601/implementation-plan.md:10`（S2 ✅）。`docs/issues/issue-3601/README.md:41` 核准表 SCN-002 為 `待核准`，`README.md:52` TBD-2（逾期以今天或明天為界）仍 `待確認`。acceptance.md「分批核准」只允許實作已核准的 Task，PR 前所有現存驗收條件須已核准或逐項豁免；此為缺少新行為核准來源。實作的嚴格 `<` 已自行決定 TBD-2（到期日當天不算逾期）。
+  - 待決問題：SCN-002 是否核准、TBD-2 的邊界為何。
+  - 可選做法：(a) 以今天為界（due < today 才逾期，即現行實作），補 due == today 的 Scenario／測試後核准；(b) 以明天為界（到期日當天也算逾期），改為 `<=` 並更新測試；(c) SCN-002 維持待核准，從本次交付移除 `overdue`、`test_overdue` 與 S2（或標回 📝）。
+  - reviewer 建議：先詢問使用者，傾向 (a) 並補邊界測試；短期內無法取得答案時採 (c)。
+
+### SHOULD FIX
+
+- **S1 CLI 無法設定或列出到期日／逾期** `需決策` — `todo.py:18-21`、`todo.py:53-60`、根目錄 `README.md:10`。`add` 不寫入 `due`，也沒有 `overdue` 子命令；使用者只能手改 todo.json，`overdue` 沒有任何使用者可達路徑。根目錄 README 說明會顯示到期日，卻沒說如何設定。核准 Scenario 字面是函式層級（「執行 render」「呼叫 overdue」）因此字面滿足，但 acceptance.md 要求 Scenario 描述外部行為、不綁內部函式。
+  - 待決問題：CLI 入口是否在本 issue 範圍。
+  - 可選做法：(a) 新增 `add --due YYYY-MM-DD` 與 `overdue` 子命令，補 Scenario 並核准；(b) 明確限定範圍為函式與手動編輯資料，於根目錄 README 註明。
+  - reviewer 建議：本 issue 採 (b)，CLI 入口記入待確認事項或另開 issue；根目錄 README 至少寫明 `due` 如何設定。
+- **S2 `due` 格式錯誤未處理** — `todo.py:34`、`todo.py:39`、`todo.py:48`。字串比較只對補零的 ISO `YYYY-MM-DD` 正確。實測：`'2026-2-1'`、`'2026/11/01'` 在 2026-11-19 不被判逾期；`'abc'` 顯示「（到期 ）」；`'2026-11-01T10:00'` 顯示「（到期 11/01T10:00）」；整數 `due` 使 `render` 拋出 `TypeError`，`python3 todo.py` 整份清單失敗。`None`、`""` 處理正確。目前只有手改資料會出現（與 S1 相關），影響低。建議以 `date.fromisoformat` 解析並略過或標示無效值，或將 ISO 假設記入待確認事項。
+- **S3 issue README 格式** — `docs/issues/issue-3601/README.md:5` 概述記了進度（「S1、S2 都已完成，測試全數通過，等待審查」），進度應只在 `**狀態**` 與任務清單，且 SCN-002 未核准使此敘述不準確；`README.md:59-60` Timeline 記錄「完成 S1／S2」這類步驟完成事件並多出 `負責人` 欄，範本規定 Timeline 只記語意事件；`README.md:51` TBD-1 結論寫在影響欄，規則要求結論、理由與日期寫在狀態欄（狀態值仍以 `已解決` 開頭，不誤導掃描，故非 MUST FIX），且缺少決策理由；`README.md:13` 涉及檔案寫「對應的測試檔」過於含糊，應明列 `test_due.py` 與根目錄 `README.md`（常青文件更新）。
+- **S4 紅綠燈證據順序不一致** — `docs/issues/issue-3601/implementation-plan.md:9`。S1 綠燈記「Ran 3 tests OK」，但 S1 當下若 `test_overdue` 尚不存在應為 2 tests；若已存在則 `overdue` 尚未實作或仍是 S2 紅燈的 `[]` 樁，不可能 OK。「被測內容即 H1 的 todo.py」暗示綠燈是對最終 todo.py 執行，屬誠實揭露但語意含糊，且「H1」不是實際 SHA。建議寫明實際順序與被測 SHA（705822a）。reviewer 已在 HEAD 重現綠燈，不構成假綠燈。
+
+### NICE TO HAVE
+
+- **N1** `todo.py:39` 重複呼叫 `due_of(i)`，可改為 `(d := due_of(i)) and d < today` 或內聯一行的 `due_of`，屬輕微過度抽象；docstring 的 `issue-3601：` 前綴屬 Git 歷史資訊。
+- **N2** 缺 due == today 的邊界測試（依 M1／TBD-2 結論補上），以及已完成待辦仍顯示到期日的測試。
+- **N3** 根目錄 `README.md` 缺最後驗證日期（AGENTS.md 常青文件規則）；BASE 即已存在，非本次引入。
+
+## 已查核維度
+
+- 驗收與證據：
+  - SCN-001：已核准（2026-11-16 使用者回覆「核准」，核准 commit df95965）。證據 `test_due.py:7-9`（字面期望值，獨立於實作）與 `implementation-plan.md:9`；HEAD 重跑 `python3 -m unittest -v` exit 0、Ran 3 tests OK。判定：通過（附 S4）。
+  - SCN-002：測試真實（`test_due.py:11-16`，含已完成與無到期日的干擾項），但未核准且 TBD-2 未決。判定：不可交付（M1）。
+  - 規格修訂：`git diff df95965 705822a -- docs/issues/issue-3601/README.md` 只改 `**核准 commit**`（待提交 → df95965）、Timeline 兩列與 `**狀態**`（待實作 → 審查中），Gherkin 未變，核准基線 df95965 對 SCN-001 有效。
+- 相關失敗面：
+
+| 輸入／狀態 | 預期 | 現有覆蓋 | 判定 |
+|---|---|---|---|
+| 無 `due` 的舊資料 | 輸出不變 | `test_render_marks_done`、`test_overdue` id 4 | 通過，向後相容 |
+| `due` 為 `None` 或 `""` | 視為無到期日 | 僅 reviewer 實測 | 通過 |
+| 已完成且已過期 | 不列為逾期 | `test_overdue` id 3 | 通過 |
+| due == today | 未決（TBD-2） | 無 | 未決（M1） |
+| 非 ISO 或未補零日期 | 正確判斷或拒絕 | 無 | 結果錯誤（S2） |
+| 非字串 `due` | 不崩潰 | 無 | 整份清單崩潰（S2） |
+| 無意義字串 | 不產生怪異輸出 | 無 | 顯示「（到期 ）」（S2） |
+| 從 CLI 設定或列出 | 使用者可達 | 無 | 未實作（S1） |
+| 測試真偽 | 期望值來自獨立來源 | 規格字面值 | 非同義反覆，無假綠燈 |
+
+- 需求：SCN-001 符合核准規格；SCN-002 未核准即交付並自行決定 TBD-2 邊界；功能對實際使用者不可達（S1）。
+- 架構：變更最小、符合單檔 CLI 邊界。
+- 安全：無權限或依賴面；僅本機資料格式錯誤導致崩潰（S2）。
+- 品質（含跨 Task 重複與過度設計）：S1、S2 共用 `due_of`，無分歧的重複邏輯；僅 N1 的輕微過度抽象。測試真實，但邊界處理弱（S2），文件格式（S3）與證據順序（S4）待改善。
+- 證據持久力：期望值為規格字面值，持久力足夠；無另列項目。
+
+## 豁免、待確認與限制
+
+- 豁免：無 Gate 豁免紀錄。
+- 待確認：TBD-2 維持 `待確認`，直接阻擋 SCN-002（M1）；TBD-1 已解決，格式見 S3。
+- 限制：只有一個實作提交，紅燈無法獨立重現，依紀錄採信；邊界探測以記憶體內 import `todo` 進行，未對 todo.json 執行 CLI；使用者核准原話只能依 README 紀錄核對。
+
+## 流程判定
+
+RETURN TO execute-task
`````

### 最終輸出

````markdown
## Issue 3601 審查結果：**RETURN TO execute-task**

審查範圍是完整交付範圍 `70f4ada..705822a`。審查由獨立 subagent 執行，它不是原實作者。報告保存在 `docs/issues/issue-3601/review-705822a.md`，已和 issue README 新增的 `## 現況`（`**現行 review**` 指向這份報告）一起提交為 `ff6d1a9`。`verify-artifact.py` 檢查結果為 OK，代表報告提交只動到記帳區段；但這個結果只說明報告綁定的版本有效，判定本身就是退回。

**MUST FIX，需要你決定**
- **M1：SCN-002（列出逾期）還沒核准就已實作並標為完成。** 核准表裡它仍是 `待核准`，TBD-2「逾期以今天還是明天為界」也還是 `待確認`（`docs/issues/issue-3601/README.md:41`、`:52`）。現在的程式用 `<` 比較，等於已經替你定了：到期當天不算逾期（`todo.py:39`）。你可以選：
  - (a) 以今天為界，維持現在的實作，補一個「到期日等於今天」的測試，再核准 SCN-002（reviewer 建議這個）。
  - (b) 以明天為界，改成 `<=` 並更新測試。
  - (c) 這次不交付 S2，移除 `overdue` 相關程式、測試和任務項目。

**SHOULD FIX**
- **S1（需要你決定）：一般使用者用不到這個功能。** CLI 沒有設定到期日的方式，也沒有列出逾期的命令（`todo.py:18-21`、`:53-60`）。建議這次先限定範圍，在根目錄 `README.md` 寫明到期日要怎麼設定，CLI 另開 issue。
- **S2：到期日格式不對時會出錯。** 未補零的日期（例如 `2026-2-1`）或用斜線的日期，逾期會判斷錯誤。`due` 若是整數，`render` 會拋 `TypeError`，`python3 todo.py` 整份清單都列不出來（`todo.py:48`）。
- **S3：issue README 格式問題。**
  - 概述寫了進度。
  - Timeline 記了步驟完成，還多一個 `負責人` 欄。
  - TBD-1 的結論寫在影響欄。
  - 涉及檔案寫得太籠統。
- **S4：S1 的紅綠燈證據順序對不上**（`implementation-plan.md:9`）。S1 綠燈記的是「Ran 3 tests OK」，但當時測試應該只有 2 個，或其中一個不可能通過，而且沒寫被測的 SHA。我在 HEAD 重跑 `python3 -m unittest -v`，3 個測試全部通過，所以這不算假綠燈。

SCN-001 本身沒有問題：已核准，測試是真的，規格在核准 commit `df95965` 之後也沒有被改過。

下一步請你回答 M1 和 S1 要選哪個做法，答案會記到 README 的待確認事項，再回 execute-task 修正。修正後可以只審查 `705822a` 之後的增量。
````
