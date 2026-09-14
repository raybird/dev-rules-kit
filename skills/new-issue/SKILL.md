---
name: new-issue
description: 將新需求轉成可核准的驗收條件與 issue 文件；需要建立或修訂 issue 範圍、驗收規格與初始計畫時使用。
---

> 本 skill 需要 `docs/AGENTS.md` **流程契約 2.0**；相容性依該檔「核心層齊備性檢查」。

## 輸入

從指令或對話取得 issue ID 與核心目標。缺少且無法辨認時詢問缺項；建立 issue 目錄前兩者都須明確。

## 流程

1. 讀 AGENTS.md 分級與風險規範、agents/project.md，以及 agents/acceptance.md。建立文件時讀 document-types.md 與 readme-templates.md。
2. 探索現況與最小修改邊界，指出最大風險，判定規模與驗證順序；避免用方案假設填補未調查的現況。
3. 對照需求與既有核准來源，依 acceptance.md 只澄清影響結果的缺項。有實質取捨才比較方案；需要探索時可調用 Superpowers brainstorming，已有共識則沿用。
4. 寫下可觀察驗收條件與核准來源。使用者的明確要求已涵蓋結果與範圍時，引用原話即可；新增或實質變更的行為取得核准後才列為可實作。分批核准的前置門檻與狀態依 acceptance.md。
5. 依規模建立初始文件：Small 在 README 寫步驟；Medium / Large 在 implementation-plan.md 寫計畫。Large 的分析文件依觸發條件建立，Phase / Task 後續由 decompose 在同一計畫細化。風險與涉及檔案清單僅在 README 維護。
6. 每項步驟標注驗收編號、產出、相依與可檢查的完成判準。測試策略依 verification.md；具體路徑與命令可由 execute-task 根據既有驗證入口選擇，不把等價命令選擇當新需求。
7. 將非阻塞未知記入待確認事項；必要安全／範圍決策仍需答案。以 issue-checklist.md 完成逐項核對。

## 完成判準

- 必要文件齊備，連結只指向存在的檔案；metadata 有分級、風險、實際狀態與日期。
- 每項驗收的內容與來源可追溯，核准集合／分批門檻符合 acceptance.md；待核准項目沒有可實作 Task。
- 任務只有一個權威來源，各步驟具產出、驗收編號與完成判準；首要驗證對應最大風險。
- 需取得答案的未知已解決，其餘已揭露；使用者要求的 gate 豁免已依 AGENTS.md 留痕。

只回報範圍、規模／風險、文件位置、已核准與待決定編號；不在對話複製整份文件。尚有必要缺項時明列，不宣稱規劃完成。
