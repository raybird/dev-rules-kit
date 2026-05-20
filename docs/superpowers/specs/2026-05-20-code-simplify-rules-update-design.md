# 設計規格書：擴充 code-simplify 規則至通用型 TypeScript 架構

- **建立日期**：2026-05-20
- **作者**：Antigravity
- **狀態**：已批准 (Approved)

## 1. 背景與動機
目前 `code-simplify`（程式碼簡化）工作流程與技能在進行精煉時，限制於 React 元件模式，且在規範參照上只指名了 `CLAUDE.md`。

然而，在實際應用中，許多下游專案是以 TypeScript 作為核心開發語言，並可能使用 Angular 前端框架，以及 Firebase Functions SDK 或 Cloud Run 等後端環境。此外，不同的開發者或平台會使用不同名稱的規則檔（如 `GEMINI.md`、`AGENTS.md` 等）。

為使該規則庫更具通用性，我們需要將 `code-simplify` 工作流程調整為通用型 TypeScript 語言與架構層級的精煉原則，並將規則參照範圍擴大至主流的 AI Agent 規範文件。

## 2. 變更範圍與目標
本專案為 Markdown 範本庫，異動目標包含以下兩個互相配對的檔案：
1. `workflows/shared/code-simplify.md` (適用於各編輯器/工作流程平台)
2. `skills/code-simplify/SKILL.md` (適用於 Claude 技能定義)

此兩份檔案內容必須保持完全一致。

## 3. 具體修改設計

### 3.1 規則檔參照擴充
修改前：
> 依據 `CLAUDE.md` 中建立的編碼標準執行，包含：

修改後：
> 依據 `CLAUDE.md`、`GEMINI.md`、`AGENTS.md` 或專案根目錄下其他 AI Agent 規則檔中建立的編碼標準執行，包含：

### 3.2 語言與架構層級規則調整
針對 TypeScript、Angular、Firebase Functions 及 Cloud Run 的特點，將原本的規則調整如下：

- **ES Modules / CommonJS 支持**：改為根據專案環境調整。
- **箭頭函式限制**：補充除作為 callback 或需 bind `this` 之外，優先使用 `function` 關鍵字。
- **型別定義**：
  - 頂層函式與導出的 API 必須明確標注 TypeScript 參數與回傳型別，避免隱式 `any`。
  - 採用強型別系統，避免隨意使用 `any`，優先使用具體型別或 `unknown`。
- **框架通用化**：將原本的 React 元件/Props 限制，改為通用框架與架構模式（如 Angular 元件/服務、Firebase Functions 或 Cloud Run 處理器），明確定義介面（Interfaces）或型別（Types）。
- **錯誤處理**：微調為「採用正確的錯誤處理模式（盡量避免無謂的 try/catch，或遵循專案既有的錯誤傳遞與處理規範）」。

## 4. 驗證與測試計畫
由於本專案為純 Markdown 範本庫，驗證方式如下：
1. 確保 `workflows/shared/code-simplify.md` 與 `skills/code-simplify/SKILL.md` 內容完全一致（忽略空白差異）。
2. 使用 Markdown 格式校對，確保語意通順且完全符合 Traditional Chinese (Taiwan style)。

## 5. 修訂紀錄 (Changelog)
- **2026-05-20**：初始設計草案建立並通過使用者評估。
