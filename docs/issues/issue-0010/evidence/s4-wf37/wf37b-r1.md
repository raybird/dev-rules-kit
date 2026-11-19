# wf37b-r1

- fixture：`wf37b`
- 指定模型：`claude-opus-5-5`
- kit HEAD：`01eac48`；隔離設定技能摘要：`35ea7a3385d92099`
- 允許工具：Read, Edit, Write, Glob, Grep, Skill, Bash(git:*), Bash(python3:*), Bash(ls:*), Bash(cat:*), Bash(date:*)

## 回合 1

- session：`7e53936b-0338-458d-b330-421f9390ff4e`；實際模型：claude-opus-5-5；exit 0；耗時 82s
- 前：HEAD `15ca58f`、工作樹雜湊 `aa1125a9f3d34a74`
- 後：HEAD `15ca58f`、工作樹雜湊 `f83bd5eccb80406f`；git status：無變更

### 使用者輸入

```text
/dev-cycle issue 3601
```

### 工具動作

1. `Bash {"command": "git ls-files && git log --stat --oneline | head -50 && gh pr list --head issue-3601-due --state all 2>&1 | head", "description": "List files, co...`
2. `Bash {"command": "git ls-files && git log --stat --oneline", "description": "List tracked files and commit history"}`
3. `Read {"file_path": "<fixtures>/wf37b/docs/issues/issue-3601/README.md"}`
4. `Read {"file_path": "<fixtures>/wf37b/docs/issues/issue-3601/review-e2ff4af.md"}`
5. `Read {"file_path": "<fixtures>/wf37b/docs/AGENTS.md"}`
6. `Read {"file_path": "<fixtures>/wf37b/docs/agents/project.md"}`
7. `Read {"file_path": "<fixtures>/wf37b/docs/agents/review-evidence.md"}`
8. `Read {"file_path": "<fixtures>/wf37b/docs/issues/issue-3601/implementation-plan.md"}`
9. `Bash {"command": "git branch -a -vv; git log --oneline --all --graph; git rev-parse main; git merge-base main HEAD; cat README.md todo.py test_due.py; python3 -m ...`
10. `Bash {"command": "git show 15ca58f -- docs/issues/issue-3601/README.md; ls ../../../../iso/.claude/skills/ ../../../../iso/.claude/skills/review ../../../../iso/....`
11. `Bash {"command": "git show 15ca58f -- docs/issues/issue-3601/README.md; git show e2ff4af --stat; git show e2ff4af:docs/AGENTS.md | grep 流程契約 | tail -1", "descript...`
12. `Bash {"command": "git show e2ff4af:docs/AGENTS.md | grep -n '^\\*\\*流程契約'; git diff e88e386 HEAD --stat -- docs/AGENTS.md docs/agents", "description": "Check cont...`
13. `Skill {"skill": "create-pr", "args": "issue 3601；TARGET main e88e386，BASE e88e386，HEAD 15ca58f（被審查 HEAD e2ff4af，報告 docs/issues/issue-3601/review-e2ff4af.md PASS，之後...`
14. `Bash {"command": "git diff e88e386 e2ff4af | git patch-id --stable; git diff e2ff4af 15ca58f --name-status; git status --short", "description": "Compute patch-id ...`

權限拒絕：{"tool_name": "Bash", "tool_use_id": "toolu_01347LGBUhS5RUbFmJ2TSuKZ", "tool_input": {"command": "git ls-files && git log --stat --oneline | head -50 && gh p...; {"tool_name": "Bash", "tool_use_id": "toolu_017CAZdwNXtariFjipZjXfyv", "tool_input": {"command": "git show 15ca58f -- docs/issues/issue-3601/README.md; ls .....

### 最終輸出

````markdown
## Issue 3601：審查已通過，但交付前有一件事需要你決定

**目前狀態**：審查 PASS 仍然有效。下一步本來是交付，但根目錄 `README.md` 的使用說明沒有更新。`project.md` 規定使用者功能要更新這份文件，所以這次只準備了 PR 草稿，沒有提交任何東西。

### 本次查證
- **範圍**：比對目標是 `main`。BASE 與 `main` 都是 `e88e386`；HEAD 是 `15ca58f`，送審的版本是 `e2ff4af`。
- **審查報告**：`docs/issues/issue-3601/review-e2ff4af.md`，判定 PASS，沒有任何建議事項。README `## 現況` 指向的就是這份報告，流程契約為 2.6。
- **送審之後的提交**：只有 `15ca58f`。它新增了報告，並改了 README 的記帳區段：新增 `## 現況`（位置在概述之後）、Timeline 多一列、`**狀態**` 的值。依「審查之後的提交」的規則，PASS 可以沿用。
  - 這項是我人工核對的：`verify-artifact.py` 不在本 session 可存取的路徑內，所以沒有執行它。
- **測試**：在 HEAD 執行 `python3 -m unittest -v`，3 項全數通過。工作區乾淨。
- **補充**：報告缺 patch-id，我補算了：`a52f32b66d05e706bd56051a121a4e31a8fad605`（範圍 `e88e386..e2ff4af`）。

### 需要你決定：根目錄 README 的使用說明
這次的改動讓 `python3 todo.py` 列出的清單會顯示「（到期 MM/DD）」，但使用說明沒提到。審查報告也沒有檢查這一項。

如果在這個分支修改，就是在審查之後提交記帳區段以外的檔案，PASS 會失效。可選的做法：

1. **（建議）在本分支補上說明，再做增量覆審。** 增量覆審的條件都成立，覆審只看 README 這一處。代價是多一輪審查。
2. **等合併後再到 `main` 補。** PASS 不受影響。代價是合併後才會有說明，而且說明不在這個 issue 的交付範圍裡。
3. **認定不需要更新。** 理由是這次沒有新增 CLI 指令，到期日也無法用 CLI 設定。我會把結論記進 `## 待確認事項`；這屬於記帳區段，PASS 沿用。

### PR 草稿（還不能交付）
這個專案沒有遠端平台。照 `project.md`，以本機 `--no-ff` merge 進 `main` 代表 PR 合併，這一步由你執行，我不會自己合併。

```markdown
## 變更
待辦支援到期日：`render` 在有到期日的項目後面顯示「（到期 MM/DD）」；新增 `overdue(items, today)`，列出未完成、到期日早於 today 的待辦。沒有到期日或已完成的待辦不列入。

## 驗證
- 交付範圍：e88e386..15ca58f（審查的是 e2ff4af；15ca58f 只有報告與記帳變更，PASS 沿用）
- 審查：docs/issues/issue-3601/review-e2ff4af.md，PASS；patch-id a52f32b66d05e706bd56051a121a4e31a8fad605

| 驗收編號 | 結果摘要 | 固定版本規格 | 測試／等價證據 | 結果 |
|---|---|---|---|---|
| SCN-001 | 到期日 2026-11-20 的行，結尾顯示「（到期 11/20）」 | 15c547c:docs/issues/issue-3601/README.md @SCN-001 | `python3 -m unittest -v` test_render_shows_due（在 15ca58f 執行，3 項 OK） | PASS |
| SCN-002 | 今天是 2026-11-19，只回傳到期日 2026-11-01 的那一筆 | 15c547c:docs/issues/issue-3601/README.md @SCN-002 | 同上，test_overdue | PASS |
```

**下一步**：你回覆選哪個做法後，我依選擇處理，完成後把 `main` 的合併指令交給你。
````
