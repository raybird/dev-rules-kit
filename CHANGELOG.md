# Changelog

本檔案記錄 dev-rules-kit 的重要變更，供下游專案更新已複製的檔案時參考。

**版本策略**：重要變更時打 git tag，規則如下——

- **Major**：破壞性變更（規則語意反轉、目錄結構調整、skill 改名或移除），下游更新前應檢視自己的客製內容
- **Minor**：新增 skill / workflow / 規則章節，下游可安全重新複製
- **Patch**：錯字修正、文字調整、文件補充，不影響行為

每個條目標注影響的目錄，方便下游判斷是否需要重新複製對應檔案。

---

## [1.3.1] - 2026-07-21

### 變更（`skills/`、`workflows/shared/`、`docs/AGENTS.md` — 下游建議重新複製）

針對 AI agent 的載入機制優化 skill 文件：`description` 是唯一常駐於 context 的部分，也是 agent 判斷「是否要載入整份 skill」的唯一依據，因此補齊觸發時機與適用範圍。

- **description 補齊觸發條件**：
  - `decompose`：明示**僅適用 Large**，agent 不必載入整份 body 即可排除 Small / Medium 的誤觸發
  - `create-pr`：`peer-request`（非通用術語）更正為 **Pull Request**，內文與 `workflows/README.md` 的殘留一併清除
  - `new-issue`：補上產出位置與觸發時機、三級產出說明
  - `create-commit`：補上 Conventional Commits 與「已 git add 後使用」
- **`decompose` 範本去重**：Output 範本中逐字重複的 Phase 2 結構改為結構說明，並加註「不要因為範本只列兩個 Phase 就固定產出兩個」（189 → 167 行）
- **分級規範 single source**：`docs/AGENTS.md`「文件動態分級規範」標示為唯一權威定義，`dev-cycle`、`execute-task` 內的分級表標注為摘要並指向該節

未引入多檔案 progressive disclosure：`sync-skills.py` 為單檔逐位元組複製，SKILL.md 若引用外部檔案會在其他平台的 workflow 端斷鏈。

## [1.3.0] - 2026-07-21

### 變更（`skills/`、`workflows/shared/`、`docs/AGENTS.md` — 下游建議重新複製）

為任務切分加入「風險優先」原則，避免 Phase / 步驟被切成技術分層而把整合風險留到最後。深度依分級遞減。

- `decompose`（Large）：新增「Phase 切分原則」——**Phase 1 應優先打通風險最高、假設最未經驗證的那條路徑**，垂直切片為手段而非目的；依未知的類型（外部整合／重構／資料遷移／需求已凍結）給出對應切法，並附正反對照。需求文件標為「未知／待確認」的事項即為排序第一依據
- `docs/AGENTS.md`（Medium / Large）：`implementation-plan.md` 章節新增「實作步驟的排序原則」，未經驗證的假設應排在最前面
- `new-issue`：新增分級自我校驗——規劃 Medium 步驟時若發現未知大到需要獨立探索階段，應升級為 Large 並補齊分析文件
- `docs/usage.md`：示範的 decompose 產出由技術分層改為垂直切片，與新原則一致

Small 級別不受影響。

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
