# Changelog

本檔案記錄 dev-rules-kit 的重要變更，供下游專案更新已複製的檔案時參考。

**版本策略**：重要變更時打 git tag，規則如下——

- **Major**：破壞性變更（規則語意反轉、目錄結構調整、skill 改名或移除），下游更新前應檢視自己的客製內容
- **Minor**：新增 skill / workflow / 規則章節，下游可安全重新複製
- **Patch**：錯字修正、文字調整、文件補充，不影響行為

每個條目標注影響的目錄，方便下游判斷是否需要重新複製對應檔案。

---

## [1.2.0] - 2026-07-21

### 變更（`skills/`、`workflows/shared/`、`docs/AGENTS.md` — 下游建議重新複製）

依 issue 分級決定是否需要 `decompose`，修正 Small 級別在閉環中缺少任務清單來源、以及 Medium 級別把實作步驟寫兩遍的問題。

- `docs/AGENTS.md`：新增「任務清單來源」對照表；分級**必須**寫入 `README.md` 結尾 metadata 的 `**分級**` 欄位（兩份 README 範本已加上該欄位）；明訂 Small / Medium 不再產生額外的分解文件
- `new-issue`：將評估出的分級寫回 README；要求實作步驟寫成可直接執行的任務清單（每項有明確產出與完成判準）
- `dev-cycle`：新增「分級判定」小節，僅 Large 觸發 `decompose`，Small / Medium 直接進入 `execute-task`；舊 issue 缺少 `**分級**` 欄位時可由現有檔案回推並補寫
- `decompose`：新增「適用範圍」，標明僅適用 Large
- `execute-task`：description 與 Input 改為依分級查表取得任務清單，不再寫死 Implementation Plan Decomposition

### 下游更新注意事項

既有 issue 文件不需回頭補 `**分級**` 欄位，`dev-cycle` 會依實際存在的檔案自動回推；但新建立的 issue 一律會帶此欄位。

## [1.1.0] - 2026-07-06

### 變更（`skills/`、`workflows/shared/` — 下游建議重新複製）

- `execute-task`：新增「確認工作分支」為第一步，明定分支命名規範（`issue-{ID}` 開頭，可加描述後綴）
- `dev-cycle`：完成階段新增 issue 文件收尾動作（README 狀態、timeline 補記）；明示推進模式為全自動執行（直接 commit、直接建 PR），`create-commit` 的人工把關僅適用於單獨呼叫
- README 開發閉環章節註明 `git-squash` 為閉環外的獨立輔助工具

## [1.0.0] - 2026-07-06

首個正式版本，作為下游專案的更新基準點。

### 現有內容盤點

- **`rules/`**：AI 行為核心規則，中（`AGENTS.zh-TW.md`）英（`AGENTS.md`）雙版，各 10 章節
- **`skills/`**：9 個技能——`new-issue`、`decompose`、`execute-task`、`code-simplify`、`create-commit`、`create-pr`、`review`、`git-squash`、`dev-cycle`，構成完整開發閉環
- **`workflows/shared/`**：與 skills 一一對應的 9 個跨平台工作流（由 `scripts/sync-skills.py` 自動同步）；`workflows/antigravity/` 另有平台特定 workaround
- **`docs/`**：下游 issue 文件規範（`AGENTS.md`）、使用指南（`usage.md`）、實體文件模板（`_templates/`）、五平台安裝指南（`setup/`）

### 本版新增（2026-07-06）

- `scripts/sync-skills.py` 新增 `--check` 模式：驗證配對同步、偵測孤兒工作流、檢查雙語規則章節數
- 新增 `scripts/check-links.py` 與 GitHub Actions CI，於 push / PR 時自動執行檢查
- 新增本 CHANGELOG 與版本策略
- 移除誤入版控的 MCP memory 資料庫並補上 `.gitignore`
- 修正 `workflows/README.md` 漏列 `dev-cycle`、`new-issue` 描述不一致等文件矛盾

### 沿革（1.0.0 之前的里程碑）

- **2026-06-29**：README 新增 Claude Code 下游專案掛載規則（`@AGENTS.md` 匯入法）
- **2026-06-20**：新增 `sync-skills.py` 自動同步腳本、實體文件模板；`new-issue` 實作任務動態分級
- **2026-06-02**：新增 `git-squash` skill 與 workflow
- **2026-05-28**：新增 `dev-cycle` orchestration skill 與使用指南 `usage.md`
- **2026-05-18**：新增五平台安裝指南與 `CLAUDE.md` 維護指引
- **2026-05-08**：建立 `skills/` 目錄結構
- **2026-04-16**：初始版本（`rules/` 與 `workflows/`）
