# code-simplify Rules Update Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 擴充 `code-simplify.md` 與 `SKILL.md`，使其不侷限於 React，並支持更多 AI Agent 規則文件（如 GEMINI.md 與 AGENTS.md）及通用型 TypeScript 語言規範。

**Architecture:** 同步修改共用工作流程檔案與 Claude 技能定義檔案，確保兩者內容完全一致。

**Tech Stack:** Markdown, Git

---

### Task 1: Update code-simplify Workflow

**Files:**
- Modify: `workflows/shared/code-simplify.md`

- [ ] **Step 1: 修改工作流程檔案**
  將 `workflows/shared/code-simplify.md` 中關於「遵循專案規範」的 React 限制及 `CLAUDE.md` 單一參照，替換為通用 TypeScript/Angular/Firebase 與多 Agent 規則檔的描述。

  **Target Content:**
  ```markdown
  ## 2. 遵循專案規範

  依據 `CLAUDE.md` 中建立的編碼標準執行，包含：

  - 使用 ES modules，正確排序 import 並加上副檔名
  - 優先使用 `function` 關鍵字，而非 arrow function
  - 頂層函式必須明確標注回傳型別
  - 遵循 React 元件模式，明確定義 Props 型別
  - 採用正確的錯誤處理模式（盡量避免 try/catch）
  - 維持一致的命名慣例
  ```

  **Replacement Content:**
  ```markdown
  ## 2. 遵循專案規範

  依據 `CLAUDE.md`、`GEMINI.md`、`AGENTS.md` 或專案根目錄下其他 AI Agent 規則檔中建立的編碼標準執行，包含：

  - 依專案環境使用 ES Modules / CommonJS，正確排序 import/require 並加上副檔名（若環境要求）
  - 優先使用 `function` 關鍵字，而非 arrow function（除非作為 callback 或需要綁定 `this` 的場合）
  - 頂層函式與導出的 API 必須明確標注 TypeScript 參數與回傳型別，避免隱式 `any`
  - 遵循框架與架構模式（如 Angular 元件/服務、Firebase Functions 或 Cloud Run 處理器），明確定義介面（Interfaces）或型別（Types）
  - 採用強型別系統，避免隨意使用 `any`，優先使用具體型別或 `unknown`
  - 採用正確的錯誤處理模式（盡量避免無謂的 try/catch，或遵循專案既有的錯誤傳遞與處理規範）
  - 維持一致的命名慣例（如 camelCase、PascalCase 等）
  ```

- [ ] **Step 2: Commit**
  Run:
  ```bash
  git add workflows/shared/code-simplify.md
  git commit -m "docs: generalize code-simplify workflow to generic TypeScript and multiple agents files"
  ```

---

### Task 2: Synchronize code-simplify SKILL

**Files:**
- Modify: `skills/code-simplify/SKILL.md`

- [ ] **Step 1: 修改技能定義檔案**
  將 `skills/code-simplify/SKILL.md` 的「遵循專案規範」段落進行與 Task 1 完全相同的修改，以維持兩檔案的一致性。

  **Target Content:**
  ```markdown
  ## 2. 遵循專案規範

  依據 `CLAUDE.md` 中建立的編碼標準執行，包含：

  - 使用 ES modules，正確排序 import 並加上副檔名
  - 優先使用 `function` 關鍵字，而非 arrow function
  - 頂層函式必須明確標注回傳型別
  - 遵循 React 元件模式，明確定義 Props 型別
  - 採用正確的錯誤處理模式（盡量避免 try/catch）
  - 維持一致的命名慣例
  ```

  **Replacement Content:**
  ```markdown
  ## 2. 遵循專案規範

  依據 `CLAUDE.md`、`GEMINI.md`、`AGENTS.md` 或專案根目錄下其他 AI Agent 規則檔中建立的編碼標準執行，包含：

  - 依專案環境使用 ES Modules / CommonJS，正確排序 import/require 並加上副檔名（若環境要求）
  - 優先使用 `function` 關鍵字，而非 arrow function（除非作為 callback 或需要綁定 `this` 的場合）
  - 頂層函式與導出的 API 必須明確標注 TypeScript 參數與回傳型別，避免隱式 `any`
  - 遵循框架與架構模式（如 Angular 元件/服務、Firebase Functions 或 Cloud Run 處理器），明確定義介面（Interfaces）或型別（Types）
  - 採用強型別系統，避免隨意使用 `any`，優先使用具體型別或 `unknown`
  - 採用正確的錯誤處理模式（盡量避免無謂的 try/catch，或遵循專案既有的錯誤傳遞與處理規範）
  - 維持一致的命名慣例（如 camelCase、PascalCase 等）
  ```

- [ ] **Step 2: 驗證檔案同步性**
  根據 `CLAUDE.md` 的要求，使用 diff 指令驗證兩檔案是否同步（忽略空白差異）。
  Run:
  ```bash
  diff -qw "skills/code-simplify/SKILL.md" "workflows/shared/code-simplify.md"
  ```
  Expected Output:（無輸出或顯示檔案完全一致，結束碼為 0）

- [ ] **Step 3: Commit**
  Run:
  ```bash
  git add skills/code-simplify/SKILL.md
  git commit -m "docs: synchronize code-simplify skill with updated workflow"
  ```
